# Rule Analysis Report

## Summary

| Rule                         | Time Complexity   | Space Complexity   |   Raw Score |   Normalized Score |   Property Accesses |
|:-----------------------------|:------------------|:-------------------|------------:|-------------------:|--------------------:|
| create_meta_rule             | O(n)              | O(1)               |       30.63 |               51   |                   0 |
| create_alternation_rule      | O(n)              | O(1)               |       24.25 |               40.4 |                   2 |
| create_historical_rule       | O(n)              | O(1)               |       48.05 |               80.1 |                   0 |
| create_balanced_rule         | O(n²)             | O(n)               |       30.54 |               50.9 |                   1 |
| create_numerical_range_rule  | O(n)              | O(1)               |       24.25 |               40.4 |                   1 |
| create_group_rule            | O(n)              | O(1)               |       36.75 |               61.3 |                   0 |
| create_composite_rule        | O(n)              | O(n)               |        9    |               15   |                   0 |
| create_bounded_sequence_rule | O(1)              | O(1)               |       46    |               76.7 |                   0 |
| create_property_trend_rule   | O(n)              | O(n)               |       19.32 |               32.2 |                   1 |
| create_ratio_rule            | O(n)              | O(n)               |       30.6  |               51   |                   8 |
| create_pattern_rule          | O(n)              | O(n)               |       39.4  |               65.7 |                   4 |
| create_property_match_rule   | O(n)              | O(1)               |       51.26 |               85.4 |                   3 |
| create_transition_rule       | O(n)              | O(1)               |       30.6  |               51   |                   1 |
| create_unique_property_rule  | O(n)              | O(n)               |       39.4  |               65.7 |                   1 |
| create_property_cycle_rule   | O(n²)             | O(n)               |       51.26 |               85.4 |                   0 |



## create_dependency_rule

⚠️ Error: Failed to analyze rule: Undefined variable in rule: e
Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 499, in analyze
    raise AnalysisError(f"Undefined variable in rule: {undefined_var}")
seqrule.analysis.base.AnalysisError: Undefined variable in rule: e

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/scripts/analyze_rules.py", line 482, in analyze_rule_generator
    analysis = analyzer.analyze(example_rule)
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 608, in analyze
    raise AnalysisError(f"Failed to analyze rule: {str(e)}") from e
seqrule.analysis.base.AnalysisError: Failed to analyze rule: Undefined variable in rule: e



## create_meta_rule

**Signature:** `(rules: List[seqrule.dsl.DSLRule], required_count: int) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring a certain number of other rules to be satisfied.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.043 |     0.013 |                  0 |                0 |
|               1 |           0.046 |     0.015 |                  0 |                0 |
|              10 |           0.043 |     0.016 |                  0 |                0 |
|             100 |           0.051 |     0.015 |                  0 |                0 |
|            1000 |           0.039 |     0.013 |                  0 |                0 |



Size-Time Correlation: 0.385

- Correlation interpretation:
  - Weak or no correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 51.0

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 9.2
- ast_node_count: 80.0
- bottleneck_count: 0.0

### Example Usage

```python
From docstring:
    any_two = create_meta_rule([rule1, rule2, rule3], 2)  # Any 2 must pass
```


## create_alternation_rule

**Signature:** `(property_name: str) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring alternating property values.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Property Access Patterns

Total Property Accesses: 2

#### Property: `property_name`

- Access Count: 2
- Access Types: PropertyAccessType.METHOD



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.012 |     0.002 |                  0 |                0 |
|               1 |           0.014 |     0.003 |                  0 |                0 |
|              10 |           0.041 |     0.011 |                  0 |                0 |
|             100 |           0.111 |     0.01  |                  0 |                0 |
|            1000 |           1.265 |     0.657 |                  0 |                6 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 40.4

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 40.0
- property_access_complexity: 0.0
- ast_node_count: 80.0
- bottleneck_count: 0.0

### Optimization Suggestions

- Consider caching property lookups to avoid repeated access
- Properties property_name are accessed frequently. Consider caching them.

### Example Usage

```python
From docstring:
    alternating_colors = create_alternation_rule("color")
```


## create_historical_rule

**Signature:** `(window: int, condition: Callable[[List[seqrule.core.AbstractObject]], bool]) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule checking a condition over a sliding window.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.015 |     0.005 |                  0 |                0 |
|               1 |           0.021 |     0.005 |                  0 |                0 |
|              10 |           0.046 |     0.031 |                  0 |                0 |
|             100 |           0.17  |     0.077 |                  0 |                0 |
|            1000 |           0.785 |     0.035 |                  0 |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.EXTREME
- Normalized Score: 80.1

Contributing Factors:
- time_complexity: 60.0
- space_complexity: 30.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 92.6
- bottleneck_count: 30.0

### Example Usage

```python
From docstring:
    def no_repeats(window): return len(set(obj["value"] for obj in window)) == len(window)
    unique_values = create_historical_rule(3, no_repeats)
```


## create_balanced_rule

**Signature:** `(property_name: str, groups: Dict[Any, Set[Any]], tolerance: float = 0.1) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring balanced representation of property value groups.


### Complexity Analysis

- Time Complexity: O(n²)
- Space Complexity: O(n)
- Description: contains 4 loops with 1 nested loops. uses 1 comprehensions. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Property Access Patterns

Total Property Accesses: 1

#### Property: `property_name`

- Access Count: 1
- Access Types: PropertyAccessType.READ



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.014 |     0.007 |                  0 |                0 |
|               1 |           0.033 |     0.015 |                  0 |                0 |
|              10 |           0.08  |     0.031 |                  0 |                0 |
|             100 |           0.257 |     0.15  |                  0 |                0 |
|            1000 |           1.748 |     1.077 |                  0 |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 50.9

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 80.0
- bottleneck_count: 0.0

### Optimization Suggestions

- High time complexity detected (O(n²)). Consider using a more efficient algorithm
- High complexity bottlenecks identified: Memory usage from temporary collections
- Consider caching property lookups to avoid repeated access

### Example Usage

```python
From docstring:
    # Equal number of red and black cards (±10%)
    balanced_colors = create_balanced_rule("color", {
        "red": {"red"}, "black": {"black"}
    })
```


## create_numerical_range_rule

**Signature:** `(property_name: str, min_value: float, max_value: float) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring numerical property values within a range.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Property Access Patterns

Total Property Accesses: 1

#### Property: `property_name`

- Access Count: 1
- Access Types: PropertyAccessType.METHOD



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.011 |     0.005 |               0    |                0 |
|               1 |           0.02  |     0.006 |               0    |                0 |
|              10 |           0.024 |     0.005 |               0    |                0 |
|             100 |           0.022 |     0.006 |               0    |                0 |
|            1000 |           0.02  |     0.007 |               0.07 |                0 |



Size-Time Correlation: 0.495

- Correlation interpretation:
  - Weak or no correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 40.4

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 40.0
- property_access_complexity: 0.0
- ast_node_count: 80.0
- bottleneck_count: 0.0

### Optimization Suggestions

- Consider caching property lookups to avoid repeated access

### Example Usage

```python
From docstring:
    valid_temperature = create_numerical_range_rule("temperature", 20, 30)
```


## create_group_rule

**Signature:** `(group_size: int, condition: Callable[[List[seqrule.core.AbstractObject]], bool]) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule checking a condition over groups of consecutive objects.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.015 |     0.006 |                  0 |                0 |
|               1 |           0.022 |     0.013 |                  0 |                0 |
|              10 |           0.044 |     0.02  |                  0 |                0 |
|             100 |           0.12  |     0.057 |                  0 |                0 |
|            1000 |           1.795 |     1.295 |                  0 |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.COMPLEX
- Normalized Score: 61.3

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 30.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 0.0
- ast_node_count: 80.0
- bottleneck_count: 30.0

### Example Usage

```python
From docstring:
    def ascending(group):
        return all(group[i]["value"] < group[i+1]["value"]
                  for i in range(len(group)-1))
    ascending_pairs = create_group_rule(2, ascending)
```


## create_composite_rule

**Signature:** `(rules: List[seqrule.dsl.DSLRule], mode: str = 'all') -> seqrule.dsl.DSLRule`

**Description:** Creates a rule that combines multiple rules with AND/OR logic.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(n)
- Description: contains 1 loops. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.036 |     0.013 |               0    |                0 |
|               1 |           0.037 |     0.011 |               0    |                0 |
|              10 |           0.034 |     0.011 |               0    |                0 |
|             100 |           0.05  |     0.012 |               0    |                0 |
|            1000 |           0.027 |     0.01  |               0.02 |                0 |



Size-Time Correlation: -0.433

- Correlation interpretation:
  - Weak or no correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.TRIVIAL
- Normalized Score: 15.0

Contributing Factors:
- time_complexity: 0.0
- space_complexity: 0.0
- cyclomatic_complexity: 20.0
- property_access_complexity: 0.0
- ast_node_count: 40.0
- bottleneck_count: 0.0

### Optimization Suggestions

- High complexity bottlenecks identified: Memory usage from temporary collections

### Example Usage

```python
From docstring:
    all_rules = create_composite_rule([rule1, rule2], mode="all")
    any_rule = create_composite_rule([rule1, rule2], mode="any")
```


## create_bounded_sequence_rule

**Signature:** `(min_length: int, max_length: int, inner_rule: seqrule.dsl.DSLRule) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule that combines length constraints with another rule.


### Complexity Analysis

- Time Complexity: O(1)
- Space Complexity: O(1)
- Description: .

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.014 |     0.004 |                  0 |                0 |
|               1 |           0.032 |     0.011 |                  0 |                0 |
|              10 |           0.036 |     0.009 |                  0 |                0 |
|             100 |           0.015 |     0.003 |                  0 |                0 |
|            1000 |           0.012 |     0.003 |                  0 |                0 |



Size-Time Correlation: -0.341

- Correlation interpretation:
  - Weak or no correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.COMPLEX
- Normalized Score: 76.7

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 30.0
- cyclomatic_complexity: 84.0
- property_access_complexity: 8.6
- ast_node_count: 99.6
- bottleneck_count: 30.0

### Example Usage

```python
From docstring:
    valid_sequence = create_bounded_sequence_rule(2, 5, pattern_rule)
```


## create_running_stat_rule

⚠️ Error: Failed to analyze rule: Undefined variable in rule: ZeroDivisionError
Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 499, in analyze
    raise AnalysisError(f"Undefined variable in rule: {undefined_var}")
seqrule.analysis.base.AnalysisError: Undefined variable in rule: ZeroDivisionError

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/scripts/analyze_rules.py", line 482, in analyze_rule_generator
    analysis = analyzer.analyze(example_rule)
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 608, in analyze
    raise AnalysisError(f"Failed to analyze rule: {str(e)}") from e
seqrule.analysis.base.AnalysisError: Failed to analyze rule: Undefined variable in rule: ZeroDivisionError



## create_sum_rule

⚠️ Error: Failed to analyze rule: Undefined variable in rule: target
Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 499, in analyze
    raise AnalysisError(f"Undefined variable in rule: {undefined_var}")
seqrule.analysis.base.AnalysisError: Undefined variable in rule: target

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/runner/work/seqrule/seqrule/scripts/analyze_rules.py", line 482, in analyze_rule_generator
    analysis = analyzer.analyze(example_rule)
  File "/home/runner/work/seqrule/seqrule/src/seqrule/analysis/analyzer.py", line 608, in analyze
    raise AnalysisError(f"Failed to analyze rule: {str(e)}") from e
seqrule.analysis.base.AnalysisError: Failed to analyze rule: Undefined variable in rule: target



## create_property_trend_rule

**Signature:** `(property_name: str, trend: str = 'increasing') -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring property values to follow a trend.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(n)
- Description: contains 2 loops. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Property Access Patterns

Total Property Accesses: 1

#### Property: `property_name`

- Access Count: 1
- Access Types: PropertyAccessType.READ



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.011 |     0.002 |               0.02 |                7 |
|               1 |           0.014 |     0.006 |               0    |               21 |
|              10 |           0.058 |     0.026 |               0    |                0 |
|             100 |           0.264 |     0.05  |               0    |                0 |
|            1000 |           2.835 |     1.549 |               0    |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.SIMPLE
- Normalized Score: 32.2

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 20.0
- property_access_complexity: 13.8
- ast_node_count: 60.0
- bottleneck_count: 0.0

### Optimization Suggestions

- High complexity bottlenecks identified: Memory usage from temporary collections
- Consider caching property lookups to avoid repeated access

### Example Usage

```python
From docstring:
    # Values must strictly increase
    increasing = create_property_trend_rule("value", "increasing")
    # Values must be non-increasing
    non_increasing = create_property_trend_rule("value", "non-increasing")
```


## create_ratio_rule

**Signature:** `(property_name: str, min_ratio: float, max_ratio: float, filter_rule: Optional[Callable[[seqrule.core.AbstractObject], bool]] = None) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring a ratio of objects meeting a condition to be within a range.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(n)
- Description: contains 3 loops. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Property Access Patterns

Total Property Accesses: 8

#### Property: `property_name`

- Access Count: 8
- Access Types: PropertyAccessType.CONDITIONAL, PropertyAccessType.COMPARISON, PropertyAccessType.READ



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.014 |     0.007 |               0    |                0 |
|               1 |           0.028 |     0.006 |               0    |                0 |
|              10 |           0.06  |     0.016 |               0    |                0 |
|             100 |           0.15  |     0.018 |               0    |                0 |
|            1000 |           1.036 |     0.074 |               0.01 |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 51.0

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 80.6
- bottleneck_count: 0.0

### Optimization Suggestions

- High complexity bottlenecks identified: Memory usage from temporary collections
- Consider caching property lookups to avoid repeated access
- Properties property_name are accessed frequently. Consider caching them.

### Example Usage

```python
From docstring:
    # At least 40% but no more than 60% GC content
    gc_content = create_ratio_rule("base", 0.4, 0.6, lambda obj: obj["base"] in ["G", "C"])
```


## create_pattern_rule

**Signature:** `(pattern: List[Any], property_name: str) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring property values to match a specific pattern.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(n)
- Description: contains 4 loops. uses 2 comprehensions. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Property Access Patterns

Total Property Accesses: 4

#### Property: `property_name`

- Access Count: 4
- Access Types: PropertyAccessType.CONDITIONAL, PropertyAccessType.METHOD



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.014 |     0.007 |               0.08 |                0 |
|               1 |           0.051 |     0.018 |               0    |                0 |
|              10 |           0.049 |     0.015 |               0.01 |                0 |
|             100 |           0.108 |     0.031 |               0.01 |                0 |
|            1000 |           0.429 |     0.039 |               0.03 |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.COMPLEX
- Normalized Score: 65.7

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 30.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 93.6
- bottleneck_count: 30.0

### Optimization Suggestions

- High complexity bottlenecks identified: Memory usage from temporary collections
- Consider caching property lookups to avoid repeated access
- Properties property_name are accessed frequently. Consider caching them.

### Example Usage

```python
From docstring:
    color_pattern = create_pattern_rule(["red", "black", "red"], "color")
```


## create_property_match_rule

**Signature:** `(property_name: str, value: Any) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring objects to have a specific property value.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Property Access Patterns

Total Property Accesses: 3

#### Property: `property_name`

- Access Count: 3
- Access Types: PropertyAccessType.CONDITIONAL, PropertyAccessType.COMPARISON, PropertyAccessType.METHOD



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.019 |     0.008 |               0    |                0 |
|               1 |           0.023 |     0.003 |               0    |                0 |
|              10 |           0.029 |     0.01  |               0.03 |                0 |
|             100 |           0.023 |     0.003 |               0    |                0 |
|            1000 |           0.028 |     0.009 |               0.02 |                0 |



Size-Time Correlation: 0.474

- Correlation interpretation:
  - Weak or no correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.EXTREME
- Normalized Score: 85.4

Contributing Factors:
- time_complexity: 60.0
- space_complexity: 30.0
- cyclomatic_complexity: 80.0
- property_access_complexity: 0.0
- ast_node_count: 87.6
- bottleneck_count: 30.0

### Optimization Suggestions

- Consider caching property lookups to avoid repeated access
- Properties property_name are accessed frequently. Consider caching them.

### Example Usage

```python
From docstring:
    color_is_red = create_property_match_rule("color", "red")
```


## create_transition_rule

**Signature:** `(property_name: str, valid_transitions: Dict[Any, Set[Any]]) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule enforcing valid transitions between property values.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(1)
- Description: contains 1 loops.

### Property Access Patterns

Total Property Accesses: 1

#### Property: `property_name`

- Access Count: 1
- Access Types: PropertyAccessType.READ



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.016 |     0.005 |               0    |                0 |
|               1 |           0.015 |     0.003 |               0    |                0 |
|              10 |           0.025 |     0.006 |               0    |                0 |
|             100 |           0.066 |     0.009 |               0.01 |                0 |
|            1000 |           0.481 |     0.047 |               0    |                0 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.MODERATE
- Normalized Score: 51.0

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 0.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 80.6
- bottleneck_count: 0.0

### Optimization Suggestions

- Consider caching property lookups to avoid repeated access

### Example Usage

```python
From docstring:
    # Valid note transitions in a scale
    scale_rule = create_transition_rule("pitch", {
        "C": {"D"}, "D": {"E"}, "E": {"F"}, "F": {"G"},
        "G": {"A"}, "A": {"B"}, "B": {"C"}
    })
```


## create_unique_property_rule

**Signature:** `(property_name: str, scope: str = 'global') -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring property values to be unique within a scope.


### Complexity Analysis

- Time Complexity: O(n)
- Space Complexity: O(n)
- Description: contains 2 loops. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Property Access Patterns

Total Property Accesses: 1

#### Property: `property_name`

- Access Count: 1
- Access Types: PropertyAccessType.READ



### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.01  |     0.003 |               0    |                0 |
|               1 |           0.034 |     0.006 |               0    |                0 |
|              10 |           0.036 |     0.004 |               0    |                0 |
|             100 |           0.098 |     0.02  |               0.02 |                0 |
|            1000 |           0.664 |     0.038 |               0.05 |                8 |



Size-Time Correlation: 1.000

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.COMPLEX
- Normalized Score: 65.7

Contributing Factors:
- time_complexity: 25.0
- space_complexity: 30.0
- cyclomatic_complexity: 60.0
- property_access_complexity: 8.6
- ast_node_count: 93.6
- bottleneck_count: 30.0

### Optimization Suggestions

- High complexity bottlenecks identified: Memory usage from temporary collections
- Consider caching property lookups to avoid repeated access

### Example Usage

```python
From docstring:
    # No duplicate IDs globally
    unique_ids = create_unique_property_rule("id", scope="global")
    # No adjacent duplicate values
    no_adjacent = create_unique_property_rule("value", scope="adjacent")
```


## create_property_cycle_rule

**Signature:** `(*properties: str) -> seqrule.dsl.DSLRule`

**Description:** Creates a rule requiring objects to cycle through property values.


### Complexity Analysis

- Time Complexity: O(n²)
- Space Complexity: O(n)
- Description: contains 4 loops with 2 nested loops. uses 1 comprehensions. creates temporary collections.
- Bottlenecks:
  - Memory usage from temporary collections

### Performance Analysis

|   Sequence Size |   Avg Time (ms) |   Std Dev |   Peak Memory (MB) |   GC Collections |
|----------------:|----------------:|----------:|-------------------:|-----------------:|
|               0 |           0.015 |     0.007 |               0    |                0 |
|               1 |           0.032 |     0.014 |               0    |                0 |
|              10 |           0.054 |     0.025 |               0    |                0 |
|             100 |           0.307 |     0.031 |               0    |                0 |
|            1000 |         188.945 |   209.15  |               0.02 |                0 |



Size-Time Correlation: 0.995

- Correlation interpretation:
  - Strong correlation between sequence size and execution time

### Rule Scoring

- Complexity Level: ComplexityScore.EXTREME
- Normalized Score: 85.4

Contributing Factors:
- time_complexity: 60.0
- space_complexity: 30.0
- cyclomatic_complexity: 80.0
- property_access_complexity: 0.0
- ast_node_count: 87.6
- bottleneck_count: 30.0

### Optimization Suggestions

- High time complexity detected (O(n²)). Consider using a more efficient algorithm
- High complexity bottlenecks identified: Memory usage from temporary collections

### Example Usage

```python
From docstring:
    color_cycle = create_property_cycle_rule("color")  # Values must cycle
```
