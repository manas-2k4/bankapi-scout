# 🛡️ BankAPI-Scout
**Automated API Attack-Surface Scanner & Risk Visualization Dashboard**  
A complete cybersecurity prototype that identifies insecure or misconfigured APIs, evaluates authentication mechanisms and headers, and presents the results in an interactive **Streamlit SOC-style dashboard**.  
Built to demonstrate how banks and fintech organizations can integrate *automated API risk analytics* into their cybersecurity governance frameworks.

---

## 🚀 Project Overview
**BankAPI-Scout** is a lightweight yet powerful scanner that simulates the API vulnerability assessment process used in financial institutions.  
It performs non-destructive, compliance-aligned tests on endpoints — checking for missing security headers, unauthenticated access, and configuration weaknesses — and outputs a structured JSON risk report, ready for visualization and audit evidence.

This project bridges three disciplines:

- 🧩 **Development:** Async Python (httpx + asyncio) for high-performance scanning  
- 🔐 **Cybersecurity:** OWASP API Top 10 & RBI cybersecurity alignment  
- 📊 **Risk & Governance:** Quantified scoring, audit-ready reporting, and compliance mapping  

---

## 💡 Why This Project Is Unique
### 🔒 Cybersecurity Perspective
- Focused specifically on **API security**, the fastest-growing attack vector in modern banking.  
- Detects risks across **authentication**, **CORS**, **HSTS**, **CSP**, and **header hygiene**.  
- Provides an evidence-based foundation for RBI-mandated vulnerability assessments and **OWASP API Top 10** compliance.

### 🏦 Banking & Risk Relevance
- Financial institutions expose hundreds of APIs for customer, payments, and partner services — each a potential risk surface.  
- **BankAPI-Scout** demonstrates how to continuously monitor that surface and classify risk for reporting to CISO / GRC teams.  
- Results map to frameworks such as:
  - RBI Cybersecurity Framework for Banks  
  - NIST Cybersecurity Framework (Identify → Protect → Detect)  
  - ISO/IEC 27001 (A.12.6 Technical Vulnerability Management)

### ⚙️ Development & Engineering Excellence
- Modular architecture (scanner / scoring / reporting / visualization)  
- Built with **asynchronous Python**, **Streamlit**, and **Plotly** for speed and interactivity  
- Provides structured outputs (JSON, CSV, HTML) suitable for integration into CI/CD or GRC pipelines  
- Includes a safe **Flask mock API** that guarantees deterministic Low/Medium/High/Critical results for demo or training purposes  

---

## 🧠 Key Features
| Category | Description |
|-----------|--------------|
| 🔍 **Automated Scanning** | Async probing of multiple API endpoints simultaneously |
| 🔐 **Auth & Header Checks** | Detects insecure CORS, missing HSTS/CSP, weak header hygiene |
| ⚖️ **Deterministic Risk Scoring** | Maps each endpoint to Low / Medium / High / Critical severity |
| 📈 **Interactive Dashboard** | SOC-style dark dashboard with KPI cards, charts & insights |
| 🧾 **Multi-Format Export** | Download results as CSV, JSON, or print-ready HTML (PDF-friendly) |
| 🧪 **Mock API Environment** | Local Flask server simulates different risk behaviors safely |

---

## 🏗️ Architecture Overview
bankapi-scout/
├─ src/
│ ├─ scanner/ # Async probes, header & auth checks, scoring
│ ├─ report/ # JSON report generator
│ └─ cli.py # Main entry for scanning
├─ webapp/
│ └─ streamlit_app.py # Dashboard UI + exports
├─ examples/ # Sample CSV endpoint inventories
├─ tests/ # Flask mock API for deterministic results
├─ reports/ # Generated scan outputs
└─ README.md


🏦 Practical Use-Cases

-Internal Security Teams: Continuous API posture monitoring
-DevSecOps Pipelines: Pre-deployment API compliance testing
-GRC / Audit Teams: Evidence generation for RBI or ISO audits
-Training / Demos: Safe illustration of API vulnerabilities for awareness sessions

📈 Dashboard Highlights

-Real-time charts: Bar & pie visualization of severity distribution
-KPI Cards: Endpoints, Avg Risk, Critical & High counts
-Insights Section: Auto-generated summaries (“2 Critical endpoints detected — immediate attention required”)
-Exports: Download results as CSV, JSON, or print-ready HTML (PDF-friendly)

⚖️ Ethical Use Notice

Do not use this tool against systems you do not own or lack permission to test.
This project uses only public or local mock APIs for educational and demonstration purposes.

🏁 Summary

BankAPI-Scout is not just another scanner — it’s a demonstration of how cybersecurity, risk management, and modern development can converge.
In an era where APIs drive the digital backbone of banking, this project shows that security can be automated, visual, and actionable.


👤 Author

  Manas Kasturi
📍 Based in Hyderabad, India
🔗 LinkedIn Profile : https://www.linkedin.com/in/manas-kasturi-741049280/
