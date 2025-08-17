import yaml
import csv

def load_rules_from_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("checks", [])

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
