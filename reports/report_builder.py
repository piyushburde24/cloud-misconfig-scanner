from collections import Counter


class ReportBuilder:

    @staticmethod
    def build(scan, findings, risk):

        severity = Counter()

        services = Counter()

        for finding in findings:

            severity[finding.severity] += 1

            services[finding.service] += 1

        return {

            "scan": scan,

            "risk": risk,

            "findings": findings,

            "severity_summary": dict(severity),

            "service_summary": dict(services),
        }
