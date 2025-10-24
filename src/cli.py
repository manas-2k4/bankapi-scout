# src/cli.py
import csv
import asyncio
from scanner.http_probe import probe_url
from scanner.auth_checks import check_auth
from scanner.cors_headers import analyze_headers
from scanner.scoring import score_endpoint
from report.generator import write_json_report

async def scan_csv(path: str, out: str):
    results = []
    with open(path) as f:
        reader = csv.DictReader(f)
        tasks = []
        for row in reader:
            url = row["base_url"].rstrip("/") + row["endpoint"]
            tasks.append(scan_one(url))
        outs = await asyncio.gather(*tasks)
        write_json_report(outs, out)

async def scan_one(url):
    probe = await probe_url(url)
    # probe may return an error dict; handle gracefully
    status = probe.get("status") if isinstance(probe, dict) else None
    if status is None:
        # if probe failed, set status 0 and empty headers
        status = 0
        headers = {}
    else:
        headers = probe.get("headers", {}) or {}

    auth = await check_auth(url)
    header_findings = analyze_headers(headers)["findings"]

    # rate_limit_flag left False for MVP; implement rate-limit checks later if needed
    risk = score_endpoint(url, status, auth, header_findings, rate_limit_flag=False)

    severity = "Critical" if risk >= 80 else "High" if risk >= 60 else "Medium" if risk >= 40 else "Low"

    return {
        "endpoint": url,
        "status": status,
        "header_findings": header_findings,
        "auth": auth,
        "risk_score": risk,
        "severity": severity
    }

if __name__ == "__main__":
    import sys
    csvp = sys.argv[1] if len(sys.argv) > 1 else "examples/sample_endpoints.csv"
    out = sys.argv[2] if len(sys.argv) > 2 else "reports/report.json"
    asyncio.run(scan_csv(csvp, out))
