# YGScript Quick Start Guide

## Installation

### From Source
```bash
cd ygscript
python setup.py install
```

### Running Directly
```bash
python src/ygscript.py run program.yg
```

## Basic Usage

### 1. Running a Program
```bash
ygscript run hello.yg
```

### 2. REPL Mode
```bash
ygscript repl
```

### 3. Compiling
```bash
ygscript compile program.yg -o output.ir
```

### 4. Debugging
```bash
# Tokenize (lexer output)
ygscript lex program.yg

# Parse (AST output)
ygscript parse program.yg
```

## Language Basics

### Variables
```ygscript
let x = 10              // Immutable variable
var y = 20              // Mutable variable
const int z = 30        // Compile-time constant
```

### Data Types
```ygscript
// Integers
int8 a = 5              // 1 byte signed integer
uint32 b = 100          // 4 byte unsigned integer
int x = 42              // Platform-dependent (4 or 8 bytes)

// Floating Point
float f = 3.14          // Single precision
double d = 2.71828     // Double precision

// Characters
char c = 'A'            // Single character
char emoji = '😊'      // Unicode character

// Booleans
bool flag = true        // Boolean value

// Strings
str message = "Hello"   // String (shorthand for string)
```

### Functions
```ygscript
// Simple function
fnc Greet(name: str) {
    show(I"Hello, {name}!")
}

// Function with return type
fnc Add(a: int32, b: int32) -> int32 {
    return a + b
}

// Generic function
fnc Max<T>(x: T, y: T) -> T {
    if (x > y) {
        return x
    } else {
        return y
    }
}

// Function with default parameters
fnc Power(base: int32, exp: int32 = 2) -> int32 {
    return base ^ exp
}
```

### Control Flow

#### If/Else
```ygscript
if (age >= 18) {
    show("Adult")
} eif (age >= 13) {
    show("Teenager")
} else {
    show("Child")
}
```

#### Switch/Case
```ygscript
incase (day) {
    case 1:
        show("Monday")
        break
    case 2:
        show("Tuesday")
        break
    default:
        show("Other day")
}
```

#### Special Conditions
```ygscript
// When - runs only once, errors if false
when (user != null) {
    show("User exists")
}

// Though - runs if condition is false
though (error_flag) {
    show("No error occurred")
}
```

### Loops

#### For Loop
```ygscript
for (let i = 0; i < 10; i++) {
    show(i)
}
```

#### While Loop
```ygscript
while (count < 100) {
    count = count + 1
}
```

#### Do-While Loop
```ygscript
do {
    show("Running")
} while (false)
```

#### Agin Loop (Repeat)
```ygscript
agin(5) {
    show("Repeat 5 times")
}

agin(10, true) {
    show(i)  // i auto-increments from 0-9
}
```

### Input/Output

#### Output
```ygscript
show("Hello, World!")
show(42)
show(3.14)
```

#### Input
```ygscript
// Basic input
var answer = input("Enter something: ")

// With variable
str name
input([name], "What is your name? ")
```

### String Interpolation
```ygscript
str name = "World"
str greeting = I"Hello, {name}!"
show(greeting)
```

### Pointers
```ygscript
int32 *ptr = null                    // Null pointer
int32 value = 42
const int32 *ptr_to_const = &value   // Address-of operator
int32 deref = *ptr_to_const          // Dereference operator
```

### Modules/Imports
```ygscript
// Import entire module
add "Math"

// Import with alias
add "Math" -as "m"

// Import specific items
from "Math" -add "Sin"

// Import multiple items
from "Math" -add ("Sin", "Cos", "Tan")
```

## Built-in Functions

### I/O Functions
- `show(value)` - Print value to console
- `input([var], "prompt")` - Read input from user

### Type Functions
- `type(value)` - Get type name
- `len(obj)` - Get length of string/array

## Example Programs

### Hello World
```ygscript
fnc Main() {
    show("Hello, World!")
    return 0
}
```

### Calculator
```ygscript
fnc Add(a: int32, b: int32) -> int32 { return a + b }
fnc Sub(a: int32, b: int32) -> int32 { return a - b }
fnc Mul(a: int32, b: int32) -> int32 { return a * b }
fnc Div(a: int32, b: int32) -> int32 { return a / b }

fnc Main() {
    show(Add(10, 5))
    show(Sub(10, 5))
    show(Mul(10, 5))
    show(Div(10, 5))
}
```

### User Interaction
```ygscript
fnc Main() {
    str name
    input([name], "Enter your name: ")
    
    var age = input("Enter your age: ")
    
    show(I"Hello {name}, you are {age} years old!")
}
```

## Error Handling

YGScript reports errors with line and column information:
```
Syntax Error: Parser error at line 5, column 12: Expected SEMICOLON, got RBRACE
```

## Tips & Tricks

1. **Type Annotations**: Always specify types for function parameters for better error checking
2. **Immutability**: Use `let` by default, only use `var` when needed
3. **Comments**: Use `//` for single-line comments
4. **Readability**: Use clear variable names and consistent indentation

## Operators

### Arithmetic
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `%` Modulo
- `^` Power (exponentiation)

### Comparison
- `==` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal

### Logical
- `&&` Logical AND
- `||` Logical OR
- `!` Logical NOT

### Bitwise
- `&` Bitwise AND
- `|` Bitwise OR
- `^` Bitwise XOR
- `~` Bitwise NOT
- `<<` Left shift
- `>>` Right shift

### Other
- `++` Increment
- `--` Decrement
- `&` Address-of (pointer)
- `*` Dereference (pointer)
- `->` Type annotation in functions
- `?` Ternary operator (condition ? true_val : false_val)

## Standard Library

Standard library modules are available via the `add` command:

- **Math** - Mathematical functions
- **String** - String manipulation
- **File** - File I/O operations
- **Time** - Time and date functions
- **Array** - Array operations
- **System** - System operations

## Troubleshooting

### "Undefined variable" Error
Make sure you declared the variable before using it, and it's in scope.

### "Type mismatch" Error
Check that the value you're assigning matches the declared type.

### Syntax Errors
Check for missing semicolons, mismatched braces, or incorrect keywords.

## Further Resources

- See `structers/` folder for detailed syntax specifications
- Check `examples/` folder for more program examples
- Run tests with: `python test_suite.py`
