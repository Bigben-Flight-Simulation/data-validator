import argparse
import glob
import os
from .loader import load_rules_from_yaml, load_csv
from .engine import RuleEngine

def main():
    parser = argparse.ArgumentParser(description="YAML-driven data validator")
    parser.add_argument("--rules", required=True, help="Path to rules.yaml")
    parser.add_argument("--data", required=True, nargs="+", help="Path(s) to CSV file(s), support glob")
    args = parser.parse_args()

    rules = load_rules_from_yaml(args.rules)
    engine = RuleEngine(rules)
    all_errors = []

    files = []
    for pattern in args.data:
        files.extend(glob.glob(pattern))
    files = list(set(files)) 

    for file in files:
        rows = load_csv(file)
        errors = engine.run(rows, filename=os.path.basename(file))
        all_errors.extend(errors)

    if all_errors:
        print("Validation errors:")
        for e in all_errors:
            print("  -", e)
        exit(1)
    else:
        print("Validation passed ✅")