# seqrule

[![codecov](https://codecov.io/gh/neumanns-workshop/seqrule/branch/develop/graph/badge.svg)](https://codecov.io/gh/neumanns-workshop/seqrule)

A Python library for defining and generating rules to validate sequences of objects. It provides both a programmatic API and a REST API for creating, evaluating, and analyzing sequence validation rules.

## Features

- Fluent builder pattern for creating sequence validation rules
- Support for multiple validation operators:
  - Comparison: `=`, `!=`, `<`, `>`, `<=`, `>=`
  - Collection: `in`, `not in`
  - Existence: `exists`, `not exists`
  - Custom predicates with sequence context (prev, next, index)
- Sequence order validation with strict ordering
- Rule complexity analysis with multiple models:
  - Weighted
  - Entropy-based
  - Log-scaled
  - Normalized
- Performance profiling with memory tracking
- FastAPI-based REST API with comprehensive validation
- Extensive test coverage with API-specific test suites
- Support for special values (None, infinity, empty strings)
- Robust error handling and logging

## Installation

Install the base package:

```bash
pip install seqrule
```

For API functionality:

```bash
pip install seqrule[api]
```

For development:

```bash
pip install seqrule[dev]
```

## Usage

### Basic Usage

```python
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
print(metrics)  # Shows detailed complexity metrics
```

### Custom Predicates

You can define custom predicates that have access to sequence context:

```python
def check_increasing_rank(obj, context):
    """Check if current card's rank is higher than previous card."""
    prev = context['prev']
    if prev is None:  # First card can have any rank
        return True
    return obj.get('rank') > prev.get('rank')

# Create a rule that requires increasing ranks
rule = RuleBuilder()\\
    .add_condition("rank", check_increasing_rank, None)\\
    .set_sequence(["first", "second", "third"])\\
    .build()
```

### Example Applications

The library includes several comprehensive examples demonstrating its capabilities:

1. **DNA Sequence Validation** (`examples/01_dna_validation.py`):
   - Validates biological DNA sequences with multiple constraints
   - Features:
     - Base pairing rules (A-T, G-C)
     - GC content analysis in sliding windows
     - TATA box promoter sequence detection
     - Sequence window analysis
   - Example usage:
   ```python
   # Create DNA validation rule
   rule = RuleBuilder()\
       .add_condition('base', 'in', ['A', 'T', 'C', 'G'])\
       .add_condition('base', check_base_pairing, None)\
       .add_condition('base', check_gc_content, None)\
       .set_sequence(['pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6'])\
       .build()
   ```

2. **Chess Move Validation** (`examples/02_chess_moves.py`):
   - Validates chess moves and common patterns
   - Features:
     - Piece-specific movement rules (knight, bishop, rook, pawn)
     - Opening sequences (Ruy Lopez, Scholar's Mate)
     - Position validation in algebraic notation
     - Complex move sequences
   - Example usage:
   ```python
   # Create a rule for knight movement
   knight_rule = RuleBuilder()\
       .add_condition("square", check_knight_move, None)\
       .set_sequence(['start', 'end'])\
       .build()
   ```

3. **Chord Progression Validation** (`examples/03_chord_progressions.py`):
   - Validates musical chord progressions
   - Features:
     - Voice leading between chords
     - Functional harmony rules
     - Secondary dominants
     - Common progressions (I-IV-V-I, ii-V-I)
   - Example usage:
   ```python
   # Create a rule for jazz harmony
   jazz_rule = RuleBuilder()\
       .add_condition('function', check_voice_leading, None)\
       .add_condition('function', check_functional_harmony, None)\
       .add_condition('root', check_secondary_dominant, None)\
       .set_sequence(['Dm7', 'G7', 'Cmaj7'])\
       .build()
   ```

4. **Eleusis Card Game Rules** (`examples/04_eleusis_rules.py`):
   - Implements complex card game rules
   - Features:
     - Color alternation rules
     - Value progression rules
     - Suit sequence patterns
     - Prime number properties
     - Face card rules
   - Example usage:
   ```python
   # Create complex Eleusis rule
   rule = RuleBuilder()\
       .add_condition('color', check_color_alternation, None)\
       .add_condition('value', check_increasing_value, None)\
       .add_condition('suit', check_suit_sequence, None)\
       .add_condition('is_face', check_face_card_rule, None)\
       .add_condition('is_prime', check_prime_suit_rule, None)\
       .set_sequence(['card1', 'card2', 'card3', 'card4'])\
       .build()
   ```

5. **Turkish Phonology** (`examples/05_turkish_phonology.py`):
   - Validates Turkish phonological rules
   - Features:
     - Vowel harmony (two-way and four-way)
     - Consonant assimilation
     - Final devoicing
     - Syllable structure constraints
   - Example usage:
   ```python
   # Create Turkish phonology rule
   word_rule = RuleBuilder()\
       .add_condition('nucleus', check_vowel_harmony, None)\
       .add_condition('coda', check_consonant_rules, None)\
       .add_condition('phonemes', check_syllable_structure, None)\
       .set_sequence(['ki', 'tap', 'lar'])\
       .build()
   ```

6. **Recipe Validation with API** (`examples/06_recipe_api.py`):
   - Demonstrates using the REST API for recipe validation
   - Features:
     - Temperature safety rules (min/max limits)
     - Duration validation for each step
     - Step sequence validation (mix → rest → shape → bake)
     - Equipment and ingredient tracking
     - Comprehensive error checking
   - Example usage:
   ```python
   # Create recipe steps
   bread_recipe = [
       await create_recipe_step(
           name="mix",
           ingredients=["flour", "yeast", "water", "salt"],
           equipment=["mixer"],
           temperature=25.0,
           duration_minutes=10
       ),
       # ... more steps ...
   ]

   async with aiohttp.ClientSession() as session:
       # Create a recipe validation rule
       rule_response = await create_recipe_rule(session)
       
       # Evaluate a recipe sequence
       result = await evaluate_recipe(session, bread_recipe)
       
       # Analyze rule complexity
       complexity = await analyze_rule_complexity(session)
   ```

Each example demonstrates different aspects of the library:
- Complex rule composition
- Context-aware validation
- Performance profiling
- Domain-specific constraints
- Real-world applications

The examples are fully documented and include:
- Detailed comments explaining the rules
- Test cases for valid and invalid sequences
- Performance metrics
- Complexity analysis

To run any example:
```bash
python examples/[example_file].py
```

### Rule Analysis

The package provides comprehensive rule analysis:

```python
# Get detailed complexity metrics
metrics = rule.analyze_complexity(model="weighted")
print(metrics)
# Output includes:
# - condition_count: Number of conditions
# - sequence_length: Length of required sequence
# - logical_depth: Depth of logical operations
# - entropy: Measure of rule complexity
# - branching_factor: Number of decision points
# - redundancy: Measure of repeated patterns
# - execution_cost: Estimated computational cost
# - contradictions: Number of conflicting conditions
# - categorical_constraints: Count of string-based conditions
# - numerical_constraints: Count of number-based conditions
# - condition_impact: Overall impact score

# Profile rule performance
avg_time, avg_memory, times, memory = rule.profile(
    test_sequences=[cards],
    runs=10
)
```

### REST API

Start the API server:

```bash
uvicorn seqrule.api:app --reload
```

Create and evaluate a rule:

```bash
curl -X POST http://localhost:8000/rules/evaluate \\
  -H "Content-Type: application/json" \\
  -d '{
    "rule_request": {
      "conditions": [
        {
          "property_name": "temperature",
          "operator": "<=",
          "value": 200
        },
        {
          "property_name": "duration_minutes",
          "operator": ">",
          "value": 0
        }
      ],
      "sequence": ["mix", "rest", "shape", "bake"]
    },
    "evaluate_request": {
      "objects": [
        {
          "name": "mix",
          "properties": {
            "temperature": 25.0,
            "duration_minutes": 10
          }
        }
      ]
    }
  }'
```

## API Documentation

The REST API documentation is available at `http://localhost:8000/docs` when running the server.

### Endpoints

- `POST /rules`: Create a new rule
  - Validates rule structure and conditions
  - Checks for contradictions and invalid operators
- `POST /rules/evaluate`: Evaluate a sequence against a rule
  - Full validation of input objects and properties
  - Detailed error reporting
- `POST /rules/analyze`: Analyze rule complexity
  - Supports multiple complexity models
  - Returns detailed metrics

## Development

### Repository Structure

```
seqrule/
├── src/seqrule/          # Source code
│   ├── __init__.py       # Package interface & RuleBuilder
│   ├── api.py           # FastAPI implementation
│   ├── analyses.py      # Complexity analysis
│   ├── evaluators.py    # Rule evaluation
│   ├── objects.py       # Core Object class
│   ├── constraints.py   # Rule constraints
│   ├── generators.py    # Rule generation
│   └── logging_config.py # Logging setup
│
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures
│   ├── test_api_*.py    # API-specific tests
│   └── test_*.py        # Core functionality tests
│
├── examples/            # Example applications
│   ├── 01_dna_validation.py
│   ├── 02_chess_moves.py
│   ├── 03_chord_progressions.py
│   ├── 04_eleusis_rules.py
│   ├── 05_turkish_phonology.py
│   └── 06_recipe_api.py
```

### Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment: `source .venv/bin/activate` (Unix) or `.venv\\Scripts\\activate` (Windows)
4. Install development dependencies: `pip install -e ".[dev,api]"`

### Testing

Run tests with coverage:

```bash
pytest --cov=seqrule
```

The test suite includes:
- API-specific test suites for endpoints, models, validation, and error handling
- Core functionality tests for all components
- Performance and memory profiling tests
- Logging configuration tests
- Edge case handling for special values and error conditions

### Code Quality

The project uses `ruff` for linting and formatting:

```bash
ruff check .
ruff format .
```

Type checking with mypy:

```bash
mypy src/seqrule
```

## License

MIT License - see LICENSE file for details.