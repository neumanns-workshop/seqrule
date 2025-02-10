"""Tests to cover missing coverage in API."""

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
async def test_create_rule_internal_error():
    """Test create_rule with an internal server error."""
    class ExplodingBuilder:
        def add_condition(self, *args):
            raise Exception("Boom!")

    with patch("seqrule.api.RuleBuilder", return_value=ExplodingBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        with pytest.raises(HTTPException) as exc_info:
            await create_rule(rule_request)
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_internal_error():
    """Test evaluate_sequence with an internal server error."""
    class ExplodingRule:
        def evaluate(self, objects):
            raise Exception("Boom!")

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return ExplodingRule()

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
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_analyze_rule_with_non_dict_metrics():
    """Test analyze_rule when metrics is not a dictionary."""
    class NonDictMetricsRule:
        def analyze_complexity(self, model):
            return "not a dict"

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return NonDictMetricsRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        response = await analyze_rule(rule_request)
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics


@pytest.mark.asyncio
async def test_analyze_rule_with_invalid_score():
    """Test analyze_rule when complexity_score is not a number."""
    class InvalidScoreRule:
        def analyze_complexity(self, model):
            return {"complexity_score": "not a number"}

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return InvalidScoreRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        response = await analyze_rule(rule_request)
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics


@pytest.mark.asyncio
async def test_analyze_rule_with_invalid_metrics():
    """Test analyze_rule when metrics values are not numbers."""
    class InvalidMetricsRule:
        def analyze_complexity(self, model):
            return {
                "complexity_score": 1.0,
                "metric1": "not a number",
                "metric2": {"also": "not a number"}
            }

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return InvalidMetricsRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        rule_request = RuleRequest(
            conditions=[
                Condition(property_name="test", operator="=", value=5)
            ],
            sequence=["test"]
        )
        response = await analyze_rule(rule_request)
        assert response.score == 1.0  # Valid score should be kept
        assert "metric1" in response.metrics
        assert response.metrics["metric1"] == 0.0  # Invalid metrics should be 0.0
        assert "metric2" in response.metrics
        assert response.metrics["metric2"] == 0.0


@pytest.mark.asyncio
async def test_evaluate_sequence_with_none_result():
    """Test evaluate_sequence when rule.evaluate returns None."""
    class NoneResultRule:
        def evaluate(self, objects):
            return None

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return NoneResultRule()

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
        response = await evaluate_sequence(rule_request, evaluate_request)
        assert response == {"matches": False}


@pytest.mark.asyncio
async def test_evaluate_sequence_with_object_creation_error():
    """Test evaluate_sequence when Object creation fails."""
    class BrokenObject:
        def __init__(self, *args, **kwargs):
            raise TypeError("Cannot create object")

    with patch("seqrule.api.Object", BrokenObject):
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
        assert "Cannot create object" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_build_error():
    """Test evaluate_sequence when rule build fails."""
    class FailingBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            raise ValueError("Cannot build rule")

    with patch("seqrule.api.RuleBuilder", return_value=FailingBuilder()):
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
        assert "Cannot build rule" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_invalid_references():
    """Test evaluate_sequence with invalid references in conditions."""
    rule_request = RuleRequest(
        conditions=[
            Condition(
                property_name="test",
                operator="=",
                value={"$ref": "invalid"}
            )
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
    assert "Invalid condition" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_evaluate_sequence_with_sequence_mismatch():
    """Test evaluate_sequence with sequence order mismatch."""
    rule_request = RuleRequest(
        conditions=[
            Condition(property_name="test", operator="=", value=5)
        ],
        sequence=["test1", "test2"]
    )
    evaluate_request = EvaluateRequest(
        objects=[
            ObjectData(name="test2", properties={"test": 5}),
            ObjectData(name="test1", properties={"test": 5})
        ]
    )
    with pytest.raises(HTTPException) as exc_info:
        await evaluate_sequence(rule_request, evaluate_request)
    assert exc_info.value.status_code == 422
    assert "Sequence order mismatch" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_exploding_rule_evaluation():
    """Test handling of rules that raise exceptions during evaluation."""
    class ExplodingRule:
        def evaluate(self, objects):
            raise Exception("Boom!")

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return ExplodingRule()

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
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_non_dict_metrics():
    """Test handling of non-dictionary metrics from analyze_complexity."""
    class NonDictMetricsRule:
        def analyze_complexity(self):
            return "not a dict"

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return NonDictMetricsRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        response = await analyze_rule(
            RuleRequest(
                conditions=[
                    Condition(property_name="test", operator="=", value=5)
                ],
                sequence=["test"]
            )
        )
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics


@pytest.mark.asyncio
async def test_invalid_score():
    """Test handling of invalid complexity scores."""
    class InvalidScoreRule:
        def analyze_complexity(self):
            return {"complexity_score": "not a number"}

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return InvalidScoreRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        response = await analyze_rule(
            RuleRequest(
                conditions=[
                    Condition(property_name="test", operator="=", value=5)
                ],
                sequence=["test"]
            )
        )
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics


@pytest.mark.asyncio
async def test_invalid_metrics():
    """Test handling of invalid metrics structure."""
    class InvalidMetricsRule:
        def analyze_complexity(self):
            return {"invalid_key": "value"}

        def build(self):
            return self

    class MockBuilder:
        def add_condition(self, *args):
            return self

        def set_sequence(self, *args):
            return self

        def build(self):
            return InvalidMetricsRule()

    with patch("seqrule.api.RuleBuilder", return_value=MockBuilder()):
        response = await analyze_rule(
            RuleRequest(
                conditions=[
                    Condition(property_name="test", operator="=", value=5)
                ],
                sequence=["test"]
            )
        )
        assert response.score == 0.0
        assert "condition_count" in response.metrics
        assert "sequence_length" in response.metrics
