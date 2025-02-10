import pytest

from seqrule import Object


@pytest.fixture
def sample_sequence():
    """Returns a sequence of test objects."""
    return [
        Object("heart", rank=7, suit="hearts"),
        Object("spade", rank=10, suit="spades")
    ]


@pytest.fixture
def complex_sequence():
    """Returns a more complex sequence for thorough testing."""
    return [
        Object("ace", rank=14, suit="hearts", value=1),
        Object("king", rank=13, suit="spades", value=10),
        Object("queen", rank=12, suit="diamonds", value=10)
    ]


@pytest.fixture
def empty_sequence():
    """Returns an empty sequence for edge case testing."""
    return []


@pytest.fixture
def single_object_sequence():
    """Returns a sequence with just one object."""
    return [Object("solo", rank=5, suit="clubs")]


@pytest.fixture
def sequence_with_missing_properties():
    """Returns a sequence where objects have different/missing properties."""
    return [
        Object("first", rank=7),  # Missing suit
        Object("second", suit="hearts"),  # Missing rank
        Object("third", rank=9, suit="diamonds", extra="value")
    ]


@pytest.fixture
def invalid_values_sequence():
    """Returns a sequence with edge case property values."""
    return [
        Object("zero", rank=0, suit=""),  # Zero and empty string
        Object("negative", rank=-1, value=-100),  # Negative values
        Object("none", rank=None, suit=None),  # None values
        Object("special", rank=float('inf'), suit="♠")  # Special values
    ]


@pytest.fixture
def rich_object():
    """Returns a test object with multiple properties."""
    return Object(
        "rich",
        rank=10,
        suit="spades",
        value=25,
        is_face_card=True,
        color="black"
    )


@pytest.fixture
def complex_conditions():
    """Returns a set of complex test conditions."""
    return [
        ("rank", ">", 5),
        ("suit", "in", ["hearts", "spades"]),
        ("value", "exists", None),
        ("is_face_card", "=", True)
    ]
