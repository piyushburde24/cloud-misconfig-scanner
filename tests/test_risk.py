from security.risk_score import RiskScoreCalculator


class Dummy:

    def __init__(self, severity):
        self.severity = severity


findings = [
    Dummy("Critical"),
    Dummy("High"),
    Dummy("High"),
    Dummy("Low"),
]

result = RiskScoreCalculator.calculate(findings)

print(result)
