"""FastAPI web service for seqrule."""

from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from . import RuleBuilder
from .objects import Object

app = FastAPI(
    title="seqrule API",
    description=(
        "API for defining and generating rules to validate sequences"
    ),
    version="1.0.0"
)


class Condition(BaseModel):
    """Model for rule conditions."""
    property_name: str = Field(..., min_length=1)
    operator: str = Field(..., min_length=1)
    value: Any

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: str) -> str:
        """Validate operator is one of the supported types."""
        valid_operators = {
            "=", "!=", "<", ">", "<=", ">=",
            "in", "not in", "exists", "not exists"
        }
        if v not in valid_operators:
            raise ValueError(
                f"Invalid operator. Must be one of: {valid_operators}"
            )
        return v

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: Any, info) -> Any:
        """Validate value based on operator type.

        Only validates operator-specific requirements. JSON serialization
        is handled during model dumping.
        """
        operator = info.data.get("operator")
        if operator in ("exists", "not exists") and v is not None:
            raise ValueError(
                f"{operator} operator requires None value"
            )
        return v


class RuleRequest(BaseModel):
    """Model for rule creation requests."""
    conditions: List[Condition] = Field(..., min_items=1)
    sequence: List[str] = Field(..., min_items=1)


class ObjectData(BaseModel):
    """Model for object data."""
    name: str = Field(..., min_length=1)
    properties: Dict[str, Any]

    @field_validator("properties")
    @classmethod
    def validate_properties(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that properties is not empty."""
        if not v:
            raise ValueError("Properties cannot be empty")
        return v


class EvaluateRequest(BaseModel):
    """Model for sequence evaluation requests."""
    objects: List[ObjectData] = Field(..., min_items=1)


class ComplexityResponse(BaseModel):
    """Model for complexity analysis response."""
    metrics: Dict[str, float]
    score: float


def validate_sequence_order(
    expected: List[str],
    actual: List[str]
) -> Tuple[bool, Optional[str]]:
    """Validate that actual sequence matches expected order."""
    if not actual:
        return False, "Empty sequence provided"
    if len(actual) != len(expected):
        return False, (
            f"Sequence length mismatch. Expected {len(expected)}, "
            f"got {len(actual)}"
        )
    if actual != expected:
        return False, (
            f"Sequence order mismatch. Expected {expected}, "
            f"got {actual}"
        )
    return True, None


def has_invalid_references(value: Any) -> Tuple[bool, Optional[str]]:
    """Recursively check for invalid references in a value."""
    if isinstance(value, dict):
        if "$function" in value:
            return True, (
                "Function references are not allowed in condition values"
            )
        if "$ref" in value:
            return True, "Invalid reference in condition value"
        for v in value.values():
            has_invalid, error = has_invalid_references(v)
            if has_invalid:
                return True, error
    elif isinstance(value, (list, tuple)):
        for item in value:
            has_invalid, error = has_invalid_references(item)
            if has_invalid:
                return True, error
    return False, None


@app.post("/rules", response_model=Dict[str, str])
async def create_rule(rule_request: RuleRequest):
    """Create a new rule and return its ID."""
    try:
        # Check for invalid references in condition values
        for condition in rule_request.conditions:
            has_invalid, error = has_invalid_references(condition.value)
            if has_invalid:
                raise ValueError(error)

        builder = RuleBuilder()
        for condition in rule_request.conditions:
            builder.add_condition(
                condition.property_name,
                condition.operator,
                condition.value
            )

        builder.set_sequence(rule_request.sequence)
        try:
            builder.build()  # Just build to validate, no need to store
        except Exception as e:
            raise ValueError(f"Rule build failed: {str(e)}") from e

        return {"status": "Rule created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e


@app.post("/rules/evaluate")
async def evaluate_sequence(
    rule_request: RuleRequest,
    evaluate_request: EvaluateRequest
):
    """Evaluate a sequence against a rule."""
    try:
        # Validate sequence order first
        valid, error = validate_sequence_order(
            rule_request.sequence,
            [obj.name for obj in evaluate_request.objects]
        )
        if not valid:
            raise HTTPException(status_code=422, detail=error)

        # Validate condition values
        for condition in rule_request.conditions:
            has_invalid, error = has_invalid_references(condition.value)
            if has_invalid:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid condition: {error}"
                )

        # Validate object properties - ensure all values are JSON serializable
        for obj in evaluate_request.objects:
            for _key, value in obj.properties.items():
                if not isinstance(value, (str, int, float, bool, type(None))):
                    raise HTTPException(
                        status_code=422,
                        detail=(
                            "Invalid object properties: values must be "
                            "primitive types"
                        )
                    )

        # Build rule
        builder = RuleBuilder()
        for condition in rule_request.conditions:
            try:
                builder.add_condition(
                    condition.property_name,
                    condition.operator,
                    condition.value
                )
            except Exception as e:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid condition: {str(e)}"
                ) from e

        builder.set_sequence(rule_request.sequence)
        try:
            rule = builder.build()
        except Exception as e:
            msg = f"Rule build failed: {str(e)}"
            raise HTTPException(status_code=422, detail=msg) from e

        # Convert request objects to Object instances
        try:
            objects = [
                Object(obj.name, **obj.properties)
                for obj in evaluate_request.objects
            ]
        except (TypeError, ValueError) as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid object properties: {str(e)}"
            ) from e

        # Evaluate
        result = rule.evaluate(objects)
        return {"matches": bool(result)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) from e


@app.post("/rules/analyze", response_model=ComplexityResponse)
async def analyze_rule(rule_request: RuleRequest, model: str = "weighted"):
    """Analyze the complexity of a rule."""
    models = {
        "weighted", "entropy_based", "normalized", "log_scaled"
    }

    # Add type validation
    msg = (
        f"Invalid model. Must be one of: {models}"
    )
    if not isinstance(model, str):
        raise HTTPException(
            status_code=422,
            detail=msg
        )

    if model not in models:
        raise HTTPException(
            status_code=422,
            detail=msg
        )

    def get_default_metrics():
        return ComplexityResponse(
            metrics={
                "condition_count": float(len(rule_request.conditions)),
                "sequence_length": float(len(rule_request.sequence)),
                "entropy": 0.0,
                "branching_factor": 0.0,
                "redundancy": 0.0
            },
            score=0.0
        )

    try:
        # Build rule
        builder = RuleBuilder()
        for condition in rule_request.conditions:
            builder.add_condition(
                condition.property_name,
                condition.operator,
                condition.value
            )
        builder.set_sequence(rule_request.sequence)
        rule = builder.build()

        # Analyze
        try:
            metrics = rule.analyze_complexity(model=model)
            if not isinstance(metrics, dict):
                return get_default_metrics()

            # Extract score and convert metrics to floats
            try:
                score = float(metrics.pop("complexity_score", 0.0))
            except (TypeError, ValueError):
                return get_default_metrics()

            # Convert remaining metrics to floats
            float_metrics = {}
            for key, value in metrics.items():
                try:
                    float_metrics[key] = float(value)
                except (TypeError, ValueError):
                    float_metrics[key] = 0.0

            return ComplexityResponse(metrics=float_metrics, score=score)
        except Exception:  # pragma: no cover
            return get_default_metrics()
    except Exception:  # pragma: no cover
        return get_default_metrics()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
