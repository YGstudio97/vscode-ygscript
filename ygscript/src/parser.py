"""
YGScript Parser - Converts tokens to AST
"""

from typing import List, Optional
from lexer import Token, TokenType, Lexer
from ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message: str):
        if self.current_token:
            raise SyntaxError(
                f"Parser error at line {self.current_token.line}, "
                f"column {self.current_token.column}: {message}"
            )
        raise SyntaxError(f"Parser error: {message}")
    
    def advance(self) -> Token:
        """Move to next token and return the previous one"""
        prev = self.current_token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        return prev
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at next token"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume token of expected type or error"""
        if self.current_token.type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of given types"""
        return self.current_token.type in token_types
    
    def consume(self, *token_types: TokenType) -> bool:
        """Consume token if it matches"""
        if self.match(*token_types):
            self.advance()
            return True
        return False
    
    def parse(self) -> Program:
        """Parse entire program"""
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """Parse a single statement"""
        # Variable declarations
        if self.match(TokenType.LET, TokenType.VAR, TokenType.CONST):
            return self.parse_variable_declaration()
        
        # Function declaration
        if self.match(TokenType.FNC):
            return self.parse_function_declaration()
        
        # Class declaration
        if self.match(TokenType.CLASS):
            return self.parse_class_declaration()
        
        # Control flow
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        
        if self.match(TokenType.WHEN):
            return self.parse_when_statement()
        
        if self.match(TokenType.THOUGH):
            return self.parse_though_statement()
        
        if self.match(TokenType.INCASE):
            return self.parse_switch_statement()
        
        if self.match(TokenType.FOR):
            return self.parse_for_loop()
        
        if self.match(TokenType.WHILE):
            return self.parse_while_loop()
        
        if self.match(TokenType.DO):
            return self.parse_do_while_loop()
        
        if self.match(TokenType.AGIN):
            return self.parse_agin_loop()
        
        # Loop control
        if self.match(TokenType.BREAK):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return BreakStmt()
        
        if self.match(TokenType.CONTINUE):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return ContinueStmt()
        
        # Return statement
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()
        
        # Import/module
        if self.match(TokenType.ADD):
            return self.parse_import_statement()
        
        if self.match(TokenType.FROM):
            return self.parse_from_import_statement()
        
        # Block statement
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expression statement
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ExpressionStmt(expr) if expr else None
    
    def parse_variable_declaration(self) -> VariableDecl:
        """Parse: let/var/const name [: type] [= value];"""
        keyword_token = self.advance()
        name = self.expect(TokenType.IDENTIFIER).value
        
        is_mutable = keyword_token.type == TokenType.VAR
        is_const = keyword_token.type == TokenType.CONST
        
        type_annotation = None
        if self.consume(TokenType.COLON):
            type_annotation = self.parse_type()
        
        initial_value = None
        if self.consume(TokenType.ASSIGN):
            initial_value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON)
        
        return VariableDecl(
            name, type_annotation, initial_value,
            is_mutable=is_mutable, is_const=is_const
        )
    
    def parse_type(self) -> Type:
        """Parse type annotation"""
        is_const = self.consume(TokenType.CONST)
        is_pointer = False
        pointer_depth = 0
        
        # Pointer prefix
        while self.consume(TokenType.STAR):
            is_pointer = True
            pointer_depth += 1
        
        # Type name
        if not self.match(TokenType.IDENTIFIER, TokenType.INT, TokenType.UINT,
                         TokenType.CHAR_TYPE, TokenType.BOOL_TYPE,
                         TokenType.FLOAT_TYPE, TokenType.DOUBLE_TYPE,
                         TokenType.STRING_TYPE, TokenType.OBJECT):
            self.error(f"Expected type, got {self.current_token.type}")
        
        type_name = self.advance().value
        
        # Generics
        generic_args = None
        if self.consume(TokenType.LT):
            generic_args = []
            generic_args.append(self.parse_type())
            while self.consume(TokenType.COMMA):
                generic_args.append(self.parse_type())
            self.expect(TokenType.GT)
        
        return Type(
            name=type_name,
            is_pointer=is_pointer,
            pointer_depth=pointer_depth,
            is_const=is_const,
            generic_args=generic_args
        )
    
    def parse_function_declaration(self) -> FunctionDecl:
        """Parse: fnc Name([params]) [-> return_type] { body }"""
        self.expect(TokenType.FNC)
        name = self.expect(TokenType.IDENTIFIER).value
        
        # Generic type parameters
        type_params = None
        is_generic = False
        if self.consume(TokenType.LT):
            is_generic = True
            type_params = []
            type_params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.consume(TokenType.COMMA):
                type_params.append(self.expect(TokenType.IDENTIFIER).value)
            self.expect(TokenType.GT)
        
        # Parameters
        self.expect(TokenType.LPAREN)
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.parse_parameter())
            while self.consume(TokenType.COMMA):
                params.append(self.parse_parameter())
        self.expect(TokenType.RPAREN)
        
        # Return type
        return_type = None
        if self.consume(TokenType.ARROW):
            return_type = self.parse_type()
        
        # Body
        body = self.parse_block()
        
        return FunctionDecl(name, params, return_type, body, type_params, is_generic)
    
    def parse_parameter(self) -> Parameter:
        """Parse function parameter"""
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.COLON)
        type_annotation = self.parse_type()
        
        default_value = None
        if self.consume(TokenType.ASSIGN):
            default_value = self.parse_expression()
        
        return Parameter(name, type_annotation, default_value)
    
    def parse_class_declaration(self) -> ClassDecl:
        """Parse class declaration"""
        self.expect(TokenType.CLASS)
        name = self.expect(TokenType.IDENTIFIER).value
        
        parent_class = None
        if self.consume(TokenType.COLON):
            parent_class = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LBRACE)
        
        fields = []
        methods = []
        
        while not self.match(TokenType.RBRACE):
            if self.match(TokenType.FNC):
                methods.append(self.parse_function_declaration())
            else:
                # Parse field
                name_field = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.COLON)
                type_field = self.parse_type()
                
                initial_value = None
                if self.consume(TokenType.ASSIGN):
                    initial_value = self.parse_expression()
                
                fields.append(ClassField(name_field, type_field, initial_value))
                self.consume(TokenType.SEMICOLON)
        
        self.expect(TokenType.RBRACE)
        return ClassDecl(name, fields, methods, parent_class)
    
    def parse_block(self) -> Block:
        """Parse block: { statements }"""
        self.expect(TokenType.LBRACE)
        statements = []
        
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_if_statement(self) -> IfStmt:
        """Parse if/eif/else statement"""
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_block = self.parse_block()
        
        elif_blocks = []
        while self.match(TokenType.EIF):
            self.advance()
            self.expect(TokenType.LPAREN)
            elif_condition = self.parse_expression()
            self.expect(TokenType.RPAREN)
            elif_block = self.parse_block()
            elif_blocks.append((elif_condition, elif_block))
        
        else_block = None
        if self.consume(TokenType.ELSE):
            else_block = self.parse_block()
        
        return IfStmt(condition, then_block, elif_blocks or None, else_block)
    
    def parse_when_statement(self) -> WhenStmt:
        """Parse when statement (runs once, errors if false)"""
        self.expect(TokenType.WHEN)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        block = self.parse_block()
        return WhenStmt(condition, block)
    
    def parse_though_statement(self) -> ThoughStmt:
        """Parse though statement (runs if condition is false)"""
        self.expect(TokenType.THOUGH)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        block = self.parse_block()
        return ThoughStmt(condition, block)
    
    def parse_switch_statement(self) -> SwitchStmt:
        """Parse incase/switch statement"""
        self.expect(TokenType.INCASE)
        self.expect(TokenType.LPAREN)
        expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.LBRACE)
        cases = []
        default_case = None
        
        while not self.match(TokenType.RBRACE):
            if self.consume(TokenType.CASE):
                value = self.parse_expression()
                self.expect(TokenType.COLON)
                block_stmts = []
                while not self.match(TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE):
                    stmt = self.parse_statement()
                    if stmt:
                        block_stmts.append(stmt)
                cases.append(Case(value, Block(block_stmts)))
            
            elif self.consume(TokenType.DEFAULT):
                self.expect(TokenType.COLON)
                block_stmts = []
                while not self.match(TokenType.CASE, TokenType.DEFAULT, TokenType.RBRACE):
                    stmt = self.parse_statement()
                    if stmt:
                        block_stmts.append(stmt)
                default_case = Block(block_stmts)
        
        self.expect(TokenType.RBRACE)
        return SwitchStmt(expr, cases, default_case)
    
    def parse_for_loop(self) -> ForStmt:
        """Parse for loop: for (init; cond; update) { body }"""
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        
        init = None
        if not self.match(TokenType.SEMICOLON):
            if self.match(TokenType.LET, TokenType.VAR):
                init = self.parse_variable_declaration()
            else:
                init = self.parse_expression()
                self.consume(TokenType.SEMICOLON)
        else:
            self.consume(TokenType.SEMICOLON)
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        update = None
        if not self.match(TokenType.RPAREN):
            update = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block()
        return ForStmt(init, condition, update, body)
    
    def parse_while_loop(self) -> WhileStmt:
        """Parse while loop"""
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStmt(condition, body)
    
    def parse_do_while_loop(self) -> DoWhileStmt:
        """Parse do-while loop"""
        self.expect(TokenType.DO)
        body = self.parse_block()
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.consume(TokenType.SEMICOLON)
        return DoWhileStmt(body, condition)
    
    def parse_agin_loop(self) -> AginStmt:
        """Parse agin loop: agin(times [, increment]) { body }"""
        self.expect(TokenType.AGIN)
        self.expect(TokenType.LPAREN)
        times = self.parse_expression()
        
        increment = False
        if self.consume(TokenType.COMMA):
            # Should be a boolean
            if self.match(TokenType.BOOLEAN):
                increment = self.advance().value == "true"
        
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return AginStmt(times, body, increment)
    
    def parse_return_statement(self) -> ReturnStmt:
        """Parse return statement"""
        self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        
        self.consume(TokenType.SEMICOLON)
        return ReturnStmt(value)
    
    def parse_import_statement(self) -> ImportStmt:
        """Parse: add "module" [-as "alias"] [*]"""
        self.expect(TokenType.ADD)
        module = self.expect(TokenType.STRING).value
        
        alias = None
        if self.consume(TokenType.MINUS):
            self.expect(TokenType.AS)
            alias = self.expect(TokenType.STRING).value
        
        import_all = self.consume(TokenType.STAR)
        self.consume(TokenType.SEMICOLON)
        
        return ImportStmt(module, alias, None, import_all)
    
    def parse_from_import_statement(self) -> ImportStmt:
        """Parse: from "module" -add "item" [as "alias"]"""
        self.expect(TokenType.FROM)
        module = self.expect(TokenType.STRING).value
        self.expect(TokenType.MINUS)
        self.expect(TokenType.ADD)
        
        specific_items = []
        
        # Single item or multiple in parentheses
        if self.consume(TokenType.LPAREN):
            specific_items.append(self.expect(TokenType.STRING).value)
            while self.consume(TokenType.COMMA):
                specific_items.append(self.expect(TokenType.STRING).value)
            self.expect(TokenType.RPAREN)
        else:
            specific_items.append(self.expect(TokenType.STRING).value)
        
        self.consume(TokenType.SEMICOLON)
        return ImportStmt(module, None, specific_items)
    
    def parse_expression(self) -> Optional[ASTNode]:
        """Parse expression"""
        return self.parse_ternary()
    
    def parse_ternary(self) -> ASTNode:
        """Parse ternary operator: expr ? true_expr : false_expr"""
        expr = self.parse_logical_or()
        
        if self.consume(TokenType.QUESTION):
            true_expr = self.parse_expression()
            self.expect(TokenType.COLON)
            false_expr = self.parse_expression()
            return TernaryOp(expr, true_expr, false_expr)
        
        return expr
    
    def parse_logical_or(self) -> ASTNode:
        """Parse logical OR"""
        left = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self) -> ASTNode:
        """Parse logical AND"""
        left = self.parse_bitwise_or()
        
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.parse_bitwise_or()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_or(self) -> ASTNode:
        """Parse bitwise OR"""
        left = self.parse_bitwise_xor()
        
        while self.match(TokenType.BIT_OR):
            op = self.advance().value
            right = self.parse_bitwise_xor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_xor(self) -> ASTNode:
        """Parse bitwise XOR"""
        left = self.parse_bitwise_and()
        
        while self.match(TokenType.BIT_XOR):
            op = self.advance().value
            right = self.parse_bitwise_and()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_bitwise_and(self) -> ASTNode:
        """Parse bitwise AND"""
        left = self.parse_equality()
        
        while self.match(TokenType.AMPERSAND):
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_equality(self) -> ASTNode:
        """Parse equality operators: ==, !="""
        left = self.parse_relational()
        
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.advance().value
            right = self.parse_relational()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_relational(self) -> ASTNode:
        """Parse relational operators: <, >, <=, >="""
        left = self.parse_shift()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op = self.advance().value
            right = self.parse_shift()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_shift(self) -> ASTNode:
        """Parse shift operators: <<, >>"""
        left = self.parse_additive()
        
        while self.match(TokenType.LSHIFT, TokenType.RSHIFT):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplication, division, modulo"""
        left = self.parse_power()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.advance().value
            right = self.parse_power()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_power(self) -> ASTNode:
        """Parse exponentiation"""
        left = self.parse_unary()
        
        if self.match(TokenType.POWER):
            op = self.advance().value
            right = self.parse_power()  # Right associative
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary operators"""
        if self.match(TokenType.MINUS, TokenType.PLUS, TokenType.NOT, TokenType.BIT_NOT):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryOp(op, operand, is_prefix=True)
        
        if self.match(TokenType.INCREMENT, TokenType.DECREMENT):
            op = self.advance().value
            operand = self.parse_postfix()
            return UnaryOp(op, operand, is_prefix=True)
        
        if self.match(TokenType.STAR):
            # Dereference
            self.advance()
            operand = self.parse_unary()
            return Pointer(operand, is_address_of=False)
        
        if self.match(TokenType.AMPERSAND):
            # Address-of
            self.advance()
            operand = self.parse_unary()
            return Pointer(operand, is_address_of=True)
        
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        """Parse postfix expressions (function calls, array access, member access)"""
        expr = self.parse_primary()
        
        while True:
            if self.consume(TokenType.INCREMENT):
                expr = UnaryOp("++", expr, is_prefix=False)
            elif self.consume(TokenType.DECREMENT):
                expr = UnaryOp("--", expr, is_prefix=False)
            elif self.consume(TokenType.LPAREN):
                # Function call
                if isinstance(expr, Identifier):
                    args = []
                    if not self.match(TokenType.RPAREN):
                        args.append(self.parse_expression())
                        while self.consume(TokenType.COMMA):
                            args.append(self.parse_expression())
                    self.expect(TokenType.RPAREN)
                    expr = FunctionCall(expr.name, args)
                else:
                    self.error("Invalid function call")
            elif self.consume(TokenType.LBRACKET):
                # Array index
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = ArrayIndex(expr, index)
            elif self.consume(TokenType.DOT):
                # Member access
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberAccess(expr, member)
            else:
                break
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions"""
        # Literals
        if self.match(TokenType.INTEGER):
            token = self.advance()
            return IntLiteral(int(token.value, 0), token.value)
        
        if self.match(TokenType.FLOAT):
            token = self.advance()
            return FloatLiteral(float(token.value.rstrip('fF')))
        
        if self.match(TokenType.DOUBLE):
            token = self.advance()
            return DoubleLiteral(float(token.value.rstrip('dD')))
        
        if self.match(TokenType.STRING):
            token = self.advance()
            return StringLiteral(token.value, False)
        
        if self.match(TokenType.CHAR):
            token = self.advance()
            return CharLiteral(token.value)
        
        if self.match(TokenType.BOOLEAN):
            token = self.advance()
            return BooleanLiteral(token.value == "true")
        
        if self.match(TokenType.NULL_TYPE):
            self.advance()
            return NullLiteral()
        
        # Identifier
        if self.match(TokenType.IDENTIFIER):
            name = self.advance().value
            
            # Check for assignment
            if self.match(TokenType.ASSIGN, TokenType.PLUS_ASSIGN, 
                          TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN,
                          TokenType.SLASH_ASSIGN):
                op = self.advance().value
                value = self.parse_expression()
                return Assignment(Identifier(name), value, op)
            
            return Identifier(name)
        
        # Parenthesized expression
        if self.consume(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token: {self.current_token.type}")

def parse_source(source: str) -> Program:
    """Convenience function to lex and parse source code"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
