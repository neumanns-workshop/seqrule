# Sequence Rules Framework

[![codecov](https://codecov.io/gh/neumanns-workshop/sequence_rule_grammar/branch/main/graph/badge.svg)](https://codecov.io/gh/neumanns-workshop/sequence_rule_grammar)

A robust, mathematically rigorous framework for sequence rule generation and evaluation. This framework provides:

- A formally defined DSL for sequence rules
- Rule parsing and evaluation with absolute position support
- Comprehensive error handling and validation
- Clean and maintainable codebase

## Installation

1. Ensure you have Python 3.10+ installed
2. Install uv:
```bash
pip install uv
```

3. Clone this repository
4. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix
.venv\Scripts\activate     # On Windows
```

5. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

6. Install ANTLR4 tools and generate parser:
```bash
# Install ANTLR tools
uv pip install antlr4-tools

# Generate Python parser
cd sequence_rules/dsl && antlr4 -Dlanguage=Python3 -visitor SequenceRule.g4
```

## Usage

The framework allows you to define and evaluate sequence rules using a simple DSL. Here are some examples:

### Simple Sequences
```python
from sequence_rules.dsl.parser import parse_rule
from sequence_rules.core.evaluator import evaluate_sequence

# Basic sequence
rule = parse_rule("heart -> spade")

# Sequence with absolute positions
rule = parse_rule("ace@0 king@2")

# Sequence with constraints
rule = parse_rule("heart(rank = 7) -> spade")
```

### Conditional Rules
```python
# Simple conditional
rule = parse_rule("if rank = 7 then heart -> spade")

# Conditional with else branch
rule = parse_rule("if rank = 7 then heart -> spade else diamond -> club")

# Complex conditions
rule = parse_rule("if (rank = 7 and suit = \"heart\") or value = \"ace\" then king")
```

### Position References
The framework uses absolute positions (0-based indexing):
```python
# Reference position in elements
rule = parse_rule("ace@0 king@2 queen@3")

# Reference position in conditions
rule = parse_rule("if rank@0 > rank@1 then ace")
```

### Evaluating Sequences
```python
sequence = [
    {"suit": "heart", "rank": 7},
    {"suit": "spade", "rank": 4}
]
is_valid = evaluate_sequence(rule, sequence)
print(f"Sequence is {'valid' if is_valid else 'invalid'}")
```

## Error Handling

The framework provides clear error messages for common issues:

- Invalid syntax: Detailed error messages with line and column information
- Position validation: Ensures all positions are non-negative
- String literals: Proper handling of unterminated strings
- Parentheses: Detection of unclosed parentheses
- Empty rules: Validation against empty or malformed rules

## Testing

Run the test suite with pytest:

```bash
pytest tests -v
```

The test suite includes:
- Basic rule parsing and evaluation
- Conditional rules and complex conditions
- Position handling and validation
- Error cases and edge conditions
- Advanced rule combinations

## Documentation

For detailed documentation, see NORTHSTAR.md which contains the formal specification and theoretical foundations of the framework.

## Roadmap

Our development roadmap aligns with our vision of creating a mathematically rigorous framework for sequence rules:

### Phase 1: Core DSL (✅ Version 1.0)
- ✅ Formal grammar definition with ANTLR4
- ✅ Robust parser with comprehensive error handling
- ✅ Support for absolute positions and constraints
- ✅ Extended test coverage for edge cases
- ✅ Performance optimization for large rule sets

### Phase 2: Rule Normalization & Equivalence (Next) [Implement SymPy-based rule normalization]
- Implement rule normalization using symbolic computation
- Add canonical form representation for rules
- Develop equivalence checking between rules
- Support for rule simplification and optimization
- Add complexity metrics and constraints

### Phase 3: Rule Generation
- Implement property-based rule generation
- Add complexity-bounded generation strategies
- Support for environment-aware rule creation
- Develop rule scoring and ranking mechanisms
- Add generation constraints and templates
- Create rule mutation and combination algorithms
- Implement rule validation during generation
- Add support for generating rule families

### Phase 4: Advanced Evaluation Features
- Implement automata-based sequence validation
- Add support for probabilistic rules
- Develop pattern matching optimizations
- Create visualization tools for rule evaluation
- Add performance benchmarking suite

### Phase 5: Formal Verification
- Formalize DSL semantics in Coq/Lean
- Prove parser soundness and completeness
- Verify rule equivalence algorithms
- Validate complexity constraint enforcement
- Verify rule generation correctness
- Integrate verified components

### Phase 6: Extended Features
- Support for non-deterministic rules
- Integration with game engines
- Real-time rule evaluation optimization
- Extended DSL for complex patterns
- Comprehensive documentation and examples
- Interactive rule generation UI
- Rule visualization and debugging tools

Legend:
- ✅ Completed
- 🔄 In Progress
- Unmarked: Planned

## License

MIT

## Development

### Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

### Code Quality

The project uses several tools to maintain code quality:

- **Ruff**: For fast Python linting and code style enforcement
  ```bash
  ruff check .
  ```

- **Black**: For code formatting
  ```bash
  black .
  ```

- **isort**: For import sorting
  ```bash
  isort .
  ```

- **mypy**: For static type checking
  ```bash
  mypy .
  ```

### Testing

Run tests with pytest:
```bash
pytest
```

This will also generate a coverage report.
