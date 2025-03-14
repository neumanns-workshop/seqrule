# SeqRule

[![coverage](.github/badges/coverage.svg)](https://github.com/neumanns-workshop/seqrule/actions/workflows/coverage.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Python library for defining, generating, and validating rules for sequences of abstract objects. SeqRule provides a flexible framework that can be applied to various domains, with built-in support for:

- DNA sequence analysis
- Tea processing validation
- Musical sequence analysis
- Card game rule validation (Eleusis)
- Software release pipeline validation

## Project Status

SeqRule 1.0.0b1 (beta) has been released with all core functionality implemented and thoroughly tested. The library is ready for testing in the supported domains, with ongoing development focused on:

- Enhanced visualization and debugging tools
- Additional domain-specific rulesets
- Performance optimizations for large sequences
- Integration with popular data science frameworks

See the [ROADMAP.md](ROADMAP.md) file for detailed development plans.

## Features

### Core Framework
- Pure formal model for sequence validation
- High-level DSL for building complex rules
- Composable rules with logical operators (AND, OR, NOT)
- Robust error handling and property validation
- Lazy evaluation and performance optimizations
- Rule analysis and profiling capabilities
  - Time and space complexity analysis
  - Cyclomatic complexity measurement
  - Property access pattern analysis
  - Bottleneck detection
  - Customizable scoring system
- Complexity and performance benchmarking

### Built-in Rule Types
- Property-based rules (trends, patterns, relationships)
- Numerical constraints and ranges
- State tracking and historical patterns
- Meta-rules and rule combinations
- Domain-specific rule collections

### Domain Support

#### DNA Sequences
- GC content analysis
- Motif detection
- Restriction site validation
- Primer design rules
- Secondary structure prediction

#### Tea Processing
- Processing step validation
- Temperature and humidity control
- Oxidation level monitoring
- Quality metrics tracking
- Regional variations

#### Musical Sequences
- Scale and chord validation
- Rhythm pattern checking
- Voice leading rules
- Melodic contour analysis
- Time signature constraints

#### Card Games (Eleusis)
- Pattern matching
- Suit and rank relationships
- Color alternation
- Complex sequence rules
- Game state tracking

#### Pipeline Validation
- Stage ordering
- Dependency checking
- Resource constraints
- Timing requirements
- Error handling

## Installation

### Using pip (standard)
```bash
# Basic installation
pip install seqrule

# With API support
pip install seqrule[api]

# Development installation
pip install seqrule[dev]
```

### Using uv (recommended)
```bash
# Basic installation
uv pip install seqrule

# With API support
uv pip install seqrule[api]

# Development installation
uv pip install seqrule[dev]

# Local development installation with uv
uv pip install -e ".[dev]"
```

## Dependency Management

This project uses uv for dependency management. The `uv.lock` file ensures reproducible builds and installations:

- `requirements.txt` - Main project dependencies
- `uv.lock` - Lock file with exact versions for reproducible environments
- When contributing, run `uv pip sync` to synchronize your environment with the project's dependencies

For more information on uv, see [the uv documentation](https://github.com/astral-sh/uv).

## Quick Start

### Basic Usage

```python
from seqrule import AbstractObject, DSLRule, check_sequence
from seqrule.analysis import RuleAnalyzer, RuleScorer

# Create objects with properties
sequence = [
    AbstractObject(value=1, color="red"),
    AbstractObject(value=2, color="blue"),
    AbstractObject(value=3, color="red"),
]

# Define a simple rule
def alternating_colors(seq):
    if len(seq) <= 1:
        return True
    return all(seq[i]["color"] != seq[i+1]["color"] 
              for i in range(len(seq)-1))

# Create a DSL rule
rule = DSLRule(alternating_colors, "colors must alternate")

# Check sequence
is_valid = check_sequence(sequence, rule)  # True

# Analyze rule performance
analyzer = RuleAnalyzer().with_sequences([sequence])
analysis = analyzer.analyze(rule)

# Score the rule
scorer = RuleScorer()  # Use default balanced weights
score = scorer.score(analysis)
print(f"Time complexity: {analysis.complexity.time_complexity}")
print(f"Complexity Level: {score.complexity_level}")
print(f"Bottlenecks: {analysis.complexity.bottlenecks}")
```

### Using Built-in Rules

```python
from seqrule.rulesets.general import (
    create_property_trend_rule,
    create_property_match_rule,
    create_balanced_rule
)

# Create rules
ascending = create_property_trend_rule("value", "ascending")
is_red = create_property_match_rule("color", "red")
balanced = create_balanced_rule("color", tolerance=0.1)

# Combine rules
from seqrule import DSLRule

# Use logical operators for rule combination
complex_rule = ascending & (is_red | balanced)  # Using operator overloading
```

### Using Sequence Generators

```python
from seqrule.generators import generate_sequences, generate_lazy, ConstrainedGenerator
from seqrule.generators.patterns import PropertyPattern

# Generate sequences that satisfy a rule
valid_sequences = generate_sequences(domain_objects, filter_rule=my_rule)

# Generate sequences lazily for memory efficiency
lazy_gen = generate_lazy(domain_objects, filter_rule=my_rule)
for sequence in lazy_gen:
    process_sequence(sequence)

# Generate constrained sequences with patterns
generator = ConstrainedGenerator(domain_objects)
generator.add_constraint(lambda seq: len(seq) >= 3)
generator.add_pattern(PropertyPattern("color", ["red", "blue", "red"]))

for sequence in generator.generate(max_length=5):
    process_sequence(sequence)
```

### Domain-Specific Examples

#### DNA Analysis
```python
from seqrule.rulesets.dna import (
    create_gc_content_rule,
    create_motif_rule
)

# Check GC content and motif
sequence = [
    AbstractObject(base="G", position=1),
    AbstractObject(base="C", position=2),
    AbstractObject(base="A", position=3),
    AbstractObject(base="T", position=4),
]

gc_rule = create_gc_content_rule(min_percent=40, max_percent=60)
motif_rule = create_motif_rule("GC")
```

#### Tea Processing
```python
from seqrule.rulesets.tea import (
    TeaType,
    create_oxidation_rule,
    create_temperature_rule
)

# Validate tea processing
sequence = [
    AbstractObject(type="withering", duration=12),
    AbstractObject(type="oxidation", duration=2),
    AbstractObject(type="drying", temperature=80),
]

oxidation = create_oxidation_rule(TeaType.BLACK)
temperature = create_temperature_rule(TeaType.BLACK, "drying")
```

#### Musical Analysis
```python
from seqrule.rulesets.music import (
    create_scale_rule,
    create_rhythm_rule
)

# Check musical rules
sequence = [
    AbstractObject(pitch="C4", duration=1.0),
    AbstractObject(pitch="E4", duration=0.5),
    AbstractObject(pitch="G4", duration=0.5),
]

scale = create_scale_rule("major", "C")
rhythm = create_rhythm_rule((4, 4))
```

## Documentation

Comprehensive documentation is available in the `docs` directory:

1. [General Concepts](docs/general/concepts.md)
   - Core abstractions
   - Rule creation
   - Sequence validation
   - DSL usage

2. [Analysis Guide](docs/general/analysis_guide.md)
   - Complexity analysis
   - Performance profiling
   - Research applications
   - Optimization patterns

3. Domain-Specific Guides
   - [DNA Sequence Analysis](docs/domains/dna/index.md)
   - [Tea Processing](docs/domains/tea/index.md)
   - [Musical Sequences](docs/domains/music/index.md)
   - [Pipeline Validation](docs/domains/pipeline/index.md)
   - [Card Games (Eleusis)](docs/domains/eleusis/index.md)

4. [API Reference](docs/general/api.md)
   - Core module
   - DSL module
   - Analysis module
   - Domain modules
   - Utility functions

5. [Best Practices](docs/general/best_practices.md)
   - Rule design
   - Performance considerations
   - Error handling
   - Testing strategies

6. [Advanced Topics](docs/general/advanced.md)
   - Custom rule creation
   - Rule composition
   - Domain extension
   - Meta-rules

## Development

### Setup
```bash
# Clone repository
git clone https://github.com/neumanns-workshop/seqrule.git
cd seqrule

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=seqrule

# Run specific test file
pytest tests/test_core.py
```

### Code Quality
```bash
# Run type checker
mypy src/seqrule

# Run linter
ruff src/seqrule
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Eleusis card game and its rule discovery mechanics
- Built with modern Python features and best practices
- Designed for extensibility and reuse across domains

