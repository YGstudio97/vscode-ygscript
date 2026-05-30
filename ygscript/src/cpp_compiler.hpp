/*
 * YGScript C++ - Compiler
 * C++20 Implementation - AST to Bytecode Compilation
 */

#ifndef YGSCRIPT_CPP_COMPILER_HPP
#define YGSCRIPT_CPP_COMPILER_HPP

#include "cpp_ast.hpp"
#include "cpp_bytecode.hpp"
#include <memory>
#include <unordered_map>
#include <vector>

namespace ygscript {

class CompileError : public std::runtime_error {
public:
    CompileError(const std::string& msg) : std::runtime_error(msg) {}
};

class Compiler {
public:
    Compiler() = default;
    
    ByteCode compile(const Program& program);
    
private:
    ByteCode bytecode;
    std::unordered_map<std::string, uint32_t> variables;
    std::vector<std::unordered_map<std::string, uint32_t>> scopes;
    
    // Compilation methods
    void compile_program(const Program& prog);
    void compile_node(const ASTNode& node);
    
    void compile_variable_decl(const VariableDecl& decl);
    void compile_function_decl(const FunctionDecl& decl);
    void compile_block(const Block& block);
    void compile_if_stmt(const IfStmt& stmt);
    void compile_for_stmt(const ForStmt& stmt);
    void compile_while_stmt(const WhileStmt& stmt);
    void compile_do_while_stmt(const DoWhileStmt& stmt);
    void compile_agin_stmt(const AginStmt& stmt);
    void compile_return_stmt(const ReturnStmt& stmt);
    void compile_expression_stmt(const ExpressionStmt& stmt);
    void compile_import_stmt(const ImportStmt& stmt);
    
    // Expression compilation
    void compile_expression(const ASTNode& expr);
    void compile_binary_op(const BinaryOp& op);
    void compile_unary_op(const UnaryOp& op);
    void compile_assignment(const Assignment& assign);
    void compile_function_call(const FunctionCall& call);
    void compile_literal(const ASTNode& literal);
    void compile_identifier(const Identifier& id);
    
    // Scope management
    void push_scope();
    void pop_scope();
    void define_variable(const std::string& name);
    bool is_variable_defined(const std::string& name) const;
    uint32_t get_variable_index(const std::string& name) const;
    
    // Utility methods
    [[noreturn]] void error(const std::string& msg);
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_COMPILER_HPP
