from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union, List


class RelationalOp(Enum):
    EQ = auto()    # =
    NEQ = auto()   # !=
    LT = auto()    # <
    GT = auto()    # >
    LTE = auto()   # <=
    GTE = auto()   # >=


class LogicalOp(Enum):
    AND = auto()
    OR = auto()


@dataclass
class Position:
    """Base class for position references"""
    pass


@dataclass
class AbsolutePosition(Position):
    """Position from start of sequence (0-based)"""
    index: int


@dataclass
class RelativePosition(Position):
    """Position relative to current element"""
    offset: int


@dataclass
class Value:
    """Base class for rule values"""
    pass


@dataclass
class NumericValue(Value):
    value: float


@dataclass
class BooleanValue(Value):
    value: bool


@dataclass
class StringValue(Value):
    value: str


@dataclass
class PropertyValue(Value):
    """Represents a property reference that can have a position"""
    identifier: str
    position: Optional[Position] = None


@dataclass
class Expression:
    """Represents a basic comparison (e.g., rank = 7)"""
    identifier: str
    position: Optional[Position]
    operator: RelationalOp
    value: Value


@dataclass
class Condition:
    """Represents a logical combination of expressions"""
    left: Optional[Union['Condition', Expression]] = None
    right: Optional[Union['Condition', Expression]] = None
    operator: Optional[LogicalOp] = None


@dataclass
class Element:
    """Represents a sequence element with optional constraints"""
    identifier: str
    constraint: Optional[Condition] = None
    position: Optional[Position] = None  # For elements like "ace@2"


@dataclass
class Sequence:
    """Represents an ordered sequence of elements"""
    elements: List[Element]


@dataclass
class Rule:
    """Base class for all rules"""
    pass


@dataclass
class SimpleRule(Rule):
    """A rule consisting of just a sequence"""
    sequence: Sequence


@dataclass
class ConditionalRule(Rule):
    """A rule with conditions and branches"""
    condition: Condition
    then_sequence: Sequence
    else_sequence: Optional[Sequence] = None 