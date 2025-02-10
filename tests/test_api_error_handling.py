"""Tests for API error handling."""

from unittest.mock import patch

import pytest
from fastapi import HTTPException

from seqrule.api import (
    Condition,
    EvaluateRequest,
    ObjectData,
    RuleRequest,
    analyze_rule,
    create_rule,
    evaluate_sequence,
)


@pytest.mark.asyncio
async def test_create_rule_with_invalid_reference():
    """Test that invalid references in condition values are rejected."""
    rule_request = RuleRequest(
        conditions=[
            Condition(
                property_name="rank",
                operator="=",
                value={"$ref": "some.path"}
            )
        ],
        sequence=["card1"]
    )
    with pytest.raises(HTTPException) as exc_info:
        await create_rule(rule_request)
    assert exc_info.value.status_code == 400
    assert "Invalid reference in condition value" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_invalid_object_properties():
    """Test evaluate_sequence with invalid object properties."""
    rule_request = RuleRequest(
        conditions=[
            Condition(property_name="test", operator="=", value=5)
        ],
        sequence=["test"]
    )
    evaluate_request = EvaluateRequest(
        objects=[
            ObjectData(
                name="test",
                properties={"test": {"complex": "value"}}  # Invalid value type
            )
        ]
    )
    with pytest.raises(HTTPException) as exc_info:
        await evaluate_sequence(rule_request, evaluate_request)
    assert exc_info.value.status_code == 422
    assert "values must be primitive types" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_analyze_rule_with_invalid_model():
    """Test analyze_rule with invalid model type."""
    rule_request = RuleRequest(
        conditions=[
            Condition(property_name="test", operator="=", value=5)
        ],
        sequence=["test"]
    )

    # Test with invalid model string
    with pytest.raises(HTTPException) as exc_info:
        await analyze_rule(rule_request, model="invalid_model")
    assert exc_info.value.status_code == 422
    assert "Invalid model" in str(exc_info.value.detail)

    # Test with None value
    with pytest.raises(HTTPException) as exc_info:
        await analyze_rule(rule_request, model=None)
    assert exc_info.value.status_code == 422
    assert "Invalid model" in str(exc_info.value.detail)

    # Test with empty string
    with pytest.raises(HTTPException) as exc_info:
        await analyze_rule(rule_request, model="")
    assert exc_info.value.status_code == 422
    assert "Invalid model" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_create_rule_with_build_failure():
    """Test create_rule when build fails."""
    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            raise Exception("Build failed")

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        with pytest.raises(HTTPException) as exc_info:
            await create_rule(rule_request)
        assert exc_info.value.status_code == 400
        assert "Build failed" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_validation_error():
    """Test evaluate_sequence when validation fails."""
    class MockRule:
        def evaluate(self, objects):
            raise ValueError("Validation failed: invalid input")

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return MockRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        evaluate_request = EvaluateRequest(
            objects=[
                ObjectData(name="test", properties={"test": 5})
            ]
        )
        with pytest.raises(HTTPException) as exc_info:
            await evaluate_sequence(rule_request, evaluate_request)
        assert exc_info.value.status_code == 422
        assert "Validation failed: invalid input" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_runtime_error():
    """Test evaluate_sequence when an internal RuntimeError occurs."""
    class BrokenBuilder:
        def add_condition(self, *args):
            raise RuntimeError("Internal runtime error")

        def set_sequence(self, *args):
            return self

        def build(self):
            return self

    with patch("seqrule.api.RuleBuilder", return_value=BrokenBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        evaluate_request = EvaluateRequest(
            objects=[
                ObjectData(name="test", properties={"test": 5})
            ]
        )
        with pytest.raises(HTTPException) as exc_info:
            await evaluate_sequence(rule_request, evaluate_request)
        assert exc_info.value.status_code == 422
        assert "Internal runtime error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_analyze_rule_with_metrics_error():
    """Test analyze_rule when metrics calculation fails."""
    class MockRule:
        def analyze_complexity(self, model):
            raise Exception("Metrics calculation failed")

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return MockRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        response = await analyze_rule(rule_request)
        # Should return default metrics
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics
