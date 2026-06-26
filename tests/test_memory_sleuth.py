from memory_sleuth import Analyzer, Insight

def test_analyze_list_comprehension():
    code = "[x for x in range(1000000)]"
    insights = Analyzer.analyze(code)
    
    assert len(insights) == 1
    insight = insights[0]
    assert insight.code_before == "[x for x in range(1000000)]"
    assert insight.code_after == "(x for x in range(1000000))"
    assert insight.memory_before == 100.0
    assert insight.memory_after == 50.0
    assert insight.confidence == "high"
    assert "generator expression" in insight.description

def test_analyze_no_patterns():
    code = "x = 1 + 1"
    insights = Analyzer.analyze(code)
    assert len(insights) == 0

def test_analyze_multiple_patterns():
    code = "[x for x in range(1000000)]\n{i: i*2 for i in range(100000)}"
    insights = Analyzer.analyze(code)
    assert len(insights) == 2
    
    list_insight = next(i for i in insights if i.code_before == "[x for x in range(1000000)]")
    dict_insight = next(i for i in insights if i.code_before == "{i: i*2 for i in range(100000)}")
    
    assert list_insight.memory_after == 50.0
    assert dict_insight.memory_after == 40.0
