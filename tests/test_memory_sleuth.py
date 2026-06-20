from memory_sleuth import detect_memory_leaks, provide_recommendations, MemoryLeak
import pytest

def test_detect_memory_leaks():
    codebase = """ 
    x = 10
    global y
    y = 20 
    """
    leaks = detect_memory_leaks(codebase)
    assert len(leaks) == 1
    assert leaks[0].variable_name == "y"
    assert leaks[0].memory_usage == 100

def test_provide_recommendations():
    leaks = [MemoryLeak("x", 100), MemoryLeak("y", 200)]
    recommendations = provide_recommendations(leaks)
    assert len(recommendations) == 2
    assert recommendations[0] == "Consider using a context manager for x to reduce memory usage"
    assert recommendations[1] == "Consider using a context manager for y to reduce memory usage"

def test_detect_memory_leaks_empty_codebase():
    codebase = ""
    leaks = detect_memory_leaks(codebase)
    assert len(leaks) == 0

def test_provide_recommendations_empty_leaks():
    leaks = []
    recommendations = provide_recommendations(leaks)
    assert len(recommendations) == 0
