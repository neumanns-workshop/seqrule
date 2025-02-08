import pytest

from sequence_rules.dsl.ast import (
    AbsolutePosition,
    ConditionalRule,
    LogicalOp,
    NumericValue,
    RelationalOp,
    SimpleRule,
)
from sequence_rules.dsl.parser import RuleParseError, parse_rule


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
        with pytest.raises(RuleParseError):
            parse_rule("invalid -> -> rule")

    def test_empty_rule(self):
        with pytest.raises(RuleParseError):
            parse_rule("")

    def test_incomplete_conditional(self):
        with pytest.raises(RuleParseError):
            parse_rule("if rank = 7 then")

    def test_invalid_position(self):
        with pytest.raises(RuleParseError):
            parse_rule("ace@invalid")

    def test_unclosed_parentheses(self):
        with pytest.raises(RuleParseError):
            parse_rule("heart(rank = 7 -> spade")


class TestValidation:
    def test_invalid_absolute_position(self):
        with pytest.raises(RuleParseError):
            parse_rule("ace@-1")
            
    def test_unclosed_string(self):
        with pytest.raises(RuleParseError):
            parse_rule("if suit = \"heart then ace")


class TestErrorHandling:
    def test_lexer_errors(self):
        # Test unterminated string
        with pytest.raises(RuleParseError):
            parse_rule('if suit = "heart then ace')

        # Test invalid character
        with pytest.raises(RuleParseError):
            parse_rule('if suit = #heart then ace')

        # Test empty rule
        with pytest.raises(RuleParseError):
            parse_rule('')
        with pytest.raises(RuleParseError):
            parse_rule('   ')

    def test_parser_errors(self):
        # Test missing then clause
        with pytest.raises(RuleParseError):
            parse_rule('if rank = 7')

        # Test missing condition
        with pytest.raises(RuleParseError):
            parse_rule('if then heart')

        # Test invalid operator
        with pytest.raises(RuleParseError):
            parse_rule('if rank === 7 then heart')

        # Test unclosed parentheses
        with pytest.raises(RuleParseError):
            parse_rule('heart(rank = 7 -> spade')

        # Test invalid position
        with pytest.raises(RuleParseError):
            parse_rule('ace@-1')
        with pytest.raises(RuleParseError):
            parse_rule('ace@abc')

    def test_semantic_errors(self):
        # Test invalid absolute position
        with pytest.raises(RuleParseError):
            parse_rule('if rank@-1 = 7 then ace')

        # Test invalid property reference
        with pytest.raises(RuleParseError):
            parse_rule('if rank = rank@-1 then ace')

        # Test invalid sequence position
        with pytest.raises(RuleParseError):
            parse_rule('ace@-1 -> king')

    def test_error_context(self):
        # Test line and column information
        try:
            parse_rule('if rank = "seven\nthen ace')
        except RuleParseError as e:
            assert e.line == 1
            assert e.column >= 0
            assert "Unterminated string" in str(e)

        # Test error message improvement
        with pytest.raises(RuleParseError):
            parse_rule('if rank = $ then ace')

        with pytest.raises(RuleParseError):
            parse_rule('if rank = 7 then')

    def test_complex_error_cases(self):
        # Test nested condition errors
        with pytest.raises(RuleParseError):
            parse_rule('if (rank = 7 and suit = "heart" then ace')

        # Test multiple errors (should catch first one)
        with pytest.raises(RuleParseError):
            parse_rule('if suit = "heart and rank = "spade then ace')

        # Test invalid sequence combinations
        with pytest.raises(RuleParseError):
            parse_rule('heart -> -> spade')
        with pytest.raises(RuleParseError):
            parse_rule('heart, -> spade')

    def test_error_listener_customization(self):
        # Test token recognition errors
        with pytest.raises(RuleParseError):
            parse_rule('if suit = "heart then ace')  # Changed to an unterminated string error

        # Test no viable alternative
        with pytest.raises(RuleParseError):
            parse_rule('if rank = then ace')

        # Test missing token
        with pytest.raises(RuleParseError):
            parse_rule('if rank = 7 ace')  # Missing 'then'

        # Test extraneous input
        with pytest.raises(RuleParseError):
            parse_rule('if heart spade diamond')  # Changed to a simpler invalid input

        # Test mismatched input
        with pytest.raises(RuleParseError):
            parse_rule('if rank = "7" = then ace') 