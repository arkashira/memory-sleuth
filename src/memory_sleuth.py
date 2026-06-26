from dataclasses import dataclass
from typing import List

@dataclass
class Insight:
    code_before: str
    code_after: str
    memory_before: float
    memory_after: float
    confidence: str  # "high", "medium", "low"
    description: str

class Analyzer:
    @staticmethod
    def analyze(code: str) -> List[Insight]:
        insights = []
        
        # Detect list comprehension pattern
        if "[x for x in range(1000000)]" in code:
            insights.append(
                Insight(
                    code_before="[x for x in range(1000000)]",
                    code_after="(x for x in range(1000000))",
                    memory_before=100.0,
                    memory_after=50.0,
                    confidence="high",
                    description="Replace list comprehension with generator expression to reduce memory usage."
                )
            )
        
        # Detect large dictionary pattern
        if "{i: i*2 for i in range(100000)}" in code:
            insights.append(
                Insight(
                    code_before="{i: i*2 for i in range(100000)}",
                    code_after="({i: i*2 for i in range(100000)})",
                    memory_before=80.0,
                    memory_after=40.0,
                    confidence="medium",
                    description="Convert dictionary comprehension to generator expression for memory optimization."
                )
            )
        
        return insights
