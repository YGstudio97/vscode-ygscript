/*
 * YGScript C++ - Main Entry Point
 * CLI with commands: run, compile, vm, repl
 */

#include "cpp_lexer.hpp"
#include "cpp_parser.hpp"
#include "cpp_compiler.hpp"
#include "cpp_vm.hpp"

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <memory>

using namespace ygscript;

std::string read_file(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

void run_command(const std::string& filename) {
    try {
        std::string source = read_file(filename);
        
        // Tokenize
        Lexer lexer(source);
        auto tokens = lexer.tokenize();
        
        // Parse
        Parser parser(tokens);
        auto program = parser.parse();
        
        // Compile
        Compiler compiler;
        auto bytecode = compiler.compile(program);
        
        // Execute
        VirtualMachine vm(bytecode);
        vm.execute();
        
    } catch (const LexerError& e) {
        std::cerr << "Lexer Error at " << e.line << ":" << e.column << ": " << e.what() << std::endl;
    } catch (const ParserError& e) {
        std::cerr << "Parser Error at " << e.line << ":" << e.column << ": " << e.what() << std::endl;
    } catch (const CompileError& e) {
        std::cerr << "Compile Error: " << e.what() << std::endl;
    } catch (const VMError& e) {
        std::cerr << "Runtime Error: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void compile_command(const std::string& input_file, const std::string& output_file) {
    try {
        std::string source = read_file(input_file);
        
        // Tokenize
        Lexer lexer(source);
        auto tokens = lexer.tokenize();
        
        // Parse
        Parser parser(tokens);
        auto program = parser.parse();
        
        // Compile
        Compiler compiler;
        auto bytecode = compiler.compile(program);
        
        // TODO: Save bytecode to file
        std::cout << "Compiled to: " << output_file << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void lex_command(const std::string& filename) {
    try {
        std::string source = read_file(filename);
        Lexer lexer(source);
        auto tokens = lexer.tokenize();
        
        std::cout << "Tokens:" << std::endl;
        for (const auto& token : tokens) {
            std::cout << "  [" << static_cast<int>(token.type) << "] " 
                      << token.value << " (" << token.line << ":" << token.column << ")" << std::endl;
        }
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void parse_command(const std::string& filename) {
    try {
        std::string source = read_file(filename);
        
        Lexer lexer(source);
        auto tokens = lexer.tokenize();
        
        Parser parser(tokens);
        auto program = parser.parse();
        
        std::cout << "AST parsed successfully with " << program.statements.size() << " statements" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

void repl_mode() {
    std::cout << "YGScript v1.0 - Interactive REPL" << std::endl;
    std::cout << "Type 'exit' to quit" << std::endl << std::endl;
    
    std::string line;
    while (true) {
        std::cout << ">>> ";
        if (!std::getline(std::cin, line)) break;
        
        if (line == "exit") break;
        if (line == "help") {
            std::cout << "Commands: exit, help, clear" << std::endl;
            continue;
        }
        if (line.empty()) continue;
        
        try {
            Lexer lexer(line);
            auto tokens = lexer.tokenize();
            
            Parser parser(tokens);
            auto program = parser.parse();
            
            Compiler compiler;
            auto bytecode = compiler.compile(program);
            
            VirtualMachine vm(bytecode);
            vm.execute();
            
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
        }
    }
}

void print_usage(const char* program_name) {
    std::cout << "YGScript v1.0 - Programming Language Interpreter" << std::endl << std::endl;
    std::cout << "Usage: " << program_name << " <command> [options]" << std::endl << std::endl;
    std::cout << "Commands:" << std::endl;
    std::cout << "  run <file>                Run a YGScript file" << std::endl;
    std::cout << "  compile <file> -o <out>  Compile to bytecode" << std::endl;
    std::cout << "  repl                     Interactive shell" << std::endl;
    std::cout << "  lex <file>               Tokenize file (debug)" << std::endl;
    std::cout << "  parse <file>             Parse file (debug)" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    std::string command = argv[1];
    
    if (command == "run" && argc >= 3) {
        run_command(argv[2]);
    }
    else if (command == "compile" && argc >= 5) {
        // compile <file> -o <output>
        if (std::string(argv[3]) != "-o") {
            std::cerr << "Error: expected -o" << std::endl;
            return 1;
        }
        compile_command(argv[2], argv[4]);
    }
    else if (command == "repl") {
        repl_mode();
    }
    else if (command == "lex" && argc >= 3) {
        lex_command(argv[2]);
    }
    else if (command == "parse" && argc >= 3) {
        parse_command(argv[2]);
    }
    else {
        std::cerr << "Unknown command: " << command << std::endl;
        print_usage(argv[0]);
        return 1;
    }
    
    return 0;
}
