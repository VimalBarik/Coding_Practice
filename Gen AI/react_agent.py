"""
ReAct Agent from Scratch
========================
A minimal ReAct (Reasoning + Acting) agent using:
  - 1 LLM  : Claude (via Anthropic API)
  - 2 Tools : web_search (DuckDuckGo, no API key needed)
              calculator (safe math eval)

Loop:
  Thought → Action → Observation → ... → Final Answer
"""

import re
import ast
import operator
import urllib.parse
import urllib.request
import json
import os

import anthropic

# ── Anthropic client ────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
MODEL = "claude-sonnet-4-20250514"

# ════════════════════════════════════════════════════════════════════════════
# Tool 1 — Calculator
# ════════════════════════════════════════════════════════════════════════════
_SAFE_OPS = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.Div:  operator.truediv,
    ast.Pow:  operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod:  operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
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
    """Safely evaluate a math expression and return the result as a string."""
    try:
        expression = expression.strip()
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


# ════════════════════════════════════════════════════════════════════════════
# Tool 2 — Web Search  (DuckDuckGo Instant Answer API — no key required)
# ════════════════════════════════════════════════════════════════════════════

def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return a short summary."""
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_redirect=1&no_html=1"
        req = urllib.request.Request(url, headers={"User-Agent": "react-agent/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())

        parts = []
        if data.get("AbstractText"):
            parts.append(data["AbstractText"])
        for r in data.get("RelatedTopics", [])[:3]:
            if isinstance(r, dict) and r.get("Text"):
                parts.append(r["Text"])
        if parts:
            return "\n".join(parts)
        return "No results found. Try a different query."
    except Exception as e:
        return f"Search error: {e}"


# ════════════════════════════════════════════════════════════════════════════
# Tool dispatcher
# ════════════════════════════════════════════════════════════════════════════
TOOLS = {
    "web_search":  web_search,
    "calculator":  calculator,
}

def run_tool(name: str, arg: str) -> str:
    if name not in TOOLS:
        return f"Unknown tool: '{name}'. Available: {list(TOOLS)}"
    return TOOLS[name](arg)


# ════════════════════════════════════════════════════════════════════════════
# System prompt
# ════════════════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are a ReAct agent. Solve tasks by alternating between
Thought, Action, and Observation steps.

You have exactly two tools:
  • web_search(query)   – search the internet for current information
  • calculator(expr)    – evaluate a math expression (e.g. "3 * (4 + 2)")

──────────────────────────────────────────
FORMAT  (follow this exactly, every loop):
──────────────────────────────────────────

Thought: <your reasoning about what to do next>
Action: <tool_name>(<argument>)

After I give you the Observation, continue with the next Thought/Action or:

Final Answer: <your answer to the original question>

Rules:
- One Action per step.
- Do NOT invent Observations; wait for them.
- When you have enough information, write "Final Answer:".
- Keep Thoughts concise.
"""


# ════════════════════════════════════════════════════════════════════════════
# ReAct loop
# ════════════════════════════════════════════════════════════════════════════
ACTION_RE = re.compile(
    r"Action:\s*(\w+)\s*\((.+?)\)\s*$",
    re.MULTILINE | re.DOTALL,
)
FINAL_RE = re.compile(r"Final Answer:\s*(.+)", re.DOTALL)


def react(question: str, max_steps: int = 10, verbose: bool = True) -> str:
    """Run the ReAct loop and return the final answer."""

    def log(text: str):
        if verbose:
            print(text)

    messages = [{"role": "user", "content": question}]
    log(f"\n{'='*60}")
    log(f"Question: {question}")
    log(f"{'='*60}\n")

    for step in range(1, max_steps + 1):
        log(f"── Step {step} ──────────────────────────────────────")

        # ── Call the LLM ────────────────────────────────────────
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        assistant_text = response.content[0].text.strip()
        log(assistant_text)

        # Append assistant turn
        messages.append({"role": "assistant", "content": assistant_text})

        # ── Check for Final Answer ──────────────────────────────
        final_match = FINAL_RE.search(assistant_text)
        if final_match:
            answer = final_match.group(1).strip()
            log(f"\n{'='*60}")
            log(f"✓ Final Answer: {answer}")
            log(f"{'='*60}\n")
            return answer

        # ── Parse and run Action ────────────────────────────────
        action_match = ACTION_RE.search(assistant_text)
        if not action_match:
            # No action found — nudge the model
            observation = (
                "No Action detected. "
                "Please write an Action line in the format: Action: tool_name(argument)"
            )
        else:
            tool_name = action_match.group(1).strip()
            tool_arg  = action_match.group(2).strip().strip('"').strip("'")
            log(f"\n→ Running {tool_name}({tool_arg!r})")
            observation = run_tool(tool_name, tool_arg)
            log(f"← Observation: {observation}\n")

        # Append observation as a new user turn
        messages.append({
            "role": "user",
            "content": f"Observation: {observation}",
        })

    return "Max steps reached without a final answer."


# ════════════════════════════════════════════════════════════════════════════
# Main — example questions
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    questions = [
        "What is the square root of the number of countries in the European Union?",
        "Who invented the World Wide Web, and in what year? How many years ago was that from 2025?",
    ]

    for q in questions:
        react(q, verbose=True)
        print()
