/*
 * YGScript C++ - Virtual Machine
 * C++20 Implementation - Stack-Based VM
 */

#ifndef YGSCRIPT_CPP_VM_HPP
#define YGSCRIPT_CPP_VM_HPP

#include "cpp_bytecode.hpp"
#include <stack>
#include <unordered_map>
#include <functional>
#include <stdexcept>

namespace ygscript {

class VMError : public std::runtime_error {
public:
    VMError(const std::string& msg) : std::runtime_error(msg) {}
};

class VirtualMachine {
public:
    explicit VirtualMachine(const ByteCode& bytecode);
    
    void execute();
    void run_instruction(const Instruction& instr);
    
    // Stack operations
    void push(const Value& val);
    Value pop();
    Value peek() const;
    
    // Utilities
    static Value to_boolean(const Value& val);
    static std::string to_string(const Value& val);
    static double to_number(const Value& val);
    
private:
    const ByteCode& bytecode;
    std::stack<Value> stack;
    std::unordered_map<std::string, Value> variables;
    size_t pc = 0;  // Program counter
    
    // Arithmetic operations
    Value add_values(const Value& a, const Value& b);
    Value sub_values(const Value& a, const Value& b);
    Value mul_values(const Value& a, const Value& b);
    Value div_values(const Value& a, const Value& b);
    Value mod_values(const Value& a, const Value& b);
    Value pow_values(const Value& a, const Value& b);
    
    // Comparison operations
    Value eq_values(const Value& a, const Value& b);
    Value ne_values(const Value& a, const Value& b);
    Value lt_values(const Value& a, const Value& b);
    Value le_values(const Value& a, const Value& b);
    Value gt_values(const Value& a, const Value& b);
    Value ge_values(const Value& a, const Value& b);
    
    // Bitwise operations
    Value and_values(const Value& a, const Value& b);
    Value or_values(const Value& a, const Value& b);
    Value xor_values(const Value& a, const Value& b);
    Value not_value(const Value& a);
    Value lshift_values(const Value& a, const Value& b);
    Value rshift_values(const Value& a, const Value& b);
};

} // namespace ygscript

#endif // YGSCRIPT_CPP_VM_HPP
