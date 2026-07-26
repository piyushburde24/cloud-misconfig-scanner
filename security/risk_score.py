from collections import Counter


class RiskScoreCalculator:
    """
    Calculates an overall security score based on findings severity.
    """

    WEIGHTS = {
        "Critical": 25,
        "High": 15,
        "Medium": 7,
        "Low": 3,
    }

    @classmethod
    def calculate(cls, findings):

        counts = Counter()

        for finding in findings:
            counts[finding.severity] += 1

        penalty = 0

        for severity, count in counts.items():
            penalty += cls.WEIGHTS.get(severity, 0) * count

        score = max(0, 100 - penalty)

        return {
            "score": score,
            "counts": dict(counts),
        }
