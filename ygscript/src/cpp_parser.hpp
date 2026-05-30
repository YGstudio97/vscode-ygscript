/*
 * YGScript C++ - Parser
 * C++20 Implementation - Recursive Descent Parser
 */

#ifndef YGSCRIPT_CPP_PARSER_HPP
#define YGSCRIPT_CPP_PARSER_HPP

#include "cpp_token.hpp"
#include "cpp_ast.hpp"
#include <vector>
#include <stdexcept>
#include <memory>

namespace ygscript {

class ParserError : public std::runtime_error {
public:
    int line, column;
    ParserError(const std::string& msg, int l, int c)
        : std::runtime_error(msg), line(l), column(c) {}
};

class Parser {
public:
    explicit Parser(const std::vector<Token>& tokens);
    
    [[nodiscard]] Program parse();
    
private:
    const std::vector<Token>& tokens;
    size_t pos = 0;
    
    [[nodiscard]] const Token& current() const noexcept;
    [[nodiscard]] const Token& peek(size_t offset = 1) const noexcept;
    const Token& advance() noexcept;
    const Token& expect(TokenType type);
    bool match(TokenType type) const noexcept;
    bool match_any(std::initializer_list<TokenType> types) const noexcept;
    bool consume(TokenType type) noexcept;
    
    // Parse methods
    ASTNodePtr parse_statement();
    ASTNodePtr parse_variable_declaration();
    ASTNodePtr parse_function_declaration();
    ASTNodePtr parse_block();
    ASTNodePtr parse_if_statement();
    ASTNodePtr parse_for_loop();
    ASTNodePtr parse_while_loop();
    ASTNodePtr parse_do_while_loop();
    ASTNodePtr parse_agin_loop();
    ASTNodePtr parse_return_statement();
    ASTNodePtr parse_import_statement();
    ASTNodePtr parse_expression_statement();
    
    // Expression parsing
    ASTNodePtr parse_expression();
    ASTNodePtr parse_ternary();
    ASTNodePtr parse_logical_or();
    ASTNodePtr parse_logical_and();
    ASTNodePtr parse_bitwise_or();
    ASTNodePtr parse_bitwise_xor();
    ASTNodePtr parse_bitwise_and();
    ASTNodePtr parse_equality();
    ASTNodePtr parse_relational();
    ASTNodePtr parse_shift();
    ASTNodePtr parse_additive();
    ASTNodePtr parse_multiplicative();
    ASTNodePtr parse_power();
    ASTNodePtr parse_unary();
    ASTNodePtr parse_postfix();
    ASTNodePtr parse_primary();
    
    // Type parsing
    Type parse_type();
    Parameter parse_parameter();
    
    // Utility
    [[noreturn]] void error(const std::string& msg);
    
    // Helper for creating nodes
    template<typename T>
    ASTNodePtr make_node(T&& value) {
        return std::make_shared<ASTNode>(std::forward<T>(value));
    }
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_PARSER_HPP
