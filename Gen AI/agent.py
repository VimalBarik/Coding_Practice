import re
import ast
import operator
import urllib.parse
import urllib.request
import json
import os


client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
MODEL = "claude-sonnet-4-20250514"

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isintance(node, ast.BinOp):
        op = type(node.op)
        if op not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op}")
        return _SAFE_OPS[op](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op = type(node.op)
        if op not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op}")
        return _SAFE_OPS[op](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculator(expression: str) -> str:
    try:
        expression = expression.strip()
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"
    
def web_search(query: str) -> str:
    try:
        encoded = urllib.parse.qoute_plus(query)
        url