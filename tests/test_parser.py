import pytest
from sequence_rules.dsl.parser import parse_rule, RuleParseError
from sequence_rules.dsl.ast import (
    Rule, SimpleRule, ConditionalRule, Sequence, Element,
    Condition, Expression, RelationalOp, LogicalOp,
    NumericValue, StringValue, BooleanValue,
    AbsolutePosition
)


class TestBasicRules:
    def test_simple_sequence(self):
        rule = parse_rule("heart -> spade")
        
        assert isinstance(rule, SimpleRule)
        assert len(rule.sequence.elements) == 2
        assert rule.sequence.elements[0].identifier == "heart"
        assert rule.sequence.elements[1].identifier == "spade"
        assert rule.sequence.elements[0].constraint is None
        assert rule.sequence.elements[1].constraint is None

    def test_constrained_element(self):
        rule = parse_rule("heart(rank = 7) -> spade")
        
        assert isinstance(rule, SimpleRule)
        element = rule.sequence.elements[0]
        assert element.identifier == "heart"
        assert element.constraint is not None
        assert element.constraint.left.identifier == "rank"
        assert element.constraint.left.operator == RelationalOp.EQ
        assert isinstance(element.constraint.left.value, NumericValue)
        assert element.constraint.left.value.value == 7

    def test_multiple_constraints(self):
        rule = parse_rule("heart(rank = 7 and suit = \"heart\") -> spade")
        
        assert isinstance(rule, SimpleRule)
        condition = rule.sequence.elements[0].constraint
        assert condition.operator == LogicalOp.AND
        assert condition.left.left.identifier == "rank"
        assert condition.right.left.identifier == "suit"


class TestConditionalRules:
    def test_simple_conditional(self):
        rule = parse_rule("if rank = 7 then heart -> spade")
        
        assert isinstance(rule, ConditionalRule)
        assert rule.condition.left.identifier == "rank"
        assert rule.condition.left.value.value == 7
        assert len(rule.then_sequence.elements) == 2
        assert rule.else_sequence is None

    def test_conditional_with_else(self):
        rule = parse_rule("if rank = 7 then heart -> spade else diamond -> club")
        
        assert isinstance(rule, ConditionalRule)
        assert len(rule.then_sequence.elements) == 2
        assert len(rule.else_sequence.elements) == 2
        assert rule.else_sequence.elements[0].identifier == "diamond"
        assert rule.else_sequence.elements[1].identifier == "club"

    def test_complex_condition(self):
        rule = parse_rule("if rank = 7 and suit = \"heart\" then ace -> king")
        
        assert isinstance(rule, ConditionalRule)
        assert rule.condition.operator == LogicalOp.AND
        assert rule.condition.left.left.identifier == "rank"
        assert rule.condition.right.left.identifier == "suit"


class TestPositionalRules:
    def test_absolute_position(self):
        rule = parse_rule("ace@0 king@2")
        
        assert isinstance(rule, SimpleRule)
        assert rule.sequence.elements[0].position is not None
        assert isinstance(rule.sequence.elements[0].position, AbsolutePosition)
        assert rule.sequence.elements[0].position.index == 0
        assert rule.sequence.elements[1].position.index == 2

    def test_position_in_condition(self):
        rule = parse_rule("if rank@0 = 7 then heart")
        
        assert isinstance(rule, ConditionalRule)
        assert rule.condition.left.position is not None
        assert isinstance(rule.condition.left.position, AbsolutePosition)
        assert rule.condition.left.position.index == 0


class TestErrorCases:
    def test_invalid_syntax(self):
        with pytest.raises(Exception):
            parse_rule("invalid -> -> rule")

    def test_empty_rule(self):
        with pytest.raises(Exception):
            parse_rule("")

    def test_incomplete_conditional(self):
        with pytest.raises(Exception):
            parse_rule("if rank = 7 then")

    def test_invalid_position(self):
        with pytest.raises(Exception):
            parse_rule("ace@invalid")

    def test_unclosed_parentheses(self):
        with pytest.raises(Exception):
            parse_rule("heart(rank = 7 -> spade")


class TestAdvancedRules:
    def test_nested_conditions(self):
        rule = parse_rule("if (rank = 7 and suit = \"heart\") or value = \"ace\" then king")
        assert isinstance(rule, ConditionalRule)
        
    def test_complex_positions(self):
        rule = parse_rule("ace@0 king@2 queen@3")
        assert isinstance(rule, SimpleRule)
        assert len(rule.sequence.elements) == 3
        
    def test_mixed_positions(self):
        rule = parse_rule("if rank@0 > rank@1 then ace")
        assert isinstance(rule, ConditionalRule)


class TestValidation:
    def test_invalid_absolute_position(self):
        with pytest.raises(RuleParseError, match="token recognition error at: '-1'"):
            parse_rule("ace@-1")
            
    def test_unclosed_string(self):
        with pytest.raises(RuleParseError, match="Unterminated string"):
            parse_rule("if suit = \"heart then ace") 