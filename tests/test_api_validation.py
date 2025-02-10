"""Tests for API validation functions."""

from seqrule.api import has_invalid_references, validate_sequence_order


def test_validate_sequence_order():
    """Test sequence order validation."""
    # Test valid sequence
    result, error = validate_sequence_order(["a", "b"], ["a", "b"])
    assert result is True
    assert error is None

    # Test empty sequence
    result, error = validate_sequence_order(["a", "b"], [])
    assert result is False
    assert error == "Empty sequence provided"

    # Test length mismatch
    result, error = validate_sequence_order(["a", "b"], ["a"])
    assert result is False
    assert "Sequence length mismatch" in error
    assert "Expected 2, got 1" in error

    # Test order mismatch
    result, error = validate_sequence_order(["a", "b"], ["b", "a"])
    assert result is False
    assert "Sequence order mismatch" in error
    assert "Expected ['a', 'b'], got ['b', 'a']" in error


def test_has_invalid_references():
    """Test invalid reference detection."""
    # Test valid values
    result, error = has_invalid_references({"normal": "value"})
    assert result is False
    assert error is None

    # Test function reference
    result, error = has_invalid_references({"$function": "some_func"})
    assert result is True
    assert "Function references are not allowed" in error

    # Test invalid reference
    result, error = has_invalid_references({"$ref": "some.path"})
    assert result is True
    assert "Invalid reference in condition value" in error

    # Test nested invalid reference
    result, error = has_invalid_references({
        "nested": {
            "deeper": {"$ref": "invalid"}
        }
    })
    assert result is True
    assert "Invalid reference in condition value" in error

    # Test list with invalid reference
    result, error = has_invalid_references([1, {"$ref": "invalid"}, 3])
    assert result is True
    assert "Invalid reference in condition value" in error

    # Test nested list with invalid reference
    result, error = has_invalid_references([1, [2, {"$ref": "invalid"}, 3], 4])
    assert result is True
    assert "Invalid reference in condition value" in error


def test_validate_sequence_order_with_duplicates():
    """Test sequence validation with duplicate names."""
    # Test sequence with duplicates in expected
    result, error = validate_sequence_order(
        ["a", "a", "b"],
        ["a", "a", "b"]
    )
    assert result is True
    assert error is None

    # Test sequence with duplicates in wrong order
    result, error = validate_sequence_order(
        ["a", "a", "b"],
        ["a", "b", "a"]
    )
    assert result is False
    assert "Sequence order mismatch" in error


def test_has_invalid_references_with_complex_structures():
    """Test invalid reference detection in complex structures."""
    # Test deeply nested structure
    complex_value = {
        "level1": {
            "level2": [
                {"level3": {"$ref": "invalid"}},
                {"level3": {"normal": "value"}}
            ]
        }
    }
    result, error = has_invalid_references(complex_value)
    assert result is True
    assert "Invalid reference in condition value" in error

    # Test mixed list and dict structure
    mixed_value = [
        {"valid": "value"},
        [{"$function": "invalid"}],
        {"nested": ["valid", {"$ref": "invalid"}]}
    ]
    result, error = has_invalid_references(mixed_value)
    assert result is True
    assert "Function references are not allowed" in error


def test_validate_sequence_order_edge_cases():
    """Test sequence validation edge cases."""
    # Test with empty expected sequence
    result, error = validate_sequence_order([], ["a", "b"])
    assert result is False
    assert "Sequence length mismatch" in error

    # Test with None values
    result, error = validate_sequence_order(["a", None, "b"], ["a", None, "b"])
    assert result is True
    assert error is None

    # Test with special characters
    result, error = validate_sequence_order(
        ["$special", "@char", "#test"],
        ["$special", "@char", "#test"]
    )
    assert result is True
    assert error is None
