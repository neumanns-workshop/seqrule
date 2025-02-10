import pytest

from seqrule import enforce_constraints


def test_valid_constraints():
    """Test constraints validation with valid inputs."""
    conditions = [
        ("rank", ">=", 5),
        ("suit", "=", "hearts"),
        ("value", "<", 10)
    ]
    sequence = ["heart", "spade"]

    assert enforce_constraints(conditions, sequence) is True


def test_none_value_constraints(invalid_values_sequence):
    """Test constraints with None values."""
    conditions = [
        ("rank", "=", None),
        ("suit", "=", None)
    ]
    sequence = ["none"]

    # None values should be handled gracefully
    assert enforce_constraints(conditions, sequence) is True


def test_special_value_constraints(invalid_values_sequence):
    """Test constraints with special values like infinity."""
    conditions = [
        ("rank", ">", float('-inf')),
        ("rank", "<", float('inf'))
    ]
    sequence = ["special"]

    assert enforce_constraints(conditions, sequence) is True


def test_empty_string_constraints(invalid_values_sequence):
    """Test constraints with empty string values."""
    conditions = [("suit", "=", "")]
    sequence = ["zero"]

    assert enforce_constraints(conditions, sequence) is True


def test_negative_value_constraints(invalid_values_sequence):
    """Test constraints with negative values."""
    conditions = [
        ("value", "<", 0),
        ("rank", "<", 0)
    ]
    sequence = ["negative"]

    assert enforce_constraints(conditions, sequence) is True


def test_complex_operator_constraints(complex_conditions):
    """Test constraints with complex operators."""
    sequence = ["heart", "spade", "diamond"]

    # Should handle complex operators like 'in' and 'exists'
    assert enforce_constraints(complex_conditions, sequence) is True


def test_missing_property_constraints(sequence_with_missing_properties):
    """Test constraints with missing properties."""
    conditions = [
        ("rank", ">", 0),  # Some objects missing rank
        ("suit", "=", "hearts"),  # Some objects missing suit
        ("extra", "exists", None)  # Only one object has this
    ]
    sequence = ["first", "second", "third"]

    # Should handle missing properties appropriately
    assert enforce_constraints(conditions, sequence) is True


def test_empty_constraints():
    """Test constraints validation with empty inputs."""
    assert enforce_constraints([], ["heart"]) is False
    assert enforce_constraints([("rank", ">=", 5)], []) is False
    assert enforce_constraints([], []) is False


def test_invalid_operator():
    """Test constraints validation with invalid operators."""
    conditions = [
        ("rank", ">=", 5),
        ("suit", "INVALID", "hearts"),  # Invalid operator
        ("value", "<", 10)
    ]
    sequence = ["heart", "spade"]

    assert enforce_constraints(conditions, sequence) is False


@pytest.mark.parametrize("operator", ["=", "!=", "<", ">", "<=", ">="])
def test_valid_operators(operator):
    """Test constraints validation with all valid operators."""
    conditions = [("rank", operator, 5)]
    sequence = ["heart"]

    assert enforce_constraints(conditions, sequence) is True


def test_rich_object_constraints(rich_object):
    """Test constraints with an object having many properties."""
    conditions = [
        ("rank", "=", 10),
        ("suit", "=", "spades"),
        ("value", "=", 25),
        ("color", "=", "black"),
        ("is_face_card", "=", True),
        ("custom_property", "=", "test")
    ]
    sequence = ["rich"]

    assert enforce_constraints(conditions, sequence) is True


def test_invalid_collection_operator_value():
    """Test constraints with invalid collection operator values."""
    conditions = [
        ("value", "in", 5),  # Should be a collection
        ("category", "not in", "invalid")  # Should be a collection
    ]
    sequence = ["test"]

    assert enforce_constraints(conditions, sequence) is False


def test_invalid_existence_operator_value():
    """Test constraints with invalid existence operator values."""
    conditions = [
        ("value", "exists", 5),  # Should be None
        ("category", "not exists", "invalid")  # Should be None
    ]
    sequence = ["test"]

    assert enforce_constraints(conditions, sequence) is False


def test_valid_collection_operators():
    """Test constraints with valid collection operator values."""
    conditions = [
        ("value", "in", [1, 2, 3]),
        ("category", "not in", {"A", "B", "C"}),
        ("tag", "in", (4, 5, 6))
    ]
    sequence = ["test"]

    assert enforce_constraints(conditions, sequence) is True


def test_valid_existence_operators():
    """Test constraints with valid existence operator values."""
    conditions = [
        ("value", "exists", None),
        ("category", "not exists", None)
    ]
    sequence = ["test"]

    assert enforce_constraints(conditions, sequence) is True
