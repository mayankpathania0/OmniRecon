# 🌐 OmniRecon-CT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/OSINT-Passive--Recon-orange.svg" alt="OSINT Tool">
  <img src="https://img.shields.io/badge/Dependencies-None-brightgreen.svg" alt="Dependencies">
</p>

OmniRecon-CT is a high-performance command-line reconnaissance utility engineered to discover and verify a target's external attack surface. 

Unlike traditional brute-force enumerators that generate noisy network traffic, this tool employs a stealth-first model: it harvest subdomains passively via **Certificate Transparency (CT) logs**, then leverages a multithreaded DNS resolution architecture to safely determine which hosts are currently alive.

---

## 🚀 Key Features

* **Stealth Reconnaissance** | Gathers subdomains without interacting with target infrastructure by querying public `crt.sh` TLS/SSL certificate logs.
* **Concurrent Verification** | Processes hundreds of extracted targets simultaneously using Python's `concurrent.futures` to confirm active IP addresses.
* **No Wordlists Required** | Eliminates the guesswork and bulk of dictionary-based brute-forcing by focusing only on valid, historically registered domains.
* **Duplicate & Wildcard Filtration** | Automatically cleans inputs, strips redundant entries, and structures raw API outputs seamlessly.

---

## 🛠️ Installation & Setup

OmniRecon-CT is designed to run out of the box with zero external overhead.

```bash
# Clone the repository
git clone [https://github.com/mayankpathania0/OmniRecon-CT.git](https://github.com/mayankpathania0/OmniRecon-CT.git)

# Navigate to the project folder
cd OmniRecon-CT

# Install lightweight web dependencies
pip install -r requirements.txt
💻 Usage & SyntaxRun the script directly from your terminal by specifying a root domain and allocating your preferred thread count:Bashpython omnirecon.py -d <target_domain> --threads <num_threads>
ExamplesObjectiveCommandStandard Discovery & Scanpython omnirecon.py -d example.comHigh-Velocity Pipeline Verificationpython omnirecon.py -d example.com --threads 100📊 Live Output PreviewPlaintext 🌐 OmniRecon-CT v1.0 
 --------------------------------------------------
 Passive CT-Log Extraction & Active Verification
 --------------------------------------------------

[*] Initializing scan on target: example.com at 21:30:15
[*] Fetching historical certificate records from crt.sh...
[✓] Extracted 42 distinct subdomains via API.

[*] Initializing multithreaded host verification (50 workers)...
-----------------------------------------------------------------
SUBDOMAIN                          IP ADDRESS       STATUS
-----------------------------------------------------------------
api.example.com                    192.168.1.99     [ACTIVE]
dev.example.com                    10.0.0.45        [ACTIVE]
portal.example.com                 172.16.22.11     [ACTIVE]
-----------------------------------------------------------------

[+] Scan complete. Total active subdomains identified: 3
[+] Complete clean list exported to: example.com_results.txt 


🛡️ Disclaimer[!IMPORTANT]This security utility is intended exclusively for educational purposes, academic research, and authorized penetration testing environments. Intercepting or querying data trends must align with standard ethical boundaries. The developer disclaims all liability for unauthorized deployment or systemic disruption.
