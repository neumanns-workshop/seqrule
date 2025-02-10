from seqrule import (
    Object,
    batch_evaluate,
    evaluate_rule,
    profile_rule_execution,
)


def test_evaluate_rule_with_valid_function(sample_sequence):
    """Test rule evaluation with a valid function."""
    def valid_rule(sequence):
        return all(obj.get("rank") >= 5 for obj in sequence)

    result, error = evaluate_rule(valid_rule, sample_sequence)
    assert result is True
    assert error is None


def test_evaluate_rule_with_invalid_function(sample_sequence):
    """Test rule evaluation with an invalid function."""
    result, error = evaluate_rule("not_a_function", sample_sequence)
    assert result is False
    assert error == "Invalid function"


def test_evaluate_empty_sequence():
    """Test rule evaluation with an empty sequence."""
    def valid_rule(sequence):
        return True

    result, error = evaluate_rule(valid_rule, [])
    assert result is False
    assert error == "Empty sequence"


def test_evaluate_rule_with_exception(sample_sequence):
    """Test rule evaluation when function raises an exception."""
    def failing_rule(sequence):
        raise ValueError("Test error")

    result, error = evaluate_rule(failing_rule, sample_sequence)
    assert result is False
    assert "Test error" in str(error)


def test_batch_evaluate(sample_sequence, complex_sequence):
    """Test batch evaluation of multiple rules and sequences."""
    def rule1(sequence):
        return all(obj.get("rank") >= 5 for obj in sequence)

    def rule2(sequence):
        return all(obj.get("suit") != "diamonds" for obj in sequence)

    sequences = [sample_sequence, complex_sequence]
    rules = [rule1, rule2]

    results = batch_evaluate(rules, sequences)
    assert len(results) == 4  # 2 rules * 2 sequences

    # Check structure of results
    for result in results:
        assert "rule" in result
        assert "sequence" in result
        assert "result" in result
        assert "failure_reason" in result


def test_profile_rule_execution(sample_sequence):
    """Test execution profiling of a rule."""
    def simple_rule(sequence):
        return all(obj.get("rank") >= 5 for obj in sequence)

    avg_time, avg_memory, seq_times, seq_memory = profile_rule_execution(
        simple_rule,
        [sample_sequence],
        runs=3
    )

    assert isinstance(avg_time, float)
    assert isinstance(avg_memory, float)
    assert len(seq_times) == 1
    assert len(seq_memory) == 1

    # Check that profiling metrics are reasonable
    assert avg_time > 0
    assert avg_memory > 0


def test_batch_evaluate_with_invalid_rule(sample_sequence):
    """Test batch evaluation with an invalid rule function."""
    def valid_rule(sequence):
        return True

    sequences = [sample_sequence]
    rules = ["not_a_function", valid_rule]

    results = batch_evaluate(rules, sequences)
    assert len(results) == 1  # Only the valid rule should be evaluated
    assert results[0]["result"] is True
    assert results[0]["failure_reason"] is None


def test_batch_evaluate_empty_inputs(sample_sequence):
    """Test batch evaluation with empty inputs."""
    results = batch_evaluate([], [])
    assert len(results) == 0

    def valid_rule(sequence):
        return True

    results = batch_evaluate([valid_rule], [])
    assert len(results) == 0

    results = batch_evaluate([], [sample_sequence])
    assert len(results) == 0


def test_batch_evaluate_single_rule():
    """Test batch_evaluate with a single rule (not in a list)."""
    def single_rule(sequence):
        return all(obj.get("rank") >= 5 for obj in sequence)

    sequences = [
        [Object("test1", rank=6)],
        [Object("test2", rank=4)]
    ]

    results = batch_evaluate(single_rule, sequences)
    assert len(results) == 2
    assert results[0]["result"] is True
    assert results[1]["result"] is False
    assert all("rule_function" in r["rule"] for r in results)
