"""
# core/constraints.py
"""

from logging import getLogger

logger = getLogger(__name__)


def enforce_constraints(conditions, sequence_constraints):
    """Validate that rule constraints are well-formed.

    Args:
        conditions: List of condition tuples
        sequence_constraints: List of sequence requirements
    Returns:
        Boolean indicating if constraints are valid"""
    logger.debug(
        "Validating constraints - "
        f"Conditions: {conditions}, "
        f"Sequence: {sequence_constraints}"
    )

    if not conditions or not sequence_constraints:
        logger.error("Empty conditions or sequence constraints")
        return False

    # Define valid operators
    valid_operators = {
        "=", "!=", "<", ">", "<=", ">=",
        "in", "not in", "exists", "not exists"
    }

    for _prop, op, value in conditions:
        if op not in valid_operators:
            logger.error(f"Invalid operator found: {op}")
            return False

        # Validate operator-value combinations
        if (
            op in ("in", "not in") and
            not isinstance(value, (list, tuple, set))
        ):
            logger.error(f"Operator {op} requires a collection value")
            return False

        if op in ("exists", "not exists") and value is not None:
            logger.error(f"Operator {op} requires None value")
            return False

    return True
