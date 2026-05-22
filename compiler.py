import re
from sympy import sympify, pretty
from rich.table import Table
from rich.panel import Panel
from rich.box import DOUBLE
from rich.console import RenderableType
from typing import Union

class MathCompiler:
    @staticmethod
    def compile_latex(latex_str: str) -> str:
        try:
            # Simple cleanup of common LaTeX wrappers
            clean_latex = latex_str.replace("$$", "").replace("$", "").strip()
            expr = sympify(clean_latex, evaluate=False)
            return pretty(expr, use_unicode=True)
        except Exception:
            return latex_str # Fallback to raw if parsing fails

class ContentCompiler:
    def __init__(self):
        self.math_compiler = MathCompiler()

    def compile(self, text: str) -> Union[str, RenderableType]:
        # Detect LaTeX blocks
        if "$$" in text or (text.count("$") >= 2):
            return self.math_compiler.compile_latex(text)
        return text

class BlackboardCanvas(Panel):
    def __init__(self, content: str, title: str = "Math Output", **kwargs):
        # Chalk & Blackboard aesthetic
        compiled_math = MathCompiler.compile_latex(content)
        super().__init__(
            compiled_math,
            title=title,
            border_style="bold white",
            box=DOUBLE,
            style="white on #0b3d1d", # Dark green blackboard
            **kwargs
        )
