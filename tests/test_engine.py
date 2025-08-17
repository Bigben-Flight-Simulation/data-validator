from data_validator.engine import RuleEngine

def test_simple_rule():
    rules = [
        {
            "name": "test_rule",
            "condition": {
                "if": {"all": ["curr['col1'] == 'z'"]},
                "then": ["curr['col2'] == 'x'"]
            },
            "throw_on": "any",
        }
    ]

    rows = [{"col1": "z", "col2": "y"}]
    engine = RuleEngine(rules)
    errors = engine.run(rows)
    assert errors, "Should detect error"
