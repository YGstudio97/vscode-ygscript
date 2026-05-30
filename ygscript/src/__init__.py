"""
YGScript - Modern Programming Language
"""

__version__ = "1.0.0"
__author__ = "YGstudio97"

from lexer import Lexer, TokenType, Token
from ast_nodes import *
from parser import Parser, parse_source
from runtime import Runtime

__all__ = [
    'Lexer', 'TokenType', 'Token',
    'Parser', 'parse_source',
    'Runtime',
    'ASTNode', 'Program', 'Block',
]
