# YGScript Implementation Guide

## Architecture Overview

YGScript is implemented as a classic interpreter following the standard three-stage architecture:

```
┌─────────────────┐
│  Source Code    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌────────────────┐
│    LEXER        │ ───→ │ Stream of      │
│ (Tokenization)  │      │ Tokens         │
└─────────────────┘      └────────┬───────┘
                                  │
                                  ↓
                         ┌─────────────────┐      ┌────────────────┐
                         │    PARSER       │ ───→ │ Abstract       │
                         │ (Syntax Analysis)      │ Syntax Tree    │
                         └─────────────────┘      └────────┬───────┘
                                                           │
                                                           ↓
                                                  ┌─────────────────┐
                                                  │    RUNTIME      │
                                                  │ (Interpretation)│
                                                  └─────────────────┘
                                                           │
                                                           ↓
                                                  ┌─────────────────┐
                                                  │ Execution &     │
                                                  │ Output          │
                                                  └─────────────────┘
```

## Module Descriptions

### 1. Lexer (`src/lexer.py`)

#### Responsibility
Convert raw source code into a stream of meaningful tokens.

#### Key Components

**TokenType Enum** (80+ types)
- Literals: INTEGER, FLOAT, DOUBLE, STRING, CHAR, BOOLEAN
- Keywords: FNC, RETURN, IF, EIF, ELSE, FOR, WHILE, etc.
- Operators: PLUS, MINUS, STAR, SLASH, EQ, NE, LT, GT, etc.
- Delimiters: LPAREN, RPAREN, LBRACE, RBRACE, SEMICOLON, etc.

**Token Class**
- `type`: TokenType enum value
- `value`: String representation of token
- `line`, `column`: Position information for error reporting

**Lexer Class**
Methods:
- `peek()`: Look ahead at current/next character
- `advance()`: Move to next character
- `skip_whitespace()`: Skip whitespace and tabs
- `read_number()`: Parse numeric literals
- `read_string()`: Parse string/char literals
- `read_identifier()`: Parse identifiers and keywords
- `tokenize()`: Main entry point

Special Handling:
- Sized integer types (int8, int32, uint64, etc.)
- Hexadecimal (0x), octal (0o), binary (0b) literals
- Escape sequences in strings (\n, \t, \\, etc.)
- String interpolation (I"...{...}...")
- Two-character operators (==, !=, <=, >=, ++, --, etc.)

#### Example
```python
lexer = Lexer("let x = 42")
tokens = lexer.tokenize()
# Result: [LET, IDENTIFIER('x'), ASSIGN, INTEGER('42'), EOF]
```

### 2. AST Nodes (`src/ast_nodes.py`)

#### Responsibility
Define the structure of the Abstract Syntax Tree.

#### Node Hierarchy

**Base Class**: `ASTNode`

**Type Nodes**
```
Type
├── PrimitiveType
└── GenericType
```

**Literal Nodes**
```
IntLiteral
FloatLiteral
DoubleLiteral
StringLiteral
CharLiteral
BooleanLiteral
NullLiteral
```

**Expression Nodes**
```
Identifier
BinaryOp
UnaryOp
Assignment
FunctionCall
MethodCall
ArrayIndex
MemberAccess
Cast
TernaryOp
Pointer
```

**Statement Nodes**
```
Block
VariableDecl
FunctionDecl
Parameter
ReturnStmt
IfStmt
WhenStmt
ThoughStmt
SwitchStmt
Case
ForStmt
WhileStmt
DoWhileStmt
AginStmt
BreakStmt
ContinueStmt
ExpressionStmt
ImportStmt
ClassDecl
ClassField
Program (root)
```

#### Design
- Simple dataclasses for easy creation
- Hierarchical structure mirrors language semantics
- No behavior, just data structure
- Visitors can traverse and process tree

### 3. Parser (`src/parser.py`)

#### Responsibility
Convert token stream into an Abstract Syntax Tree.

#### Parsing Strategy
**Recursive Descent Parser**
- Each grammar rule implemented as a method
- Lookahead for decision making
- Easy to understand and modify

#### Method Organization
By Precedence Level:
```
parse()                     # Entry point
  parse_statement()         # Statements
    parse_variable_decl()
    parse_function_decl()
    parse_if_statement()
    etc.
  parse_expression()        # Expressions
    parse_ternary()
    parse_logical_or()
    parse_logical_and()
    parse_equality()
    parse_relational()
    parse_additive()
    parse_multiplicative()
    parse_power()
    parse_unary()
    parse_postfix()
    parse_primary()
```

#### Operator Precedence
Implemented via call chain:
```python
def parse_additive(self):
    left = self.parse_multiplicative()
    while self.match(PLUS, MINUS):
        op = self.advance().value
        right = self.parse_multiplicative()
        left = BinaryOp(left, op, right)
    return left
```

Higher precedence = deeper in the call chain

#### Error Handling
- `error()`: Raises SyntaxError with line/column
- `expect()`: Asserts token type
- `consume()`: Optional token matching
- `match()`: Check token type without consuming

#### Example
```python
parser = Parser(tokens)
program = parser.parse()
# Result: Program with statements
```

### 4. Runtime (`src/runtime.py`)

#### Responsibility
Execute the AST (interpret the program).

#### Key Concepts

**Environment (Scope)**
- Maps variable names to Variable objects
- Parent pointer for scope chain
- Methods: define, get, set, define_function, get_function

**Variable**
- Stores runtime value
- Tracks type and mutability
- Enforces immutability for `let`

**Function**
- Wraps FunctionDecl with environment
- Stores closure environment

**BuiltinFunction**
- Wraps Python function
- Used for show(), input(), etc.

#### Execution Flow
```
Program
  ├─ Global Environment created
  ├─ Builtins registered
  └─ Statements executed
      ├─ Variable Declarations
      │   └─ Value evaluated and stored
      ├─ Function Declarations
      │   └─ Function registered
      ├─ Statements
      │   ├─ IfStmt: Condition evaluated, block executed
      │   ├─ Loops: Condition checked, body executed
      │   └─ Expressions: Evaluated for side effects
      └─ Return: Exception thrown with value
```

#### Exception-Based Control Flow
- `ReturnValue`: Implements return statements
- `BreakException`: Implements break
- `ContinueException`: Implements continue

#### Expression Evaluation
Handles all operators:
- Arithmetic: +, -, *, /, %
- Comparison: ==, !=, <, >, <=, >=
- Logical: &&, ||, !
- Bitwise: &, |, ^, ~, <<, >>
- Assignment: =, +=, -=, *=, /=

#### Type Coercion
Python-like truthiness:
```python
def is_truthy(self, value):
    if value is None or value is False:
        return False
    if value == 0 or value == "" or (isinstance(...) and len(...) == 0):
        return False
    return True
```

### 5. CLI (`src/ygscript.py`)

#### Responsibility
Command-line interface for the language.

#### Commands

**run <file>**
- Read source file
- Parse and execute
- Display output

**compile <file> -o <output>**
- Read source file
- Parse to AST
- Output AST representation

**repl**
- Interactive shell
- Read-Eval-Print-Loop
- Persistent environment
- Commands: exit, help, clear

**lex <file>** (debug)
- Tokenize file
- Print tokens with positions

**parse <file>** (debug)
- Tokenize and parse
- Print AST representation

#### Error Handling
- FileNotFoundError: File not found
- SyntaxError: Parse errors
- RuntimeError: Execution errors
- NameError: Undefined variables
- Generic Exception: Unexpected errors

#### Argument Parsing
Uses argparse for clean CLI:
- Subparsers for each command
- Optional arguments (-o, -as)
- Help text

## Data Flow Examples

### Simple Variable Assignment
```
"let x = 42;"
    ↓ [Lexer]
[LET, IDENTIFIER, ASSIGN, INTEGER, SEMICOLON, EOF]
    ↓ [Parser]
VariableDecl(name='x', initial_value=IntLiteral(42), is_mutable=False)
    ↓ [Runtime]
Environment defines Variable(value=42, type='int', mutable=False)
```

### Function Call
```
"show(Add(3, 4))"
    ↓ [Lexer]
[IDENTIFIER, LPAREN, IDENTIFIER, LPAREN, INTEGER, COMMA, INTEGER, RPAREN, RPAREN, EOF]
    ↓ [Parser]
FunctionCall(
  name='show',
  args=[FunctionCall(name='Add', args=[IntLiteral(3), IntLiteral(4)])]
)
    ↓ [Runtime]
1. Lookup 'show' function → BuiltinFunction
2. Evaluate argument: call Add(3, 4) → 7
3. Call show(7) → prints "7"
```

### If Statement
```
"if (x > 5) { show("big"); }"
    ↓ [Lexer]
[IF, LPAREN, IDENTIFIER, GT, INTEGER, RPAREN, LBRACE, IDENTIFIER, LPAREN, STRING, RPAREN, SEMICOLON, RBRACE, EOF]
    ↓ [Parser]
IfStmt(
  condition=BinaryOp(Identifier('x'), '>', IntLiteral(5)),
  then_block=Block([ExpressionStmt(FunctionCall('show', [StringLiteral('big')]))])
)
    ↓ [Runtime]
1. Evaluate condition: get x, compare with 5
2. If true: execute then_block
3. Call show("big") → prints "big"
```

## Extension Points

### Adding a New Keyword
1. Add to `TokenType` enum in lexer.py
2. Add to `KEYWORDS` dict in Lexer class
3. Add parsing logic in parser.py
4. Add evaluation logic in runtime.py
5. Add test case

### Adding a New Operator
1. Add to `TokenType` enum
2. Add tokenization logic in lexer.py
3. Add parsing logic in parser.py (in correct precedence chain)
4. Add evaluation logic in runtime.py
5. Add test case

### Adding a Built-in Function
1. Implement function in Runtime class
2. Register in `setup_builtins()` method
3. Test and document

### Adding AST Node Type
1. Define new class inheriting from ASTNode
2. Add parsing logic to parser
3. Add evaluation logic to runtime
4. Update documentation

## Testing Strategy

### Unit Tests
Each component tested independently:
- Lexer: Token recognition
- Parser: AST structure
- Runtime: Expression evaluation

### Integration Tests
Full pipeline tests:
- Tokenize → Parse → Execute
- Verify output

### Example Programs
Real programs test:
- Multiple features together
- Realistic scenarios
- Performance

## Performance Considerations

### Current Implementation
- Tree-walking interpreter (simple, slow)
- No optimizations
- Python-based (good for prototyping)

### Optimization Opportunities
1. **Bytecode Compilation**: Compile AST to bytecode
2. **Caching**: Cache compiled functions
3. **JIT Compilation**: Native code generation
4. **Type Inference**: Remove runtime type checks
5. **Dead Code Elimination**: Remove unused code

### Memory Management
- Python garbage collection for objects/strings
- Stack-based for primitives
- Manual pointer operations

## Conclusion

The YGScript implementation follows classic interpreter architecture:
- **Lexer**: Simple finite state machine
- **Parser**: Recursive descent with precedence climbing
- **Runtime**: Tree-walking with environment chains

This design prioritizes:
- ✅ Clarity and maintainability
- ✅ Easy to extend
- ✅ Easy to debug
- ❌ Performance (trade-off accepted)

The modular structure allows for gradual optimization without rewriting core components.
