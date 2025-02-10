# core/generators.py

import logging

logger = logging.getLogger(__name__)

def sequence_rule_generator(conditions, sequence_constraints, verbose=False):
    """
    Generates a function representing a valid sequence rule.

    :param conditions: A list of conditions [(property, operator, value), ...]
    :param sequence_constraints: An ordered list of required objects
    :param verbose: Boolean flag to enable detailed condition checking logs
    :return: A function that enforces the sequence rule
    """
    logger.info(f"Generating rule with conditions: {conditions}")
    logger.info(f"Sequence constraints: {sequence_constraints}")

    def rule_function(sequence):
        """
        Enforces the generated rule on a given sequence.

        :param sequence: The input sequence of objects
        :return: Boolean indicating rule satisfaction
        """
        # Handle empty sequences
        if not sequence and not sequence_constraints:
            logger.warning("Empty sequence and constraints provided")
            return False

        sequence_names = [obj.name for obj in sequence]
        logger.debug(f"Checking sequence order: {sequence_names}")

        # ✅ Enforce strict sequence order
        if sequence_names != sequence_constraints:
            logger.warning(
                f"Sequence order mismatch. Expected: {sequence_constraints}, "
                f"Got: {sequence_names}"
            )
            return False

        # ✅ Check object conditions
        for i, obj in enumerate(sequence):
            logger.debug(f"Checking conditions for object: {obj.name}")
            failed_conditions = []

            for prop, op, value in conditions:
                # Get the current object's value
                if not obj.has_property(prop) and value is None:
                    obj_value = None
                else:
                    obj_value = obj.get(prop)
                    if obj_value is None and value is not None:
                        logger.error(f"Property {prop} not found in object {obj.name}")
                        return False

                # Handle sequence-based conditions
                if callable(op):
                    # For custom predicates, pass the current object and sequence context
                    context = {
                        'prev': sequence[i-1] if i > 0 else None,
                        'next': sequence[i+1] if i < len(sequence)-1 else None,
                        'index': i,
                        'sequence': sequence
                    }
                    try:
                        comparison = op(obj, context)
                    except Exception as e:
                        logger.error(f"Error applying custom comparison function: {e}")
                        return False
                else:
                    # Handle standard operators
                    comparison = _compare(obj_value, op, value)

                if comparison:
                    if verbose:  # ✅ Only log successful checks if verbose is enabled
                        logger.debug(f"Condition passed: {obj_value} {op} {value}")
                else:
                    failed_conditions.append(f"{obj.name}: {obj_value} {op} {value}")

            if failed_conditions:
                logger.warning(
                    f"Conditions failed on {obj.name}: {', '.join(failed_conditions)}"
                )
                return False  # One or more conditions failed

        logger.info(f"All conditions satisfied for sequence: {sequence_names}")
        return True

    return rule_function

def _compare(obj_value, operator, value):
    """Applies a logical operator comparison, supporting extended conditions."""
    logger.debug(f"Comparing values: {obj_value} {operator} {value}")

    # Handle None values
    if obj_value is None or value is None:
        if operator == "=":
            return obj_value is value
        elif operator == "!=":
            return obj_value is not value
        elif operator == "exists":
            return obj_value is not None
        elif operator == "not exists":
            return obj_value is None
        else:
            logger.warning(f"Cannot apply operator {operator} to None values")
            return False

    # Handle collection membership
    if operator == "in":
        return obj_value in value
    elif operator == "not in":
        return obj_value not in value

    # ✅ Standard operator comparison
    ops = {
        "=": obj_value == value,
        "!=": obj_value != value,
        "<": obj_value < value,
        ">": obj_value > value,
        "<=": obj_value <= value,
        ">=": obj_value >= value,
        "exists": True,  # If we got here, the value exists
        "not exists": False  # If we got here, the value exists
    }
    result = ops.get(operator, False)

    logger.debug(f"Comparison result: {result}")
    return result
