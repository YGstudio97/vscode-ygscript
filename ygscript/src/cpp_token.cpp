/*
 * YGScript C++ - Token Implementation
 */

#include "cpp_token.hpp"

namespace ygscript {

bool Token::is_keyword() const noexcept {
    switch (type) {
        case TokenType::LET:
        case TokenType::VAR:
        case TokenType::CONST:
        case TokenType::FNC:
        case TokenType::RETURN:
        case TokenType::IF:
        case TokenType::EIF:
        case TokenType::ELSE:
        case TokenType::INCASE:
        case TokenType::CASE:
        case TokenType::DEFAULT:
        case TokenType::WHEN:
        case TokenType::THOUGH:
        case TokenType::FOR:
        case TokenType::WHILE:
        case TokenType::DO:
        case TokenType::AGIN:
        case TokenType::BREAK:
        case TokenType::CONTINUE:
        case TokenType::ADD:
        case TokenType::FROM:
        case TokenType::AS:
        case TokenType::CLASS:
            return true;
        default:
            return false;
    }
}

bool Token::is_type() const noexcept {
    switch (type) {
        case TokenType::INT:
        case TokenType::UINT:
        case TokenType::CHAR_TYPE:
        case TokenType::BOOL_TYPE:
        case TokenType::FLOAT_TYPE:
        case TokenType::DOUBLE_TYPE:
        case TokenType::STRING_TYPE:
        case TokenType::OBJECT:
        case TokenType::NULL_TYPE:
            return true;
        default:
            return false;
    }
}

bool Token::is_operator() const noexcept {
    switch (type) {
        case TokenType::PLUS:
        case TokenType::MINUS:
        case TokenType::STAR:
        case TokenType::SLASH:
        case TokenType::PERCENT:
        case TokenType::EQ:
        case TokenType::NE:
        case TokenType::LT:
        case TokenType::LE:
        case TokenType::GT:
        case TokenType::GE:
        case TokenType::AND:
        case TokenType::OR:
        case TokenType::NOT:
        case TokenType::BIT_AND:
        case TokenType::BIT_OR:
        case TokenType::BIT_XOR:
        case TokenType::BIT_NOT:
        case TokenType::LSHIFT:
        case TokenType::RSHIFT:
        case TokenType::ASSIGN:
        case TokenType::PLUS_ASSIGN:
        case TokenType::MINUS_ASSIGN:
        case TokenType::STAR_ASSIGN:
        case TokenType::SLASH_ASSIGN:
        case TokenType::INCREMENT:
        case TokenType::DECREMENT:
            return true;
        default:
            return false;
    }
}

std::string_view token_type_name(TokenType type) noexcept {
#define TOKEN_NAME(t) case TokenType::t: return #t
    switch (type) {
        TOKEN_NAME(INTEGER);
        TOKEN_NAME(FLOAT);
        TOKEN_NAME(DOUBLE);
        TOKEN_NAME(STRING);
        TOKEN_NAME(CHAR);
        TOKEN_NAME(BOOLEAN);
        TOKEN_NAME(LET);
        TOKEN_NAME(VAR);
        TOKEN_NAME(CONST);
        TOKEN_NAME(FNC);
        TOKEN_NAME(RETURN);
        TOKEN_NAME(IF);
        TOKEN_NAME(EIF);
        TOKEN_NAME(ELSE);
        TOKEN_NAME(INCASE);
        TOKEN_NAME(CASE);
        TOKEN_NAME(DEFAULT);
        TOKEN_NAME(WHEN);
        TOKEN_NAME(THOUGH);
        TOKEN_NAME(FOR);
        TOKEN_NAME(WHILE);
        TOKEN_NAME(DO);
        TOKEN_NAME(AGIN);
        TOKEN_NAME(BREAK);
        TOKEN_NAME(CONTINUE);
        TOKEN_NAME(ADD);
        TOKEN_NAME(FROM);
        TOKEN_NAME(AS);
        TOKEN_NAME(INT);
        TOKEN_NAME(UINT);
        TOKEN_NAME(CHAR_TYPE);
        TOKEN_NAME(BOOL_TYPE);
        TOKEN_NAME(FLOAT_TYPE);
        TOKEN_NAME(DOUBLE_TYPE);
        TOKEN_NAME(STRING_TYPE);
        TOKEN_NAME(OBJECT);
        TOKEN_NAME(NULL_TYPE);
        TOKEN_NAME(CLASS);
        TOKEN_NAME(PLUS);
        TOKEN_NAME(MINUS);
        TOKEN_NAME(STAR);
        TOKEN_NAME(SLASH);
        TOKEN_NAME(PERCENT);
        TOKEN_NAME(EQ);
        TOKEN_NAME(NE);
        TOKEN_NAME(LT);
        TOKEN_NAME(LE);
        TOKEN_NAME(GT);
        TOKEN_NAME(GE);
        TOKEN_NAME(AND);
        TOKEN_NAME(OR);
        TOKEN_NAME(NOT);
        TOKEN_NAME(BIT_AND);
        TOKEN_NAME(BIT_OR);
        TOKEN_NAME(BIT_XOR);
        TOKEN_NAME(BIT_NOT);
        TOKEN_NAME(LSHIFT);
        TOKEN_NAME(RSHIFT);
        TOKEN_NAME(ASSIGN);
        TOKEN_NAME(PLUS_ASSIGN);
        TOKEN_NAME(MINUS_ASSIGN);
        TOKEN_NAME(STAR_ASSIGN);
        TOKEN_NAME(SLASH_ASSIGN);
        TOKEN_NAME(INCREMENT);
        TOKEN_NAME(DECREMENT);
        TOKEN_NAME(LPAREN);
        TOKEN_NAME(RPAREN);
        TOKEN_NAME(LBRACE);
        TOKEN_NAME(RBRACE);
        TOKEN_NAME(LBRACKET);
        TOKEN_NAME(RBRACKET);
        TOKEN_NAME(SEMICOLON);
        TOKEN_NAME(COLON);
        TOKEN_NAME(COMMA);
        TOKEN_NAME(DOT);
        TOKEN_NAME(ARROW);
        TOKEN_NAME(QUESTION);
        TOKEN_NAME(AMPERSAND);
        TOKEN_NAME(IDENTIFIER);
        TOKEN_NAME(EOF_TOKEN);
        TOKEN_NAME(NEWLINE);
    }
#undef TOKEN_NAME
    return "UNKNOWN";
}

} // namespace ygscript
