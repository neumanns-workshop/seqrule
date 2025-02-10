import pytest

from seqrule import Object, sequence_rule_generator


@pytest.fixture
def test_objects():
    """Create test objects for rule evaluation."""
    return [
        Object("heart", rank=7, suit="hearts"),
        Object("spade", rank=10, suit="spades")
    ]


def test_basic_rule_generation(test_objects):
    """Test basic rule generation and evaluation."""
    conditions = [
        ("rank", ">=", 5),
        ("suit", "!=", "diamonds")
    ]
    sequence_constraints = ["heart", "spade"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(test_objects) is True


def test_sequence_order_validation(test_objects):
    """Test that sequence order is strictly enforced."""
    conditions = [("rank", ">=", 5)]
    sequence_constraints = ["spade", "heart"]  # Reversed order

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(test_objects) is False


def test_property_not_found():
    """Test handling of missing properties."""
    objects = [Object("test", suit="hearts")]  # Missing 'rank' property
    conditions = [("rank", ">=", 5)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is False


def test_verbose_mode(test_objects, caplog):
    """Test verbose logging mode."""
    import logging
    caplog.set_level(logging.DEBUG)

    conditions = [("rank", ">=", 5)]
    sequence_constraints = ["heart", "spade"]

    rule_func = sequence_rule_generator(
        conditions,
        sequence_constraints,
        verbose=True
    )

    rule_func(test_objects)
    assert any("Condition passed" in record.message
              for record in caplog.records)


def test_custom_predicate():
    """Test rule generation with a custom predicate function."""
    def custom_compare(obj, context):
        # obj is current object, value is passed as condition
        prefix = obj.get('prefix')
        return isinstance(prefix, str) and prefix.startswith('a')

    objects = [Object("test", prefix="abc")]
    # Value is not used in the predicate
    conditions = [("prefix", custom_compare, None)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is True


def test_multiple_conditions(test_objects):
    """Test rule with multiple conditions per object."""
    conditions = [
        ("rank", ">=", 5),
        ("rank", "<", 15),
        ("suit", "!=", "diamonds"),
        ("suit", "!=", "clubs")
    ]
    sequence_constraints = ["heart", "spade"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(test_objects) is True


def test_failing_conditions():
    """Test rule when conditions are not met."""
    objects = [
        Object("heart", rank=3, suit="hearts"),  # rank < 5
        Object("spade", rank=10, suit="spades")
    ]
    conditions = [("rank", ">=", 5)]
    sequence_constraints = ["heart", "spade"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is False


@pytest.mark.parametrize("operator,value,expected", [
    ("=", 7, True),
    ("!=", 6, True),
    ("<", 8, True),
    (">", 6, True),
    ("<=", 7, True),
    (">=", 7, True),
    ("=", 8, False),
    ("<", 7, False),
    (">", 7, False)
])
def test_comparison_operators(operator, value, expected):
    """Test all comparison operators."""
    objects = [Object("test", rank=7)]
    conditions = [("rank", operator, value)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is expected


def test_invalid_custom_predicate():
    """Test error handling with failing custom predicate."""
    def failing_predicate(a, b):
        raise ValueError("Test error")

    objects = [Object("test", value=1)]
    conditions = [("value", failing_predicate, 1)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is False


def test_none_value_handling(invalid_values_sequence):
    """Test handling of None values in object properties."""
    conditions = [("rank", "=", None)]
    sequence_constraints = ["none"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should handle None values gracefully
    assert rule_func([invalid_values_sequence[2]]) is True


def test_infinity_comparison(invalid_values_sequence):
    """Test handling of infinity in numeric comparisons."""
    conditions = [("rank", ">", 1000)]
    sequence_constraints = ["special"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Infinity should be greater than any finite number
    assert rule_func([invalid_values_sequence[3]]) is True


def test_empty_string_comparison(invalid_values_sequence):
    """Test handling of empty string values."""
    conditions = [("suit", "=", "")]
    sequence_constraints = ["zero"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should handle empty strings correctly
    assert rule_func([invalid_values_sequence[0]]) is True


def test_negative_value_comparison(invalid_values_sequence):
    """Test handling of negative values."""
    conditions = [
        ("rank", "<", 0),
        ("value", "<", 0)
    ]
    sequence_constraints = ["negative"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should handle negative values correctly
    assert rule_func([invalid_values_sequence[1]]) is True


def test_missing_properties_handling(sequence_with_missing_properties):
    """Test handling of objects with missing properties."""
    conditions = [
        ("rank", ">", 5),  # First object has rank but no suit
        ("suit", "=", "hearts"),  # Second object has suit but no rank
        ("extra", "=", "value")  # Third object has an extra property
    ]
    sequence_constraints = ["first", "second", "third"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should fail gracefully when properties are missing
    assert rule_func(sequence_with_missing_properties) is False


def test_empty_sequence_constraints(empty_sequence):
    """Test handling of empty sequence constraints."""
    conditions = [("rank", ">", 5)]
    sequence_constraints = []

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should handle empty sequence constraints appropriately
    assert rule_func(empty_sequence) is False


def test_single_object_sequence(single_object_sequence):
    """Test handling of sequences with only one object."""
    conditions = [("rank", "=", 5), ("suit", "=", "clubs")]
    sequence_constraints = ["solo"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(single_object_sequence) is True


def test_custom_compare_with_none():
    """Test custom comparison function with None values."""
    def custom_compare(obj, context):
        value = obj.get('value')
        if value is None:
            return False
        # Compare directly with value
        return value > 5

    # Test with None value
    objects = [Object("test", value=None)]
    # The value parameter isn't used by custom predicates
    conditions = [("value", custom_compare, None)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert not rule_func(objects)  # Should fail since value is None

    # Test with valid value
    objects = [Object("test", value=10)]
    assert rule_func(objects)  # Should pass since 10 > 5


def test_custom_predicate_type_error():
    """Test custom predicate handling type errors."""
    def custom_compare(a, b):
        # This will raise TypeError when comparing str with int
        return a > b

    objects = [Object("test", value="string")]
    conditions = [("value", custom_compare, 5)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is False


def test_none_value_with_operators():
    """Test None value handling with different operators."""
    objects = [Object("test", value=None)]
    sequence_constraints = ["test"]

    # Test each operator with None values
    operators = ["<", ">", "<=", ">=", "in", "not in"]
    for op in operators:
        conditions = [("value", op, 5)]
        rule_func = sequence_rule_generator(conditions, sequence_constraints)
        assert rule_func(objects) is False


def test_collection_membership_operators():
    """Test 'in' and 'not in' operators."""
    objects = [
        Object("test1", value=5, category="A"),
        Object("test2", value=10, category="B")
    ]
    sequence_constraints = ["test1", "test2"]

    conditions = [
        ("value", "in", [5, 10, 15]),
        ("category", "not in", ["C", "D"])
    ]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is True


def test_invalid_operator_comparison():
    """Test comparison with an invalid operator."""
    objects = [Object("test", value=5)]
    conditions = [("value", "INVALID", 5)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is False


def test_none_value_comparisons():
    """Test all comparison cases with None values."""
    obj = Object("test", value=None)
    sequence_constraints = ["test"]

    # Test each operator with None value
    operators = ["=", "!=", "exists", "not exists", "<", ">", "<=", ">="]
    for op in operators:
        conditions = [("value", op, None)]
        rule_func = sequence_rule_generator(conditions, sequence_constraints)

        if op in ["=", "not exists"]:
            assert rule_func([obj]) is True
        elif op in ["!=", "exists"]:
            assert rule_func([obj]) is False
        else:
            # Other operators should fail with None values
            assert rule_func([obj]) is False


def test_existence_operators():
    """Test exists and not exists operators with non-None values."""
    obj = Object("test", value=5)
    sequence_constraints = ["test"]

    # Test exists with a value (should pass)
    conditions = [("value", "exists", None)]
    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func([obj]) is True

    # Test not exists with a value (should fail)
    conditions = [("value", "not exists", None)]
    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func([obj]) is False


def test_none_property_value_match():
    """Test handling of None values that match None conditions."""
    obj = Object("test", value=None)
    conditions = [("value", "=", None)]
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    # Should match since missing prop is treated as None
    assert rule_func([obj]) is True


def test_missing_property_with_none_value():
    """Test when a missing property matches a None condition value."""
    obj = Object("test")  # Object with no properties
    conditions = [("missing_prop", "=", None)]  # Condition expecting None
    sequence_constraints = ["test"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func([obj]) is True  # Should match since missing prop is treated as None


def test_sequence_based_predicate():
    """Test rule with a predicate that checks relationships between objects."""
    def check_increasing_rank(obj, context):
        prev = context['prev']
        if prev is None:  # First object can have any rank
            return True
        return obj.get('rank') > prev.get('rank')

    objects = [
        Object("first", rank=5),
        Object("second", rank=7),  # Increasing
        Object("third", rank=10)   # Increasing
    ]
    conditions = [("rank", check_increasing_rank, None)]
    sequence_constraints = ["first", "second", "third"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is True

    # Test failing case (not increasing)
    failing_objects = [
        Object("first", rank=5),
        Object("second", rank=3),  # Not increasing
        Object("third", rank=10)
    ]
    assert rule_func(failing_objects) is False


def test_sequence_based_predicate_with_next():
    """Test rule with a predicate that looks ahead in the sequence."""
    def check_rank_bounds(obj, context):
        _prev, next_obj = context['prev'], context['next']
        if next_obj is None:  # Last object can have any rank
            return True
        return obj.get('rank') < next_obj.get('rank')

    objects = [
        Object("first", rank=5),
        Object("second", rank=6),  # Within 2 of both neighbors
        Object("third", rank=7)    # Within 2 of previous
    ]
    conditions = [("rank", check_rank_bounds, None)]
    sequence_constraints = ["first", "second", "third"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is True

    # Test failing case (gap too large)
    failing_objects = [
        Object("first", rank=5),
        Object("second", rank=8),  # Gap of 3 to next
        Object("third", rank=5)
    ]
    assert rule_func(failing_objects) is False


def test_sequence_based_predicate_with_index():
    """Test rule with a predicate that uses sequence position."""
    def check_rank_by_position(obj, context):
        i = context['index']
        rank = obj.get('rank')
        if i == 0:  # First must be lowest
            next_obj = context['next']
            return rank < next_obj.get('rank')
        elif i == len(context['sequence']) - 1:  # Last must be highest
            prev = context['prev']
            return rank > prev.get('rank')
        else:  # Middle must be between neighbors
            prev = context['prev']
            next_obj = context['next']
            return prev.get('rank') < rank < next_obj.get('rank')

    objects = [
        Object("first", rank=5),   # Lowest
        Object("second", rank=7),  # In between
        Object("third", rank=10)   # Highest
    ]
    conditions = [("rank", check_rank_by_position, None)]
    sequence_constraints = ["first", "second", "third"]

    rule_func = sequence_rule_generator(conditions, sequence_constraints)
    assert rule_func(objects) is True

    # Test failing case (middle not between neighbors)
    failing_objects = [
        Object("first", rank=5),
        Object("second", rank=10),  # Higher than last
        Object("third", rank=7)
    ]
    assert rule_func(failing_objects) is False
