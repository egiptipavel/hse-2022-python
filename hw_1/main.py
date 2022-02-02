import _ast
import ast
import inspect

import matplotlib.pyplot as plt
import networkx as nx


def recursive_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return recursive_fib(n - 1) + recursive_fib(n - 2)


fib_rec = ast.parse(inspect.getsource(recursive_fib))


def str_node(node):
    if isinstance(node, ast.AST):
        if isinstance(node, ast.Module):
            return node.__class__.__name__
        if isinstance(node, ast.FunctionDef):
            args = node.__dict__['args'].__dict__['args']
            return 'def ' + node.name + '(' + ', '.join('%s' % ast.unparse(arg) for arg in args) + ')'
        if isinstance(node, ast.Compare):
            res = 'compare'
            res += ' op: ' + node.__dict__['ops'][0].__class__.__name__
            return res
        if isinstance(node, ast.Name):
            return 'variable name: ' + ast.unparse(node)
        if isinstance(node, ast.Constant):
            return 'constant value: ' + ast.unparse(node)
        if isinstance(node, ast.If):
            return 'if'
        if isinstance(node, ast.Return):
            return 'return'
        if isinstance(node, ast.BinOp):
            bin_op = node.op.__class__.__name__
            op = '+' if bin_op == 'Add' else '-'
            return 'bin op: ' + op
        if isinstance(node, ast.Call):
            return 'function'
    else:
        return repr(node)


graph = nx.Graph()


def check(value):
    return isinstance(value, ast.Sub) or isinstance(value, ast.Load) or isinstance(value, ast.arguments) or \
           isinstance(value, _ast.cmpop) or isinstance(value, _ast.operator)


def ast_visit(node):
    str_of_node = str_node(node)

    graph.add_node(str_of_node)

    for _, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            if check(value):
                continue
            graph.add_edge(*(str_of_node, ast_visit(value)))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    if check(item):
                        continue
                    graph.add_edge(*(str_of_node, ast_visit(item)))
    return str_of_node


ast_visit(fib_rec)

nx.draw(graph, with_labels=True)
plt.show()
