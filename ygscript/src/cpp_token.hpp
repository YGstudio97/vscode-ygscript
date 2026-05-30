/*
 * YGScript C++ - Token Type and Token Definition
 * C++20 Implementation
 */

#ifndef YGSCRIPT_CPP_TOKEN_HPP
#define YGSCRIPT_CPP_TOKEN_HPP

#include <string>
#include <string_view>
#include <ostream>

namespace ygscript {

enum class TokenType : unsigned char {
    // Literals
    INTEGER = 0, FLOAT, DOUBLE, STRING, CHAR, BOOLEAN,
    
    // Keywords
    LET, VAR, CONST, FNC, RETURN,
    IF, EIF, ELSE, INCASE, CASE, DEFAULT,
    WHEN, THOUGH, FOR, WHILE, DO, AGIN,
    BREAK, CONTINUE, ADD, FROM, AS,
    
    // Types
    INT, UINT, CHAR_TYPE, BOOL_TYPE,
    FLOAT_TYPE, DOUBLE_TYPE, STRING_TYPE,
    OBJECT, NULL_TYPE, CLASS,
    
    // Operators
    PLUS, MINUS, STAR, SLASH, PERCENT,
    EQ, NE, LT, LE, GT, GE,
    AND, OR, NOT, BIT_AND, BIT_OR, BIT_XOR,
    BIT_NOT, LSHIFT, RSHIFT, ASSIGN,
    PLUS_ASSIGN, MINUS_ASSIGN, STAR_ASSIGN, SLASH_ASSIGN,
    INCREMENT, DECREMENT,
    
    // Delimiters
    LPAREN, RPAREN, LBRACE, RBRACE,
    LBRACKET, RBRACKET, SEMICOLON, COLON,
    COMMA, DOT, ARROW, QUESTION, AMPERSAND,
    
    // Special
    IDENTIFIER, EOF_TOKEN, NEWLINE
};

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;
    
    Token() : type(TokenType::EOF_TOKEN), line(0), column(0) {}
    
    Token(TokenType t, std::string_view v, int l, int c)
        : type(t), value(v), line(l), column(c) {}
    
    bool is(TokenType t) const noexcept { return type == t; }
    bool is_keyword() const noexcept;
    bool is_type() const noexcept;
    bool is_operator() const noexcept;
};

std::string_view token_type_name(TokenType type) noexcept;

} // namespace ygscript

#endif // YGSCRIPT_CPP_TOKEN_HPP
