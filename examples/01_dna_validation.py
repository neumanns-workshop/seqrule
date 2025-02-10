"""
Example 01: DNA Sequence Validation
=================================

This example demonstrates how to use seqrule to validate DNA sequences,
including biologically relevant patterns and properties:
- Base pairing rules (A-T, G-C) for double-stranded DNA
- GC content analysis in sequence windows
- Common regulatory elements (TATA box)
"""

import logging

from seqrule import Object, RuleBuilder

# Set up logging - only show INFO and above, with a cleaner format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

# Disable debug logging for specific modules
logging.getLogger('seqrule.generators').setLevel(logging.ERROR)
logging.getLogger('seqrule.objects').setLevel(logging.ERROR)
logging.getLogger('seqrule.analyses').setLevel(logging.ERROR)
logging.getLogger('seqrule.evaluators').setLevel(logging.WARNING)


def check_base_pairing(obj, context):
    """Check if bases can form valid pairs in double-stranded DNA."""
    curr_base = obj.get('base')
    idx = context['index']
    sequence = context['sequence']

    # Only check pairs at even positions (0-1, 2-3, 4-5)
    if idx % 2 == 0:
        # If we're at the last position, no need to check pairing
        if idx + 1 >= len(sequence):
            return True
        next_base = sequence[idx + 1].get('base')
        # Define valid base pairs
        pairs = {
            'A': 'T',  # Adenine-Thymine
            'T': 'A',
            'G': 'C',  # Guanine-Cytosine
            'C': 'G'
        }
        # Check if bases form a valid pair
        result = (
            pairs.get(curr_base) == next_base or
            pairs.get(next_base) == curr_base
        )
        if not result:
            print(
                f"Invalid base pair at positions {idx+1}-{idx+2}: "
                f"{curr_base}-{next_base}"
            )
        return result
    return True  # Odd positions are checked when processing the previous even position


def check_gc_content(obj, context):
    """Check if GC content is within biological range."""
    window_size = 4
    idx = context['index']
    sequence = context['sequence']

    # Get bases in current window
    start = max(0, idx - window_size + 1)
    window = sequence[start:idx + 1]

    # Skip check if window is too small
    if len(window) < window_size:
        return True

    # Get window sequence
    bases = ''.join(obj.get('base') for obj in window)

    # Skip GC content check for TATA box regions
    if 'TATA' in bases:
        print(f"Skipping GC check for TATA box at position {idx+1}")
        return True

    # Count GC content
    gc_bases = ['G', 'C']
    gc_count = sum(1 for obj in window if obj.get('base') in gc_bases)
    gc_percent = (gc_count / len(window)) * 100

    # More lenient GC content range for short sequences
    min_gc = 15 if len(window) < window_size else 20
    max_gc = 85 if len(window) < window_size else 80

    # Print debug info for GC content
    if gc_percent < min_gc or gc_percent > max_gc:
        print(
            f"GC content {gc_percent:.1f}% at position {idx+1} "
            f"(window: {bases})"
        )

    return min_gc <= gc_percent <= max_gc


def check_tata_box(obj, context):
    """Check for TATA box promoter sequence."""
    idx = context['index']
    sequence = context['sequence']

    # Need at least 4 bases for TATA box
    if idx + 3 >= len(sequence):
        return False

    # Get next 4 bases
    bases = [sequence[idx + i].get('base') for i in range(4)]
    return ''.join(bases) == 'TATA'


# Create DNA validation rule
rule = RuleBuilder()\
    .add_condition('base', 'in', ['A', 'T', 'C', 'G'])\
    .add_condition('base', check_base_pairing, None)\
    .add_condition('base', check_gc_content, None)\
    .set_sequence(['pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6'])\
    .build()

print("\nTesting DNA sequences:")

# Test valid sequence (TATA box followed by GC-rich region)
valid_sequence = [
    Object('pos1', base='T'),  # Start of TATA box
    Object('pos2', base='A'),  # Valid pair with T
    Object('pos3', base='T'),  # Valid pair with A
    Object('pos4', base='A'),  # Valid pair with T
    Object('pos5', base='G'),  # Start GC-rich region
    Object('pos6', base='C')   # Valid pair with G
]

result = rule.evaluate(valid_sequence)
print("Valid sequence:", result)

# Test invalid base pairing
invalid_pairs = [
    Object('pos1', base='A'),
    Object('pos2', base='A'),  # Invalid - should pair with T
    Object('pos3', base='T'),
    Object('pos4', base='T'),  # Invalid - should pair with A
    Object('pos5', base='G'),
    Object('pos6', base='G')   # Invalid - should pair with C
]

result = rule.evaluate(invalid_pairs)
print("Invalid base pairs:", result)

# Test invalid GC content
invalid_gc = [
    Object('pos1', base='G'),
    Object('pos2', base='G'),  # Too much GC content
    Object('pos3', base='C'),
    Object('pos4', base='C'),
    Object('pos5', base='G'),
    Object('pos6', base='C')
]

result = rule.evaluate(invalid_gc)
print("Invalid GC content:", result)

# Analyze rule complexity
print("\nRule complexity analysis:")
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
print("\nPerformance metrics:")
avg_time, avg_memory, _, _ = rule.profile(
    [valid_sequence, invalid_pairs, invalid_gc],
    runs=5  # Reduced number of runs
)
print(f"Average execution time: {avg_time:.6f} seconds")
print(f"Average memory usage: {avg_memory:.2f} KB")
