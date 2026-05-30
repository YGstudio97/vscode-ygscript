# YGScript Language Specification v1.0

## Table of Contents
1. [Overview](#overview)
2. [Lexical Structure](#lexical-structure)
3. [Types](#types)
4. [Variables](#variables)
5. [Functions](#functions)
6. [Statements](#statements)
7. [Expressions](#expressions)
8. [Operators](#operators)
9. [Standard Library](#standard-library)

## Overview

YGScript is a modern, statically-typed programming language designed with:
- **Explicit Type System**: All types are explicit and must be declared
- **Memory Safety**: Pointers with address-of and dereference operations
- **Clean Syntax**: Inspired by Python, Go, and Rust
- **Flexible Control Flow**: Multiple loop and condition types
- **Module System**: Simple import/export mechanism

### Language Features
- Primitive and composite types
- Functions with generics
- Multiple loop types (for, while, do-while, agin)
- Rich control flow (if/eif/else, switch, when, though)
- String interpolation
- Pointer operations
- Module imports

## Lexical Structure

### Comments
```ygscript
// Single-line comment
```

### Identifiers
- Start with letter or underscore
- Followed by letters, digits, or underscores
- Case-sensitive
- Lowercase for variables and functions, PascalCase for types

### Keywords
Reserved keywords (cannot be used as identifiers):
- Control: `if`, `eif`, `else`, `incase`, `case`, `default`, `when`, `though`
- Loops: `for`, `while`, `do`, `agin`, `break`, `continue`
- Functions: `fnc`, `return`
- Types: `int`, `uint`, `char`, `bool`, `float`, `double`, `string`, `str`, `obj`, `null`, `class`
- Variables: `let`, `var`, `const`
- Modules: `add`, `from`, `as`
- Boolean: `true`, `false`

### Literals

#### Integers
```ygscript
42                  // Decimal
0x2A                // Hexadecimal
0o52                // Octal
0b101010            // Binary
32i8                // int8 literal
1000u64             // uint64 literal
```

#### Floating-Point
```ygscript
3.14                // Float
1.2e-6              // Scientific notation
3.14f32             // float32 literal
3.14d64             // double64 literal
```

#### Characters
```ygscript
'A'                 // ASCII character
'😊'                // Unicode character
'\n'                // Newline escape
'\t'                // Tab escape
'\\'                // Backslash
```

#### Strings
```ygscript
"Hello, World!"     // String literal
I"Hello, {name}!"   // Interpolated string
```

#### Booleans
```ygscript
true                // Boolean true
false               // Boolean false
```

#### Null
```ygscript
null                // Null pointer/value
```

### Operators and Delimiters
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&`, `||`, `!`
- Bitwise: `&`, `|`, `^`, `~`, `<<`, `>>`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`
- Increment/Decrement: `++`, `--`
- Pointer: `&`, `*`
- Delimiters: `(`, `)`, `{`, `}`, `[`, `]`, `;`, `:`, `,`, `.`, `?`, `->`

## Types

### Primitive Types

#### Integer Types
```
int8, int16, int32, int64, int128, int256, int512    // Signed
uint8, uint16, uint32, uint64, uint128, uint256, uint512  // Unsigned
int, uint                                              // Platform-dependent
```

#### Floating-Point Types
```
float8, float16, float32, float64, float80, float128, float256, float512
double8, double16, double32, double64, double80, double128, double256, double512
float, double
```

#### Character Types
```
char8, char16, char32, char64, char128, char256, char512
char
```

#### Boolean Types
```
bool8, bool16, bool32, bool64, bool128, bool256, bool512
bool
```

#### String and Special Types
```
str, string         // String type
obj, object         // Generic object
null                // Null type
```

### Type Aliases
- `str` → `string`
- `int` → `int32` or `int64` (platform-dependent)
- `uint` → `uint32` or `uint64` (platform-dependent)
- `char` → Unicode character
- `bool` → 1-byte boolean
- `float` → `float64`
- `double` → `double64`
- `obj` → `object`

### Pointer Types
```ygscript
int32 *ptr          // Pointer to int32
const *int32 ptr    // Const pointer
*int32 const ptr    // Pointer to const
**int64 ptr         // Pointer to pointer
```

### Generic Types
```ygscript
fnc Get<T>(index: int32) -> T { ... }
```

## Variables

### Declaration Syntax
```ygscript
let name: type = initial_value     // Immutable
var name: type = initial_value     // Mutable
const type name = initial_value    // Constant
```

### Examples
```ygscript
let x = 42                         // Type inferred
let y: int32 = 100                 // Explicit type
var count: int32 = 0               // Mutable
const int PI = 31415926            // Constant
```

### Immutability Rules
- `let` variables cannot be reassigned (compile-time error)
- `var` variables can be reassigned
- `const` variables are compile-time constants

## Functions

### Syntax
```ygscript
fnc FunctionName(param1: Type1, param2: Type2) -> ReturnType {
    // body
    return value
}
```

### Features
- Required type annotations for parameters
- Optional return type (void if omitted)
- Return statements (optional if last expression matches return type)
- Default parameters
- Generic functions

### Examples
```ygscript
// Simple function
fnc Greet(name: str) {
    show(I"Hello, {name}!")
}

// With return type
fnc Add(a: int32, b: int32) -> int32 {
    return a + b
}

// With default parameter
fnc Power(base: int32, exp: int32 = 2) -> int32 {
    return base ^ exp
}

// Generic function
fnc Max<T>(x: T, y: T) -> T {
    if (x > y) {
        return x
    } else {
        return y
    }
}

// No return type (void)
fnc PrintNumber(n: int32) {
    show(n)
}
```

## Statements

### Variable Declaration
```ygscript
let x = 10
var y: int32 = 20
const int z = 30
```

### Function Declaration
```ygscript
fnc Main() {
    show("Hello")
}
```

### If Statement
```ygscript
if (condition) {
    // true block
} eif (condition2) {
    // else-if block
} else {
    // else block
}
```

### When Statement (runs once, errors if false)
```ygscript
when (user != null) {
    show("User exists")
}  // Error if user == null
```

### Though Statement (inverse condition)
```ygscript
though (error_flag) {
    // Runs if error_flag is false
}
```

### Switch Statement
```ygscript
incase (value) {
    case 1:
        show("One")
        break
    case 2:
        show("Two")
        break
    default:
        show("Other")
}
```

### For Loop
```ygscript
for (let i = 0; i < 10; i++) {
    show(i)
}
```

### While Loop
```ygscript
while (condition) {
    // loop body
}
```

### Do-While Loop
```ygscript
do {
    // loop body
} while (condition)
```

### Agin Loop (Repeat N times)
```ygscript
agin(5) {
    show("Runs 5 times")
}

agin(10, true) {  // true enables auto-increment
    show(i)       // i goes from 0 to 9
}
```

### Break and Continue
```ygscript
for (let i = 0; i < 10; i++) {
    if (i == 5) {
        break        // Exit loop
    }
    if (i == 3) {
        continue     // Skip to next iteration
    }
    show(i)
}
```

### Return Statement
```ygscript
return value        // Return from function
return              // Return null/void
```

### Block Statement
```ygscript
{
    // Creates new scope
}
```

## Expressions

### Primary Expressions
- Literals: `42`, `3.14`, `"string"`, `true`, `null`
- Identifiers: `x`, `Count`, `get_value`
- Parenthesized: `(expression)`

### Postfix Expressions
```ygscript
function_call()         // Function call
array[index]            // Array subscript
object.member           // Member access
i++, i--                // Post-increment/decrement
```

### Unary Expressions
```ygscript
-x                      // Negation
+x                      // Unary plus
!condition              // Logical NOT
~value                  // Bitwise NOT
++i, --i                // Pre-increment/decrement
&variable               // Address-of (pointer)
*pointer                // Dereference
```

### Binary Expressions
```ygscript
a + b                   // Addition
a - b                   // Subtraction
a * b                   // Multiplication
a / b                   // Division
a % b                   // Modulo
a == b                  // Equality
a != b                  // Inequality
a < b, a > b            // Relational
a <= b, a >= b          // Relational
a && b                  // Logical AND
a || b                  // Logical OR
a & b                   // Bitwise AND
a | b                   // Bitwise OR
a ^ b                   // Bitwise XOR
a << b                  // Left shift
a >> b                  // Right shift
```

### Ternary Expression
```ygscript
condition ? true_value : false_value
```

### Assignment
```ygscript
x = value               // Simple assignment
x += value              // Add and assign
x -= value              // Subtract and assign
x *= value              // Multiply and assign
x /= value              // Divide and assign
```

## Operators

### Operator Precedence (highest to lowest)
1. Postfix: `()`, `[]`, `.`, `++`, `--`
2. Unary: `-`, `+`, `!`, `~`, `&`, `*`, `++`, `--`
3. Exponentiation: `^`
4. Multiplicative: `*`, `/`, `%`
5. Additive: `+`, `-`
6. Shift: `<<`, `>>`
7. Relational: `<`, `>`, `<=`, `>=`
8. Equality: `==`, `!=`
9. Bitwise AND: `&`
10. Bitwise XOR: `^`
11. Bitwise OR: `|`
12. Logical AND: `&&`
13. Logical OR: `||`
14. Ternary: `? :`
15. Assignment: `=`, `+=`, `-=`, `*=`, `/=`

### Operator Associativity
- Most binary operators: Left-associative
- Exponentiation `^`: Right-associative
- Assignment: Right-associative
- Ternary `? :`: Right-associative

## Standard Library

### Built-in Functions

#### I/O Functions
```ygscript
show(value)                 // Output to console
input([variable], "prompt") // Read from user
```

#### Type Functions
```ygscript
type(value)                 // Get type name
len(object)                 // Get length
```

### Standard Modules
Available via `add "ModuleName"`:

- **Math**: sin, cos, tan, sqrt, pow, etc.
- **String**: length, substring, trim, split, etc.
- **Array**: push, pop, insert, remove, etc.
- **File**: open, close, read, write, etc.
- **Time**: now, sleep, format, etc.
- **System**: exit, env, args, etc.

### Importing
```ygscript
add "Math"                              // Import entire module
add "Math" -as "m"                      // With alias
from "Math" -add "Sin"                  // Specific function
from "Math" -add ("Sin", "Cos", "Tan")  // Multiple
```

## Memory Management

### Stack vs Heap
- Primitives stored on stack
- Objects/strings on heap (garbage collected)

### Pointers
```ygscript
var x = 42
int32 *ptr = &x          // Address-of
show(*ptr)               // Dereference
```

## Type Checking

YGScript performs static type checking:
- Type mismatch errors at compile-time
- Implicit conversions for compatible types
- Explicit casting available

## Scope and Lifetime

- Block scope: Variables limited to enclosing block
- Function scope: Parameters and locals
- Global scope: Top-level declarations
- Variables last until scope ends

## Error Handling

### Syntax Errors
```
Lexer error at line 5, column 12: Unexpected character
Parser error at line 3, column 5: Expected semicolon
```

### Runtime Errors
```
Runtime Error: Undefined variable: x
Runtime Error: Type mismatch: expected int32, got string
```

## Best Practices

1. **Use explicit types** for function parameters
2. **Use `let` by default**, only `var` when needed
3. **Name types in PascalCase**, variables in snake_case
4. **Add comments** for complex logic
5. **Use meaningful variable names**
6. **Check for null** before dereferencing pointers
7. **Handle errors** appropriately in your code

## Version History

### v1.0 (Current)
- Initial release
- Basic types, functions, and control flow
- Module system
- Pointer support
