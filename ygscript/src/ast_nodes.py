"""
YGScript AST - Abstract Syntax Tree node definitions
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum, auto

class ASTNode:
    """Base class for all AST nodes"""
    pass

# ============== Type Nodes ==============
@dataclass
class Type(ASTNode):
    """Base type node"""
    name: str
    is_pointer: bool = False
    pointer_depth: int = 0
    is_const: bool = False
    generic_args: Optional[List['Type']] = None

@dataclass
class PrimitiveType(Type):
    """Primitive types (int, float, etc.)"""
    pass

@dataclass
class GenericType(Type):
    """Generic type with type parameters"""
    type_params: List[str]

# ============== Value/Literal Nodes ==============
@dataclass
class IntLiteral(ASTNode):
    value: int
    type_hint: Optional[str] = None

@dataclass
class FloatLiteral(ASTNode):
    value: float
    type_hint: Optional[str] = None

@dataclass
class DoubleLiteral(ASTNode):
    value: float
    type_hint: Optional[str] = None

@dataclass
class StringLiteral(ASTNode):
    value: str
    is_interpolated: bool = False

@dataclass
class CharLiteral(ASTNode):
    value: str

@dataclass
class BooleanLiteral(ASTNode):
    value: bool

@dataclass
class NullLiteral(ASTNode):
    pass

# ============== Expression Nodes ==============
@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode
    is_prefix: bool = True

@dataclass
class Assignment(ASTNode):
    target: ASTNode
    value: ASTNode
    op: str = "="  # Can be +=, -=, etc.

@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]
    type_args: Optional[List[Type]] = None

@dataclass
class MethodCall(ASTNode):
    obj: ASTNode
    method: str
    args: List[ASTNode]
    type_args: Optional[List[Type]] = None

@dataclass
class ArrayIndex(ASTNode):
    array: ASTNode
    index: ASTNode

@dataclass
class MemberAccess(ASTNode):
    obj: ASTNode
    member: str

@dataclass
class Cast(ASTNode):
    value: ASTNode
    target_type: Type

@dataclass
class TernaryOp(ASTNode):
    condition: ASTNode
    true_expr: ASTNode
    false_expr: ASTNode

@dataclass
class Pointer(ASTNode):
    """Address-of or dereference operations"""
    operand: ASTNode
    is_address_of: bool = True

# ============== Statement Nodes ==============
@dataclass
class Block(ASTNode):
    statements: List[ASTNode]

@dataclass
class VariableDecl(ASTNode):
    name: str
    type_annotation: Optional[Type]
    initial_value: Optional[ASTNode]
    is_mutable: bool = True  # True for 'var', False for 'let'
    is_const: bool = False   # True for 'const'

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List['Parameter']
    return_type: Optional[Type]
    body: Block
    type_params: Optional[List[str]] = None
    is_generic: bool = False

@dataclass
class Parameter(ASTNode):
    name: str
    type_annotation: Type
    default_value: Optional[ASTNode] = None

@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_block: Block
    elif_blocks: List[tuple] = None  # List of (condition, block) tuples
    else_block: Optional[Block] = None

@dataclass
class WhenStmt(ASTNode):
    """Condition that runs once, errors if false"""
    condition: ASTNode
    block: Block

@dataclass
class ThoughStmt(ASTNode):
    """Runs if condition is false"""
    condition: ASTNode
    block: Block

@dataclass
class SwitchStmt(ASTNode):
    expr: ASTNode
    cases: List['Case']
    default_case: Optional[Block] = None

@dataclass
class Case(ASTNode):
    value: ASTNode
    block: Block

@dataclass
class ForStmt(ASTNode):
    init: Optional[ASTNode]
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: Block

@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: Block

@dataclass
class DoWhileStmt(ASTNode):
    body: Block
    condition: ASTNode

@dataclass
class AginStmt(ASTNode):
    """Repeat N times loop"""
    times: ASTNode
    body: Block
    increment: bool = False  # If True, auto-increment loop counter

@dataclass
class BreakStmt(ASTNode):
    pass

@dataclass
class ContinueStmt(ASTNode):
    pass

@dataclass
class ExpressionStmt(ASTNode):
    expr: ASTNode

# ============== Import/Module Nodes ==============
@dataclass
class ImportStmt(ASTNode):
    module: str
    alias: Optional[str] = None
    specific_items: Optional[List[str]] = None
    import_all: bool = False

@dataclass
class ClassDecl(ASTNode):
    name: str
    fields: List['ClassField']
    methods: List[FunctionDecl]
    parent_class: Optional[str] = None

@dataclass
class ClassField(ASTNode):
    name: str
    type_annotation: Type
    initial_value: Optional[ASTNode] = None
    is_public: bool = True

# ============== Program ==============
@dataclass
class Program(ASTNode):
    statements: List[ASTNode]
