"""
YGScript Test Suite
"""

import sys
import os
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from lexer import Lexer, TokenType
from parser import parse_source
from runtime import Runtime
import io
from contextlib import redirect_stdout

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, func):
        """Register a test"""
        self.tests.append((name, func))
    
    def run_all(self):
        """Run all tests"""
        print("YGScript Test Suite")
        print("=" * 50)
        
        for test_name, test_func in self.tests:
            try:
                test_func()
                self.passed += 1
                print(f"✓ {test_name}")
            except AssertionError as e:
                self.failed += 1
                print(f"✗ {test_name}: {e}")
            except Exception as e:
                self.failed += 1
                print(f"✗ {test_name}: {type(e).__name__}: {e}")
        
        print("=" * 50)
        print(f"Passed: {self.passed}, Failed: {self.failed}")
        return self.failed == 0

runner = TestRunner()

# ============ LEXER TESTS ============

def test_lexer_integers():
    lexer = Lexer("let x = 42")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.LET
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.INTEGER

runner.test("Lexer: Integer literals", test_lexer_integers)

def test_lexer_strings():
    lexer = Lexer('"hello"')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "hello"

runner.test("Lexer: String literals", test_lexer_strings)

def test_lexer_keywords():
    lexer = Lexer("fnc if else while for")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.FNC
    assert tokens[1].type == TokenType.IF
    assert tokens[2].type == TokenType.ELSE
    assert tokens[3].type == TokenType.WHILE
    assert tokens[4].type == TokenType.FOR

runner.test("Lexer: Keywords", test_lexer_keywords)

# ============ PARSER TESTS ============

def test_parser_variable():
    program = parse_source("let x = 42;")
    assert len(program.statements) == 1
    assert program.statements[0].__class__.__name__ == "VariableDecl"

runner.test("Parser: Variable declaration", test_parser_variable)

def test_parser_function():
    program = parse_source("fnc Add(x: int32, y: int32) -> int32 { return x + y; }")
    assert len(program.statements) == 1
    assert program.statements[0].__class__.__name__ == "FunctionDecl"

runner.test("Parser: Function declaration", test_parser_function)

def test_parser_if_statement():
    program = parse_source("if (true) { show(1); } else { show(2); }")
    assert len(program.statements) == 1
    assert program.statements[0].__class__.__name__ == "IfStmt"

runner.test("Parser: If statement", test_parser_if_statement)

# ============ RUNTIME TESTS ============

def test_runtime_integer_arithmetic():
    runtime = Runtime()
    program = parse_source("let x = 5 + 3;")
    runtime.execute(program)

runner.test("Runtime: Integer arithmetic", test_runtime_integer_arithmetic)

def test_runtime_show_function():
    program = parse_source('show("Hello");')
    runtime = Runtime()
    
    # Capture output
    f = io.StringIO()
    with redirect_stdout(f):
        runtime.execute(program)
    
    output = f.getvalue()
    assert "Hello" in output

runner.test("Runtime: show() function", test_runtime_show_function)

def test_runtime_for_loop():
    program = parse_source("""
    let count = 0;
    for (let i = 0; i < 3; i++) {
        count = count + 1;
    }
    """)
    runtime = Runtime()
    runtime.execute(program)

runner.test("Runtime: for loop", test_runtime_for_loop)

def test_runtime_while_loop():
    program = parse_source("""
    let i = 0;
    while (i < 3) {
        i = i + 1;
    }
    """)
    runtime = Runtime()
    runtime.execute(program)

runner.test("Runtime: while loop", test_runtime_while_loop)

def test_runtime_if_statement():
    program = parse_source("""
    if (true) {
        let x = 42;
    }
    """)
    runtime = Runtime()
    runtime.execute(program)

runner.test("Runtime: if statement", test_runtime_if_statement)

def test_runtime_function_call():
    program = parse_source("""
    fnc Add(x: int32, y: int32) -> int32 {
        return x + y;
    }
    let result = Add(3, 4);
    """)
    runtime = Runtime()
    runtime.execute(program)

runner.test("Runtime: function call", test_runtime_function_call)

# ============ RUN TESTS ============

if __name__ == '__main__':
    success = runner.run_all()
    sys.exit(0 if success else 1)
