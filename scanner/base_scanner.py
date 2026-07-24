class BaseScanner:

    def __init__(self):
        self.findings = []

    def add_finding(
        self,
        service,
        resource,
        severity,
        title,
        description,
        recommendation,
    ):

        self.findings.append(
            {
                "service": service,
                "resource": resource,
                "severity": severity,
                "title": title,
                "description": description,
                "recommendation": recommendation,
            }
        )

    def get_findings(self):
        return self.findings
