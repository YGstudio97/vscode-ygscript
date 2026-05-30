/*
 * YGScript C++ - Parser Implementation (Simplified)
 */

#include "cpp_parser.hpp"
#include <stdexcept>

namespace ygscript {

Parser::Parser(const std::vector<Token>& tokens_) : tokens(tokens_) {}

Program Parser::parse() {
    Program program;
    while (!current().is(TokenType::EOF_TOKEN)) {
        auto stmt = parse_statement();
        if (stmt) {
            program.statements.push_back(stmt);
        }
    }
    return program;
}

const Token& Parser::current() const noexcept {
    if (pos < tokens.size()) {
        return tokens[pos];
    }
    static const Token eof_token(TokenType::EOF_TOKEN, "", 0, 0);
    return eof_token;
}

const Token& Parser::peek(size_t offset) const noexcept {
    if (pos + offset < tokens.size()) {
        return tokens[pos + offset];
    }
    static const Token eof_token(TokenType::EOF_TOKEN, "", 0, 0);
    return eof_token;
}

const Token& Parser::advance() noexcept {
    if (pos < tokens.size()) {
        return tokens[pos++];
    }
    static const Token eof_token(TokenType::EOF_TOKEN, "", 0, 0);
    return eof_token;
}

const Token& Parser::expect(TokenType type) {
    if (!current().is(type)) {
        error("Expected " + std::string(token_type_name(type)));
    }
    return advance();
}

bool Parser::match(TokenType type) const noexcept {
    return current().is(type);
}

bool Parser::match_any(std::initializer_list<TokenType> types) const noexcept {
    for (TokenType t : types) {
        if (current().is(t)) return true;
    }
    return false;
}

bool Parser::consume(TokenType type) noexcept {
    if (current().is(type)) {
        advance();
        return true;
    }
    return false;
}

ASTNodePtr Parser::parse_statement() {
    if (match(TokenType::LET) || match(TokenType::VAR) || match(TokenType::CONST)) {
        return parse_variable_declaration();
    }
    if (match(TokenType::FNC)) {
        return parse_function_declaration();
    }
    if (match(TokenType::IF)) {
        return parse_if_statement();
    }
    if (match(TokenType::FOR)) {
        return parse_for_loop();
    }
    if (match(TokenType::WHILE)) {
        return parse_while_loop();
    }
    if (match(TokenType::DO)) {
        return parse_do_while_loop();
    }
    if (match(TokenType::AGIN)) {
        return parse_agin_loop();
    }
    if (match(TokenType::RETURN)) {
        return parse_return_statement();
    }
    if (match(TokenType::ADD)) {
        return parse_import_statement();
    }
    if (match(TokenType::LBRACE)) {
        return parse_block();
    }
    if (match(TokenType::BREAK)) {
        advance();
        consume(TokenType::SEMICOLON);
        return make_node(BreakStmt{});
    }
    if (match(TokenType::CONTINUE)) {
        advance();
        consume(TokenType::SEMICOLON);
        return make_node(ContinueStmt{});
    }
    
    auto expr = parse_expression();
    consume(TokenType::SEMICOLON);
    return make_node(ExpressionStmt{expr});
}

ASTNodePtr Parser::parse_variable_declaration() {
    const auto& keyword = advance();
    bool is_mutable = keyword.is(TokenType::VAR);
    bool is_const = keyword.is(TokenType::CONST);
    
    const auto& name_token = expect(TokenType::IDENTIFIER);
    std::string name = name_token.value;
    
    std::optional<Type> type_annotation;
    if (consume(TokenType::COLON)) {
        type_annotation = parse_type();
    }
    
    std::optional<ASTNodePtr> initial_value;
    if (consume(TokenType::ASSIGN)) {
        initial_value = parse_expression();
    }
    
    consume(TokenType::SEMICOLON);
    
    VariableDecl decl;
    decl.name = name;
    decl.type_annotation = type_annotation;
    decl.initial_value = initial_value;
    decl.is_mutable = is_mutable;
    decl.is_const = is_const;
    
    return make_node(decl);
}

ASTNodePtr Parser::parse_function_declaration() {
    expect(TokenType::FNC);
    const auto& name_token = expect(TokenType::IDENTIFIER);
    std::string name = name_token.value;
    
    expect(TokenType::LPAREN);
    std::vector<Parameter> params;
    if (!match(TokenType::RPAREN)) {
        do {
            params.push_back(parse_parameter());
        } while (consume(TokenType::COMMA));
    }
    expect(TokenType::RPAREN);
    
    std::optional<Type> return_type;
    if (consume(TokenType::ARROW)) {
        return_type = parse_type();
    }
    
    auto body = *parse_block()->get<Block>();
    
    FunctionDecl decl;
    decl.name = name;
    decl.params = params;
    decl.return_type = return_type;
    decl.body = body;
    
    return make_node(decl);
}

ASTNodePtr Parser::parse_block() {
    expect(TokenType::LBRACE);
    ASTNodeList statements;
    
    while (!match(TokenType::RBRACE) && !match(TokenType::EOF_TOKEN)) {
        auto stmt = parse_statement();
        if (stmt) {
            statements.push_back(stmt);
        }
    }
    
    expect(TokenType::RBRACE);
    
    Block block;
    block.statements = statements;
    return make_node(block);
}

ASTNodePtr Parser::parse_if_statement() {
    expect(TokenType::IF);
    expect(TokenType::LPAREN);
    auto condition = parse_expression();
    expect(TokenType::RPAREN);
    auto then_block = *parse_block()->get<Block>();
    
    std::vector<std::pair<ASTNodePtr, Block>> elif_blocks;
    while (match(TokenType::EIF)) {
        advance();
        expect(TokenType::LPAREN);
        auto elif_cond = parse_expression();
        expect(TokenType::RPAREN);
        auto elif_blk = *parse_block()->get<Block>();
        elif_blocks.push_back({elif_cond, elif_blk});
    }
    
    std::optional<Block> else_block;
    if (consume(TokenType::ELSE)) {
        else_block = *parse_block()->get<Block>();
    }
    
    IfStmt stmt;
    stmt.condition = condition;
    stmt.then_block = then_block;
    stmt.elif_blocks = elif_blocks;
    stmt.else_block = else_block;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_for_loop() {
    expect(TokenType::FOR);
    expect(TokenType::LPAREN);
    
    std::optional<ASTNodePtr> init;
    if (!match(TokenType::SEMICOLON)) {
        init = parse_expression();
    }
    expect(TokenType::SEMICOLON);
    
    std::optional<ASTNodePtr> condition;
    if (!match(TokenType::SEMICOLON)) {
        condition = parse_expression();
    }
    expect(TokenType::SEMICOLON);
    
    std::optional<ASTNodePtr> update;
    if (!match(TokenType::RPAREN)) {
        update = parse_expression();
    }
    expect(TokenType::RPAREN);
    
    auto body = *parse_block()->get<Block>();
    
    ForStmt stmt;
    stmt.init = init;
    stmt.condition = condition;
    stmt.update = update;
    stmt.body = body;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_while_loop() {
    expect(TokenType::WHILE);
    expect(TokenType::LPAREN);
    auto condition = parse_expression();
    expect(TokenType::RPAREN);
    auto body = *parse_block()->get<Block>();
    
    WhileStmt stmt;
    stmt.condition = condition;
    stmt.body = body;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_do_while_loop() {
    expect(TokenType::DO);
    auto body = *parse_block()->get<Block>();
    expect(TokenType::WHILE);
    expect(TokenType::LPAREN);
    auto condition = parse_expression();
    expect(TokenType::RPAREN);
    consume(TokenType::SEMICOLON);
    
    DoWhileStmt stmt;
    stmt.body = body;
    stmt.condition = condition;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_agin_loop() {
    expect(TokenType::AGIN);
    expect(TokenType::LPAREN);
    auto times = parse_expression();
    expect(TokenType::RPAREN);
    auto body = *parse_block()->get<Block>();
    
    AginStmt stmt;
    stmt.times = times;
    stmt.body = body;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_return_statement() {
    expect(TokenType::RETURN);
    
    std::optional<ASTNodePtr> value;
    if (!match(TokenType::SEMICOLON) && !match(TokenType::RBRACE)) {
        value = parse_expression();
    }
    
    consume(TokenType::SEMICOLON);
    
    ReturnStmt stmt;
    stmt.value = value;
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_import_statement() {
    expect(TokenType::ADD);
    const auto& module_token = expect(TokenType::STRING);
    
    ImportStmt stmt;
    stmt.module = module_token.value;
    
    consume(TokenType::SEMICOLON);
    
    return make_node(stmt);
}

ASTNodePtr Parser::parse_expression_statement() {
    auto expr = parse_expression();
    consume(TokenType::SEMICOLON);
    return make_node(ExpressionStmt{expr});
}

ASTNodePtr Parser::parse_expression() {
    return parse_ternary();
}

ASTNodePtr Parser::parse_ternary() {
    auto expr = parse_logical_or();
    
    if (consume(TokenType::QUESTION)) {
        auto true_expr = parse_expression();
        expect(TokenType::COLON);
        auto false_expr = parse_expression();
        // TODO: Create ternary node
    }
    
    return expr;
}

ASTNodePtr Parser::parse_logical_or() {
    auto left = parse_logical_and();
    
    while (match(TokenType::OR)) {
        auto op_token = advance();
        auto right = parse_logical_and();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_logical_and() {
    auto left = parse_bitwise_or();
    
    while (match(TokenType::AND)) {
        auto op_token = advance();
        auto right = parse_bitwise_or();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_bitwise_or() {
    auto left = parse_bitwise_xor();
    
    while (match(TokenType::BIT_OR)) {
        auto op_token = advance();
        auto right = parse_bitwise_xor();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_bitwise_xor() {
    auto left = parse_bitwise_and();
    
    while (match(TokenType::BIT_XOR)) {
        auto op_token = advance();
        auto right = parse_bitwise_and();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_bitwise_and() {
    auto left = parse_equality();
    
    while (match(TokenType::BIT_AND)) {
        auto op_token = advance();
        auto right = parse_equality();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_equality() {
    auto left = parse_relational();
    
    while (match_any({TokenType::EQ, TokenType::NE})) {
        auto op_token = advance();
        auto right = parse_relational();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_relational() {
    auto left = parse_shift();
    
    while (match_any({TokenType::LT, TokenType::LE, TokenType::GT, TokenType::GE})) {
        auto op_token = advance();
        auto right = parse_shift();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_shift() {
    auto left = parse_additive();
    
    while (match_any({TokenType::LSHIFT, TokenType::RSHIFT})) {
        auto op_token = advance();
        auto right = parse_additive();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_additive() {
    auto left = parse_multiplicative();
    
    while (match_any({TokenType::PLUS, TokenType::MINUS})) {
        auto op_token = advance();
        auto right = parse_multiplicative();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_multiplicative() {
    auto left = parse_power();
    
    while (match_any({TokenType::STAR, TokenType::SLASH, TokenType::PERCENT})) {
        auto op_token = advance();
        auto right = parse_power();
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        left = make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_power() {
    auto left = parse_unary();
    
    if (match(TokenType::BIT_XOR)) {  // Using ^ for power
        auto op_token = advance();
        auto right = parse_power();  // Right associative
        
        BinaryOp binop;
        binop.left = left;
        binop.op = op_token.value;
        binop.right = right;
        
        return make_node(binop);
    }
    
    return left;
}

ASTNodePtr Parser::parse_unary() {
    if (match_any({TokenType::MINUS, TokenType::PLUS, TokenType::NOT, TokenType::BIT_NOT})) {
        auto op_token = advance();
        auto operand = parse_unary();
        
        UnaryOp unop;
        unop.op = op_token.value;
        unop.operand = operand;
        
        return make_node(unop);
    }
    
    if (match(TokenType::AMPERSAND)) {
        auto op_token = advance();
        auto operand = parse_unary();
        
        UnaryOp unop;
        unop.op = op_token.value;
        unop.operand = operand;
        
        return make_node(unop);
    }
    
    return parse_postfix();
}

ASTNodePtr Parser::parse_postfix() {
    auto expr = parse_primary();
    
    while (true) {
        if (match(TokenType::LPAREN)) {
            advance();
            ASTNodeList args;
            if (!match(TokenType::RPAREN)) {
                do {
                    args.push_back(parse_expression());
                } while (consume(TokenType::COMMA));
            }
            expect(TokenType::RPAREN);
            
            if (auto id = expr->get<Identifier>()) {
                FunctionCall call;
                call.name = id->name;
                call.args = args;
                
                expr = make_node(call);
            }
        }
        else if (match(TokenType::LBRACKET)) {
            advance();
            auto index = parse_expression();
            expect(TokenType::RBRACKET);
            // TODO: Array access
        }
        else if (match(TokenType::DOT)) {
            advance();
            const auto& member_token = expect(TokenType::IDENTIFIER);
            // TODO: Member access
        }
        else {
            break;
        }
    }
    
    return expr;
}

ASTNodePtr Parser::parse_primary() {
    if (match(TokenType::INTEGER)) {
        const auto& token = advance();
        IntLiteral lit;
        lit.value = std::stoll(token.value);
        return make_node(lit);
    }
    
    if (match(TokenType::FLOAT)) {
        const auto& token = advance();
        FloatLiteral lit;
        lit.value = std::stod(token.value);
        return make_node(lit);
    }
    
    if (match(TokenType::STRING)) {
        const auto& token = advance();
        StringLiteral lit;
        lit.value = token.value;
        return make_node(lit);
    }
    
    if (match(TokenType::BOOLEAN)) {
        const auto& token = advance();
        BooleanLiteral lit;
        lit.value = (token.value == "true");
        return make_node(lit);
    }
    
    if (match(TokenType::NULL_TYPE)) {
        advance();
        return make_node(NullLiteral{});
    }
    
    if (match(TokenType::IDENTIFIER)) {
        const auto& token = advance();
        Identifier id;
        id.name = token.value;
        
        // Check for assignment
        if (match_any({TokenType::ASSIGN, TokenType::PLUS_ASSIGN, 
                       TokenType::MINUS_ASSIGN, TokenType::STAR_ASSIGN,
                       TokenType::SLASH_ASSIGN})) {
            auto op_token = advance();
            auto value = parse_expression();
            
            Assignment assign;
            assign.target = make_node(id);
            assign.value = value;
            assign.op = op_token.value;
            
            return make_node(assign);
        }
        
        return make_node(id);
    }
    
    if (consume(TokenType::LPAREN)) {
        auto expr = parse_expression();
        expect(TokenType::RPAREN);
        return expr;
    }
    
    error("Unexpected token: " + current().value);
}

Type Parser::parse_type() {
    const auto& type_token = expect(TokenType::IDENTIFIER);
    
    Type type;
    type.name = type_token.value;
    
    return type;
}

Parameter Parser::parse_parameter() {
    const auto& name_token = expect(TokenType::IDENTIFIER);
    expect(TokenType::COLON);
    auto type_annotation = parse_type();
    
    Parameter param;
    param.name = name_token.value;
    param.type_annotation = type_annotation;
    
    return param;
}

void Parser::error(const std::string& msg) {
    throw ParserError(msg, current().line, current().column);
}

} // namespace ygscript
