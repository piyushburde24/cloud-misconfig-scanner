from ai.gemini_client import GeminiClient

findings = [
    {
        "service": "EC2",
        "resource": "web-server",
        "severity": "Critical",
        "title": "SSH Open to Internet",
        "description": "Security Group allows SSH from 0.0.0.0/0",
        "recommendation": "Restrict SSH access."
    }
]

client = GeminiClient()

result = client.analyze_findings(findings)

print(result)
