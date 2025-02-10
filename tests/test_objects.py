import pytest

from seqrule import Object, Rule, RuleBuilder


def test_object_creation():
    """Test basic object creation with properties."""
    obj = Object("test", rank=5, suit="hearts")
    assert obj.name == "test"
    assert obj.get("rank") == 5
    assert obj.get("suit") == "hearts"


def test_invalid_object_name():
    """Test that creating an object with invalid name type raises TypeError."""
    with pytest.raises(TypeError):
        Object(123, rank=5)  # name must be string


def test_property_access():
    """Test property access methods."""
    obj = Object("test", rank=7, suit="spades")
    assert obj.get("rank") == 7
    assert obj.get("nonexistent") is None
    assert obj.has_property("suit") is True
    assert obj.has_property("color") is False


def test_object_equality():
    """Test object equality comparison."""
    obj1 = Object("test", rank=5, suit="hearts")
    obj2 = Object("test", rank=5, suit="hearts")
    obj3 = Object("different", rank=5, suit="hearts")

    assert obj1 == obj2
    assert obj1 != obj3
    assert obj1 != "not_an_object"


def test_object_hash():
    """Test object hashing for set/dict usage."""
    obj1 = Object("test", rank=5, suit="hearts")
    obj2 = Object("test", rank=5, suit="hearts")
    obj3 = Object("different", rank=5, suit="hearts")

    # Objects with same properties should have same hash
    assert hash(obj1) == hash(obj2)
    # Different objects should have different hashes
    assert hash(obj1) != hash(obj3)

    # Test usage in sets
    object_set = {obj1, obj2, obj3}
    assert len(object_set) == 2  # obj1 and obj2 are equal


def test_object_to_dict():
    """Test dictionary representation of object."""
    obj = Object("test", rank=5, suit="hearts", value=10)
    dict_repr = obj.to_dict()

    assert dict_repr["name"] == "test"
    assert dict_repr["properties"] == {"rank": 5, "suit": "hearts", "value": 10}


def test_object_str_representation():
    """Test string representation of object."""
    obj = Object("test", rank=5, suit="hearts")
    str_repr = str(obj)
    assert "test" in str_repr
    assert "rank=5" in str_repr
    assert "suit=hearts" in str_repr


def test_object_repr():
    """Test detailed string representation of object."""
    obj = Object("test", rank=5, suit="hearts")
    repr_str = repr(obj)
    assert repr_str.startswith("Object(")
    assert "name='test'" in repr_str
    assert "properties=" in repr_str


def test_object_bool_comparison():
    """Test boolean comparison of objects."""
    obj1 = Object("test1", rank=5)
    obj2 = Object("test2", rank=5)

    # Objects should not be directly comparable with boolean operators
    with pytest.raises(TypeError):
        _ = obj1 < obj2

    with pytest.raises(TypeError):
        _ = obj1 > obj2


def test_object_property_access_methods():
    """Test different ways to access object properties."""
    obj = Object("test", rank=5, suit="hearts")

    # Test get with default
    assert obj.get("rank", 0) == 5
    assert obj.get("nonexistent", "default") == "default"

    # Test direct property access
    with pytest.raises(AttributeError):
        _ = obj.nonexistent_property


def test_rule_profile():
    """Test rule profiling functionality."""
    obj = Object("test", rank=5, suit="hearts")
    rule = (RuleBuilder()
            .add_condition("rank", ">", 0)
            .set_sequence(["test"])
            .build())

    test_sequences = [[obj]]
    avg_time, avg_memory, times, memory = rule.profile(
        test_sequences,
        runs=2
    )

    assert isinstance(avg_time, float)
    assert isinstance(avg_memory, float)
    assert isinstance(times, dict)
    assert isinstance(memory, dict)
    assert len(times) == len(test_sequences)
    assert len(memory) == len(test_sequences)


def test_rule_profile_with_multiple_sequences():
    """Test rule profiling with multiple sequences."""
    sequences = [
        [Object("test1", rank=5)],
        [Object("test2", rank=10)]
    ]
    rule = RuleBuilder()\
        .add_condition("rank", ">", 0)\
        .set_sequence(["test1", "test2"])\
        .build()

    avg_time, avg_memory, times, memory = rule.profile(sequences, runs=2)

    assert isinstance(avg_time, float)
    assert isinstance(avg_memory, float)
    assert len(times) == len(sequences)
    assert len(memory) == len(sequences)
    for seq_key in times:
        assert isinstance(times[seq_key], float)
        assert isinstance(memory[seq_key], float)


def test_batch_evaluate():
    """Test batch evaluation of sequences."""
    # Create a simple rule
    rule = RuleBuilder()\
        .add_condition("rank", ">", 5)\
        .set_sequence(["card1", "card2"])\
        .build()

    # Create test sequences
    valid_sequence = [
        Object("card1", rank=6),
        Object("card2", rank=7)
    ]
    invalid_sequence = [
        Object("card1", rank=4),
        Object("card2", rank=5)
    ]
    wrong_order = [
        Object("card2", rank=6),
        Object("card1", rank=7)
    ]

    sequences = [valid_sequence, invalid_sequence, wrong_order]
    results = rule.batch_evaluate(sequences)

    assert len(results) == 3
    assert results[0] is True  # Valid sequence
    assert results[1] is False  # Invalid ranks
    assert results[2] is False  # Wrong order


def test_rule_batch_evaluate():
    """Test batch evaluation of multiple sequences."""
    rule = RuleBuilder()\
        .add_condition("rank", ">", 5)\
        .set_sequence(["card1", "card2"])\
        .build()

    sequences = [
        [
            Object("card1", rank=6),
            Object("card2", rank=7)
        ],
        [
            Object("card1", rank=4),  # Should fail
            Object("card2", rank=5)
        ]
    ]

    results = rule.batch_evaluate(sequences)
    assert len(results) == 2
    assert results[0] is True   # First sequence passes
    assert results[1] is False  # Second sequence fails


def test_rule_batch_evaluate_empty():
    """Test batch evaluation with empty input."""
    rule = RuleBuilder()\
        .add_condition("rank", ">", 5)\
        .set_sequence(["card"])\
        .build()

    results = rule.batch_evaluate([])
    assert len(results) == 0


def test_rule_evaluate_with_tuple_result():
    """Test rule evaluation when rule function returns a tuple."""
    # Test failing case
    def mock_rule_func(sequence):
        return (False, "Validation error")

    rule = Rule(mock_rule_func, [], [])
    with pytest.raises(ValueError, match="Validation error"):
        rule.evaluate([])

    # Test successful case
    def mock_success_func(sequence):
        return (True, "Success")

    rule = Rule(mock_success_func, [], [])
    assert rule.evaluate([]) is True
