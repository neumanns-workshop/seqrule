"""
Example 04: Eleusis Card Game Rules
=================================

This example demonstrates how to use seqrule to validate rules for the Eleusis
card game, where players must discover hidden rules about card sequences.
The rules can involve:
- Color patterns (red/black alternation)
- Value relationships (increasing/decreasing)
- Suit sequences and patterns
- Complex combinations of multiple conditions
- Mathematical properties (prime numbers)
- Compound rules with multiple dependencies
"""

import logging
import math

from seqrule import Object, RuleBuilder

# Set up logging with cleaner format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


def is_prime_number(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def create_card(rank: str, suit: str, name: str = None) -> Object:
    """Create a card object with full properties."""
    # Map ranks to numeric values
    rank_values = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13
    }

    # Determine card properties
    value = rank_values.get(str(rank))
    if value is None:
        try:
            value = int(rank)
        except ValueError as err:
            raise ValueError(f"Invalid rank: {rank}") from err

    color = 'red' if suit in ['hearts', 'diamonds'] else 'black'
    is_face = value > 10
    is_prime = is_prime_number(value)

    properties = {
        'rank': rank,
        'suit': suit,
        'value': value,
        'color': color,
        'is_face': is_face,
        'is_prime': is_prime
    }

    return Object(name or f"{rank}{suit[0]}", **properties)


def check_color_alternation(obj, context):
    """Check if card colors alternate (red/black)."""
    prev = context['prev']
    if prev is None:  # First card can be any color
        return True

    result = prev.get('color') != obj.get('color')
    if not result:
        print(
            "Color alternation violated: "
            f"{prev.get('color')} -> {obj.get('color')}"
        )
    return result


def check_increasing_value(obj, context):
    """Check if card value increases after red cards."""
    prev = context['prev']
    if prev is None or prev.get('color') != 'red':
        return True

    curr_val = obj.get('value')
    prev_val = prev.get('value')
    result = curr_val > prev_val

    if not result:
        print(f"Value not increasing after red: {prev_val} -> {curr_val}")
    return result


def check_suit_sequence(obj, context):
    """Check if suits follow a specific pattern."""
    prev = context['prev']
    next_obj = context['next']
    curr_suit = obj.get('suit')

    # First card must be hearts or diamonds
    if prev is None:
        result = curr_suit in ['hearts', 'diamonds']
        if not result:
            print(f"First card must be hearts/diamonds, got {curr_suit}")
        return result

    # Last card must be spades
    if next_obj is None:
        result = curr_suit == 'spades'
        if not result:
            print(f"Last card must be spades, got {curr_suit}")
        return result

    # Middle cards must be clubs
    result = curr_suit == 'clubs'
    if not result:
        print(f"Middle cards must be clubs, got {curr_suit}")
    return result


def check_face_card_rule(obj, context):
    """Additional rule: Face cards can't follow each other."""
    prev = context['prev']
    if prev is None or not prev.get('is_face'):
        return True

    result = not obj.get('is_face')
    if not result:
        print(
            "Face cards cannot follow each other: "
            f"{prev.get('rank')} -> {obj.get('rank')}"
        )
    return result


def check_prime_suit_rule(obj, context):
    """Complex rule: Prime numbers must be hearts/diamonds, and their next card
    must be clubs with a value that's the smallest prime factor of
    (value + 4)."""
    curr_val = obj.get('value')
    curr_suit = obj.get('suit')
    curr_is_prime = obj.get('is_prime')

    # If current card is prime, it must be hearts/diamonds
    if curr_is_prime and curr_suit not in ['hearts', 'diamonds']:
        print(
            f"Prime card {curr_val} must be hearts/diamonds, "
            f"got {curr_suit}"
        )
        return False

    # Check the rule for the card after a prime
    prev = context['prev']
    if prev and prev.get('is_prime'):
        prev_val = prev.get('value')
        target = prev_val + 4

        # Find smallest prime factor
        smallest_factor = None
        for i in range(2, target + 1):
            if target % i == 0 and is_prime_number(i):
                smallest_factor = i
                break

        # Current card must be clubs with value = smallest prime factor
        if curr_suit != 'clubs':
            print(f"Card after prime must be clubs, got {curr_suit}")
            return False

        if curr_val != smallest_factor:
            print(f"After prime {prev_val}, value must be {smallest_factor}")
            return False

    return True


def main():
    """Example usage of Eleusis rule validation."""
    print("Eleusis Card Game Rule Validation")
    print("================================\n")

    # Create a complex Eleusis rule
    rule = RuleBuilder()\
        .add_condition('color', check_color_alternation, None)\
        .add_condition('value', check_increasing_value, None)\
        .add_condition('suit', check_suit_sequence, None)\
        .add_condition('is_face', check_face_card_rule, None)\
        .add_condition('is_prime', check_prime_suit_rule, None)\
        .set_sequence(['card1', 'card2', 'card3', 'card4'])\
        .build()

    # Test valid sequence with prime number rule
    print("Testing Valid Prime Sequence...")
    valid_prime_sequence = [
        create_card('7', 'hearts', 'card1'),    # Prime number (7)
        # 7+4=11, smallest prime factor is 11
        create_card('2', 'clubs', 'card2'),
        create_card('5', 'diamonds', 'card3'),  # Prime number (5)
        # 5+4=9, smallest prime factor is 3
        create_card('3', 'spades', 'card4')
    ]

    result = rule.evaluate(valid_prime_sequence)
    print(f"Valid prime sequence result: {result[0]}\n")

    # Test invalid prime sequence
    print("Testing Invalid Prime Sequence...")
    invalid_prime_sequence = [
        create_card('7', 'clubs', 'card1'),     # Prime in wrong suit
        create_card('4', 'clubs', 'card2'),     # Wrong value after prime
        create_card('5', 'hearts', 'card3'),    # Prime in hearts (ok)
        create_card('8', 'spades', 'card4')     # Wrong value after prime
    ]

    result = rule.evaluate(invalid_prime_sequence)
    print(f"Invalid prime sequence result: {result[0]}\n")

    # Test valid sequence
    print("Testing Valid Sequence...")
    valid_sequence = [
        create_card('7', 'hearts', 'card1'),     # Hearts start
        create_card('10', 'clubs', 'card2'),     # Clubs middle
        create_card('5', 'clubs', 'card3'),      # Clubs middle
        create_card('8', 'spades', 'card4')      # Spades end
    ]

    result = rule.evaluate(valid_sequence)
    print(f"Valid sequence result: {result[0]}\n")

    # Test invalid color alternation
    print("Testing Invalid Color Alternation...")
    invalid_colors = [
        create_card('7', 'hearts', 'card1'),
        create_card('8', 'diamonds', 'card2'),   # Should be black
        create_card('9', 'clubs', 'card3'),
        create_card('10', 'spades', 'card4')
    ]

    result = rule.evaluate(invalid_colors)
    print(f"Invalid colors result: {result[0]}\n")

    # Test invalid value progression
    print("Testing Invalid Value Progression...")
    invalid_values = [
        create_card('K', 'hearts', 'card1'),
        create_card('2', 'clubs', 'card2'),      # Valid after red K
        create_card('A', 'clubs', 'card3'),      # Should be > 2
        create_card('3', 'spades', 'card4')
    ]

    result = rule.evaluate(invalid_values)
    print(f"Invalid values result: {result[0]}\n")

    # Test invalid suit sequence
    print("Testing Invalid Suit Sequence...")
    invalid_suits = [
        create_card('7', 'clubs', 'card1'),      # Should be hearts/diamonds
        create_card('8', 'clubs', 'card2'),
        create_card('9', 'clubs', 'card3'),
        create_card('10', 'hearts', 'card4')     # Should be spades
    ]

    result = rule.evaluate(invalid_suits)
    print(f"Invalid suits result: {result[0]}\n")

    # Test face card rule
    print("Testing Face Card Rule...")
    invalid_faces = [
        create_card('J', 'hearts', 'card1'),
        create_card('Q', 'clubs', 'card2'),      # Face cards can't follow
        create_card('5', 'clubs', 'card3'),
        create_card('K', 'spades', 'card4')
    ]

    result = rule.evaluate(invalid_faces)
    print(f"Invalid face cards result: {result[0]}\n")

    # Analyze rule complexity
    print("Rule Complexity Analysis:")
    metrics = rule.analyze_complexity()
    important_metrics = {
        'condition_count': metrics['condition_count'],
        'sequence_length': metrics['sequence_length'],
        'complexity_score': metrics['complexity_score'],
        'execution_cost': metrics['execution_cost']
    }
    for metric, value in important_metrics.items():
        print(f"{metric}: {value}")

    # Profile performance
    print("\nPerformance Metrics:")
    test_sequences = [
        valid_sequence,
        invalid_colors,
        invalid_values,
        invalid_suits,
        invalid_faces
    ]
    avg_time, avg_memory, _, _ = rule.profile(
        test_sequences=test_sequences,
        runs=5
    )
    print(f"Average execution time: {avg_time:.6f} seconds")
    print(f"Average memory usage: {avg_memory:.2f} KB")


if __name__ == "__main__":
    main()
