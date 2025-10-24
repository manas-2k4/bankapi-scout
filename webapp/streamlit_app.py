import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# Page setup
st.set_page_config(page_title="BankAPI-Scout Dashboard", layout="centered", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #0f1720;
        color: #e6eef6;
    }
    /* Subtle card backgrounds */
    .css-1d391kg { background-color: rgba(255,255,255,0.02); }
    .css-1v3fvcr { background-color: rgba(255,255,255,0.02); }
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255,255,255,0.02);
        border-radius: 8px;
        padding: 10px;
    }
    /* Dataframe text color */
    .stDataFrame table tbody td { color: #e6eef6; }
    .stDataFrame table thead th { color: #cbd5e1; }
    .small-caption { color: #cbd5e1; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<h1 style='color:#ffffff; font-weight:700; margin-bottom:6px;'>🛡️ BankAPI-Scout — Demo Dashboard</h1>", unsafe_allow_html=True)
st.caption("Automated API attack-surface scan — demo data only.")

uploaded = st.file_uploader("Upload report.json", type="json")

def generate_html_report(report, df):
    """Create a simple print-friendly HTML summary that can be saved as PDF from browser."""
    timestamp = report.get("scan_date", datetime.utcnow().isoformat())
    title = "BankAPI-Scout — Scan Report"

    # compute endpoints count safely
    endpoints_count = report.get("summary", {}).get("endpoints", len(report.get("results", [])))

    rows_html = ""
    for r in report.get("results", []):
        header_list = r.get("header_findings", []) or []
        headers_html = ", ".join(header_list)
        rows_html += f"""
        <tr>
          <td style="padding:8px;border:1px solid #ddd;">{r.get('endpoint','')}</td>
          <td style="padding:8px;border:1px solid #ddd;">{r.get('severity','')}</td>
          <td style="padding:8px;border:1px solid #ddd;">{r.get('risk_score','')}</td>
          <td style="padding:8px;border:1px solid #ddd;">{headers_html}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
      <style>
        body {{ font-family: Arial, sans-serif; background: #0f1720; color: #e6eef6; }}
        .container {{ max-width: 1000px; margin: 30px auto; padding: 20px; background: #081225; border-radius:8px; }}
        table {{ width:100%; border-collapse: collapse; margin-top: 16px; }}
        th {{ text-align:left; padding:8px; border:1px solid #333; background:#071826; color:#cbd5e1; }}
        td {{ color:#e6eef6; }}
        h1, h3 {{ color: #ffffff; }}
        .meta {{ color:#9aa7b8; font-size:0.9rem; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>{title}</h1>
        <div class="meta">Scan date: {timestamp}</div>
        <div class="meta">Endpoints scanned: {endpoints_count}</div>
        <h3>Summary</h3>
        <table>
          <thead>
            <tr><th>Endpoint</th><th>Severity</th><th>Risk Score</th><th>Header Findings</th></tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </body>
    </html>
    """
    return html


if uploaded:
    report = json.load(uploaded)
    df = pd.json_normalize(report.get("results", []))

    # Ensure columns exist and defaults
    if "risk_score" not in df.columns:
        df["risk_score"] = 0
    if "endpoint" not in df.columns:
        df["endpoint"] = df.index.astype(str)
    if "severity" not in df.columns:
        df["severity"] = df["risk_score"].apply(lambda s: "Low" if s < 40 else "Medium" if s < 60 else "High" if s < 80 else "Critical")

    # Summary values
    endpoints_count = int(report.get("summary", {}).get("endpoints", len(df)))
    avg_score = float(report.get("summary", {}).get("avg_score", df["risk_score"].mean() if not df["risk_score"].empty else 0))
    critical_count = int((df["severity"] == "Critical").sum())
    high_count = int((df["severity"] == "High").sum())
    medium_count = int((df["severity"] == "Medium").sum())
    low_count = int((df["severity"] == "Low").sum())

    # Scan-completed card (feature 1)
    st.success(f"✅ Scan completed successfully — {endpoints_count} endpoints analyzed.")
    st.write("")  # spacing

    # KPI metrics
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    col1.markdown(f"<div style='background:#081225; padding:12px 18px; border-radius:8px; text-align:center;'><h3 style='margin:0; color:#9be7a5'>{endpoints_count}</h3><div style='color:#a8b3c7'>Endpoints scanned</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='background:#081225; padding:12px 18px; border-radius:8px; text-align:center;'><h3 style='margin:0; color:#ffd97d'>{avg_score:.1f}</h3><div style='color:#a8b3c7'>Avg Risk Score</div></div>", unsafe_allow_html=True)
    col3.markdown(f"<div style='background:#081225; padding:12px 18px; border-radius:8px; text-align:center;'><h3 style='margin:0; color:#ff6b6b'>{critical_count}</h3><div style='color:#a8b3c7'>Critical</div></div>", unsafe_allow_html=True)
    col4.markdown(f"<div style='background:#081225; padding:12px 18px; border-radius:8px; text-align:center;'><h3 style='margin:0; color:#f4b042'>{high_count}</h3><div style='color:#a8b3c7'>High</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Color map
    color_sequence = {
        "Low": "#2ecc71",       # green
        "Medium": "#f4d03f",    # yellow
        "High": "#f39c12",      # orange
        "Critical": "#e74c3c"   # red
    }

    # Styled table
    st.subheader("Endpoint Risk Summary")
    styled_df = df[["endpoint", "severity", "risk_score"]].copy()
    styled_df["risk_score"] = styled_df["risk_score"].fillna(0).astype(int)

    def color_severity(val):
        cmap = color_sequence
        bg = cmap.get(val, "#ffffff")
        text_color = "#081225" if val == "Medium" else "#ffffff"
        return f"background-color: {bg}; color: {text_color}; font-weight:700;"

    styler = styled_df.style.applymap(color_severity, subset=["severity"]) \
        .set_properties(**{"background-color": "transparent", "color": "#e6eef6"}) \
        .format({"risk_score": "{:.0f}"})
    st.dataframe(styler, use_container_width=True)

    st.write("")  # spacing

    # Two-column charts: bar + pie
    c1, c2 = st.columns([2,1])

    with c1:
        fig = px.bar(
            df,
            x="endpoint",
            y="risk_score",
            color="severity",
            color_discrete_map=color_sequence,
            title="Risk Score by Endpoint",
            text="risk_score",
            template="plotly_dark"
        )
        fig.update_layout(
            xaxis_title="Endpoint",
            yaxis_title="Risk Score (0–100)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e6eef6", size=13),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=40, r=10, t=60, b=40),
        )
        fig.update_xaxes(tickangle=-45, showgrid=False, color="#cbd5e1")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", color="#cbd5e1")
        fig.update_traces(textposition="outside", textfont=dict(color="#e6eef6", size=11))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        severity_counts = df["severity"].value_counts().reindex(["Critical","High","Medium","Low"]).fillna(0).reset_index()
        severity_counts.columns = ["Severity", "Count"]
        fig2 = px.pie(
            severity_counts,
            names="Severity",
            values="Count",
            color="Severity",
            color_discrete_map=color_sequence,
            hole=0.4,
            title="Severity Breakdown",
            template="plotly_dark"
        )
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(margin=dict(l=10,r=10,t=40,b=10), legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")  # spacing

    # Insights box
    st.subheader("🧠 Insights")
    crit = int((df["severity"] == "Critical").sum())
    high = int((df["severity"] == "High").sum())
    med = int((df["severity"] == "Medium").sum())
    low = int((df["severity"] == "Low").sum())

    if crit > 0:
        st.error(f"🔴 {crit} Critical endpoint(s) detected — immediate attention required.")
        if high > 0:
            st.warning(f"🟠 {high} High-risk endpoint(s) — prioritize remediation next.")
    elif high > 0:
        st.warning(f"🟠 {high} High-risk endpoint(s) found — please review.")
    elif med > 0:
        st.info(f"🟡 {med} Medium-risk endpoints — monitor and remediate.")
    else:
        st.success("✅ All scanned endpoints indicate a low risk posture.")

    st.markdown("---")

    # ===== Export buttons (feature 2) =====
    # CSV
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Download report as CSV", data=csv_bytes, file_name="api_scan_report.csv", mime="text/csv")

    # JSON
    json_str = json.dumps(report, indent=2)
    st.download_button(label="📥 Download raw JSON report", data=json_str, file_name="api_scan_report.json", mime="application/json")

    # HTML (print-friendly) - user can open and Save as PDF from browser
    html_report = generate_html_report(report, df)
    st.download_button(label="🖨️ Download print-friendly HTML (Save as PDF)", data=html_report, file_name="api_scan_report.html", mime="text/html")

    st.markdown(
        "<div style='text-align:center; color:grey; margin-top:12px;'>"
        "Developed by <b>Manas Kasturi</b> • BankAPI-Scout  (Demo data only)"
        "</div>",
        unsafe_allow_html=True
    )

else:
    st.info("Upload a JSON report to visualize results.")
