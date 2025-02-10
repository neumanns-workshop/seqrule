"""Tests for API models and validation."""

import pytest

from seqrule.api import Condition, EvaluateRequest, ObjectData, RuleRequest


def test_condition_model():
    """Test Condition model validation."""
    # Test valid models
    condition = Condition(
        property_name="rank",
        operator=">",
        value=5
    )
    assert condition.property_name == "rank"
    assert condition.operator == ">"
    assert condition.value == 5

    # Test invalid operator
    with pytest.raises(ValueError) as exc_info:
        Condition(
            property_name="test",
            operator="invalid",
            value=5
        )
    assert "Invalid operator" in str(exc_info.value)

    # Test empty property name
    with pytest.raises(ValueError):
        Condition(property_name="", operator="=", value=5)

    # Test exists operator with non-None value
    with pytest.raises(ValueError) as exc_info:
        Condition(
            property_name="test",
            operator="exists",
            value={"some": "value"}
        )
    assert "exists operator requires None value" in str(exc_info.value)

    # Test not exists operator with non-None value
    with pytest.raises(ValueError) as exc_info:
        Condition(
            property_name="test",
            operator="not exists",
            value=42
        )
    assert "not exists operator requires None value" in str(exc_info.value)


def test_rule_request_model():
    """Test RuleRequest model validation."""
    # Test valid model
    request = RuleRequest(
        conditions=[
            Condition(property_name="rank", operator=">", value=5),
            Condition(
                property_name="suit",
                operator="in",
                value=["hearts", "spades"]
            )
        ],
        sequence=["ace", "king"]
    )
    assert len(request.conditions) == 2
    assert len(request.sequence) == 2

    # Test empty conditions
    with pytest.raises(ValueError):
        RuleRequest(conditions=[], sequence=["test"])

    # Test empty sequence
    with pytest.raises(ValueError):
        RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=[]
        )


def test_object_data_model():
    """Test ObjectData model validation."""
    # Test valid model
    object_data = ObjectData(
        name="ace",
        properties={"rank": 14, "suit": "hearts"}
    )
    assert object_data.name == "ace"
    assert object_data.properties["rank"] == 14

    # Test empty name
    with pytest.raises(ValueError):
        ObjectData(name="", properties={"test": 5})

    # Test empty properties
    with pytest.raises(ValueError) as exc_info:
        ObjectData(name="test", properties={})
    assert "Properties cannot be empty" in str(exc_info.value)


def test_evaluate_request_model():
    """Test EvaluateRequest model validation."""
    # Test valid model
    request = EvaluateRequest(
        objects=[
            ObjectData(name="ace", properties={"rank": 14, "suit": "hearts"}),
            ObjectData(name="king", properties={"rank": 13, "suit": "spades"})
        ]
    )
    assert len(request.objects) == 2

    # Test empty objects list
    with pytest.raises(ValueError):
        EvaluateRequest(objects=[])


def test_complex_condition_values():
    """Test Condition model with complex values."""
    # Test list values
    condition = Condition(
        property_name="test",
        operator="in",
        value=[1, 2, 3]
    )
    assert condition.value == [1, 2, 3]

    # Test dict values
    condition = Condition(
        property_name="test",
        operator="=",
        value={"key": "value"}
    )
    assert condition.value == {"key": "value"}

    # Test nested structures
    condition = Condition(
        property_name="test",
        operator="in",
        value=[{"key": [1, 2, 3]}, {"other": "value"}]
    )
    assert isinstance(condition.value, list)
    assert len(condition.value) == 2
