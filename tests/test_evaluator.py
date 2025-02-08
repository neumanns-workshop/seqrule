from sequence_rules.core.evaluator import (
    evaluate_condition,
    evaluate_expression,
    evaluate_sequence,
)
from sequence_rules.dsl.parser import parse_rule
from sequence_rules.dsl.sequence_ast import (
    AbsolutePosition,
    BooleanValue,
    Condition,
    Element,
    Expression,
    LogicalOp,
    NumericValue,
    Position,
    PropertyValue,
    RelationalOp,
    Rule,
    Sequence,
    SimpleRule,
    StringValue,
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
        assert evaluate_expression(
            Expression("value", None, RelationalOp.EQ, NumericValue(7)), obj
        )
        assert evaluate_expression(
            Expression("value", None, RelationalOp.NEQ, NumericValue(8)), obj
        )
        assert evaluate_expression(
            Expression("value", None, RelationalOp.LT, NumericValue(8)), obj
        )
        assert evaluate_expression(
            Expression("value", None, RelationalOp.GT, NumericValue(6)), obj
        )
        assert evaluate_expression(
            Expression("value", None, RelationalOp.LTE, NumericValue(7)), obj
        )
        assert evaluate_expression(
            Expression("value", None, RelationalOp.GTE, NumericValue(7)), obj
        )

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

    def test_invalid_expression_type(self):
        # Test with non-Expression type
        assert not evaluate_expression(None, {})
        assert not evaluate_expression(42, {})
        assert not evaluate_expression("not an expression", {})

    def test_property_value_edge_cases(self):
        # Test property value without sequence
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", AbsolutePosition(0))
        )
        assert not evaluate_expression(expr, {"rank": 7})

        # Test property value with invalid position
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", AbsolutePosition(99))
        )
        sequence = [{"rank": 7}, {"rank": 8}]
        assert not evaluate_expression(expr, sequence[0], sequence, 0)

        # Test property value with missing property
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("missing", None)
        )
        assert not evaluate_expression(expr, {"rank": 7}, None, 0)

    def test_type_conversion_edge_cases(self):
        # Test invalid numeric conversion
        expr = Expression("value", None, RelationalOp.EQ, NumericValue(7))
        assert not evaluate_expression(expr, {"value": "not a number"})
        assert not evaluate_expression(expr, {"value": None})
        assert not evaluate_expression(expr, {"value": True})

        # Test invalid boolean conversion
        expr = Expression("value", None, RelationalOp.EQ, BooleanValue(True))
        assert not evaluate_expression(expr, {"value": 1})
        assert not evaluate_expression(expr, {"value": "true"})

    def test_position_edge_cases(self):
        # Test with base Position class (should never happen in practice)
        class UnknownPosition(Position):
            pass
        
        expr = Expression("rank", UnknownPosition(), RelationalOp.EQ, NumericValue(7))
        assert not evaluate_expression(expr, {"rank": 7}, [{"rank": 7}], 0)

    def test_property_value_type_conversion(self):
        # Test numeric conversion failure with different types
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", None)
        )
        # Test when both values are non-numeric strings
        obj = {"rank": "ace"}
        assert evaluate_expression(expr, obj, None, 0)  # String comparison
        
        # Test when one value is numeric and other isn't
        obj = {"rank": "ace"}
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("value", None)
        )
        sequence = [{"value": 7}]
        assert not evaluate_expression(expr, obj, sequence, 0)

        # Test property value with invalid position
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", AbsolutePosition(99))
        )
        sequence = [{"rank": 7}]
        assert not evaluate_expression(expr, {"rank": 7}, sequence, 0)

        # Test property value with missing property in sequence
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("missing", AbsolutePosition(0))
        )
        sequence = [{"rank": 7}]
        assert not evaluate_expression(expr, {"rank": 7}, sequence, 0)

        # Test property value with position but no sequence
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", AbsolutePosition(0))
        )
        assert not evaluate_expression(expr, {"rank": 7})

        # Test property value with numeric conversion
        expr = Expression(
            "rank", None, RelationalOp.EQ,
            PropertyValue("rank", None)
        )
        obj = {"rank": "7"}
        assert evaluate_expression(expr, obj, None, 0)

        # Test property value with failed numeric conversion
        expr = Expression(
            "rank", None, RelationalOp.GT,
            PropertyValue("rank", None)
        )
        obj = {"rank": "ace"}  # Can't convert to number for comparison
        assert not evaluate_expression(expr, obj, None, 0)


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

    def test_condition_edge_cases(self):
        # Test empty condition
        assert evaluate_condition(None, {})
        
        # Test condition with no operator
        condition = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        )
        assert evaluate_condition(condition, {"rank": 7})
        
        # Test nested condition with no operator
        nested = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        )
        condition = Condition(nested)
        assert evaluate_condition(condition, {"rank": 7})

        # Test nested condition in right branch
        nested = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        )
        condition = Condition(
            Expression("suit", None, RelationalOp.EQ, StringValue("heart")),
            operator=LogicalOp.AND,
            right=nested
        )
        assert evaluate_condition(condition, {"rank": 7, "suit": "heart"})

        # Test condition with unknown operator
        condition = Condition(
            Expression("rank", None, RelationalOp.EQ, NumericValue(7)),
            operator="UNKNOWN",
            right=Expression("suit", None, RelationalOp.EQ, StringValue("heart"))
        )
        assert not evaluate_condition(condition, {"rank": 7, "suit": "heart"})

        # Test condition with no left expression
        condition = Condition(
            None,
            operator=LogicalOp.AND,
            right=Expression("rank", None, RelationalOp.EQ, NumericValue(7))
        )
        assert not evaluate_condition(condition, {"rank": 7})


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

    def test_empty_sequence(self):
        # Test conditional rule with empty sequence
        rule = parse_rule("if rank = 7 then heart -> spade")
        assert not evaluate_sequence(rule, [])

    def test_invalid_positions(self):
        # Test absolute position out of bounds
        rule = parse_rule("ace@99")
        assert not evaluate_sequence(rule, [{"value": "ace"}])

        # Test position with missing identifier
        rule = parse_rule("ace@0")
        assert not evaluate_sequence(rule, [{"value": "king"}])

    def test_sequential_search_failure(self):
        # Test when sequential search fails to find element
        rule = parse_rule("heart spade")
        assert not evaluate_sequence(rule, [{"suit": "diamond"}, {"suit": "club"}])

        # Test when constraint fails in sequential search
        rule = parse_rule("heart(rank = 7) spade")
        assert not evaluate_sequence(rule, [
            {"suit": "heart", "rank": 6},
            {"suit": "spade"}
        ])

    def test_sequence_edge_cases(self):
        # Test unknown rule type
        class UnknownRule(Rule):
            pass
        assert not evaluate_sequence(UnknownRule(), [{"rank": 7}])

        # Test conditional rule with empty sequence
        rule = parse_rule("if rank = 7 then heart else spade")
        assert not evaluate_sequence(rule, [])

        # Test conditional rule with non-matching condition and no else branch
        rule = parse_rule("if rank = 7 then heart")
        assert not evaluate_sequence(rule, [{"rank": 8}])

        # Test conditional rule with non-matching condition and else branch
        rule = parse_rule("if rank = 7 then heart else spade")
        sequence = [{"rank": 8, "suit": "club"}]  # Neither heart nor spade
        assert not evaluate_sequence(rule, sequence)

        # Test absolute position out of bounds
        rule = parse_rule("ace@99")
        assert not evaluate_sequence(rule, [{"value": "ace"}])

        # Test sequential search with no matches
        rule = parse_rule("heart spade")
        assert not evaluate_sequence(rule, [{"suit": "diamond"}, {"suit": "club"}])

        # Test sequential search with constraint failure
        rule = parse_rule("heart(rank = 7) spade")
        assert not evaluate_sequence(rule, [
            {"suit": "heart", "rank": 6},
            {"suit": "spade"}
        ])

        # Test conditional rule with matching condition but failing sequence
        rule = parse_rule("if rank = 7 then heart spade")
        sequence = [{"rank": 7, "suit": "diamond"}]
        assert not evaluate_sequence(rule, sequence)

        # Test conditional rule with non-matching condition and failing else sequence
        rule = parse_rule("if rank = 7 then heart else spade")
        sequence = [{"rank": 8, "suit": "diamond"}]
        assert not evaluate_sequence(rule, sequence)

        # Test positional element with missing identifier
        rule = parse_rule("ace@0")
        sequence = [{"rank": 7}]  # Missing "ace" value
        assert not evaluate_sequence(rule, sequence)

        # Test positional element with constraint failure
        element = Element(
            identifier="ace",
            position=AbsolutePosition(0),
            constraint=Condition(
                left=Expression("rank", None, RelationalOp.EQ, NumericValue(7))
            )
        )
        rule = SimpleRule(sequence=Sequence(elements=[element]))
        sequence = [{"value": "ace", "rank": 6}]  # Wrong rank value
        assert not evaluate_sequence(rule, sequence)
