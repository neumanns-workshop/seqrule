# Generated from SequenceRule.g4 by ANTLR 4.13.2
from antlr4.tree.Tree import ParseTreeListener

if "." in __name__:
    from .SequenceRuleParser import SequenceRuleParser
else:
    from SequenceRuleParser import SequenceRuleParser

# This class defines a complete listener for a parse tree produced by SequenceRuleParser.
class SequenceRuleListener(ParseTreeListener):

    # Enter a parse tree produced by SequenceRuleParser#SimpleRule.
    def enterSimpleRule(self, ctx:SequenceRuleParser.SimpleRuleContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#SimpleRule.
    def exitSimpleRule(self, ctx:SequenceRuleParser.SimpleRuleContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#ConditionalRule.
    def enterConditionalRule(self, ctx:SequenceRuleParser.ConditionalRuleContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#ConditionalRule.
    def exitConditionalRule(self, ctx:SequenceRuleParser.ConditionalRuleContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#CommaSequence.
    def enterCommaSequence(self, ctx:SequenceRuleParser.CommaSequenceContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#CommaSequence.
    def exitCommaSequence(self, ctx:SequenceRuleParser.CommaSequenceContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#ArrowSequence.
    def enterArrowSequence(self, ctx:SequenceRuleParser.ArrowSequenceContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#ArrowSequence.
    def exitArrowSequence(self, ctx:SequenceRuleParser.ArrowSequenceContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#SpaceSequence.
    def enterSpaceSequence(self, ctx:SequenceRuleParser.SpaceSequenceContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#SpaceSequence.
    def exitSpaceSequence(self, ctx:SequenceRuleParser.SpaceSequenceContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#SimpleElement.
    def enterSimpleElement(self, ctx:SequenceRuleParser.SimpleElementContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#SimpleElement.
    def exitSimpleElement(self, ctx:SequenceRuleParser.SimpleElementContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#ConstrainedElement.
    def enterConstrainedElement(self, ctx:SequenceRuleParser.ConstrainedElementContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#ConstrainedElement.
    def exitConstrainedElement(self, ctx:SequenceRuleParser.ConstrainedElementContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#PosElement.
    def enterPosElement(self, ctx:SequenceRuleParser.PosElementContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#PosElement.
    def exitPosElement(self, ctx:SequenceRuleParser.PosElementContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#SignedNumber.
    def enterSignedNumber(self, ctx:SequenceRuleParser.SignedNumberContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#SignedNumber.
    def exitSignedNumber(self, ctx:SequenceRuleParser.SignedNumberContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#SingleCondition.
    def enterSingleCondition(self, ctx:SequenceRuleParser.SingleConditionContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#SingleCondition.
    def exitSingleCondition(self, ctx:SequenceRuleParser.SingleConditionContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#ParenCondition.
    def enterParenCondition(self, ctx:SequenceRuleParser.ParenConditionContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#ParenCondition.
    def exitParenCondition(self, ctx:SequenceRuleParser.ParenConditionContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#OrCondition.
    def enterOrCondition(self, ctx:SequenceRuleParser.OrConditionContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#OrCondition.
    def exitOrCondition(self, ctx:SequenceRuleParser.OrConditionContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#AndCondition.
    def enterAndCondition(self, ctx:SequenceRuleParser.AndConditionContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#AndCondition.
    def exitAndCondition(self, ctx:SequenceRuleParser.AndConditionContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#ComparisonExpression.
    def enterComparisonExpression(self, ctx:SequenceRuleParser.ComparisonExpressionContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#ComparisonExpression.
    def exitComparisonExpression(self, ctx:SequenceRuleParser.ComparisonExpressionContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#property.
    def enterProperty(self, ctx:SequenceRuleParser.PropertyContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#property.
    def exitProperty(self, ctx:SequenceRuleParser.PropertyContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#relOp.
    def enterRelOp(self, ctx:SequenceRuleParser.RelOpContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#relOp.
    def exitRelOp(self, ctx:SequenceRuleParser.RelOpContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#NumericValue.
    def enterNumericValue(self, ctx:SequenceRuleParser.NumericValueContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#NumericValue.
    def exitNumericValue(self, ctx:SequenceRuleParser.NumericValueContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#BooleanValue.
    def enterBooleanValue(self, ctx:SequenceRuleParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#BooleanValue.
    def exitBooleanValue(self, ctx:SequenceRuleParser.BooleanValueContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#StringValue.
    def enterStringValue(self, ctx:SequenceRuleParser.StringValueContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#StringValue.
    def exitStringValue(self, ctx:SequenceRuleParser.StringValueContext):
        pass


    # Enter a parse tree produced by SequenceRuleParser#PropertyValue.
    def enterPropertyValue(self, ctx:SequenceRuleParser.PropertyValueContext):
        pass

    # Exit a parse tree produced by SequenceRuleParser#PropertyValue.
    def exitPropertyValue(self, ctx:SequenceRuleParser.PropertyValueContext):
        pass



del SequenceRuleParser