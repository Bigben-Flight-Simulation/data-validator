from dataclasses import dataclass

@dataclass
class ValidationResult:
    row: int
    rule: str
    message: str
    level: str = "error"
    description: str = ""
    failed_expr: str = ""
    filename: str = ""
    def __str__(self):
        return (
            f"[{self.level.upper()}] In {self.filename}, on Line {self.row + 1} | {self.rule} failed on expr {self.failed_expr}"
        )