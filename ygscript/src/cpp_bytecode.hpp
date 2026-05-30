/*
 * YGScript C++ - Bytecode Definition
 * C++20 Implementation - VM Instruction Set
 */

#ifndef YGSCRIPT_CPP_BYTECODE_HPP
#define YGSCRIPT_CPP_BYTECODE_HPP

#include <vector>
#include <cstdint>
#include <string>
#include <variant>
#include <array>

namespace ygscript {

enum class OpCode : uint8_t {
    // Constants
    LOAD_CONST,      // Load constant from pool
    LOAD_VAR,        // Load variable
    STORE_VAR,       // Store to variable
    
    // Arithmetic
    ADD,
    SUB,
    MUL,
    DIV,
    MOD,
    POW,
    
    // Comparison
    EQ,
    NE,
    LT,
    LE,
    GT,
    GE,
    
    // Logical
    AND,
    OR,
    NOT,
    
    // Bitwise
    BIT_AND,
    BIT_OR,
    BIT_XOR,
    BIT_NOT,
    LSHIFT,
    RSHIFT,
    
    // Control Flow
    JMP,             // Jump
    JMP_TRUE,        // Jump if true
    JMP_FALSE,       // Jump if false
    
    // Functions
    CALL,            // Call function
    RETURN,          // Return from function
    DEFINE_FNC,      // Define function
    
    // Stack
    POP,             // Pop from stack
    DUP,             // Duplicate top
    
    // I/O
    SHOW,            // Output
    INPUT,           // Input
    
    // Halt
    HALT,            // End program
    
    // Loops
    AGIN,            // Repeat N times
    BREAK,
    CONTINUE,
};

using Value = std::variant<
    std::monostate,  // null
    bool,
    int64_t,
    double,
    std::string
>;

struct Instruction {
    OpCode op;
    std::array<uint32_t, 3> args = {0, 0, 0};  // Up to 3 arguments per instruction
    
    Instruction() : op(OpCode::HALT) {}
    Instruction(OpCode o) : op(o) {}
    Instruction(OpCode o, uint32_t a1) : op(o), args{a1, 0, 0} {}
    Instruction(OpCode o, uint32_t a1, uint32_t a2) : op(o), args{a1, a2, 0} {}
    Instruction(OpCode o, uint32_t a1, uint32_t a2, uint32_t a3) : op(o), args{a1, a2, a3} {}
};

class ByteCode {
public:
    std::vector<Instruction> instructions;
    std::vector<Value> constants;
    std::vector<std::string> string_pool;
    std::vector<std::string> variable_names;
    
    void add_instruction(const Instruction& instr) {
        instructions.push_back(instr);
    }
    
    uint32_t add_constant(const Value& val) {
        constants.push_back(val);
        return constants.size() - 1;
    }
    
    uint32_t add_string(const std::string& str) {
        string_pool.push_back(str);
        return string_pool.size() - 1;
    }
    
    uint32_t register_variable(const std::string& name) {
        variable_names.push_back(name);
        return variable_names.size() - 1;
    }
    
    size_t instruction_count() const {
        return instructions.size();
    }
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_BYTECODE_HPP
