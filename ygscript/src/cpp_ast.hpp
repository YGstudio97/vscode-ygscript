/*
 * YGScript C++ - AST Node Definitions
 * C++20 Implementation with Variant Pattern
 */

#ifndef YGSCRIPT_CPP_AST_HPP
#define YGSCRIPT_CPP_AST_HPP

#include <memory>
#include <vector>
#include <string>
#include <variant>
#include <optional>

namespace ygscript {

// Forward declarations
struct ASTNode;
using ASTNodePtr = std::shared_ptr<ASTNode>;
using ASTNodeList = std::vector<ASTNodePtr>;

// ============= Type Nodes =============
struct Type {
    std::string name;
    bool is_pointer = false;
    int pointer_depth = 0;
    bool is_const = false;
    std::optional<std::vector<Type>> generic_args;
};

// ============= Literal Nodes =============
struct IntLiteral {
    long long value;
    std::optional<std::string> type_hint;
};

struct FloatLiteral {
    double value;
    std::optional<std::string> type_hint;
};

struct StringLiteral {
    std::string value;
    bool is_interpolated = false;
};

struct CharLiteral {
    char value;
};

struct BooleanLiteral {
    bool value;
};

struct NullLiteral {};

// ============= Expression Nodes =============
struct Identifier {
    std::string name;
};

struct BinaryOp {
    ASTNodePtr left;
    std::string op;
    ASTNodePtr right;
};

struct UnaryOp {
    std::string op;
    ASTNodePtr operand;
    bool is_prefix = true;
};

struct Assignment {
    ASTNodePtr target;
    ASTNodePtr value;
    std::string op = "=";
};

struct FunctionCall {
    std::string name;
    ASTNodeList args;
    std::optional<std::vector<Type>> type_args;
};

// ============= Statement Nodes =============
struct Block {
    ASTNodeList statements;
};

struct VariableDecl {
    std::string name;
    std::optional<Type> type_annotation;
    std::optional<ASTNodePtr> initial_value;
    bool is_mutable = true;
    bool is_const = false;
};

struct Parameter {
    std::string name;
    Type type_annotation;
    std::optional<ASTNodePtr> default_value;
};

struct FunctionDecl {
    std::string name;
    std::vector<Parameter> params;
    std::optional<Type> return_type;
    Block body;
    std::optional<std::vector<std::string>> type_params;
    bool is_generic = false;
};

struct ReturnStmt {
    std::optional<ASTNodePtr> value;
};

struct IfStmt {
    ASTNodePtr condition;
    Block then_block;
    std::vector<std::pair<ASTNodePtr, Block>> elif_blocks;
    std::optional<Block> else_block;
};

struct ForStmt {
    std::optional<ASTNodePtr> init;
    std::optional<ASTNodePtr> condition;
    std::optional<ASTNodePtr> update;
    Block body;
};

struct WhileStmt {
    ASTNodePtr condition;
    Block body;
};

struct DoWhileStmt {
    Block body;
    ASTNodePtr condition;
};

struct AginStmt {
    ASTNodePtr times;
    Block body;
    bool increment = false;
};

struct BreakStmt {};
struct ContinueStmt {};

struct ExpressionStmt {
    ASTNodePtr expr;
};

struct ImportStmt {
    std::string module;
    std::optional<std::string> alias;
    std::optional<std::vector<std::string>> specific_items;
    bool import_all = false;
};

// ============= Program Node =============
struct Program {
    ASTNodeList statements;
};

// ============= Variant Type =============
using ASTNodeVariant = std::variant<
    Program,
    Block,
    VariableDecl,
    FunctionDecl,
    ReturnStmt,
    IfStmt,
    ForStmt,
    WhileStmt,
    DoWhileStmt,
    AginStmt,
    BreakStmt,
    ContinueStmt,
    ExpressionStmt,
    ImportStmt,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    CharLiteral,
    BooleanLiteral,
    NullLiteral,
    Identifier,
    BinaryOp,
    UnaryOp,
    Assignment,
    FunctionCall
>;

struct ASTNode {
    ASTNodeVariant data;
    
    template<typename T>
    ASTNode(T&& value) : data(std::forward<T>(value)) {}
    
    template<typename T>
    [[nodiscard]] bool is() const {
        return std::holds_alternative<T>(data);
    }
    
    template<typename T>
    [[nodiscard]] T* get() {
        return std::get_if<T>(&data);
    }
    
    template<typename T>
    [[nodiscard]] const T* get() const {
        return std::get_if<T>(&data);
    }
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_AST_HPP
