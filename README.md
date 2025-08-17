# data-validator

A rule-based data validation tool powered by YAML configuration.

## Features
- Load validation rules from YAML
- Row / cross-row validation
- Expression syntax with `curr`, `prev`, `next`
- CLI integration

## Quick Start

```bash
poetry install
poetry run data-validator --rules examples/rules.yaml --data examples/sample.csv
```
