"""
Example 03: Chord Progression Validation
=====================================

This example demonstrates how to use seqrule to validate music chord progressions,
enforcing music theory rules like:
- Voice leading between chords
- Functional harmony constraints
- Common chord progression patterns
- Secondary dominants
- Modal interchange
"""

import logging

from seqrule import Object, RuleBuilder

logging.basicConfig(
    level=logging.INFO
)
logging.disable(logging.NOTSET)


def create_chord(symbol: str, name: str = None, **properties) -> Object:
    """Create a chord object with the given symbol and properties."""
    root = symbol[0]
    quality = 'minor' if 'm' in symbol else 'major'
    has_seventh = '7' in symbol or 'maj7' in symbol
    is_major_seventh = 'maj7' in symbol

    # Map chord symbols to scale degrees and functions
    scale_degrees = {
        'C': 1, 'Dm': 2, 'Em': 3, 'F': 4, 'G': 5, 'Am': 6, 'B': 7,
        'Dm7': 2, 'G7': 5, 'Cmaj7': 1
    }

    functions = {
        'C': 'tonic', 'F': 'subdominant', 'G': 'dominant',
        'G7': 'dominant', 'Dm': 'supertonic', 'Em': 'mediant',
        'Am': 'submediant', 'B': 'leading', 'Dm7': 'supertonic',
        'Cmaj7': 'tonic'
    }

    # Set properties for the chord
    properties.update({
        'root': root,
        'quality': quality,
        'has_seventh': has_seventh,
        'is_major_seventh': is_major_seventh,
        'scale_degree': scale_degrees.get(symbol, 0),
        'function': functions.get(symbol, 'unknown'),
        'symbol': symbol
    })

    return Object(name or symbol, **properties)


def check_voice_leading(obj, context):
    """Check if the voice leading between chords is smooth."""
    prev = context['prev']
    if prev is None:
        return True  # First chord is always valid

    # Get the functions of both chords
    current_func = obj.get('function')
    prev_func = prev.get('function')

    # Define valid voice leading progressions (stricter than functional harmony)
    valid_progressions = {
        'tonic': ['subdominant', 'dominant'],  # I -> IV or V
        'subdominant': ['dominant'],           # IV -> V only
        'dominant': ['tonic'],                 # V -> I only
        'supertonic': ['dominant']             # ii -> V only
    }

    # Check if the progression follows voice leading rules
    if prev_func not in valid_progressions:
        print(f"Invalid voice leading: unknown function '{prev_func}'")
        return False

    valid = current_func in valid_progressions[prev_func]
    if not valid:
        print(f"Invalid voice leading: {prev_func} -> {current_func}")
    return valid


def check_functional_harmony(obj, context):
    """Check if the chord progression follows functional harmony rules."""
    prev = context['prev']
    if prev is None:
        return True  # First chord is always valid

    # Get the functions of both chords
    current_func = obj.get('function')
    prev_func = prev.get('function')

    # Define valid progressions based on functional harmony (more flexible)
    valid_progressions = {
        'tonic': ['subdominant', 'dominant', 'supertonic'],  # I -> IV, V, or ii
        'subdominant': ['dominant', 'tonic'],                # IV -> V or I
        'dominant': ['tonic'],                               # V -> I only
        'supertonic': ['dominant']                          # ii -> V only
    }

    # Check if the progression follows functional harmony rules
    if prev_func not in valid_progressions:
        print(f"Invalid harmony: unknown function '{prev_func}'")
        return False

    valid = current_func in valid_progressions[prev_func]
    if not valid:
        print(f"Invalid functional harmony: {prev_func} -> {current_func}")
    return valid


def check_secondary_dominant(
    current_obj: Object,
    prev_obj: Object = None
) -> bool:
    """Check if the chord is a valid secondary dominant."""
    if not prev_obj:
        return True

    # Get properties of both chords
    current_root = current_obj.get('root')
    has_seventh = prev_obj.get('has_seventh')
    quality = prev_obj.get('quality')

    # Secondary dominants are typically V7 of the next chord
    # For example, D7 -> G or A7 -> D
    if has_seventh and quality == 'minor':
        # The root of the current chord should be a fourth above
        # the root of the previous chord for a secondary dominant
        roots = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        prev_idx = roots.index(current_root)
        target_root = roots[(prev_idx + 4) % 7]
        return target_root == current_root

    return True


def main():
    """Example usage of the chord progression validation."""
    print("Chord Progression Validation Example")
    print("===================================\n")

    # Test basic I-IV-V-I progression
    print("Testing Basic I-IV-V-I Progression...")
    basic_prog = [
        create_chord("C"),      # I
        create_chord("F"),      # IV
        create_chord("G7"),     # V7
        create_chord("C")       # I
    ]

    # Create a rule that enforces voice leading and functional harmony
    basic_rule = RuleBuilder()\
        .add_condition('function', check_voice_leading, None)\
        .add_condition('function', check_functional_harmony, None)\
        .set_sequence(['C', 'F', 'G7', 'C'])\
        .build()

    result = basic_rule.evaluate(basic_prog)
    print(f"Basic I-IV-V-I progression valid: {result[0]}")
    print("Progression: C -> F -> G7 -> C\n")

    # Test invalid progression (V -> IV, violates voice leading)
    print("Testing Invalid Voice Leading...")
    invalid_prog = [
        create_chord("C"),      # I
        create_chord("F"),      # IV
        create_chord("G7"),     # V7
        create_chord("F")       # IV (invalid after V7)
    ]

    # Create a rule for testing invalid voice leading
    invalid_rule = RuleBuilder()\
        .add_condition('function', check_voice_leading, None)\
        .add_condition('function', check_functional_harmony, None)\
        .set_sequence(['C', 'F', 'G7', 'F'])\
        .build()

    result = invalid_rule.evaluate(invalid_prog)
    print(f"Invalid progression (V7->IV) valid: {result[0]}")
    print("Progression: C -> F -> G7 -> F (should be invalid)\n")

    # Test jazz ii-V-I progression
    print("Testing Jazz ii-V-I Progression...")
    jazz_prog = [
        create_chord("Dm7"),    # ii7
        create_chord("G7"),     # V7
        create_chord("Cmaj7")   # Imaj7
    ]

    # Create a rule that validates jazz harmony
    jazz_rule = RuleBuilder()\
        .add_condition('function', check_voice_leading, None)\
        .add_condition('function', check_functional_harmony, None)\
        .add_condition('root', check_secondary_dominant, None)\
        .set_sequence(['Dm7', 'G7', 'Cmaj7'])\
        .build()

    result = jazz_rule.evaluate(jazz_prog)
    print(f"Jazz ii-V-I progression valid: {result[0]}")
    print("Progression: Dm7 -> G7 -> Cmaj7\n")

    # Performance metrics
    print("Performance:")
    avg_time, avg_memory, _, _ = jazz_rule.profile(
        test_sequences=[jazz_prog],
        runs=5
    )
    print(f"Average validation time: {avg_time*1000:.3f}ms")
    print(f"Memory usage: {avg_memory:.2f}KB")


if __name__ == "__main__":
    main()
