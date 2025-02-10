import pytest

from seqrule import (
    analyze_rule_complexity,
    compute_branching_factor,
    compute_condition_impact,
    compute_custom_complexity_score,
    compute_entropy,
    compute_redundancy,
    count_categorical_constraints,
    count_numerical_constraints,
    detect_contradictions,
    estimate_execution_cost,
)

# Sample test data
sample_conditions = [
    ("rank", ">", 7),
    ("suit", "=", "hearts"),
    ("value", "<", 10),
    ("rank", "<", 9),
    ("color", "=", "red")
]

sample_sequence_constraints = ["card1", "card2", "card3"]

def test_analyze_rule_complexity():
    """Test that analyze_rule_complexity computes all metrics correctly."""
    # Mock rule function
    def rule_func(sequence):
        return True

    # Test conditions with various types
    conditions = [
        ("rank", ">", 5),     # numerical, strict inequality
        ("value", "<=", 10),  # numerical, non-strict inequality
        ("suit", "=", "hearts"),  # categorical
        ("color", "=", "red")     # categorical
    ]
    sequence_constraints = ["card1", "card2"]

    # Analyze complexity
    metrics = analyze_rule_complexity(rule_func, conditions, sequence_constraints)

    # Verify all expected metrics are present and have correct values
    assert metrics["condition_count"] == 4
    assert metrics["sequence_length"] == 2
    assert metrics["logical_depth"] == 4  # All conditions are tuples
    assert metrics["entropy"] == 1.0  # All conditions are unique
    assert metrics["branching_factor"] == 2  # Two inequality conditions
    assert metrics["redundancy"] == 0.25  # One repeated pattern (=)
    assert metrics["execution_cost"] == 8  # 4 conditions * 2 sequence items
    assert metrics["contradictions"] == 0  # No contradictions
    assert metrics["categorical_constraints"] == 2  # suit and color
    assert metrics["numerical_constraints"] == 2  # rank and value
    assert metrics["condition_impact"] == (1.5 + 1.2 + 1.0 + 1.0) / 2

    # Test with empty conditions and sequence
    empty_metrics = analyze_rule_complexity(rule_func, [], [])
    assert empty_metrics["condition_count"] == 0
    assert empty_metrics["sequence_length"] == 0
    assert empty_metrics["logical_depth"] == 0
    assert empty_metrics["entropy"] == 0.0
    assert empty_metrics["branching_factor"] == 0
    assert empty_metrics["redundancy"] == 0.0
    assert empty_metrics["execution_cost"] == 0
    assert empty_metrics["contradictions"] == 0
    assert empty_metrics["categorical_constraints"] == 0
    assert empty_metrics["numerical_constraints"] == 0
    assert empty_metrics["condition_impact"] == 0.0

def test_compute_entropy():
    entropy = compute_entropy(sample_conditions)
    assert 0 <= entropy <= 1
    assert entropy == len(set(sample_conditions)) / len(sample_conditions)

def test_compute_entropy_error_handling():
    """Test that compute_entropy handles errors gracefully."""
    # Test with invalid conditions that would cause TypeError
    invalid_conditions = [(None, None, None)]
    assert compute_entropy(invalid_conditions) == 0.0

    # Test with conditions that would cause ValueError
    invalid_value_conditions = [("prop", "=", {})]  # Dict value will cause issues
    assert compute_entropy(invalid_value_conditions) == 0.0

def test_compute_entropy_list_values():
    """Test that compute_entropy handles list values correctly."""
    # Test with list values that need to be converted to tuples
    conditions = [
        ("cards", "=", [1, 2, 3]),
        ("values", "=", [4, 5, 6]),
        ("cards", "=", [1, 2, 3])  # Duplicate after conversion
    ]
    entropy = compute_entropy(conditions)
    assert entropy == 2/3  # Two unique conditions after list conversion

    # Test with mixed value types
    mixed_conditions = [
        ("cards", "=", [1, 2]),
        ("rank", ">", 5),
        ("suit", "=", "hearts"),
        ("cards", "=", [1, 2])  # Duplicate
    ]
    entropy = compute_entropy(mixed_conditions)
    assert entropy == 3/4  # Three unique conditions

    # Test with empty lists
    empty_list_conditions = [
        ("cards", "=", []),
        ("values", "=", []),  # Should be considered duplicate
        ("rank", ">", 5)
    ]
    entropy = compute_entropy(empty_list_conditions)
    assert entropy == 2/3  # Two unique conditions

def test_compute_branching_factor():
    factor = compute_branching_factor(sample_conditions)
    assert factor == 3  # Three range-based conditions (>, <, <)

def test_compute_branching_factor_error_handling():
    """Test that compute_branching_factor handles invalid conditions."""
    # Test with None value
    invalid_conditions = [("prop", "=", None)]
    assert compute_branching_factor(invalid_conditions) == 0.0

    # Test with dict value
    dict_conditions = [("prop", "=", {"key": "value"})]
    assert compute_branching_factor(dict_conditions) == 0.0

def test_compute_redundancy():
    redundancy = compute_redundancy(sample_conditions)
    assert 0 <= redundancy <= 1
    # We have 5 conditions with 5 unique patterns
    assert redundancy == 0.0  # No redundancy since all patterns are unique

def test_compute_redundancy_empty_conditions():
    """Test computing redundancy with empty conditions."""
    conditions = []
    redundancy = compute_redundancy(conditions)
    assert redundancy == 1.0  # Maximum redundancy when no conditions exist

def test_compute_redundancy_with_duplicates():
    """Test computing redundancy with duplicate condition patterns."""
    conditions = [
        ("rank", ">", 7),  # First pattern
        ("suit", "=", "hearts"),
        ("rank", ">", 10),  # Same pattern as first, different value
        ("value", "<", 10)
    ]
    redundancy = compute_redundancy(conditions)
    assert redundancy == 0.25  # One duplicate out of four conditions

def test_estimate_execution_cost():
    cost = estimate_execution_cost(sample_conditions, sample_sequence_constraints)
    assert cost == len(sample_conditions) * len(sample_sequence_constraints)

def test_detect_contradictions():
    contradicting_conditions = [
        ("rank", ">", 7),
        ("rank", "<", 7),
        ("suit", "=", "hearts"),
        ("suit", ">", "diamonds")
    ]
    contradictions = detect_contradictions(contradicting_conditions)
    assert contradictions == 2

def test_detect_contradictions_edge_cases():
    """Test edge cases for contradiction detection."""
    # Test equality vs inequality contradiction
    conditions = [
        ("rank", "=", 7),
        ("rank", ">", 5)  # Contradicts with equality
    ]
    assert detect_contradictions(conditions) == 1

    # Test reverse order of operations
    conditions = [
        ("rank", "<", 7),
        ("rank", ">", 8)  # Clear contradiction
    ]
    assert detect_contradictions(conditions) == 1

    # Test equal values in inequality
    conditions = [
        ("rank", ">", 7),
        ("rank", "<", 7)  # Equal value makes it contradictory
    ]
    assert detect_contradictions(conditions) == 1

    # Test no contradictions with compatible conditions
    conditions = [
        ("rank", ">", 5),
        ("rank", "<", 10)  # Compatible range
    ]
    assert detect_contradictions(conditions) == 0

def test_count_constraints():
    categorical = count_categorical_constraints(sample_conditions)
    numerical = count_numerical_constraints(sample_conditions)
    assert categorical == 2  # "hearts" and "red"
    assert numerical == 3   # 7, 10, 9

def test_compute_condition_impact():
    """Test condition impact calculation with different operators."""
    # Test with strict inequalities (>, <)
    strict_conditions = [
        ("rank", ">", 5),
        ("value", "<", 10)
    ]
    sequence = ["card1", "card2"]
    impact = compute_condition_impact(strict_conditions, sequence)
    assert impact == (1.5 + 1.5) / 2  # Two strict inequalities, normalized by sequence length

    # Test with non-strict inequalities (>=, <=)
    non_strict_conditions = [
        ("rank", ">=", 5),
        ("value", "<=", 10)
    ]
    impact = compute_condition_impact(non_strict_conditions, sequence)
    assert impact == (1.2 + 1.2) / 2  # Two non-strict inequalities

    # Test with equality operators
    equality_conditions = [
        ("suit", "=", "hearts"),
        ("color", "=", "red")
    ]
    impact = compute_condition_impact(equality_conditions, sequence)
    assert impact == (1.0 + 1.0) / 2  # Two equality operators

    # Test with mixed operators
    mixed_conditions = [
        ("rank", ">", 5),    # 1.5
        ("value", "<=", 10), # 1.2
        ("suit", "=", "hearts") # 1.0
    ]
    impact = compute_condition_impact(mixed_conditions, sequence)
    assert impact == (1.5 + 1.2 + 1.0) / 2  # Mixed operators

    # Test with empty sequence (should avoid division by zero)
    empty_sequence = []
    impact = compute_condition_impact(mixed_conditions, empty_sequence)
    assert impact == (1.5 + 1.2 + 1.0) / 1  # Normalized by max(1, len(sequence))

def test_compute_custom_complexity_score():
    metrics = {
        "condition_count": 5,
        "sequence_length": 3,
        "entropy": 0.8,
        "branching_factor": 3,
        "redundancy": 0.2
    }

    # Test weighted model
    weights = {"condition_count": 2.0, "entropy": 1.5}
    weighted_score = compute_custom_complexity_score(metrics, model="weighted", weights=weights)
    assert weighted_score == 11.2  # 5*2.0 + 0.8*1.5 + 3 + 0.2

    # Test entropy-based model
    entropy_score = compute_custom_complexity_score(metrics, model="entropy_based")
    assert entropy_score == metrics["entropy"] * 10

    # Test log-scaled model
    import math
    log_score = compute_custom_complexity_score(metrics, model="log_scaled")
    expected_log = sum(math.log1p(val) for val in metrics.values())
    assert log_score == expected_log

    # Test normalized model
    norm_score = compute_custom_complexity_score(metrics, model="normalized")
    assert norm_score == sum(val / max(1, val) for val in metrics.values())

    # Test invalid model
    with pytest.raises(ValueError):
        compute_custom_complexity_score(metrics, model="invalid")

def test_compute_custom_complexity_score_with_empty_weights():
    """Test weighted model with empty weights dictionary."""
    metrics = {
        "condition_count": 5,
        "sequence_length": 3,
        "entropy": 0.8
    }

    # Test weighted model with no weights provided
    score = compute_custom_complexity_score(metrics, model="weighted")
    assert score == sum(metrics.values())  # Default weight of 1.0 for each metric

def test_compute_custom_complexity_score_with_missing_metrics():
    """Test weighted model with weights for metrics not in the input."""
    metrics = {
        "condition_count": 5,
        "sequence_length": 3
    }

    weights = {
        "condition_count": 2.0,
        "missing_metric": 1.5  # This metric is not in the input
    }

    score = compute_custom_complexity_score(metrics, model="weighted", weights=weights)
    assert score == 10.0  # 5 * 2.0 for condition_count, sequence_length uses default weight

def test_compute_custom_complexity_score_models():
    """Test different models for computing complexity scores."""
    metrics = {
        "entropy": 0.5,
        "branching": 2.0,
        "redundancy": 0.3
    }

    # Test weighted model with custom weights
    weights = {"entropy": 2.0, "branching": 1.5, "redundancy": 1.0}
    weighted_score = compute_custom_complexity_score(metrics, "weighted", weights)
    assert weighted_score == 0.5 * 2.0 + 2.0 * 1.5 + 0.3 * 1.0

    # Test weighted model with default weights
    default_weighted = compute_custom_complexity_score(metrics, "weighted")
    assert default_weighted == sum(metrics.values())

    # Test entropy-based model
    entropy_score = compute_custom_complexity_score(metrics, "entropy_based")
    assert entropy_score == metrics["entropy"] * 10

    # Test log-scaled model
    import math
    log_score = compute_custom_complexity_score(metrics, "log_scaled")
    assert log_score == sum(math.log1p(v) for v in metrics.values())

    # Test normalized model
    norm_score = compute_custom_complexity_score(metrics, "normalized")
    assert norm_score == sum(v / max(1, v) for v in metrics.values())

    # Test invalid model
    with pytest.raises(ValueError):
        compute_custom_complexity_score(metrics, "invalid_model")

    # Test zero entropy case
    zero_metrics = {"entropy": 0.0, "branching": 2.0}
    assert compute_custom_complexity_score(zero_metrics, "weighted") == 0.0

def test_compute_entropy_type_error():
    """Test that compute_entropy handles TypeError gracefully."""
    # Create conditions that will cause TypeError during set conversion
    conditions = [
        ("prop", "=", {"unhashable": [1, 2, 3]}),  # Dictionary is unhashable
        ("prop2", "=", {"another": "dict"})  # Another unhashable value
    ]
    entropy = compute_entropy(conditions)
    assert entropy == 0.0  # Should return 0.0 on error

def test_compute_entropy_value_error():
    """Test that compute_entropy handles ValueError gracefully."""
    # Create a custom class that raises ValueError when used in set operations
    class CustomValue:
        def __eq__(self, other):
            raise ValueError("Test error")

        def __hash__(self):
            raise ValueError("Test error")

    conditions = [
        ("prop", "=", CustomValue()),
        ("prop2", "=", CustomValue())
    ]
    entropy = compute_entropy(conditions)
    assert entropy == 0.0  # Should return 0.0 on error

def test_compute_entropy_empty_conditions():
    """Test that compute_entropy handles empty conditions correctly."""
    entropy = compute_entropy([])
    assert entropy == 0.0  # Should return 0.0 for empty conditions

def test_analyze_rule_complexity_edge_cases():
    """Test edge cases in rule complexity analysis."""
    # Test with a rule function that always returns True
    def simple_rule_func(sequence):
        return True

    # Test with empty conditions
    metrics = analyze_rule_complexity(simple_rule_func, [], [])
    assert metrics["entropy"] == 0.0
    assert metrics["branching_factor"] == 0.0
    assert metrics["condition_impact"] == 0.0

    # Test with None values in conditions
    conditions = [("prop", "=", None)]
    metrics = analyze_rule_complexity(simple_rule_func, conditions, [])
    assert metrics["entropy"] == 0.0  # None values should result in zero entropy

    # Test with dict values in conditions
    conditions = [("prop", "=", {"key": "value"})]
    metrics = analyze_rule_complexity(simple_rule_func, conditions, [])
    assert metrics["entropy"] == 0.0  # Dict values should result in zero entropy

    # Test with mixed value types
    conditions = [
        ("rank", ">", 5),
        ("suit", "in", ["hearts", "spades"]),
        ("value", "=", None),
        ("props", "=", {"key": "value"})
    ]
    metrics = analyze_rule_complexity(simple_rule_func, conditions, ["test"])
    assert 0.0 <= metrics["entropy"] <= 1.0
    assert metrics["branching_factor"] >= 0.0
    assert metrics["condition_impact"] >= 0.0
