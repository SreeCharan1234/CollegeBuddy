import streamlit as st
import ast
import graphviz
from graphviz import Digraph
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import google.generativeai as genai
def syntax_highlight(code, language):
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style="colorful", full=True, noclasses=True)
        return highlight(code, lexer, formatter)
    except Exception as e:
        st.error(f"Syntax highlighting failed: {e}")
        return code

def generate_ast(code):
    try:
        tree = ast.parse(code)
        dot = Digraph()
        
        def add_nodes(node, parent=None):
            if isinstance(node, ast.AST):
                node_name = f"{node.__class__.__name__}_{id(node)}"
                dot.node(node_name, label=node.__class__.__name__)
                if parent:
                    dot.edge(parent, node_name)
                for child in ast.iter_child_nodes(node):
                    add_nodes(child, node_name)
            else:
                leaf_name = f"{str(node)}_{id(node)}"
                dot.node(leaf_name, label=str(node))
                if parent:
                    dot.edge(parent, leaf_name)

        add_nodes(tree)
        return dot
    except SyntaxError:
        st.error("The provided code does not appear to be valid Python syntax.")
        return None

def generate_flowchart(code):
    flowchart = Digraph()
    lines = code.splitlines()
    
    # Add start node
    flowchart.node("start", "Start", shape="ellipse", style="filled", color="lightblue")
    previous = "start"
    
    # Regex patterns to detect main function structures in various languages
    func_patterns = [
        re.compile(r"def\s+(\w+)\s*\("),       # Python
        re.compile(r"function\s+(\w+)\s*\("),  # JavaScript
        re.compile(r"(\w+\s+)?(\w+)\s*\("),    # Java, C, C++, C#
    ]
    
    for line in lines:
        if line.strip().startswith("//") or line.strip().startswith("#"):  # Comment step
            node = line.strip().lstrip("//#").strip()
            flowchart.node(node, node, shape="box", style="rounded,filled", color="lightgrey")
            flowchart.edge(previous, node)
            previous = node
        else:
            for pattern in func_patterns:
                match = pattern.match(line.strip())
                if match:  # New function detected as a major step
                    func_name = match.group(2) if len(match.groups()) > 1 else match.group(1)
                    flowchart.node(func_name, func_name, shape="parallelogram", style="filled", color="lightyellow")
                    flowchart.edge(previous, func_name)
                    previous = func_name

    # Add end node
    flowchart.node("end", "End", shape="ellipse", style="filled", color="lightblue")
    flowchart.edge(previous, "end")
    return flowchart

