import pytest
from sequence_rules.dsl.parser import parse_rule
from sequence_rules.core.evaluator import evaluate_sequence, evaluate_expression, evaluate_condition
from sequence_rules.dsl.ast import (
    Expression, RelationalOp, NumericValue, StringValue, BooleanValue,
    Condition, LogicalOp, PropertyValue, AbsolutePosition
)


class TestExpressionEvaluation:
    def test_numeric_comparisons(self):
        expr = Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        assert evaluate_expression(expr, {"rank": 7})
        assert evaluate_expression(expr, {"rank": 7.0})
        assert not evaluate_expression(expr, {"rank": 8})
        
        # Test string that can be converted to number
        assert evaluate_expression(expr, {"rank": "7"})
        
        # Test invalid numeric conversions
        assert not evaluate_expression(expr, {"rank": "seven"})
        assert not evaluate_expression(expr, {"rank": None})
        assert not evaluate_expression(expr, {"rank": True})

    def test_string_comparisons(self):
        expr = Expression("suit", None, RelationalOp.EQ, StringValue("heart"))
        assert evaluate_expression(expr, {"suit": "heart"})
        assert not evaluate_expression(expr, {"suit": "spade"})
        
        # Test non-string values
        assert evaluate_expression(expr, {"suit": StringValue("heart")})
        assert not evaluate_expression(expr, {"suit": 42})

    def test_boolean_comparisons(self):
        expr = Expression("is_face", None, RelationalOp.EQ, BooleanValue(True))
        assert evaluate_expression(expr, {"is_face": True})
        assert not evaluate_expression(expr, {"is_face": False})
        
        # Test non-boolean values
        assert not evaluate_expression(expr, {"is_face": "true"})
        assert not evaluate_expression(expr, {"is_face": 1})

    def test_missing_properties(self):
        expr = Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        assert not evaluate_expression(expr, {})
        assert not evaluate_expression(expr, {"suit": "heart"})

    def test_all_operators(self):
        obj = {"value": 7}
        assert evaluate_expression(Expression("value", None, RelationalOp.EQ, NumericValue(7)), obj)
        assert evaluate_expression(Expression("value", None, RelationalOp.NEQ, NumericValue(8)), obj)
        assert evaluate_expression(Expression("value", None, RelationalOp.LT, NumericValue(8)), obj)
        assert evaluate_expression(Expression("value", None, RelationalOp.GT, NumericValue(6)), obj)
        assert evaluate_expression(Expression("value", None, RelationalOp.LTE, NumericValue(7)), obj)
        assert evaluate_expression(Expression("value", None, RelationalOp.GTE, NumericValue(7)), obj)

    def test_property_value_comparisons(self):
        # Test property value with position
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", AbsolutePosition(0))
        )
        sequence = [{"rank": 7}, {"rank": 8}]
        assert not evaluate_expression(expr, sequence[1], sequence, 1)  # 8 != 7
        assert evaluate_expression(expr, sequence[0], sequence, 0)      # 7 == 7

        # Test property value without position
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", None)
        )
        assert evaluate_expression(expr, {"rank": 7}, None, 0)         # 7 == 7


class TestConditionEvaluation:
    def test_simple_condition(self):
        condition = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        )
        assert evaluate_condition(condition, {"rank": 7})
        assert not evaluate_condition(condition, {"rank": 8})

    def test_and_condition(self):
        condition = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7)),
            operator=LogicalOp.AND,
            right=Expression("suit", None, RelationalOp.EQ, StringValue("heart"))
        )
        assert evaluate_condition(condition, {"rank": 7, "suit": "heart"})
        assert not evaluate_condition(condition, {"rank": 7, "suit": "spade"})
        assert not evaluate_condition(condition, {"rank": 8, "suit": "heart"})

    def test_or_condition(self):
        condition = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7)),
            operator=LogicalOp.OR,
            right=Expression("suit", None, RelationalOp.EQ, StringValue("heart"))
        )
        assert evaluate_condition(condition, {"rank": 7, "suit": "spade"})
        assert evaluate_condition(condition, {"rank": 8, "suit": "heart"})
        assert not evaluate_condition(condition, {"rank": 8, "suit": "spade"})

    def test_nested_conditions(self):
        # (rank = 7 and suit = "heart") or value = "ace"
        condition = Condition(
            Condition(
                Expression("rank", None, RelationalOp.EQ, NumericValue(7)),
                operator=LogicalOp.AND,
                right=Expression("suit", None, RelationalOp.EQ, StringValue("heart"))
            ),
            operator=LogicalOp.OR,
            right=Expression("value", None, RelationalOp.EQ, StringValue("ace"))
        )
        assert evaluate_condition(condition, {"rank": 7, "suit": "heart"})
        assert evaluate_condition(condition, {"rank": 1, "value": "ace"})
        assert not evaluate_condition(condition, {"rank": 7, "suit": "spade"})


class TestSequenceEvaluation:
    def test_simple_sequence(self):
        rule = parse_rule("heart -> spade")
        assert evaluate_sequence(rule, [
            {"suit": "heart"},
            {"suit": "spade"}
        ])
        assert not evaluate_sequence(rule, [
            {"suit": "heart"},
            {"suit": "heart"}
        ])

    def test_conditional_sequence(self):
        rule = parse_rule("if rank = 7 then heart -> spade else diamond -> club")
        # Test then branch
        assert evaluate_sequence(rule, [
            {"suit": "heart", "rank": 7},
            {"suit": "spade"}
        ])
        # Test else branch
        assert evaluate_sequence(rule, [
            {"suit": "diamond", "rank": 8},
            {"suit": "club"}
        ])
        # Test invalid sequences
        assert not evaluate_sequence(rule, [
            {"suit": "heart", "rank": 8},
            {"suit": "spade"}
        ])

    def test_constrained_elements(self):
        rule = parse_rule("heart(rank = 7) -> spade(rank > 7)")
        assert evaluate_sequence(rule, [
            {"suit": "heart", "rank": 7},
            {"suit": "spade", "rank": 8}
        ])
        assert not evaluate_sequence(rule, [
            {"suit": "heart", "rank": 7},
            {"suit": "spade", "rank": 6}
        ])

    def test_absolute_positions(self):
        rule = parse_rule("ace@0 king@2 queen@3")
        assert evaluate_sequence(rule, [
            {"value": "ace"},
            {"value": "jack"},
            {"value": "king"},
            {"value": "queen"}
        ])
        assert not evaluate_sequence(rule, [
            {"value": "ace"},
            {"value": "king"},
            {"value": "queen"}
        ])

    def test_position_references(self):
        rule = parse_rule("if rank@0 > rank@1 then ace")
        assert evaluate_sequence(rule, [
            {"rank": 8},
            {"rank": 7},
            {"value": "ace"}
        ])
        assert not evaluate_sequence(rule, [
            {"rank": 7},
            {"rank": 8},
            {"value": "ace"}
        ])
