#!/usr/bin/env python3
"""
OmniRecon: OSINT Certificate Transparency Reconnaissance Tool
This script passively collects subdomains of a target domain via crt.sh
and concurrently resolves them using local DNS queries to verify active hosts.
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Set a default global socket timeout to prevent the DNS resolution thread 
# from locking up on unresponsive configurations.
socket.setdefaulttimeout(3.0)

ASCII_BANNER = """
======================================================================
  ___           _ ____                     
 / _ \ _ __ ___ (_)  _ \ ___  ___ ___  _ __ 
| | | | '_ ` _ \| | |_) / _ \/ __/ _ \| '_ \\
| |_| | | | | | | |  _ <  __/ (_| (_) | | | |
 \___/|_| |_| |_|_|_| \_\___|\___\___/|_| |_|
                                             
   Certificate Transparency Log Domain Verifier
======================================================================
"""


def parse_arguments():
    """
    Sets up argparse to handle command-line interfaces.
    Returns parsed arguments with target domain and thread count.
    """
    parser = argparse.ArgumentParser(
        description="OmniRecon: Passive Certificate Transparency Log Domain Verifier"
    )
    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="The target root domain to extract subdomains for (e.g., example.com).",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=50,
        help="Number of concurrent DNS resolution threads (default: 50).",
    )
    return parser.parse_args()


def fetch_crt_sh_subdomains(domain):
    """
    Phase 1: Passive Extraction
    Queries crt.sh JSON API for the requested domain.
    Parses the response to extract, clean, and deduplicate subdomains.
    """
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    subdomains = set()

    print(f"[*] Fetching subdomains for '{domain}' from crt.sh...")

    try:
        # Request data with a defined timeout to prevent blocking indefinitely
        response = requests.get(url, headers=headers, timeout=25)
        response.raise_for_status()

        # Handle potentials failures in json parsing if crt.sh returns an invalid payload
        try:
            records = response.json()
        except ValueError as json_err:
            print(f"[-] JSON Parsing Error: Failed to parse crt.sh response. {json_err}")
            return subdomains

        for record in records:
            name_value = record.get("name_value", "")
            # Subdomains can be newline-separated within a single database entry
            for entry in name_value.split("\n"):
                entry = entry.strip().lower()
                # Skip wildcards and empty strings
                if entry.startswith("*") or not entry:
                    continue
                # Double check to ensure we only collect subdomains belonging to the target domain
                if entry.endswith(domain):
                    subdomains.add(entry)

        print(f"[+] Passive extraction completed. Extracted {len(subdomains)} unique subdomains.")
        return subdomains

    except requests.exceptions.Timeout:
        print("[-] Error: Request to crt.sh API timed out.")
    except requests.exceptions.HTTPError as http_err:
        print(f"[-] HTTP Error: Received unexpected status from crt.sh. Details: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"[-] Connection Error: Unable to reach crt.sh. Details: {req_err}")

    return subdomains


def resolve_subdomain(subdomain):
    """
    Phase 2: Active Verification Helper
    Attempts to map a single subdomain to an IP address.
    Returns (subdomain, IP, STATUS) if active, or (subdomain, None, STATUS) otherwise.
    """
    try:
        ip_address = socket.gethostbyname(subdomain)
        return subdomain, ip_address, "[ACTIVE]"
    except (socket.gaierror, socket.timeout):
        # socket.gaierror typically indicates resolution failures
        return subdomain, None, None
    except Exception:
        # Catch unexpected errors to avoid thread workers crashing
        return subdomain, None, None


def verify_subdomains(subdomains, thread_count):
    """
    Phase 2: Active Verification
    Leverages ThreadPoolExecutor to verify multiple subdomains in parallel.
    Collects and logs successfully resolved hosts.
    """
    active_results = []
    if not subdomains:
        print("[-] No subdomains to verify.")
        return active_results

    print(f"[*] Starting active verification utilizing {thread_count} threads...")
    print(f"\n{'SUBDOMAIN':<55} {'IP ADDRESS':<18} {'STATUS':<10}")
    print("-" * 88)

    try:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            # Map future objects to their associated subdomain
            future_to_sub = {
                executor.submit(resolve_subdomain, sub): sub for sub in subdomains
            }

            for future in as_completed(future_to_sub):
                subdomain, ip, status = future.result()
                if status == "[ACTIVE]" and ip:
                    print(f"{subdomain:<55} {ip:<18} {status:<10}")
                    active_results.append((subdomain, ip))
    except KeyboardInterrupt:
        print("\n[-] Thread execution canceled by user.")
        sys.exit(1)

    print("-" * 88)
    print(f"[+] Resolution complete. {len(active_results)} subdomains are verified active.\n")
    return active_results


def write_results_to_file(domain, active_results):
    """
    Saves only the active, resolved subdomains to <domain>_results.txt.
    """
    if not active_results:
        print("[*] No active subdomains found to save.")
        return

    filename = f"{domain}_results.txt"
    try:
        # Sort results alphabetically by subdomain
        sorted_subdomains = sorted([result[0] for result in active_results])
        with open(filename, "w", encoding="utf-8") as f:
            for sub in sorted_subdomains:
                f.write(f"{sub}\n")
        print(f"[+] Active subdomains exported to: {filename}")
    except IOError as io_err:
        print(f"[-] System Error: Failed to write output file: {io_err}")


def main():
    print(ASCII_BANNER)
    args = parse_arguments()

    # Step 1: Passive Phase
    extracted_subdomains = fetch_crt_sh_subdomains(args.domain)

    # Step 2: Active Phase
    if extracted_subdomains:
        active_results = verify_subdomains(extracted_subdomains, args.threads)
        
        # Step 3: Write Output
        write_results_to_file(args.domain, active_results)
    else:
        print("[-] No valid records fetched from the logs. Terminating.")


if __name__ == "__main__":
    main()
