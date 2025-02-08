# Generated from SequenceRule.g4 by ANTLR 4.13.2
from antlr4.tree.Tree import ParseTreeVisitor

if "." in __name__:
    from .SequenceRuleParser import SequenceRuleParser
else:
    from SequenceRuleParser import SequenceRuleParser

# This class defines a complete generic visitor for a parse tree produced by SequenceRuleParser.

class SequenceRuleVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SequenceRuleParser#SimpleRule.
    def visitSimpleRule(self, ctx:SequenceRuleParser.SimpleRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#ConditionalRule.
    def visitConditionalRule(self, ctx:SequenceRuleParser.ConditionalRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#CommaSequence.
    def visitCommaSequence(self, ctx:SequenceRuleParser.CommaSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#ArrowSequence.
    def visitArrowSequence(self, ctx:SequenceRuleParser.ArrowSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#SpaceSequence.
    def visitSpaceSequence(self, ctx:SequenceRuleParser.SpaceSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#SimpleElement.
    def visitSimpleElement(self, ctx:SequenceRuleParser.SimpleElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#ConstrainedElement.
    def visitConstrainedElement(self, ctx:SequenceRuleParser.ConstrainedElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#PosElement.
    def visitPosElement(self, ctx:SequenceRuleParser.PosElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#SignedNumber.
    def visitSignedNumber(self, ctx:SequenceRuleParser.SignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#SingleCondition.
    def visitSingleCondition(self, ctx:SequenceRuleParser.SingleConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#ParenCondition.
    def visitParenCondition(self, ctx:SequenceRuleParser.ParenConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#OrCondition.
    def visitOrCondition(self, ctx:SequenceRuleParser.OrConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#AndCondition.
    def visitAndCondition(self, ctx:SequenceRuleParser.AndConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#ComparisonExpression.
    def visitComparisonExpression(self, ctx:SequenceRuleParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#property.
    def visitProperty(self, ctx:SequenceRuleParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#relOp.
    def visitRelOp(self, ctx:SequenceRuleParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#NumericValue.
    def visitNumericValue(self, ctx:SequenceRuleParser.NumericValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#BooleanValue.
    def visitBooleanValue(self, ctx:SequenceRuleParser.BooleanValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#StringValue.
    def visitStringValue(self, ctx:SequenceRuleParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SequenceRuleParser#PropertyValue.
    def visitPropertyValue(self, ctx:SequenceRuleParser.PropertyValueContext):
        return self.visitChildren(ctx)



del SequenceRuleParser