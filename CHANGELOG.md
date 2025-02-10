# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of the seqrule library
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
- Comprehensive example applications:
  - DNA sequence validation
  - Chess move validation
  - Chord progression validation
  - Eleusis card game rules
  - Turkish phonology
  - Recipe validation with API

### Changed
- Set line length limit to 99 characters
- Updated linting configuration to use ruff

### Fixed
- Whitespace and formatting issues across multiple files
- Exception handling in example code 