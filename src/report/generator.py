# src/report/generator.py
import json
from datetime import datetime

def write_json_report(results: list, outpath: str):
    report = {
        "scan_date": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "endpoints": len(results),
            "avg_score": sum(r["risk_score"] for r in results) / (len(results) or 1)
        },
        "results": results
    }
    with open(outpath, "w") as f:
        json.dump(report, f, indent=2)
