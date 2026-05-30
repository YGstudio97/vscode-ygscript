/*
 * YGScript C++ - Lexer (Tokenizer)
 * C++20 Implementation
 */

#ifndef YGSCRIPT_CPP_LEXER_HPP
#define YGSCRIPT_CPP_LEXER_HPP

#include "cpp_token.hpp"
#include <vector>
#include <string_view>
#include <unordered_map>
#include <stdexcept>

namespace ygscript {

class LexerError : public std::runtime_error {
public:
    int line, column;
    LexerError(const std::string& msg, int l, int c)
        : std::runtime_error(msg), line(l), column(c) {}
};

class Lexer {
public:
    explicit Lexer(std::string_view source);
    
    std::vector<Token> tokenize();
    
private:
    const std::string_view source;
    size_t pos = 0;
    int line = 1;
    int column = 1;
    std::vector<Token> tokens;
    
    static inline const std::unordered_map<std::string, TokenType> keywords = {
        {"let", TokenType::LET},
        {"var", TokenType::VAR},
        {"const", TokenType::CONST},
        {"fnc", TokenType::FNC},
        {"return", TokenType::RETURN},
        {"if", TokenType::IF},
        {"eif", TokenType::EIF},
        {"else", TokenType::ELSE},
        {"incase", TokenType::INCASE},
        {"case", TokenType::CASE},
        {"default", TokenType::DEFAULT},
        {"when", TokenType::WHEN},
        {"though", TokenType::THOUGH},
        {"for", TokenType::FOR},
        {"while", TokenType::WHILE},
        {"do", TokenType::DO},
        {"agin", TokenType::AGIN},
        {"break", TokenType::BREAK},
        {"continue", TokenType::CONTINUE},
        {"add", TokenType::ADD},
        {"from", TokenType::FROM},
        {"as", TokenType::AS},
        {"int", TokenType::INT},
        {"uint", TokenType::UINT},
        {"char", TokenType::CHAR_TYPE},
        {"bool", TokenType::BOOL_TYPE},
        {"float", TokenType::FLOAT_TYPE},
        {"double", TokenType::DOUBLE_TYPE},
        {"string", TokenType::STRING_TYPE},
        {"str", TokenType::STRING_TYPE},
        {"obj", TokenType::OBJECT},
        {"object", TokenType::OBJECT},
        {"null", TokenType::NULL_TYPE},
        {"class", TokenType::CLASS},
        {"true", TokenType::BOOLEAN},
        {"false", TokenType::BOOLEAN},
    };
    
    [[nodiscard]] char peek(size_t offset = 0) const noexcept;
    [[nodiscard]] char advance() noexcept;
    void skip_whitespace() noexcept;
    void skip_comment() noexcept;
    void add_token(TokenType type, std::string_view value);
    
    Token read_number();
    Token read_string();
    Token read_identifier();
    
    [[noreturn]] void error(const std::string& message);
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_LEXER_HPP
