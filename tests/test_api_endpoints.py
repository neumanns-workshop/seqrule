"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from seqrule.api import (
    Condition,
    EvaluateRequest,
    ObjectData,
    RuleRequest,
    app,
)

client = TestClient(app)


@pytest.fixture
def sample_rule_request():
    """Returns a sample rule request."""
    return RuleRequest(
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


@pytest.fixture
def sample_evaluate_request():
    """Returns a sample sequence evaluation request."""
    return EvaluateRequest(
        objects=[
            ObjectData(name="ace", properties={"rank": 14, "suit": "hearts"}),
            ObjectData(name="king", properties={"rank": 13, "suit": "spades"})
        ]
    )


def test_create_rule(sample_rule_request):
    """Test rule creation endpoint."""
    response = client.post("/rules", json=sample_rule_request.model_dump(mode='json'))
    assert response.status_code == 200
    assert response.json() == {"status": "Rule created successfully"}


def test_evaluate_sequence(sample_rule_request, sample_evaluate_request):
    """Test sequence evaluation endpoint."""
    response = client.post(
        "/rules/evaluate",
        json={
            "rule_request": sample_rule_request.model_dump(mode='json'),
            "evaluate_request": sample_evaluate_request.model_dump(mode='json')
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert isinstance(data["matches"], bool)
    assert data["matches"] is True  # Valid sequence should match


def test_analyze_rule(sample_rule_request):
    """Test rule complexity analysis endpoint."""
    response = client.post(
        "/rules/analyze",
        json=sample_rule_request.model_dump(mode='json'),
        params={"model": "weighted"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "score" in data

    # Check specific metrics
    metrics = data["metrics"]
    assert "condition_count" in metrics
    assert metrics["condition_count"] == 2  # Two conditions in sample
    assert "sequence_length" in metrics
    assert metrics["sequence_length"] == 2  # Two items in sequence
    assert "entropy" in metrics
    assert "branching_factor" in metrics
    assert "redundancy" in metrics


def test_analyze_rule_with_different_models(sample_rule_request):
    """Test rule analysis with different complexity models."""
    models = ["weighted", "entropy_based", "normalized", "log_scaled"]

    for model in models:
        response = client.post(
            "/rules/analyze",
            json=sample_rule_request.model_dump(mode='json'),
            params={"model": model}
        )
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "score" in data
        assert all(isinstance(v, float) for v in data["metrics"].values())
        assert isinstance(data["score"], float)


def test_api_documentation():
    """Test API documentation endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert "paths" in response.json()
    assert "/rules" in response.json()["paths"]
    assert "/rules/evaluate" in response.json()["paths"]
    assert "/rules/analyze" in response.json()["paths"]


def test_error_handling():
    """Test various error conditions."""
    # Test missing required fields
    response = client.post("/rules", json={})
    assert response.status_code == 422

    # Test invalid JSON
    response = client.post("/rules", data="invalid json")
    assert response.status_code == 422

    # Test method not allowed
    response = client.get("/rules")
    assert response.status_code == 405
