"""
YGScript Runtime - Executes AST
"""

from typing import Dict, Any, Optional, List
from ast_nodes import *
import sys

class Variable:
    """Represents a runtime variable"""
    def __init__(self, value: Any, type_name: str, is_mutable: bool = True):
        self.value = value
        self.type_name = type_name
        self.is_mutable = is_mutable
    
    def set(self, value: Any):
        if not self.is_mutable:
            raise RuntimeError(f"Cannot modify immutable variable")
        self.value = value

class Function:
    """Represents a user-defined function"""
    def __init__(self, decl: FunctionDecl, env: 'Environment'):
        self.decl = decl
        self.env = env

class BuiltinFunction:
    """Represents a built-in function"""
    def __init__(self, name: str, func):
        self.name = name
        self.func = func
    
    def call(self, args: List[Any]):
        return self.func(*args)

class Environment:
    """Represents a scope for variable lookup"""
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, Variable] = {}
        self.functions: Dict[str, Function] = {}
        self.builtins: Dict[str, BuiltinFunction] = {}
    
    def define(self, name: str, value: Any, type_name: str, is_mutable: bool = True):
        """Define a variable in this scope"""
        self.variables[name] = Variable(value, type_name, is_mutable)
    
    def get(self, name: str) -> Variable:
        """Get variable from this or parent scope"""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any):
        """Set variable value in this or parent scope"""
        if name in self.variables:
            self.variables[name].set(value)
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise NameError(f"Undefined variable: {name}")
    
    def define_function(self, name: str, func: Function):
        """Define a function"""
        self.functions[name] = func
    
    def get_function(self, name: str) -> Optional[Function]:
        """Get function from this or parent scope"""
        if name in self.functions:
            return self.functions[name]
        elif name in self.builtins:
            return self.builtins[name]
        elif self.parent:
            return self.parent.get_function(name)
        return None
    
    def define_builtin(self, name: str, func: BuiltinFunction):
        """Define a built-in function"""
        self.builtins[name] = func

class ReturnValue(Exception):
    """Used to implement return statements"""
    def __init__(self, value: Any):
        self.value = value

class BreakException(Exception):
    """Used to implement break statements"""
    pass

class ContinueException(Exception):
    """Used to implement continue statements"""
    pass

class Runtime:
    """Executes YGScript AST"""
    
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()
    
    def setup_builtins(self):
        """Setup built-in functions"""
        self.global_env.define_builtin("show", BuiltinFunction("show", self.builtin_show))
        self.global_env.define_builtin("input", BuiltinFunction("input", self.builtin_input))
        self.global_env.define_builtin("len", BuiltinFunction("len", self.builtin_len))
        self.global_env.define_builtin("type", BuiltinFunction("type", self.builtin_type))
    
    def builtin_show(self, *args):
        """Output function"""
        output = ' '.join(str(arg) for arg in args)
        print(output)
        return None
    
    def builtin_input(self, *args):
        """Input function"""
        prompt = ""
        if len(args) > 0:
            prompt = str(args[0])
        result = input(prompt)
        return result
    
    def builtin_len(self, obj):
        """Length function"""
        if isinstance(obj, (str, list)):
            return len(obj)
        raise TypeError(f"object of type '{type(obj).__name__}' has no len()")
    
    def builtin_type(self, obj):
        """Type function"""
        return type(obj).__name__
    
    def execute(self, program: Program) -> Any:
        """Execute a program"""
        result = None
        try:
            for stmt in program.statements:
                result = self.eval_statement(stmt, self.global_env)
        except ReturnValue as ret:
            return ret.value
        return result
    
    def eval_statement(self, stmt: ASTNode, env: Environment) -> Any:
        """Evaluate a statement"""
        if isinstance(stmt, Block):
            result = None
            for s in stmt.statements:
                result = self.eval_statement(s, env)
            return result
        
        elif isinstance(stmt, VariableDecl):
            initial_value = None
            if stmt.initial_value:
                initial_value = self.eval_expression(stmt.initial_value, env)
            
            type_name = stmt.type_annotation.name if stmt.type_annotation else "auto"
            env.define(stmt.name, initial_value, type_name, is_mutable=stmt.is_mutable)
            return None
        
        elif isinstance(stmt, FunctionDecl):
            func = Function(stmt, env)
            env.define_function(stmt.name, func)
            return None
        
        elif isinstance(stmt, ReturnStmt):
            value = None
            if stmt.value:
                value = self.eval_expression(stmt.value, env)
            raise ReturnValue(value)
        
        elif isinstance(stmt, IfStmt):
            if self.is_truthy(self.eval_expression(stmt.condition, env)):
                return self.eval_statement(stmt.then_block, env)
            
            if stmt.elif_blocks:
                for elif_condition, elif_block in stmt.elif_blocks:
                    if self.is_truthy(self.eval_expression(elif_condition, env)):
                        return self.eval_statement(elif_block, env)
            
            if stmt.else_block:
                return self.eval_statement(stmt.else_block, env)
            return None
        
        elif isinstance(stmt, WhenStmt):
            condition_value = self.eval_expression(stmt.condition, env)
            if not self.is_truthy(condition_value):
                raise RuntimeError("when condition must be true")
            return self.eval_statement(stmt.block, env)
        
        elif isinstance(stmt, ThoughStmt):
            condition_value = self.eval_expression(stmt.condition, env)
            if not self.is_truthy(condition_value):
                return self.eval_statement(stmt.block, env)
            return None
        
        elif isinstance(stmt, SwitchStmt):
            expr_value = self.eval_expression(stmt.expr, env)
            
            for case in stmt.cases:
                case_value = self.eval_expression(case.value, env)
                if expr_value == case_value:
                    return self.eval_statement(case.block, env)
            
            if stmt.default_case:
                return self.eval_statement(stmt.default_case, env)
            return None
        
        elif isinstance(stmt, ForStmt):
            if stmt.init:
                self.eval_statement(stmt.init, env)
            
            while not stmt.condition or self.is_truthy(self.eval_expression(stmt.condition, env)):
                try:
                    self.eval_statement(stmt.body, env)
                except BreakException:
                    break
                except ContinueException:
                    pass
                
                if stmt.update:
                    self.eval_expression(stmt.update, env)
            return None
        
        elif isinstance(stmt, WhileStmt):
            while self.is_truthy(self.eval_expression(stmt.condition, env)):
                try:
                    self.eval_statement(stmt.body, env)
                except BreakException:
                    break
                except ContinueException:
                    pass
            return None
        
        elif isinstance(stmt, DoWhileStmt):
            while True:
                try:
                    self.eval_statement(stmt.body, env)
                except BreakException:
                    break
                except ContinueException:
                    pass
                
                if not self.is_truthy(self.eval_expression(stmt.condition, env)):
                    break
            return None
        
        elif isinstance(stmt, AginStmt):
            times = self.eval_expression(stmt.times, env)
            if not isinstance(times, int) or times < 0:
                raise TypeError("agin times must be non-negative integer")
            
            for i in range(times):
                if stmt.increment:
                    env.define("i", i, "int")
                
                try:
                    self.eval_statement(stmt.body, env)
                except BreakException:
                    break
                except ContinueException:
                    pass
            return None
        
        elif isinstance(stmt, BreakStmt):
            raise BreakException()
        
        elif isinstance(stmt, ContinueStmt):
            raise ContinueException()
        
        elif isinstance(stmt, ExpressionStmt):
            return self.eval_expression(stmt.expr, env)
        
        elif isinstance(stmt, ImportStmt):
            # For now, silently ignore imports
            return None
        
        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt)}")
    
    def eval_expression(self, expr: ASTNode, env: Environment) -> Any:
        """Evaluate an expression"""
        if isinstance(expr, IntLiteral):
            return expr.value
        
        elif isinstance(expr, FloatLiteral):
            return expr.value
        
        elif isinstance(expr, DoubleLiteral):
            return expr.value
        
        elif isinstance(expr, StringLiteral):
            return expr.value
        
        elif isinstance(expr, CharLiteral):
            return expr.value
        
        elif isinstance(expr, BooleanLiteral):
            return expr.value
        
        elif isinstance(expr, NullLiteral):
            return None
        
        elif isinstance(expr, Identifier):
            return env.get(expr.name).value
        
        elif isinstance(expr, BinaryOp):
            left = self.eval_expression(expr.left, env)
            right = self.eval_expression(expr.right, env)
            
            if expr.op == '+':
                return left + right
            elif expr.op == '-':
                return left - right
            elif expr.op == '*':
                return left * right
            elif expr.op == '/':
                if isinstance(left, int) and isinstance(right, int):
                    return left // right
                return left / right
            elif expr.op == '%':
                return left % right
            elif expr.op == '==':
                return left == right
            elif expr.op == '!=':
                return left != right
            elif expr.op == '<':
                return left < right
            elif expr.op == '>':
                return left > right
            elif expr.op == '<=':
                return left <= right
            elif expr.op == '>=':
                return left >= right
            elif expr.op == '&&':
                return self.is_truthy(left) and self.is_truthy(right)
            elif expr.op == '||':
                return self.is_truthy(left) or self.is_truthy(right)
            elif expr.op == '&':
                return left & right
            elif expr.op == '|':
                return left | right
            elif expr.op == '^':
                return left ^ right
            elif expr.op == '<<':
                return left << right
            elif expr.op == '>>':
                return left >> right
            else:
                raise RuntimeError(f"Unknown binary operator: {expr.op}")
        
        elif isinstance(expr, UnaryOp):
            operand = self.eval_expression(expr.operand, env)
            
            if expr.op == '-':
                return -operand
            elif expr.op == '+':
                return +operand
            elif expr.op == '!':
                return not self.is_truthy(operand)
            elif expr.op == '~':
                return ~operand
            elif expr.op == '++':
                # For now, just return incremented value
                return operand + 1
            elif expr.op == '--':
                return operand - 1
            else:
                raise RuntimeError(f"Unknown unary operator: {expr.op}")
        
        elif isinstance(expr, Assignment):
            value = self.eval_expression(expr.value, env)
            
            if isinstance(expr.target, Identifier):
                if expr.op == '=':
                    env.set(expr.target.name, value)
                elif expr.op == '+=':
                    current = env.get(expr.target.name).value
                    env.set(expr.target.name, current + value)
                elif expr.op == '-=':
                    current = env.get(expr.target.name).value
                    env.set(expr.target.name, current - value)
                elif expr.op == '*=':
                    current = env.get(expr.target.name).value
                    env.set(expr.target.name, current * value)
                elif expr.op == '/=':
                    current = env.get(expr.target.name).value
                    env.set(expr.target.name, current / value)
            else:
                raise RuntimeError("Invalid assignment target")
            
            return value
        
        elif isinstance(expr, FunctionCall):
            func = env.get_function(expr.name)
            
            if func is None:
                raise NameError(f"Undefined function: {expr.name}")
            
            # Evaluate arguments
            args = [self.eval_expression(arg, env) for arg in expr.args]
            
            if isinstance(func, BuiltinFunction):
                return func.call(args)
            
            # User-defined function
            func_decl = func.decl
            
            # Create new environment for function execution
            func_env = Environment(func.env)
            
            # Bind parameters
            for i, param in enumerate(func_decl.params):
                if i < len(args):
                    func_env.define(param.name, args[i], param.type_annotation.name)
                elif param.default_value:
                    default_val = self.eval_expression(param.default_value, func_env)
                    func_env.define(param.name, default_val, param.type_annotation.name)
            
            # Execute function body
            try:
                self.eval_statement(func_decl.body, func_env)
                return None  # No explicit return
            except ReturnValue as ret:
                return ret.value
        
        elif isinstance(expr, TernaryOp):
            condition = self.eval_expression(expr.condition, env)
            if self.is_truthy(condition):
                return self.eval_expression(expr.true_expr, env)
            else:
                return self.eval_expression(expr.false_expr, env)
        
        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")
    
    def is_truthy(self, value: Any) -> bool:
        """Python-like truthiness"""
        if value is None or value is False:
            return False
        if value == 0 or value == "" or (isinstance(value, (list, dict)) and len(value) == 0):
            return False
        return True
