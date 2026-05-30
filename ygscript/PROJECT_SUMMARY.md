# YGScript Programming Language - Project Summary

## Overview

YGScript is a modern, statically-typed programming language built from the ground up with:
- **Comprehensive Type System**: Support for primitive, pointer, and generic types
- **Clean Syntax**: Easy to read and write code
- **Rich Control Flow**: Multiple looping and conditional constructs
- **Module System**: Simple import/export mechanism
- **Safety**: Type checking and memory management with pointers

## Project Structure

```
ygscript/
├── README.md                 # Main project documentation
├── QUICKSTART.md            # Getting started guide
├── LANGUAGE_SPEC.md         # Complete language specification
├── setup.py                 # Installation configuration
├── test_suite.py            # Automated test suite
├── ygscript.bat             # Windows command wrapper
├── hello_world.yg           # Example: Hello World
├── variables.yg             # Example: Variable types
├── functions.yg             # Example: Functions
├── control_flow.yg          # Example: Control flow
│
├── src/                      # Source code
│   ├── __init__.py          # Package initialization
│   ├── lexer.py             # Tokenizer (17.9 KB)
│   ├── ast_nodes.py         # AST definitions (5.3 KB)
│   ├── parser.py            # Parser (26.3 KB)
│   ├── runtime.py           # Interpreter/Runtime (16.5 KB)
│   └── ygscript.py          # CLI entry point (5.6 KB)
│
├── bin/                      # Compiled executables (future)
├── libs/                     # Standard library modules (future)
└── docs/                     # Additional documentation (future)
```

## Components

### 1. Lexer (`lexer.py`)
**Purpose**: Tokenizes YGScript source code

**Features**:
- Recognizes all keywords (50+ reserved words)
- Handles multiple numeric formats (decimal, hex, octal, binary)
- Supports string interpolation (I"...")
- Manages escape sequences
- Tracks line and column information for error reporting
- 80+ token types

**Key Classes**:
- `TokenType`: Enum of all token types
- `Token`: Represents a single token with value and position
- `Lexer`: Main tokenization engine

### 2. AST Nodes (`ast_nodes.py`)
**Purpose**: Defines the structure of the Abstract Syntax Tree

**Node Types** (50+):
- **Literals**: IntLiteral, StringLiteral, BooleanLiteral, etc.
- **Expressions**: BinaryOp, UnaryOp, Assignment, FunctionCall, etc.
- **Statements**: VariableDecl, FunctionDecl, IfStmt, ForStmt, etc.
- **Types**: Type, PrimitiveType, GenericType
- **Program**: Root node containing all statements

### 3. Parser (`parser.py`)
**Purpose**: Converts tokens into an Abstract Syntax Tree

**Features**:
- Recursive descent parser
- Operator precedence handling
- Error recovery with line/column reporting
- Support for all language constructs
- Generic type parameter handling

**Key Methods**:
- `parse()`: Main entry point
- `parse_statement()`: Parse any statement
- `parse_expression()`: Parse expressions with proper precedence
- `parse_primary()`, `parse_postfix()`: Low-level parsing

### 4. Runtime (`runtime.py`)
**Purpose**: Executes the AST (interpreter)

**Features**:
- Executes all statement types
- Evaluates all expression types
- Variable and function management
- Environment/scope handling
- Built-in function support
- Return/break/continue exception handling

**Key Classes**:
- `Environment`: Manages variable scope
- `Variable`: Runtime variable wrapper
- `Function`: User-defined function
- `Runtime`: Main execution engine

**Built-in Functions**:
- `show(value)`: Output to console
- `input([var], "prompt")`: Read from user
- `len(obj)`: Get length
- `type(value)`: Get type name

### 5. CLI (`ygscript.py`)
**Purpose**: Command-line interface for the language

**Commands**:
- `run <file>`: Execute a YGScript program
- `compile <file> -o <output>`: Compile to IR
- `repl`: Interactive shell
- `lex <file>`: Debug tokenization
- `parse <file>`: Debug parsing

## Language Features

### Type System
- **Primitive Types**: int, uint, float, double, char, bool, string, object, null
- **Sized Types**: int8-int512, uint8-uint512, float8-float512, double8-double512, etc.
- **Type Aliases**: str (string), obj (object)
- **Pointers**: Single and double pointers with address-of (&) and dereference (*) operators
- **Generic Types**: Templates with type parameters (e.g., `<T>`)

### Variables
- **let**: Immutable variable (cannot be reassigned)
- **var**: Mutable variable (can be reassigned)
- **const**: Compile-time constant

### Functions
- Explicit return types
- Default parameters
- Generic functions with type parameters
- Nested scopes

### Control Flow
- **if/eif/else**: Conditional branching
- **incase**: Switch statement with cases
- **when**: Runs only once, errors if condition is false
- **though**: Inverse condition (runs if false)
- **for**: C-style for loop
- **while**: While loop
- **do-while**: Do-while loop
- **agin**: Repeat N times with optional auto-increment
- **break/continue**: Loop control

### Operators
- Arithmetic: +, -, *, /, %, ^ (power)
- Comparison: ==, !=, <, >, <=, >=
- Logical: &&, ||, !
- Bitwise: &, |, ^, ~, <<, >>
- Assignment: =, +=, -=, *=, /=
- Unary: -, +, !, ~, ++, --
- Pointer: & (address-of), * (dereference)

### Module System
- `add "Module"`: Import entire module
- `add "Module" -as "alias"`: Import with alias
- `from "Module" -add "Item"`: Import specific item
- `from "Module" -add ("Item1", "Item2")`: Import multiple items

### String Features
- Double-quoted strings: "Hello"
- Single-quoted characters: 'A'
- Escape sequences: \n, \t, \\, etc.
- Unicode support: '😊'
- String interpolation: I"Hello, {name}!"

## Examples

### Hello World
```ygscript
fnc Main() {
    show("Hello, World!")
    return 0
}
```

### Variables and Types
```ygscript
let count = 42              // Integer
let pi = 3.14159            // Float
let active = true           // Boolean
str message = "Hello!"      // String
char symbol = 'A'           // Character
```

### Functions
```ygscript
fnc Add(a: int32, b: int32) -> int32 {
    return a + b
}

fnc Main() {
    let result = Add(5, 10)
    show(result)
}
```

### Loops
```ygscript
// For loop
for (let i = 0; i < 5; i++) {
    show(i)
}

// While loop
while (count < 10) {
    count = count + 1
}

// Agin loop (repeat)
agin(3) {
    show("Hello")
}
```

### Conditionals
```ygscript
if (age >= 18) {
    show("Adult")
} eif (age >= 13) {
    show("Teenager")
} else {
    show("Child")
}
```

### Pointers
```ygscript
var x = 42
int32 *ptr = &x             // Address-of
show(*ptr)                  // Dereference
```

## Testing

Run the test suite:
```bash
python test_suite.py
```

Test Coverage:
- Lexer tests: Integers, strings, keywords
- Parser tests: Variables, functions, statements
- Runtime tests: Arithmetic, functions, loops, conditionals

## File Statistics

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| lexer.py | 17.9 KB | 580 | Tokenization |
| parser.py | 26.3 KB | 850 | Parsing |
| runtime.py | 16.5 KB | 490 | Execution |
| ast_nodes.py | 5.3 KB | 180 | AST definitions |
| ygscript.py | 5.6 KB | 200 | CLI |
| **Total** | **71.6 KB** | **2,300** | |

## Getting Started

### Installation
```bash
cd ygscript
python setup.py install
```

### Run an Example
```bash
python src/ygscript.py run hello_world.yg
```

### Interactive Shell
```bash
python src/ygscript.py repl
```

### Compile a Program
```bash
python src/ygscript.py compile program.yg -o program.ir
```

### Debug Tokenization
```bash
python src/ygscript.py lex program.yg
```

### Debug Parsing
```bash
python src/ygscript.py parse program.yg
```

## Supported Platforms

- Windows (via batch wrapper)
- Linux/Mac (direct Python execution)
- Python 3.8+

## Future Enhancements

### Phase 2
- [ ] Classes and OOP
- [ ] Error handling (try/catch)
- [ ] Tuple and struct types
- [ ] Array and dictionary literals
- [ ] Slice notation
- [ ] Range expressions

### Phase 3
- [ ] Standard library implementation
- [ ] Module caching
- [ ] Optimization passes
- [ ] Native code compilation
- [ ] REPL history and autocomplete

### Phase 4
- [ ] Async/await
- [ ] Decorators
- [ ] Pattern matching
- [ ] Macro system
- [ ] FFI (Foreign Function Interface)

## Language Design Decisions

1. **Explicit Types**: All types must be declared for safety
2. **Immutability by Default**: `let` for variables, `var` for mutable
3. **Multiple Loop Types**: Different constructs for different situations
4. **Simple Module System**: Easy to understand imports
5. **Pointer Support**: Explicit memory operations
6. **String Interpolation**: Modern convenience feature

## Documentation Files

- **README.md**: Main project overview
- **QUICKSTART.md**: Getting started guide with examples
- **LANGUAGE_SPEC.md**: Complete language reference
- **This file**: Project summary and architecture

## Architecture Diagram

```
Source Code (.yg file)
        ↓
    [LEXER] → Tokens
        ↓
    [PARSER] → AST
        ↓
    [RUNTIME] → Execution
        ↓
    Output / Errors
```

## Conclusion

YGScript is a fully-functional programming language with:
- ✅ Complete lexer with 80+ token types
- ✅ Recursive descent parser with full language support
- ✅ Tree-walking interpreter
- ✅ Comprehensive type system
- ✅ Rich control flow constructs
- ✅ Module system
- ✅ Built-in functions
- ✅ Example programs
- ✅ Test suite
- ✅ Complete documentation

The implementation is clean, well-structured, and ready for extension and optimization.
