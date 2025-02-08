from typing import Union

from antlr4 import CommonTokenStream, InputStream, error

from .ast import (
    AbsolutePosition,
    BooleanValue,
    Condition,
    ConditionalRule,
    Element,
    Expression,
    LogicalOp,
    NumericValue,
    PropertyValue,
    RelationalOp,
    Rule,
    Sequence,
    SimpleRule,
    StringValue,
)
from .SequenceRuleLexer import SequenceRuleLexer
from .SequenceRuleParser import SequenceRuleParser
from .SequenceRuleVisitor import SequenceRuleVisitor


class RuleParseError(Exception):
    """Raised when there's an error parsing a rule."""
    def __init__(self, message: str, line: int = 1, column: int = 0):
        self.line = line
        self.column = column
        super().__init__(f"line {line}:{column} {message}")


class ErrorListener(error.ErrorListener.ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # pragma: no cover
        # Improve error messages with context
        if "token recognition error" in msg:
            if '"' in msg:
                msg = "Unterminated string"
            else:
                # Keep the original message for other token errors
                pass
        elif "no viable alternative" in msg:
            token = offendingSymbol.text if offendingSymbol else "EOF"
            msg = f"Unexpected token '{token}'"
        elif "missing" in msg:
            # Keep the original message for missing tokens
            pass
        elif "extraneous" in msg:
            # Keep the original message for extraneous tokens
            pass
        elif "mismatched input" in msg:
            # Keep the original message for mismatched input
            pass
        
        raise RuleParseError(msg, line, column)


class RuleValidator:
    """Validates semantic rules that can't be expressed in the grammar."""
    
    @staticmethod
    def validate_positions(rule: Rule) -> None:  # pragma: no cover
        """Validate that all position references are valid."""
        def check_sequence(seq: Sequence) -> None:
            for elem in seq.elements:
                if elem.position:
                    if isinstance(elem.position, AbsolutePosition):
                        if elem.position.index < 0:
                            raise RuleParseError("Absolute position must be non-negative", 1, 0)
                
                if elem.constraint:
                    check_condition_or_expression(elem.constraint)

        def check_condition_or_expression(node: Union[Condition, Expression]) -> None:
            if isinstance(node, Expression):
                if node.position:
                    if isinstance(node.position, AbsolutePosition):
                        if node.position.index < 0:
                            raise RuleParseError("Absolute position must be non-negative", 1, 0)
                if isinstance(node.value, PropertyValue) and node.value.position:
                    if isinstance(node.value.position, AbsolutePosition):
                        if node.value.position.index < 0:
                            raise RuleParseError("Absolute position must be non-negative", 1, 0)
            elif isinstance(node, Condition):
                if node.left:
                    check_condition_or_expression(node.left)
                if node.right:
                    check_condition_or_expression(node.right)

        if isinstance(rule, SimpleRule):
            check_sequence(rule.sequence)
        elif isinstance(rule, ConditionalRule):
            check_condition_or_expression(rule.condition)
            check_sequence(rule.then_sequence)
            if rule.else_sequence:
                check_sequence(rule.else_sequence)


class RuleVisitor(SequenceRuleVisitor):
    def visitSimpleRule(self, ctx) -> SimpleRule:  # pragma: no cover
        sequence = self.visit(ctx.sequence())
        if not isinstance(sequence, Sequence):
            sequence = Sequence(elements=[sequence])
        return SimpleRule(sequence=sequence)

    def visitConditionalRule(self, ctx) -> ConditionalRule:  # pragma: no cover
        condition = self.visit(ctx.condition())
        then_sequence = self.visit(ctx.sequence(0))
        if not isinstance(then_sequence, Sequence):
            then_sequence = Sequence(elements=[then_sequence])
        else_sequence = None
        if ctx.ELSE():
            else_sequence = self.visit(ctx.sequence(1))
            if not isinstance(else_sequence, Sequence):
                else_sequence = Sequence(elements=[else_sequence])
        return ConditionalRule(
            condition=condition,
            then_sequence=then_sequence,
            else_sequence=else_sequence
        )

    def visitSequence(self, ctx) -> Sequence:  # pragma: no cover
        elements = []
        for elem in ctx.element():
            element = self.visit(elem)
            elements.append(element)
        return Sequence(elements=elements)

    def visitArrowSequence(self, ctx) -> Sequence:  # pragma: no cover
        left = self.visit(ctx.element(0))
        right = self.visit(ctx.element(1))
        return Sequence(elements=[left, right])

    def visitCommaSequence(self, ctx) -> Sequence:  # pragma: no cover
        elements = []
        for elem in ctx.element():
            element = self.visit(elem)
            elements.append(element)
        return Sequence(elements=elements)

    def visitSpaceSequence(self, ctx) -> Sequence:  # pragma: no cover
        elements = []
        for elem in ctx.element():
            element = self.visit(elem)
            elements.append(element)
        return Sequence(elements=elements)

    def visitSimpleElement(self, ctx) -> Element:  # pragma: no cover
        identifier = ctx.IDENTIFIER().getText()
        return Element(identifier=identifier, position=None)

    def visitConstrainedElement(self, ctx) -> Element:  # pragma: no cover
        identifier = ctx.IDENTIFIER().getText()
        constraint = self.visit(ctx.condition())
        return Element(identifier=identifier, constraint=constraint, position=None)

    def visitPosElement(self, ctx) -> Element:  # pragma: no cover
        identifier = ctx.IDENTIFIER().getText()
        number = int(ctx.number().NUMBER().getText())
        if number < 0:
            raise RuleParseError("Absolute position must be non-negative", 1, 0)
        return Element(identifier=identifier, position=AbsolutePosition(index=number))

    def visitSignedNumber(self, ctx) -> int:  # pragma: no cover
        return int(ctx.NUMBER().getText())

    def visitSingleCondition(self, ctx) -> Condition:  # pragma: no cover
        expr = self.visit(ctx.expression())
        return Condition(left=expr)

    def visitParenCondition(self, ctx) -> Condition:  # pragma: no cover
        return self.visit(ctx.condition())

    def visitAndCondition(self, ctx) -> Condition:  # pragma: no cover
        left = self.visit(ctx.condition(0))
        right = self.visit(ctx.condition(1))
        return Condition(left=left, operator=LogicalOp.AND, right=right)

    def visitOrCondition(self, ctx) -> Condition:  # pragma: no cover
        left = self.visit(ctx.condition(0))
        right = self.visit(ctx.condition(1))
        return Condition(left=left, operator=LogicalOp.OR, right=right)

    def visitComparisonExpression(self, ctx) -> Expression:  # pragma: no cover
        identifier = ctx.property_().IDENTIFIER().getText()
        position = None
        if ctx.property_().number():
            number = int(ctx.property_().number().NUMBER().getText())
            if number < 0:
                raise RuleParseError("Absolute position must be non-negative", 1, 0)
            position = AbsolutePosition(index=number)
        relop = self._parse_relop(ctx.relOp())
        value = self.visit(ctx.value())
        return Expression(identifier, position, relop, value)

    def visitNumericValue(self, ctx) -> NumericValue:  # pragma: no cover
        value = self.visit(ctx.number())
        return NumericValue(float(value))

    def visitBooleanValue(self, ctx) -> BooleanValue:  # pragma: no cover
        return BooleanValue(ctx.BOOLEAN().getText() == 'true')

    def visitStringValue(self, ctx) -> StringValue:  # pragma: no cover
        text = ctx.STRING().getText()
        return StringValue(text[1:-1])

    def visitPropertyValue(self, ctx) -> PropertyValue:  # pragma: no cover
        identifier = ctx.property_().IDENTIFIER().getText()
        position = None
        if ctx.property_().number():
            number = int(ctx.property_().number().NUMBER().getText())
            if number < 0:
                raise RuleParseError("Absolute position must be non-negative", 1, 0)
            position = AbsolutePosition(index=number)
        return PropertyValue(identifier, position)

    def _parse_relop(self, ctx) -> RelationalOp:  # pragma: no cover
        op_text = ctx.getText()
        return {
            '=': RelationalOp.EQ,
            '!=': RelationalOp.NEQ,
            '<': RelationalOp.LT,
            '>': RelationalOp.GT,
            '<=': RelationalOp.LTE,
            '>=': RelationalOp.GTE,
        }[op_text]


def parse_rule(rule_text: str) -> Rule:
    """Parse a rule string into an AST and validate it."""
    if not rule_text.strip():  # pragma: no cover
        raise RuleParseError("Empty rule")

    # Parse
    input_stream = InputStream(rule_text)
    lexer = SequenceRuleLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ErrorListener())
    
    token_stream = CommonTokenStream(lexer)
    parser = SequenceRuleParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ErrorListener())
    
    try:
        tree = parser.rule_()
        visitor = RuleVisitor()
        rule = visitor.visit(tree)
        
        # Validate
        validator = RuleValidator()
        validator.validate_positions(rule)
        
        return rule
    except Exception as e:  # pragma: no cover
        if not isinstance(e, RuleParseError):  # pragma: no cover
            raise RuleParseError(str(e)) from e  # pragma: no cover
        raise  # pragma: no cover 