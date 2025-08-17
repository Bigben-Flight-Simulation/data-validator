import ast
from simpleeval import SimpleEval
from .utils import SafeRow
from .models import ValidationResult

class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def eval_expr(self, expr, context):
        s = SimpleEval(names=context)
        print(f"Evaluating expression: {expr}")
        return s.eval(expr)

    def check_row(self, row_idx, rows, rule, filename=""):
        curr = rows[row_idx]
        prev = rows[row_idx - 1] if row_idx > 0 else None
        next_ = rows[row_idx + 1] if row_idx < len(rows) - 1 else None
        context = {"curr": curr, "prev": prev, "next": next_}

        cond = rule["condition"]
        exprs = []
        if_all = cond.get("if", {}).get("all", [])
        if_any = cond.get("if", {}).get("any", [])
        then_exprs = cond.get("then", [])
        exprs.extend(if_all)
        exprs.extend(if_any)
        exprs.extend(then_exprs)

        if next_ is None and any("next" in expr for expr in exprs):
            return []
        if prev is None and any("prev" in expr for expr in exprs):
            return []
        
        cond = rule["condition"]
        if_all = cond.get("if", {}).get("all")
        if_any = cond.get("if", {}).get("any")

        if if_all:
            if_result = all(self.eval_expr(expr, context) for expr in if_all)
        elif if_any:
            if_result = any(self.eval_expr(expr, context) for expr in if_any)
        else:
            if_result = True

        errors = []
        if if_result:
            then_exprs = cond.get("then", [])
            results = [self.eval_expr(expr, context) for expr in then_exprs]
            throw_on = rule.get("throw_on", "any")
            rule_name = rule.get("name", "")
            rule_desc = rule.get("description", "")

            if throw_on == "any" and not all(results):
                for expr, ok in zip(then_exprs, results):
                    if not ok:
                        errors.append(
                            ValidationResult(
                                row=row_idx + 1,
                                rule=rule_name,
                                message=f"`{expr}` failed",
                                level=rule.get("level", "error"),
                                description=rule_desc,
                                failed_expr=expr,
                                filename=filename,
                            )
                        )
            elif throw_on == "all" and not any(results):
                errors.append(
                    ValidationResult(
                        row=row_idx + 1,
                        rule=rule_name,
                        message=f"all failed {then_exprs}",
                        level=rule.get("level", "error"),
                        description=rule_desc,
                        failed_expr="; ".join(then_exprs),
                        filename=filename,
                    )
                )
        return errors

    def run(self, rows, filename=""):
        all_errors = []
        for i in range(len(rows)):
            for rule in self.rules:
                all_errors.extend(self.check_row(i, rows, rule, filename=filename))
        return all_errors
    