"""
seqrule - A library for defining and generating rules to validate
sequences of objects.

The library provides two main workflows:

1. Define rules using a fluent builder pattern:
    rule = RuleBuilder()\\
        .add_condition("rank", ">", 0)\\
        .add_condition("suit", "in", ["hearts", "spades"])\\
        .set_sequence(["ace", "king"])\\
        .build()

2. Generate and use rule functions:
    # Rule function is generated internally during build()
    result = rule.evaluate(sequence)
    metrics = rule.analyze_complexity()

Example usage:
    from seqrule import RuleBuilder, Object

    # Create objects to validate
    cards = [
        Object("ace", rank=1, suit="hearts"),
        Object("king", rank=13, suit="spades")
    ]

    # Define and generate a rule
    rule = RuleBuilder()\\
        .add_condition("rank", ">", 0)\\
        .add_condition("suit", "in", ["hearts", "spades"])\\
        .set_sequence(["ace", "king"])\\
        .build()

    # Evaluate the sequence
    result = rule.evaluate(cards)

    # Analyze rule complexity
    metrics = rule.analyze_complexity()
    print(metrics)
"""

from .analyses import (
    analyze_rule_complexity,
    compute_branching_factor,
    compute_condition_impact,
    compute_custom_complexity_score,
    compute_entropy,
    compute_redundancy,
    count_categorical_constraints,
    count_numerical_constraints,
    detect_contradictions,
    estimate_execution_cost,
)
from .constraints import enforce_constraints
from .evaluators import batch_evaluate, evaluate_rule, profile_rule_execution
from .generators import sequence_rule_generator
from .logging_config import set_logging_level, setup_logging
from .objects import Object

__version__ = "1.0.0"


class RuleBuilder:
    """Builder for creating sequence validation rules."""

    def __init__(self):
        self.conditions = []
        self.sequence_constraints = []
        self._rule_func = None

    def add_condition(self, property_name, operator, value):
        """Add a condition to the rule.

        Args:
            property_name (str): Name of the property to check
            operator (str): One of: =, !=, <, >, <=, >=, in, not in,
                exists, not exists
            value: The value to compare against
        """
        self.conditions.append((property_name, operator, value))
        return self

    def set_sequence(self, sequence):
        """Set the required sequence order.

        Args:
            sequence (list[str]): List of object names in required order
        """
        self.sequence_constraints = sequence
        return self

    def build(self, verbose=False):
        """Build and return the rule."""
        self._rule_func = sequence_rule_generator(
            self.conditions,
            self.sequence_constraints,
            verbose=verbose
        )
        return Rule(
            self._rule_func,
            self.conditions,
            self.sequence_constraints
        )


class Rule:
    """A compiled sequence validation rule."""

    def __init__(self, rule_func, conditions, sequence_constraints):
        self._rule_func = rule_func
        self.conditions = conditions
        self.sequence_constraints = sequence_constraints

    def evaluate(self, sequence):
        """Evaluate if a sequence matches this rule.

        Args:
            sequence (list[Object]): List of objects to evaluate

        Returns:
            bool: True if sequence matches rule conditions and order
        """
        result = self._rule_func(sequence)
        # Handle both tuple returns (result, message) and direct boolean returns
        if isinstance(result, tuple):
            return result[0]
        return result

    def batch_evaluate(self, sequences):
        """Evaluate multiple sequences against this rule.

        Args:
            sequences (list[list[Object]]): List of sequences to evaluate

        Returns:
            list[bool]: Results for each sequence
        """
        return [self.evaluate(seq) for seq in sequences]

    def analyze_complexity(self, model="weighted"):
        """Analyze the complexity of this rule.

        Args:
            model (str): Complexity model to use: weighted, entropy_based,
                normalized

        Returns:
            dict: Complexity metrics
        """
        return analyze_rule_complexity(
            self._rule_func,
            self.conditions,
            self.sequence_constraints,
            model=model
        )

    def profile(self, test_sequences, runs=10):
        """Profile the performance of this rule.

        Args:
            test_sequences (list[list[Object]]): Sequences to test with
            runs (int): Number of profiling runs

        Returns:
            tuple: (avg_time, avg_memory, per_sequence_times,
                   per_sequence_memory)
        """
        return profile_rule_execution(
            self._rule_func,
            test_sequences,
            runs=runs
        )


__all__ = [
    "Object",
    "RuleBuilder",
    "Rule",
    "sequence_rule_generator",
    "analyze_rule_complexity",
    "compute_custom_complexity_score",
    "compute_entropy",
    "compute_branching_factor",
    "compute_redundancy",
    "estimate_execution_cost",
    "detect_contradictions",
    "count_categorical_constraints",
    "count_numerical_constraints",
    "compute_condition_impact",
    "evaluate_rule",
    "batch_evaluate",
    "profile_rule_execution",
    "enforce_constraints",
    "setup_logging",
    "set_logging_level"
]
