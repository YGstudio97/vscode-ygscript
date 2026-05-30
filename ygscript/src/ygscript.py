#!/usr/bin/env python3
"""
YGScript - Main entry point and CLI
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from lexer import Lexer
from parser import parse_source
from runtime import Runtime

def run_file(filename: str):
    """Run a YGScript file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse and execute
        program = parse_source(source)
        runtime = Runtime()
        runtime.execute(program)
        
    except FileNotFoundError:
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def compile_file(filename: str, output: str):
    """Compile a YGScript file to intermediate representation"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse
        program = parse_source(source)
        
        # For now, just output AST as string representation
        with open(output, 'w', encoding='utf-8') as f:
            f.write(repr(program))
        
        print(f"Compiled to: {output}")
        
    except FileNotFoundError:
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)

def repl():
    """Interactive REPL mode"""
    print("YGScript v1.0 - Interactive Shell")
    print("Type 'exit' to quit, 'help' for commands")
    print()
    
    runtime = Runtime()
    
    while True:
        try:
            # Read input
            line = input(">>> ")
            
            if line.lower() == 'exit':
                break
            
            if line.lower() == 'help':
                print("Commands:")
                print("  exit     - Exit the REPL")
                print("  help     - Show this help")
                print("  clear    - Clear screen")
                continue
            
            if line.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            if not line.strip():
                continue
            
            # Parse and execute
            program = parse_source(line)
            result = runtime.execute(program)
            
            # Print result if not None
            if result is not None:
                print(result)
        
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
        except RuntimeError as e:
            print(f"Runtime Error: {e}")
        except NameError as e:
            print(f"Name Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='YGScript Programming Language',
        prog='ygscript'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run a YGScript file')
    run_parser.add_argument('file', help='YGScript file to run')
    
    # compile command
    compile_parser = subparsers.add_parser('compile', help='Compile YGScript file')
    compile_parser.add_argument('file', help='YGScript file to compile')
    compile_parser.add_argument('-o', '--output', default='output.ir', help='Output file')
    
    # repl command
    repl_parser = subparsers.add_parser('repl', help='Interactive shell')
    
    # lex command (for debugging)
    lex_parser = subparsers.add_parser('lex', help='Tokenize file (debug)')
    lex_parser.add_argument('file', help='YGScript file to tokenize')
    
    # parse command (for debugging)
    parse_parser = subparsers.add_parser('parse', help='Parse file to AST (debug)')
    parse_parser.add_argument('file', help='YGScript file to parse')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_file(args.file)
    elif args.command == 'compile':
        compile_file(args.file, args.output)
    elif args.command == 'repl':
        repl()
    elif args.command == 'lex':
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            for token in tokens:
                print(f"{token.type.name:15} {token.value!r:20} ({token.line}:{token.column})")
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
    elif args.command == 'parse':
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                source = f.read()
            program = parse_source(source)
            print(program)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
