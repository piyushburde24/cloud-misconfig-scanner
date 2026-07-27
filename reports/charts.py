from collections import Counter

import pandas as pd


class ChartBuilder:
    """
    Builds data for dashboard charts.
    """

    @staticmethod
    def severity_chart(findings):

        counts = Counter()

        for finding in findings:
            counts[finding.severity] += 1

        return pd.DataFrame(
            {
                "Severity": list(counts.keys()),
                "Count": list(counts.values()),
            }
        )

    @staticmethod
    def service_chart(findings):

        counts = Counter()

        for finding in findings:
            counts[finding.service] += 1

        return pd.DataFrame(
            {
                "Service": list(counts.keys()),
                "Count": list(counts.values()),
            }
        )
