# YGScript Programming Language

A modern, statically-typed programming language designed with explicit type support, advanced control flow, and clean syntax.

## Language Features

### 1. Type System
- **Primitive Types**: `int`, `uint`, `char`, `bool`, `float`, `double`, `string`
- **Sized Types**: `int8`, `int16`, `int32`, `int64`, `int128`, `int256`, `int512`
- **Advanced Types**: Pointers, generics, objects, classes, nullable types
- **Type Aliases**: `str`, `int`, `bool`, `float`, `double`, `obj`

### 2. Variable Declaration
```ygscript
let immutable_var = 10        // Immutable (compile-time error if reassigned)
var mutable_var = 20          // Mutable (can be reassigned)
const int fixed_val = 30      // Compile-time constant
```

### 3. Functions
```ygscript
fnc Add(x: int32, y: int32) -> int32 {
    return x + y
}

fnc Div<T>(x: T, y: T) -> T {
    return x / y
}

fnc Main() {
    show("Hello, World!")
    return 0
}
```

### 4. Control Flow

**Conditionals:**
- `if` / `eif` (else if) / `else`
- `incase` (switch statement)
- `when` (runs once, only if true - error otherwise)
- `though` (inverse condition - runs if false)

**Loops:**
- `for (init; condition; update) { }`
- `while (condition) { }`
- `do { } while (condition)`
- `agin(times, increment?) { }` (repeat N times)

### 5. Built-in Functions
- `show(value)` - Output to console
- `input([var], "message")` - Read from user
- Standard library functions (Math, etc.)

### 6. Module System
```ygscript
add "Math"                           // Import module
add "Math" -as "m"                   // Import with alias
from "Math" -add "Sin"               // Import specific function
from "Math" -add ("Sin", "Cos")      // Import multiple
```

## Project Structure

```
ygscript/
├── src/
│   ├── lexer.py          # Tokenizer
│   ├── parser.py         # AST builder
│   ├── compiler.py       # Code compilation
│   ├── runtime.py        # Execution engine
│   ├── builtins.py       # Built-in functions
│   └── ygscript.py       # Main entry point
├── libs/
│   ├── math.yg           # Math library
│   └── io.yg             # I/O utilities
├── bin/
│   └── ygscript          # CLI executable
└── tests/
    └── test_suite.py     # Test cases
```

## Getting Started

### Running a YGScript File
```bash
ygscript run program.yg
```

### Compiling to IR
```bash
ygscript compile program.yg -o program.ir
```

### REPL Mode
```bash
ygscript repl
```

## Example Programs

### Hello World
```ygscript
fnc Main() {
    show("Hello, World!")
    return 0
}
```

### Input/Output
```ygscript
fnc Main() {
    str name
    input([name], "Enter your name: ")
    show(I"Hello, {name}!")
    return 0
}
```

### Loops
```ygscript
fnc Main() {
    agin(5) {
        show("This runs 5 times")
    }
    return 0
}
```

## Language Syntax Reference

See individual files in `structers/` folder for detailed syntax specifications.
