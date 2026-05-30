"""
YGScript Lexer - Tokenizes YGScript source code
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Dict

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    DOUBLE = auto()
    STRING = auto()
    CHAR = auto()
    BOOLEAN = auto()
    
    # Keywords
    LET = auto()
    VAR = auto()
    CONST = auto()
    FNC = auto()
    RETURN = auto()
    IF = auto()
    EIF = auto()
    ELSE = auto()
    INCASE = auto()
    CASE = auto()
    DEFAULT = auto()
    WHEN = auto()
    THOUGH = auto()
    FOR = auto()
    WHILE = auto()
    DO = auto()
    AGIN = auto()
    BREAK = auto()
    CONTINUE = auto()
    ADD = auto()
    FROM = auto()
    AS = auto()
    
    # Type keywords
    INT = auto()
    UINT = auto()
    CHAR_TYPE = auto()
    BOOL_TYPE = auto()
    FLOAT_TYPE = auto()
    DOUBLE_TYPE = auto()
    STRING_TYPE = auto()
    OBJECT = auto()
    NULL_TYPE = auto()
    CLASS = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()
    
    # Comparison
    EQ = auto()          # ==
    NE = auto()          # !=
    LT = auto()          # <
    LE = auto()          # <=
    GT = auto()          # >
    GE = auto()          # >=
    
    # Logical
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !
    
    # Assignment
    ASSIGN = auto()      # =
    PLUS_ASSIGN = auto() # +=
    MINUS_ASSIGN = auto()# -=
    STAR_ASSIGN = auto() # *=
    SLASH_ASSIGN = auto()# /=
    
    # Increment/Decrement
    INCREMENT = auto()   # ++
    DECREMENT = auto()   # --
    
    # Bitwise
    BIT_AND = auto()     # &
    BIT_OR = auto()      # |
    BIT_XOR = auto()     # ^
    BIT_NOT = auto()     # ~
    LSHIFT = auto()      # <<
    RSHIFT = auto()      # >>
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    ARROW = auto()       # ->
    QUESTION = auto()
    AT = auto()          # @
    HASH = auto()        # #
    
    # Pointer
    AMPERSAND = auto()   # &
    POINTER = auto()     # *
    
    # String interpolation
    STRING_START = auto() # I"
    STRING_MIDDLE = auto()
    STRING_END = auto()
    
    # Special
    IDENTIFIER = auto()
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    KEYWORDS = {
        'let': TokenType.LET,
        'var': TokenType.VAR,
        'const': TokenType.CONST,
        'fnc': TokenType.FNC,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'eif': TokenType.EIF,
        'else': TokenType.ELSE,
        'incase': TokenType.INCASE,
        'case': TokenType.CASE,
        'default': TokenType.DEFAULT,
        'when': TokenType.WHEN,
        'though': TokenType.THOUGH,
        'for': TokenType.FOR,
        'while': TokenType.WHILE,
        'do': TokenType.DO,
        'agin': TokenType.AGIN,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'add': TokenType.ADD,
        'from': TokenType.FROM,
        'as': TokenType.AS,
        'int': TokenType.INT,
        'uint': TokenType.UINT,
        'char': TokenType.CHAR_TYPE,
        'bool': TokenType.BOOL_TYPE,
        'float': TokenType.FLOAT_TYPE,
        'double': TokenType.DOUBLE_TYPE,
        'string': TokenType.STRING_TYPE,
        'str': TokenType.STRING_TYPE,
        'obj': TokenType.OBJECT,
        'object': TokenType.OBJECT,
        'null': TokenType.NULL_TYPE,
        'class': TokenType.CLASS,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.source):
            char = self.source[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        # Handle hex, octal, binary
        if self.peek() == '0':
            num_str += self.advance()
            if self.peek() in 'xXoObB':
                base_char = self.advance()
                num_str += base_char
                while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                    num_str += self.advance()
                return Token(TokenType.INTEGER, num_str, start_line, start_column)
        
        # Read integer part
        while self.peek() and self.peek().isdigit():
            num_str += self.advance()
        
        # Check for float/double suffix or decimal point
        is_float = False
        is_double = False
        
        if self.peek() == '.':
            is_float = True
            num_str += self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()
        
        # Scientific notation
        if self.peek() and self.peek() in 'eE':
            is_float = True
            num_str += self.advance()
            if self.peek() and self.peek() in '+-':
                num_str += self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()
        
        # Type suffix
        if self.peek() and self.peek() in 'fFdDiIuU':
            suffix = self.advance()
            num_str += suffix
            if suffix in 'fF':
                is_float = True
            elif suffix in 'dD':
                is_double = True
        
        if is_double:
            return Token(TokenType.DOUBLE, num_str, start_line, start_column)
        elif is_float:
            return Token(TokenType.FLOAT, num_str, start_line, start_column)
        else:
            return Token(TokenType.INTEGER, num_str, start_line, start_column)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_column = self.column
        quote_char = self.advance()  # consume " or '
        string_val = ''
        
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
                self.advance()
                escape_char = self.advance()
                escape_map = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'",
                    '0': '\0',
                }
                string_val += escape_map.get(escape_char, escape_char)
            else:
                string_val += self.advance()
        
        if not self.peek():
            self.error(f"Unterminated string")
        
        self.advance()  # consume closing quote
        
        token_type = TokenType.CHAR if quote_char == "'" else TokenType.STRING
        return Token(token_type, string_val, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_column = self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() in '_'):
            ident += self.advance()
        
        # Check for sized types (int8, float32, etc.)
        if self.peek() and self.peek().isdigit():
            size_num = ''
            temp_pos = self.pos
            while self.peek() and self.peek().isdigit():
                size_num += self.advance()
            
            if self.peek() and self.peek() in 'bfdu':
                suffix = self.advance()
                ident += size_num + suffix
        
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.peek() == '\n':
                self.advance()
                continue
            
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            start_line = self.line
            start_column = self.column
            char = self.peek()
            
            if char is None:
                break
            
            # String interpolation: I"..."
            if char == 'I' and self.peek(1) == '"':
                self.advance()  # consume I
                self.advance()  # consume "
                self.tokens.append(Token(TokenType.STRING_START, 'I"', start_line, start_column))
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings and chars
            elif char in '"\'':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.advance()
                if self.peek() == '+':
                    self.advance()
                    self.tokens.append(Token(TokenType.INCREMENT, '++', start_line, start_column))
                elif self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))
            
            elif char == '-':
                self.advance()
                if self.peek() == '-':
                    self.advance()
                    self.tokens.append(Token(TokenType.DECREMENT, '--', start_line, start_column))
                elif self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', start_line, start_column))
                elif self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))
            
            elif char == '*':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.STAR_ASSIGN, '*=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.STAR, '*', start_line, start_column))
            
            elif char == '/':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.SLASH_ASSIGN, '/=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.SLASH, '/', start_line, start_column))
            
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.PERCENT, '%', start_line, start_column))
            
            elif char == '=':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_column))
            
            elif char == '!':
                self.advance()
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, '!=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', start_line, start_column))
            
            elif char == '<':
                self.advance()
                if self.peek() == '<':
                    self.advance()
                    self.tokens.append(Token(TokenType.LSHIFT, '<<', start_line, start_column))
                elif self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.LE, '<=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.LT, '<', start_line, start_column))
            
            elif char == '>':
                self.advance()
                if self.peek() == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.RSHIFT, '>>', start_line, start_column))
                elif self.peek() == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.GE, '>=', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.GT, '>', start_line, start_column))
            
            elif char == '&':
                self.advance()
                if self.peek() == '&':
                    self.advance()
                    self.tokens.append(Token(TokenType.AND, '&&', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.AMPERSAND, '&', start_line, start_column))
            
            elif char == '|':
                self.advance()
                if self.peek() == '|':
                    self.advance()
                    self.tokens.append(Token(TokenType.OR, '||', start_line, start_column))
                else:
                    self.tokens.append(Token(TokenType.BIT_OR, '|', start_line, start_column))
            
            elif char == '^':
                self.advance()
                self.tokens.append(Token(TokenType.BIT_XOR, '^', start_line, start_column))
            
            elif char == '~':
                self.advance()
                self.tokens.append(Token(TokenType.BIT_NOT, '~', start_line, start_column))
            
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))
            
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))
            
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_column))
            
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_column))
            
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_column))
            
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_column))
            
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_column))
            
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
            
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_column))
            
            elif char == '?':
                self.advance()
                self.tokens.append(Token(TokenType.QUESTION, '?', start_line, start_column))
            
            elif char == '@':
                self.advance()
                self.tokens.append(Token(TokenType.AT, '@', start_line, start_column))
            
            elif char == '#':
                self.advance()
                self.tokens.append(Token(TokenType.HASH, '#', start_line, start_column))
            
            else:
                self.error(f"Unexpected character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
