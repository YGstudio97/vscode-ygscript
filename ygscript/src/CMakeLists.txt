cmake_minimum_required(VERSION 3.20)
project(YGScript VERSION 1.0.0 LANGUAGES CXX)

# C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compiler options
if(MSVC)
    add_compile_options(/W4 /permissive-)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/src)

# Header files
set(HEADERS
    src/cpp_token.hpp
    src/cpp_lexer.hpp
    src/cpp_ast.hpp
    src/cpp_parser.hpp
    src/cpp_compiler.hpp
    src/cpp_bytecode.hpp
    src/cpp_vm.hpp
)

# Source files
set(SOURCES
    src/cpp_token.cpp
    src/cpp_lexer.cpp
    src/cpp_parser.cpp
    src/cpp_compiler.cpp
    src/cpp_vm.cpp
    src/cpp_builtins.cpp
    src/main.cpp
)

# Create executable
add_executable(ygscript ${SOURCES} ${HEADERS})

# Set output directory
set_target_properties(ygscript PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# Enable testing
enable_testing()

# Test executable
add_executable(ygscript_test 
    ${SOURCES}
    tests/test_main.cpp
)
add_test(NAME YGScriptTests COMMAND ygscript_test)

# Install
install(TARGETS ygscript DESTINATION bin)
