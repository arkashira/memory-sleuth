import json
from dataclasses import dataclass
from typing import List

@dataclass
class MemoryLeak:
    """Represents a memory leak"""
    variable_name: str
    memory_usage: int

def detect_memory_leaks(codebase: str) -> List[MemoryLeak]:
    """Detects memory leaks in a given codebase"""
    # Simulate memory leak detection
    leaks = []
    for line in codebase.splitlines():
        if "global" in line:
            words = line.split()
            for word in words:
                if word.startswith("global"):
                    variable_name = words[words.index(word) + 1]
                    memory_usage = 100  # Simulated memory usage
                    leaks.append(MemoryLeak(variable_name, memory_usage))
    return leaks

def provide_recommendations(leaks: List[MemoryLeak]) -> List[str]:
    """Provides actionable recommendations for fixing memory leaks"""
    recommendations = []
    for leak in leaks:
        recommendation = f"Consider using a context manager for {leak.variable_name} to reduce memory usage"
        recommendations.append(recommendation)
    return recommendations
