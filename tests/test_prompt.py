from ai.prompts import build_prompt

findings = [
    {
        "service": "S3",
        "title": "Public Bucket",
        "severity": "Critical"
    }
]

print(build_prompt(findings))
