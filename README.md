<div align="center">

# 🔐 SRI Sentinel

### Web Integrity Scanner

**Detect missing Subresource Integrity attributes before attackers exploit them.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Security](https://img.shields.io/badge/Focus-Supply%20Chain%20Security-ef4444?style=flat-square)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-6366f1?style=flat-square)](CONTRIBUTING.md)

</div>

---

## Overview

SRI Sentinel is a lightweight CLI security tool that scans websites for missing [Subresource Integrity (SRI)](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) attributes on externally loaded resources.

A missing `integrity` attribute means the browser will execute any script or apply any stylesheet served by a third-party CDN — **even if it has been tampered with.** This is the attack vector behind Magecart-style supply chain compromises.

```
[Target Domain] → Fetch HTML → Parse Resources → Check SRI → JSON Report
```

---

## Features

| Capability | Details |
|---|---|
| 🔍 **Resource Detection** | Scans `<script>`, `<link>` (stylesheets), and font resources |
| 🚨 **SRI Validation** | Flags any external resource missing an `integrity` attribute |
| 🌐 **Bulk Scanning** | Accepts a flat file of domains for batch analysis |
| 🧹 **Deduplication** | Consolidates repeated findings per domain |
| 📄 **JSON Output** | Machine-readable results for pipeline integration |
| ⚡ **Zero Config** | Runs with a single command, no API keys or accounts required |

---

## How It Works

```
1. Read domains.txt
2. Fetch each domain's HTML response
3. Parse the DOM with BeautifulSoup
4. Identify all externally loaded resources
5. Check each resource for an integrity= attribute
6. Write flagged assets to sri_results.json
```

SRI hashes (e.g. `sha256-...`) allow browsers to verify that a fetched file matches a known-good cryptographic digest. If the file has been altered, the browser refuses to execute it. Without SRI, there is no such verification.

---

## Installation

**Requirements:** Python 3.8+

```bash
pip install requests beautifulsoup4 urllib3
```

Clone the repository:

```bash
git clone https://github.com/your-username/sri-sentinel.git
cd sri-sentinel
```

---

## Usage

**1. Populate `domains.txt` with your target domains (one per line):**

```
example.com
google.com
github.com
```

**2. Run the scanner:**

```bash
python sri_scanner.py
```

**3. Review results in `sri_results.json`.**

---

## Example Output

```json
{
  "domain": "https://example.com",
  "status": "vulnerable",
  "sri_missing": [
    {
      "type": "script",
      "resource": "https://cdn.example.com/analytics.js"
    },
    {
      "type": "stylesheet",
      "resource": "https://fonts.googleapis.com/css2?family=Inter"
    }
  ]
}
```

A domain with no missing SRI attributes will report `"status": "ok"`.

---

## Security Context

Without SRI, loading external resources creates an implicit trust dependency on every CDN in your supply chain.

| Threat | Impact |
|---|---|
| CDN compromise | Attacker-controlled script executes on all visitor browsers |
| Dependency hijacking | Malicious package version served transparently |
| Magecart / skimming | Payment credentials exfiltrated silently |
| DNS poisoning | Alternate file served with no browser-level warning |

SRI is a browser-enforced mitigation. Adding `integrity` and `crossorigin` attributes to external resource tags is one of the lowest-effort, highest-impact hardening steps for any web property.

> **Reference:** [OWASP – Third Party JavaScript Management](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html)

---

## Roadmap

- [ ] Multithreading for high-volume domain lists
- [ ] HTTP → HTTPS downgrade detection
- [ ] Security headers analysis (`CSP`, `HSTS`, `X-Frame-Options`)
- [ ] CSV and HTML report formats
- [ ] Severity scoring based on resource type and origin
- [ ] CI/CD integration mode (non-zero exit on findings)

---

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

Distributed under the [MIT License](LICENSE). See `LICENSE` for full terms.

---

<div align="center">

Built for defenders. Use responsibly and only against domains you own or have explicit permission to test.

</div>
