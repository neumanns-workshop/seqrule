"""
Example 05: Turkish Phonology
===========================

This example demonstrates how to use seqrule to validate Turkish phonological
rules, including:
- Vowel harmony (both two-way and four-way) for suffixes
- Consonant assimilation and final devoicing
- Syllable structure constraints
"""

import logging

from seqrule import Object, RuleBuilder

# Set up logging
logging.basicConfig(level=logging.INFO)


# Define Turkish phoneme sets
FRONT_VOWELS = {'e', 'i', 'ö', 'ü'}
BACK_VOWELS = {'a', 'ı', 'o', 'u'}
UNROUNDED_VOWELS = {'e', 'i', 'a', 'ı'}
ROUNDED_VOWELS = {'ö', 'ü', 'o', 'u'}
HIGH_VOWELS = {'i', 'ı', 'ü', 'u'}
LOW_VOWELS = {'e', 'a', 'ö', 'o'}
ALL_VOWELS = FRONT_VOWELS | BACK_VOWELS

VOICED_STOPS = {'b', 'd', 'g', 'c'}
VOICELESS_STOPS = {'p', 't', 'k', 'ç'}
CONTINUANTS = {'f', 'v', 's', 'z', 'ş', 'j', 'h'}
SONORANTS = {'m', 'n', 'r', 'l', 'y'}
ALL_CONSONANTS = VOICED_STOPS | VOICELESS_STOPS | CONTINUANTS | SONORANTS


def create_syllable(phonemes: str, name: str = None, **properties) -> Object:
    """Create a syllable object with phonological properties."""
    # Extract onset (initial consonants), nucleus (vowel), and coda
    nucleus_idx = next(
        (i for i, p in enumerate(phonemes) if p in ALL_VOWELS),
        -1
    )
    if nucleus_idx == -1:
        raise ValueError(f"No vowel found in syllable: {phonemes}")

    onset = phonemes[:nucleus_idx]
    nucleus = phonemes[nucleus_idx]
    coda = phonemes[nucleus_idx + 1:]

    # Set syllable properties
    properties.update({
        'onset': onset,
        'nucleus': nucleus,
        'coda': coda,
        'phonemes': phonemes,
        'is_front': nucleus in FRONT_VOWELS,
        'is_back': nucleus in BACK_VOWELS,
        'is_rounded': nucleus in ROUNDED_VOWELS,
        'is_high': nucleus in HIGH_VOWELS
    })

    return Object(name or phonemes, **properties)


def check_vowel_harmony(obj, context):
    """Check if vowel harmony rules are followed for suffixes."""
    if not context['prev']:
        return True  # First syllable can have any vowel

    prev = context['prev'].get('nucleus')
    curr = obj.get('nucleus')

    # Only check harmony for suffixes
    suffixes = ['lar', 'ler', 'lık', 'lik', 'luk', 'lük']  # Common suffixes
    if obj.get('phonemes') not in suffixes:
        return True

    # Two-way (e/a) harmony
    if prev in ['e', 'i', 'ö', 'ü']:  # Front vowels
        if curr in ['a', 'ı', 'o', 'u']:  # Back vowels
            print(f"Vowel harmony error: {prev} (front) -> {curr} (back)")
            return False
    elif prev in ['a', 'ı', 'o', 'u']:  # Back vowels
        if curr in ['e', 'i', 'ö', 'ü']:  # Front vowels
            print(f"Vowel harmony error: {prev} (back) -> {curr} (front)")
            return False

    # Four-way (i/ı/ü/u) harmony for high vowels
    if curr in ['i', 'ı', 'ü', 'u']:  # High vowels
        if prev in ['e', 'i']:  # Front unrounded
            if curr not in ['i', 'e']:
                print(f"Vowel harmony error: {prev} (front) -> {curr}")
                return False
        elif prev in ['ö', 'ü']:  # Front rounded
            if curr not in ['ü', 'ö']:
                print(f"Vowel harmony error: {prev} (rounded) -> {curr}")
                return False
        elif prev in ['a', 'ı']:  # Back unrounded
            if curr not in ['ı', 'a']:
                print(f"Vowel harmony error: {prev} (back) -> {curr}")
                return False
        elif prev in ['o', 'u']:  # Back rounded
            if curr not in ['u', 'o']:
                print(f"Vowel harmony error: {prev} (rounded) -> {curr}")
                return False

    return True


def check_consonant_rules(obj, context):
    """Check Turkish consonant rules (final devoicing and assimilation)."""
    coda = obj.get('coda')
    if not coda:
        return True

    # Final devoicing: voiced stops become voiceless in coda
    final_consonant = coda[-1]
    if final_consonant in VOICED_STOPS:
        print(
            "Final devoicing violation: "
            f"voiced stop {final_consonant} in coda"
        )
        return False

    # Consonant assimilation in clusters
    if len(coda) > 1:
        for i in range(len(coda) - 1):
            c1, c2 = coda[i], coda[i + 1]
            # Voice assimilation: obstruent clusters must agree in voicing
            if c1 in VOICED_STOPS and c2 in VOICELESS_STOPS:
                print(f"Voice assimilation violation: {c1}{c2}")
                return False
            if c1 in VOICELESS_STOPS and c2 in VOICED_STOPS:
                print(f"Voice assimilation violation: {c1}{c2}")
                return False

    return True


def check_syllable_structure(obj, context):
    """Check if syllable follows Turkish phonotactic constraints."""
    onset = obj.get('onset')
    coda = obj.get('coda')

    # Onset constraints
    if len(onset) > 1:
        # Turkish generally doesn't allow complex onsets
        print(f"Invalid onset cluster: {onset}")
        return False

    # Coda constraints
    if len(coda) > 2:
        # Maximum two consonants in coda
        print(f"Invalid coda cluster: {coda}")
        return False

    # Sonority sequencing in coda clusters
    if len(coda) == 2:
        c1, c2 = coda[0], coda[1]
        if c1 in SONORANTS and c2 not in SONORANTS:
            # Sonorants should come after obstruents in coda
            print(f"Invalid sonority sequence in coda: {c1}{c2}")
            return False

    return True


def main():
    """Example usage of Turkish phonology validation."""
    print("Turkish Phonology Validation Example")
    print("===================================\n")

    # Test vowel harmony
    print("Testing Vowel Harmony...")
    harmony_test = [
        create_syllable("ka"),    # Back unrounded
        create_syllable("lem"),   # Front unrounded - violation!
        create_syllable("lar")    # Back unrounded
    ]

    harmony_rule = RuleBuilder()\
        .add_condition('nucleus', check_vowel_harmony, None)\
        .set_sequence(['ka', 'lem', 'lar'])\
        .build()

    result = harmony_rule.evaluate(harmony_test)
    print(f"Vowel harmony test result: {result[0]}\n")

    # Test consonant rules
    print("Testing Consonant Rules...")
    consonant_test = [
        create_syllable("kitb"),   # Final voiced stop - violation!
        create_syllable("renk"),   # Valid final cluster
        create_syllable("kent")    # Valid final cluster
    ]

    consonant_rule = RuleBuilder()\
        .add_condition('coda', check_consonant_rules, None)\
        .set_sequence(['kitb', 'renk', 'kent'])\
        .build()

    result = consonant_rule.evaluate(consonant_test)
    print(f"Consonant rules test result: {result[0]}\n")

    # Test syllable structure
    print("Testing Syllable Structure...")
    structure_test = [
        create_syllable("tre"),    # Complex onset - violation!
        create_syllable("kalp"),   # Valid CVC
        create_syllable("türk")    # Valid CVC
    ]

    structure_rule = RuleBuilder()\
        .add_condition('phonemes', check_syllable_structure, None)\
        .set_sequence(['tre', 'kalp', 'türk'])\
        .build()

    result = structure_rule.evaluate(structure_test)
    print(f"Syllable structure test result: {result[0]}\n")

    # Test all rules together with a valid word
    print("Testing Valid Turkish Word...")
    valid_word = [
        create_syllable("ki"),    # High front unrounded
        create_syllable("tap"),   # Back unrounded, final devoicing
        create_syllable("lar")    # Back unrounded
    ]

    word_rule = RuleBuilder()\
        .add_condition('nucleus', check_vowel_harmony, None)\
        .add_condition('coda', check_consonant_rules, None)\
        .add_condition('phonemes', check_syllable_structure, None)\
        .set_sequence(['ki', 'tap', 'lar'])\
        .build()

    result = word_rule.evaluate(valid_word)
    print(f"Valid word 'kitaplar' test result: {result[0]}")

    # Performance metrics
    print("\nPerformance:")
    avg_time, avg_memory, _, _ = word_rule.profile(
        test_sequences=[valid_word],
        runs=5
    )
    print(f"Average validation time: {avg_time*1000:.3f}ms")
    print(f"Memory usage: {avg_memory:.2f}KB")


if __name__ == "__main__":
    main()
