# src/scanner/scoring.py
def score_endpoint(endpoint: str, status: int, auth_result: dict, header_findings: list, rate_limit_flag: bool=False) -> int:
    """
    Demo-friendly scoring:
    - 401 or 404 => Low (30)
    - 200 but endpoint requires valid token (invalid_token_status==401) => Low (30)
    - 200 & unauthenticated allowed (no_auth_status==200) => Critical (90-100)
    - 200 & authenticated required but some header issues => Medium/High depending on header count
    - Add rate_limit_flag to push severity a bit higher
    """
    # normalize inputs
    header_findings = header_findings or []
    no_auth = auth_result.get("no_auth_status")
    invalid_token = auth_result.get("invalid_token_status")

    # unreachable or requires auth (safe)
    if status in (401, 404):
        return 30  # Low

    # unauthenticated public endpoint -> Critical
    if no_auth == 200:
        base = 90
        # penalize missing headers further
        base += min(10, 3 * len(header_findings))
        if rate_limit_flag:
            base += 0
        return min(100, base)

    # invalid token accepted but no_auth not 200 -> serious problem
    if invalid_token == 200 and no_auth != 200:
        base = 80 + min(10, 3 * len(header_findings))
        return min(100, base)

    # Now endpoint appears to require auth properly (or was 200 but responded with 401 for invalid)
    # Use header_count to set Medium/High:
    header_count = len(header_findings)
    if header_count == 0:
        score = 30  # Low — good headers
    elif header_count <= 2:
        score = 50  # Medium
    else:
        score = 70  # High

    # small bump for missing rate limit
    if rate_limit_flag:
        score += 10

    return min(100, score)
