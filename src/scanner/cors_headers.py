# src/scanner/cors_headers.py
def analyze_headers(headers: dict) -> dict:
    findings = []
    cors = headers.get("access-control-allow-origin")
    if cors in (None, "*"):
        findings.append("Permissive CORS" if cors == "*" else "No CORS header")
    # check common security headers
    for h in ["x-frame-options","content-security-policy","strict-transport-security","x-content-type-options"]:
        if h not in {k.lower() for k in headers.keys()}:
            findings.append(f"Missing header: {h}")
    return {"findings": findings}
