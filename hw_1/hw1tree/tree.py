import ast

import matplotlib.pyplot as plt
import networkx as nx


class Tree:
    def __init__(self):
        self.count = 0

    FIB = """def fib(n):
        res = []
        a = 0
        b = 1
        while n != 0:
            res.append(a)
            a = a + b
            b = a - b
            n = n - 1
        return res"""

    def __str_node(self, node):
        if isinstance(node, ast.Module):
            return node.__class__.__name__
        if isinstance(node, ast.FunctionDef):
            args = node.__dict__['args'].__dict__['args']
            return 'def ' + node.name + '(' + ', '.join('%s' % ast.unparse(arg) for arg in args) + ')'
        if isinstance(node, ast.Compare):
            res = 'cmp'
            res += ' op: ' + node.__dict__['ops'][0].__class__.__name__
            return res
        if isinstance(node, ast.Name):
            return 'var: ' + ast.unparse(node)
        if isinstance(node, ast.Constant):
            return 'cont val: ' + ast.unparse(node)
        if isinstance(node, ast.If):
            return 'if'
        if isinstance(node, ast.Return):
            return 'return'
        if isinstance(node, ast.BinOp):
            bin_op = node.op.__class__.__name__
            op = '+' if bin_op == 'Add' else '-'
            return 'bin op: ' + op
        if isinstance(node, ast.Call):
            return 'func'
        if isinstance(node, ast.Assign):
            return 'assign'
        if isinstance(node, ast.While):
            return 'while'
        if isinstance(node, ast.Expr):
            return 'expr'
        return ast.unparse(node)

    def __check(self, value):
        return isinstance(value, ast.Sub) or isinstance(value, ast.Load) or isinstance(value, ast.arguments) or \
               isinstance(value, ast.cmpop) or isinstance(value, ast.operator) or isinstance(value, ast.Store)

    def __ast_visit(self, node, graph):
        str_of_node = str(self.count) + ' ' + self.__str_node(node)
        self.count += 1

        graph.add_node(str_of_node)

        for _, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                if self.__check(value):
                    continue
                graph.add_edge(*(str_of_node, self.__ast_visit(value, graph)))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        if self.__check(item):
                            continue
                        graph.add_edge(*(str_of_node, self.__ast_visit(item, graph)))
        return str_of_node

    def run(self, file_name):
        graph = nx.Graph()

        self.__ast_visit(ast.parse(Tree.FIB), graph)

        nx.draw(graph, with_labels=True, node_color='#00b4d9')
        plt.savefig(file_name)

        self.count = 0
