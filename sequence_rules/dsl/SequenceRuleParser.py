# Generated from SequenceRule.g4 by ANTLR 4.13.2
# encoding: utf-8
import sys

from antlr4 import (
	ATN,
	DFA,
	ATNDeserializer,
	NoViableAltException,
	Parser,
	ParserATNSimulator,
	ParserRuleContext,
	PredictionContextCache,
	RecognitionException,
	Token,
	TokenStream,
)
from antlr4.tree.Tree import ParseTreeListener, ParseTreeVisitor

if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

if "." in __name__:
    pass
else:
    pass

def serializedATN():
    return [
        4,1,21,100,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,26,8,0,3,0,28,
        8,0,1,1,1,1,1,1,5,1,33,8,1,10,1,12,1,36,9,1,1,1,1,1,1,1,1,1,1,1,
        1,1,5,1,44,8,1,10,1,12,1,47,9,1,3,1,49,8,1,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,3,2,60,8,2,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,70,8,4,1,
        4,1,4,1,4,1,4,1,4,5,4,78,8,4,10,4,12,4,81,9,4,1,5,1,5,1,5,1,5,1,
        6,1,6,1,6,3,6,90,8,6,1,7,1,7,1,8,1,8,1,8,1,8,3,8,98,8,8,1,8,0,1,8,9,
        0,2,4,6,8,10,12,14,16,0,1,1,0,14,19,105,0,27,1,0,0,0,2,48,1,0,0,0,
        4,59,1,0,0,0,6,61,1,0,0,0,8,69,1,0,0,0,10,82,1,0,0,0,12,86,1,0,0,0,
        14,91,1,0,0,0,16,97,1,0,0,0,18,28,3,2,1,0,19,20,5,3,0,0,20,21,3,8,4,0,
        21,22,5,4,0,0,22,25,3,2,1,0,23,24,5,5,0,0,24,26,3,2,1,0,25,23,1,0,0,0,
        25,26,1,0,0,0,26,28,1,0,0,0,27,18,1,0,0,0,27,19,1,0,0,0,28,1,1,0,0,0,
        29,34,3,4,2,0,30,31,5,2,0,0,31,33,3,4,2,0,32,30,1,0,0,0,33,36,1,0,0,0,
        34,32,1,0,0,0,34,35,1,0,0,0,35,49,1,0,0,0,36,34,1,0,0,0,37,38,3,4,2,0,
        38,39,5,9,0,0,39,40,3,4,2,0,40,49,1,0,0,0,41,45,3,4,2,0,42,44,3,4,2,0,
        43,42,1,0,0,0,44,47,1,0,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,49,1,0,0,0,
        47,45,1,0,0,0,48,29,1,0,0,0,48,37,1,0,0,0,48,41,1,0,0,0,49,3,1,0,0,0,
        50,60,5,11,0,0,51,52,5,11,0,0,52,53,5,12,0,0,53,54,3,8,4,0,54,55,5,
        13,0,0,55,60,1,0,0,0,56,57,5,11,0,0,57,58,5,8,0,0,58,60,3,6,3,0,59,
        50,1,0,0,0,59,51,1,0,0,0,59,56,1,0,0,0,60,5,1,0,0,0,61,62,5,1,0,0,
        62,7,1,0,0,0,63,64,6,4,-1,0,64,70,3,10,5,0,65,66,5,12,0,0,66,67,3,8,4,0,
        67,68,5,13,0,0,68,70,1,0,0,0,69,63,1,0,0,0,69,65,1,0,0,0,70,79,1,0,0,0,
        71,72,10,2,0,0,72,73,5,6,0,0,73,78,3,8,4,3,74,75,10,1,0,0,75,76,5,7,0,0,
        76,78,3,8,4,2,77,71,1,0,0,0,77,74,1,0,0,0,78,81,1,0,0,0,79,77,1,0,0,0,
        79,80,1,0,0,0,80,9,1,0,0,0,81,79,1,0,0,0,82,83,3,12,6,0,83,84,3,14,7,0,
        84,85,3,16,8,0,85,11,1,0,0,0,86,89,5,11,0,0,87,88,5,8,0,0,88,90,3,6,3,0,
        89,87,1,0,0,0,89,90,1,0,0,0,90,13,1,0,0,0,91,92,7,0,0,0,92,15,1,0,0,0,
        93,98,3,6,3,0,94,98,5,20,0,0,95,98,5,10,0,0,96,98,3,12,6,0,97,93,1,0,0,0,
        97,94,1,0,0,0,97,95,1,0,0,0,97,96,1,0,0,0,98,17,1,0,0,0,11,25,27,34,45,
        48,59,69,77,79,89,97
    ]

class SequenceRuleParser ( Parser ):

    grammarFileName = "SequenceRule.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "','", "'if'", "'then'", 
                     "'else'", "'and'", "'or'", "'@'", "'->'", "<INVALID>", 
                     "<INVALID>", "'('", "')'", "'='", "'!='", "'<'", "'>'", 
                     "'<='", "'>='" ]

    symbolicNames = [ "<INVALID>", "NUMBER", "COMMA", "IF", "THEN", "ELSE", 
                      "AND", "OR", "AT", "ARROW", "STRING", "IDENTIFIER", 
                      "LPAREN", "RPAREN", "EQ", "NEQ", "LT", "GT", "LTE", 
                      "GTE", "BOOLEAN", "WS" ]

    RULE_rule = 0
    RULE_sequence = 1
    RULE_element = 2
    RULE_number = 3
    RULE_condition = 4
    RULE_expression = 5
    RULE_property = 6
    RULE_relOp = 7
    RULE_value = 8

    ruleNames =  [ "rule", "sequence", "element", "number", "condition", 
                   "expression", "property", "relOp", "value" ]

    EOF = Token.EOF
    NUMBER=1
    COMMA=2
    IF=3
    THEN=4
    ELSE=5
    AND=6
    OR=7
    AT=8
    ARROW=9
    STRING=10
    IDENTIFIER=11
    LPAREN=12
    RPAREN=13
    EQ=14
    NEQ=15
    LT=16
    GT=17
    LTE=18
    GTE=19
    BOOLEAN=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_rule

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SimpleRuleContext(RuleContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.RuleContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def sequence(self):
            return self.getTypedRuleContext(SequenceRuleParser.SequenceContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleRule" ):
                listener.enterSimpleRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleRule" ):
                listener.exitSimpleRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleRule" ):
                return visitor.visitSimpleRule(self)
            else:
                return visitor.visitChildren(self)


    class ConditionalRuleContext(RuleContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.RuleContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF(self):
            return self.getToken(SequenceRuleParser.IF, 0)
        def condition(self):
            return self.getTypedRuleContext(SequenceRuleParser.ConditionContext,0)

        def THEN(self):
            return self.getToken(SequenceRuleParser.THEN, 0)
        def sequence(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.SequenceContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.SequenceContext,i)

        def ELSE(self):
            return self.getToken(SequenceRuleParser.ELSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConditionalRule" ):
                listener.enterConditionalRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConditionalRule" ):
                listener.exitConditionalRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditionalRule" ):
                return visitor.visitConditionalRule(self)
            else:
                return visitor.visitChildren(self)



    def rule_(self):

        localctx = SequenceRuleParser.RuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_rule)
        _la = 0 # Token type
        try:
            self.state = 27
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                localctx = SequenceRuleParser.SimpleRuleContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.sequence()
                pass
            elif token in [3]:
                localctx = SequenceRuleParser.ConditionalRuleContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 19
                self.match(SequenceRuleParser.IF)
                self.state = 20
                self.condition(0)
                self.state = 21
                self.match(SequenceRuleParser.THEN)
                self.state = 22
                self.sequence()
                self.state = 25
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==5:
                    self.state = 23
                    self.match(SequenceRuleParser.ELSE)
                    self.state = 24
                    self.sequence()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_sequence

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ArrowSequenceContext(SequenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.SequenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.ElementContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.ElementContext,i)

        def ARROW(self):
            return self.getToken(SequenceRuleParser.ARROW, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrowSequence" ):
                listener.enterArrowSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrowSequence" ):
                listener.exitArrowSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrowSequence" ):
                return visitor.visitArrowSequence(self)
            else:
                return visitor.visitChildren(self)


    class CommaSequenceContext(SequenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.SequenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.ElementContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.ElementContext,i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SequenceRuleParser.COMMA)
            else:
                return self.getToken(SequenceRuleParser.COMMA, i)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommaSequence" ):
                listener.enterCommaSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommaSequence" ):
                listener.exitCommaSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommaSequence" ):
                return visitor.visitCommaSequence(self)
            else:
                return visitor.visitChildren(self)


    class SpaceSequenceContext(SequenceContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.SequenceContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.ElementContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.ElementContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSpaceSequence" ):
                listener.enterSpaceSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSpaceSequence" ):
                listener.exitSpaceSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSpaceSequence" ):
                return visitor.visitSpaceSequence(self)
            else:
                return visitor.visitChildren(self)



    def sequence(self):

        localctx = SequenceRuleParser.SequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_sequence)
        self._la = 0 # Token type
        try:
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = SequenceRuleParser.CommaSequenceContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.element()
                self.state = 34
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==2:
                    self.state = 30
                    self.match(SequenceRuleParser.COMMA)
                    self.state = 31
                    self.element()
                    self.state = 36
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                localctx = SequenceRuleParser.ArrowSequenceContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 37
                self.element()
                self.state = 38
                self.match(SequenceRuleParser.ARROW)
                self.state = 39
                self.element()
                pass

            elif la_ == 3:
                localctx = SequenceRuleParser.SpaceSequenceContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 41
                self.element()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11:
                    self.state = 42
                    self.element()
                    self.state = 47
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_element

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SimpleElementContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(SequenceRuleParser.IDENTIFIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleElement" ):
                listener.enterSimpleElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleElement" ):
                listener.exitSimpleElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleElement" ):
                return visitor.visitSimpleElement(self)
            else:
                return visitor.visitChildren(self)


    class PosElementContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(SequenceRuleParser.IDENTIFIER, 0)
        def AT(self):
            return self.getToken(SequenceRuleParser.AT, 0)
        def number(self):
            return self.getTypedRuleContext(SequenceRuleParser.NumberContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPosElement" ):
                listener.enterPosElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPosElement" ):
                listener.exitPosElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPosElement" ):
                return visitor.visitPosElement(self)
            else:
                return visitor.visitChildren(self)


    class ConstrainedElementContext(ElementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ElementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(SequenceRuleParser.IDENTIFIER, 0)
        def LPAREN(self):
            return self.getToken(SequenceRuleParser.LPAREN, 0)
        def condition(self):
            return self.getTypedRuleContext(SequenceRuleParser.ConditionContext,0)

        def RPAREN(self):
            return self.getToken(SequenceRuleParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstrainedElement" ):
                listener.enterConstrainedElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstrainedElement" ):
                listener.exitConstrainedElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstrainedElement" ):
                return visitor.visitConstrainedElement(self)
            else:
                return visitor.visitChildren(self)



    def element(self):

        localctx = SequenceRuleParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_element)
        try:
            self.state = 59
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                localctx = SequenceRuleParser.SimpleElementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.match(SequenceRuleParser.IDENTIFIER)
                pass

            elif la_ == 2:
                localctx = SequenceRuleParser.ConstrainedElementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.match(SequenceRuleParser.IDENTIFIER)
                self.state = 52
                self.match(SequenceRuleParser.LPAREN)
                self.state = 53
                self.condition(0)
                self.state = 54
                self.match(SequenceRuleParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = SequenceRuleParser.PosElementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.match(SequenceRuleParser.IDENTIFIER)
                self.state = 57
                self.match(SequenceRuleParser.AT)
                self.state = 58
                self.number()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_number

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SignedNumberContext(NumberContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.NumberContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(SequenceRuleParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSignedNumber" ):
                listener.enterSignedNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSignedNumber" ):
                listener.exitSignedNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignedNumber" ):
                return visitor.visitSignedNumber(self)
            else:
                return visitor.visitChildren(self)



    def number(self):

        localctx = SequenceRuleParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_number)
        try:
            localctx = SequenceRuleParser.SignedNumberContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(SequenceRuleParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_condition

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class SingleConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expression(self):
            return self.getTypedRuleContext(SequenceRuleParser.ExpressionContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleCondition" ):
                listener.enterSingleCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleCondition" ):
                listener.exitSingleCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleCondition" ):
                return visitor.visitSingleCondition(self)
            else:
                return visitor.visitChildren(self)


    class ParenConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(SequenceRuleParser.LPAREN, 0)
        def condition(self):
            return self.getTypedRuleContext(SequenceRuleParser.ConditionContext,0)

        def RPAREN(self):
            return self.getToken(SequenceRuleParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenCondition" ):
                listener.enterParenCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenCondition" ):
                listener.exitParenCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenCondition" ):
                return visitor.visitParenCondition(self)
            else:
                return visitor.visitChildren(self)


    class OrConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.ConditionContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.ConditionContext,i)

        def OR(self):
            return self.getToken(SequenceRuleParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrCondition" ):
                listener.enterOrCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrCondition" ):
                listener.exitOrCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrCondition" ):
                return visitor.visitOrCondition(self)
            else:
                return visitor.visitChildren(self)


    class AndConditionContext(ConditionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ConditionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def condition(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SequenceRuleParser.ConditionContext)
            else:
                return self.getTypedRuleContext(SequenceRuleParser.ConditionContext,i)

        def AND(self):
            return self.getToken(SequenceRuleParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndCondition" ):
                listener.enterAndCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndCondition" ):
                listener.exitAndCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndCondition" ):
                return visitor.visitAndCondition(self)
            else:
                return visitor.visitChildren(self)



    def condition(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = SequenceRuleParser.ConditionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_condition, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                localctx = SequenceRuleParser.SingleConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 64
                self.expression()
                pass
            elif token in [12]:
                localctx = SequenceRuleParser.ParenConditionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 65
                self.match(SequenceRuleParser.LPAREN)
                self.state = 66
                self.condition(0)
                self.state = 67
                self.match(SequenceRuleParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 79
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 77
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        localctx = SequenceRuleParser.AndConditionContext(self, SequenceRuleParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 71
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 72
                        self.match(SequenceRuleParser.AND)
                        self.state = 73
                        self.condition(3)
                        pass

                    elif la_ == 2:
                        localctx = SequenceRuleParser.OrConditionContext(self, SequenceRuleParser.ConditionContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_condition)
                        self.state = 74
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 75
                        self.match(SequenceRuleParser.OR)
                        self.state = 76
                        self.condition(2)
                        pass

             
                self.state = 81
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_expression

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ComparisonExpressionContext(ExpressionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ExpressionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def property_(self):
            return self.getTypedRuleContext(SequenceRuleParser.PropertyContext,0)

        def relOp(self):
            return self.getTypedRuleContext(SequenceRuleParser.RelOpContext,0)

        def value(self):
            return self.getTypedRuleContext(SequenceRuleParser.ValueContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonExpression" ):
                listener.enterComparisonExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonExpression" ):
                listener.exitComparisonExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonExpression" ):
                return visitor.visitComparisonExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self):

        localctx = SequenceRuleParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_expression)
        try:
            localctx = SequenceRuleParser.ComparisonExpressionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.property_()
            self.state = 83
            self.relOp()
            self.state = 84
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SequenceRuleParser.IDENTIFIER, 0)

        def AT(self):
            return self.getToken(SequenceRuleParser.AT, 0)

        def number(self):
            return self.getTypedRuleContext(SequenceRuleParser.NumberContext,0)


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_property

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperty" ):
                listener.enterProperty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperty" ):
                listener.exitProperty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty" ):
                return visitor.visitProperty(self)
            else:
                return visitor.visitChildren(self)




    def property_(self):

        localctx = SequenceRuleParser.PropertyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_property)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(SequenceRuleParser.IDENTIFIER)
            self.state = 89
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 87
                self.match(SequenceRuleParser.AT)
                self.state = 88
                self.number()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(SequenceRuleParser.EQ, 0)

        def NEQ(self):
            return self.getToken(SequenceRuleParser.NEQ, 0)

        def LT(self):
            return self.getToken(SequenceRuleParser.LT, 0)

        def GT(self):
            return self.getToken(SequenceRuleParser.GT, 0)

        def LTE(self):
            return self.getToken(SequenceRuleParser.LTE, 0)

        def GTE(self):
            return self.getToken(SequenceRuleParser.GTE, 0)

        def getRuleIndex(self):
            return SequenceRuleParser.RULE_relOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelOp" ):
                listener.enterRelOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelOp" ):
                listener.exitRelOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelOp" ):
                return visitor.visitRelOp(self)
            else:
                return visitor.visitChildren(self)




    def relOp(self):

        localctx = SequenceRuleParser.RelOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_relOp)
        _la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1032192) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return SequenceRuleParser.RULE_value

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BooleanValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOLEAN(self):
            return self.getToken(SequenceRuleParser.BOOLEAN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanValue" ):
                listener.enterBooleanValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanValue" ):
                listener.exitBooleanValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanValue" ):
                return visitor.visitBooleanValue(self)
            else:
                return visitor.visitChildren(self)


    class PropertyValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def property_(self):
            return self.getTypedRuleContext(SequenceRuleParser.PropertyContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyValue" ):
                listener.enterPropertyValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyValue" ):
                listener.exitPropertyValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyValue" ):
                return visitor.visitPropertyValue(self)
            else:
                return visitor.visitChildren(self)


    class NumericValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def number(self):
            return self.getTypedRuleContext(SequenceRuleParser.NumberContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumericValue" ):
                listener.enterNumericValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumericValue" ):
                listener.exitNumericValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumericValue" ):
                return visitor.visitNumericValue(self)
            else:
                return visitor.visitChildren(self)


    class StringValueContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a SequenceRuleParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(SequenceRuleParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringValue" ):
                listener.enterStringValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringValue" ):
                listener.exitStringValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringValue" ):
                return visitor.visitStringValue(self)
            else:
                return visitor.visitChildren(self)



    def value(self):

        localctx = SequenceRuleParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_value)
        try:
            self.state = 97
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = SequenceRuleParser.NumericValueContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 93
                self.number()
                pass
            elif token in [20]:
                localctx = SequenceRuleParser.BooleanValueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 94
                self.match(SequenceRuleParser.BOOLEAN)
                pass
            elif token in [10]:
                localctx = SequenceRuleParser.StringValueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 95
                self.match(SequenceRuleParser.STRING)
                pass
            elif token in [11]:
                localctx = SequenceRuleParser.PropertyValueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 96
                self.property_()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            self._predicates = dict()
        self._predicates[4] = self.condition_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def condition_sempred(self, localctx:ConditionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         




