# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - Unreleased

### Added
- Core DSL implementation:
  - ANTLR4-based grammar for sequence rules
  - Support for simple sequences (e.g., "heart -> spade")
  - Support for absolute positions (e.g., "ace@0 king@2")
  - Property value comparisons with operators (=, !=, <, >, <=, >=)
  - Conditional rules with if/then/else branches
  - Logical operators (AND, OR)
  - Element constraints (e.g., "heart(rank = 7)")
- Robust parser with error handling:
  - Detailed error messages with line/column information
  - Validation for positions and constraints
  - Proper handling of string literals and parentheses
- Evaluator implementation:
  - Support for evaluating simple sequences
  - Property value comparison and type conversion
  - Position-aware evaluation
  - Conditional rule branching
  - Constraint checking
- Testing infrastructure:
  - Comprehensive test suite with 74% coverage
  - Integration with GitHub Actions and Codecov
  - Test cases for parsing, evaluation, and error handling 