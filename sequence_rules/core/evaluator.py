from typing import Any, Dict, List, Optional

from ..dsl.ast import (
    Rule, SimpleRule, ConditionalRule, Sequence,
    Element, Condition, Expression, RelationalOp, LogicalOp, Value,
    NumericValue, BooleanValue, StringValue, PropertyValue,
    Position, AbsolutePosition, RelativePosition
)

def evaluate_expression(expr: Expression, obj: Dict[str, Any], sequence: Optional[List[Dict[str, Any]]] = None, current_pos: int = 0) -> bool:
    """Evaluate a single expression against an object."""
    # Type check to ensure we're dealing with an Expression
    if not isinstance(expr, Expression):
        return False

    # Get the object value based on position
    if expr.position is not None and sequence is not None:
        # Handle positional reference
        if isinstance(expr.position, AbsolutePosition):
            pos = expr.position.index
            
        if pos < 0 or pos >= len(sequence):
            return False
            
        obj = sequence[pos]

    if expr.identifier not in obj:
        return False
    
    obj_value = obj[expr.identifier]

    # Handle property value references
    if isinstance(expr.value, PropertyValue):
        if sequence is None:
            # For property values without position, compare directly
            if expr.value.position is None:
                rule_value = obj[expr.value.identifier]
            else:
                return False
        else:
            # Get the referenced property value
            ref_pos = expr.value.position.index if expr.value.position else current_pos
            if ref_pos < 0 or ref_pos >= len(sequence):
                return False
                
            ref_obj = sequence[ref_pos]
            if expr.value.identifier not in ref_obj:
                return False
                
            rule_value = ref_obj[expr.value.identifier]
        
        # Convert to same type if needed
        try:
            obj_value = float(obj_value)
            rule_value = float(rule_value)
        except (TypeError, ValueError):
            # Not numeric values, compare as strings
            obj_value = str(obj_value)
            rule_value = str(rule_value)
    else:
        rule_value = expr.value
        # Convert rule value to correct type
        if isinstance(rule_value, NumericValue):
            try:
                obj_value = float(obj_value)
                rule_value = rule_value.value
            except (TypeError, ValueError):
                return False
        elif isinstance(rule_value, BooleanValue):
            if not isinstance(obj_value, bool):
                return False
            rule_value = rule_value.value
        elif isinstance(rule_value, StringValue):
            if isinstance(obj_value, StringValue):
                obj_value = obj_value.value
            else:
                obj_value = str(obj_value)
            rule_value = rule_value.value

    # Compare values based on operator
    if expr.operator == RelationalOp.EQ:
        return obj_value == rule_value
    elif expr.operator == RelationalOp.NEQ:
        return obj_value != rule_value
    elif expr.operator == RelationalOp.LT:
        return obj_value < rule_value
    elif expr.operator == RelationalOp.GT:
        return obj_value > rule_value
    elif expr.operator == RelationalOp.LTE:
        return obj_value <= rule_value
    elif expr.operator == RelationalOp.GTE:
        return obj_value >= rule_value
    
    return False

def evaluate_condition(condition: Optional[Condition], obj: Dict[str, Any], sequence: Optional[List[Dict[str, Any]]] = None, current_pos: int = 0) -> bool:
    """Evaluate a condition tree against an object."""
    if condition is None:
        return True

    # Handle nested conditions
    if isinstance(condition.left, Condition):
        result = evaluate_condition(condition.left, obj, sequence, current_pos)
    else:
        result = evaluate_expression(condition.left, obj, sequence, current_pos)
    
    if condition.operator is None or condition.right is None:
        return result
        
    # Handle nested conditions in right branch
    if isinstance(condition.right, Condition):
        right_result = evaluate_condition(condition.right, obj, sequence, current_pos)
    else:
        right_result = evaluate_expression(condition.right, obj, sequence, current_pos)
    
    if condition.operator == LogicalOp.AND:
        return result and right_result
    elif condition.operator == LogicalOp.OR:
        return result or right_result
    
    return False

def evaluate_sequence(rule: Rule, sequence: List[Dict[str, Any]]) -> bool:
    """Evaluate if a sequence of objects satisfies a rule."""
    
    def check_sequence(seq: Sequence, objects: List[Dict[str, Any]]) -> bool:
        # For each element in the sequence rule
        for i, element in enumerate(seq.elements):
            # Handle positional elements
            if element.position is not None:
                if isinstance(element.position, AbsolutePosition):
                    pos = element.position.index
                    
                if pos < 0 or pos >= len(objects):
                    return False
                    
                obj = objects[pos]
                
                # Check if object has the required identifier property
                if element.identifier not in obj.values():
                    return False
                    
                # Check if object matches element constraints
                if not evaluate_condition(element.constraint, obj, objects, pos):
                    return False
            else:
                # For non-positional elements, check sequentially
                found = False
                for j in range(i, len(objects)):
                    obj = objects[j]
                    # Check if any property matches the identifier
                    if element.identifier in obj.values():
                        if evaluate_condition(element.constraint, obj, objects, j):
                            found = True
                            break
                            
                if not found:
                    return False
                
        return True

    if isinstance(rule, SimpleRule):
        return check_sequence(rule.sequence, sequence)
    
    elif isinstance(rule, ConditionalRule):
        # Evaluate condition on first object
        if not sequence:
            return False
            
        if evaluate_condition(rule.condition, sequence[0], sequence, 0):
            return check_sequence(rule.then_sequence, sequence)
        elif rule.else_sequence is not None:
            return check_sequence(rule.else_sequence, sequence)
            
    return False 