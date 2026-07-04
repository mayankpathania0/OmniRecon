# 🔍 OmniRecon

<p align="center">
  <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/OSINT-Tool-brightgreen.svg" alt="OSINT Tool">
  <img src="https://img.shields.io/badge/dependencies-zero-orange.svg" alt="Zero Dependencies">
</p>

**OmniRecon** is a high-performance, lightweight OSINT reconnaissance utility for passive subdomain discovery and active host verification. Instead of brute‑forcing subdomains with wordlists (which generates noisy network traffic), it quietly harvests historical subdomain records from public **Certificate Transparency (CT) logs** via [crt.sh](https://crt.sh), then uses a concurrent DNS resolution engine to verify which hosts are actually alive.

---

## ✨ Key Features

- **🕵️ Stealth Reconnaissance** – Gathers subdomains without touching the target infrastructure by querying public TLS/SSL certificate logs.
- **⚡ Concurrent Verification** – Uses Python's `concurrent.futures` to resolve hundreds of subdomains in parallel.
- **📦 No Wordlists Required** – Eliminates the guesswork and bloat of dictionary‑based brute‑forcing by focusing on domains that have actually been registered.
- **🧹 Smart Filtering** – Automatically strips duplicates, filters out wildcard entries (`*.example.com`), and cleans raw API responses.
- **📄 Clean Output** – Saves only verified, active subdomains to a simple `{domain}_results.txt` file.
- **🔧 Zero External Overhead** – Runs out of the box with just the Python standard library + `requests`.

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/mayankpathania0/OmniRecon.git

# Navigate into the project folder
cd OmniRecon

# Install the only lightweight dependency
pip install -r requirements.txt
🚀 Usage
bash
python OmniRecon.py -d <target_domain> [-t <threads>]
Argument	Description
-d, --domain	Required. The root domain to enumerate (e.g., example.com).
-t, --threads	Optional. Number of concurrent DNS resolution threads (default: 50).
📌 Examples
Objective	Command
Standard discovery & scan	python OmniRecon.py -d example.com
High‑velocity pipeline	python OmniRecon.py -d example.com --threads 100
📊 Sample Output
text
======================================================================
 / _ \ _ __   ___ (_) _ \ ___   ___ ___ _ __
| | | | '_ \ / _ \| | |_) / _ \ / __/ _ \| '_ \
| |_| | | | | (_) | |  _ <  __/| (_| (_) | | | |
 \___/|_| |_|\___/|_|_| \_\___| \___\___/|_| |_|
          Certificate Transparency Log Domain Verifier
======================================================================

[*] Fetching subdomains for 'example.com' from crt.sh...
[+] Passive extraction completed. Extracted 42 unique subdomains.

[*] Starting active verification utilizing 50 threads...

SUBDOMAIN                                             IP ADDRESS          STATUS    
----------------------------------------------------------------------------------------
api.example.com                                       192.168.1.99        [ACTIVE]
dev.example.com                                       10.0.0.45           [ACTIVE]
portal.example.com                                    172.16.22.11        [ACTIVE]

----------------------------------------------------------------------------------------
[+] Resolution complete. 3 subdomains are verified active.

[+] Active subdomains exported to: example.com_results.txt
⚙️ How It Works
Passive Extraction – Queries the public crt.sh API for all certificates that match %.{domain} and extracts every unique subdomain from the name_value field.

Deduplication & Cleaning – Removes duplicates, strips wildcard entries (*), and ensures only subdomains belonging to the target domain are kept.

Active Verification – Spawns a configurable thread pool to perform DNS lookups (socket.gethostbyname) on each subdomain.

Output – Writes only the successfully resolved subdomains to {domain}_results.txt.

⚠️ Disclaimer
IMPORTANT – This tool is intended exclusively for educational purposes, academic research, and authorized penetration testing environments. Intercepting or querying data trends must align with standard ethical boundaries. The developer disclaims all liability for unauthorized deployment or systemic disruption.

🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

📄 License
This project is open‑source and available under the MIT License.

🙏 Acknowledgments
crt.sh for providing the Certificate Transparency log data.

The OSINT and security community for inspiration and shared knowledge.

Made with ❤️ by mayankpathania0
