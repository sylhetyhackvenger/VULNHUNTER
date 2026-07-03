# 🔍 Vuln Hunter – The Multi‑Tool Web Vulnerability Scanner

<p align="center">
  <img src="https://raw.githubusercontent.com/SYLHETYHACKVENGER/vuln-hunter/assets/banner.png" alt="Vuln Hunter Banner" width="100%">
</p>

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-brightgreen.svg" alt="Python 3.8+"></a>
  <a href="#-tools-used-dashboard"><img src="https://img.shields.io/badge/tools-20+-orange.svg" alt="Tools"></a>
  <a href="https://github.com/SYLHETYHACKVENGER/vuln-hunter"><img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status"></a>
</p>

**Vuln Hunter** is an advanced, red‑team friendly vulnerability orchestration framework that consolidates **20+ of the most powerful security tools** into a single, automated intelligence workflow. It delivers comprehensive visibility into your attack surface—ranging from critical DNS misconfigurations to deeply embedded SSL weaknesses, open ports, and exploitable web application entry points.

> 🛠️ **Credits & Origin:** Vuln Hunter is built as an extensively upgraded and enhanced version of the popular open-source tool **RapidScan**, integrating broader multi-tool checks, robust error handling, and refined execution parameters.

---

## 🖥️ Live Simulations

### 🔹 Safe Mode Scan
![Safe Mode Simulation](https://raw.githubusercontent.com/SYLHETYHACKVENGER/vuln-hunter/main/assets/safe_scan.gif)

### 🔹 Aggressive Mode Scan
![Aggressive Mode Simulation](https://raw.githubusercontent.com/SYLHETYHACKVENGER/vuln-hunter/main/assets/aggressive_scan.gif)

---

## 📖 Tool Overview

Vuln Hunter is a Python-based automation framework integrating industry-standard tools like **Nmap, Nikto, Wapiti, Amass, SSLyze, Golismero, TheHarvester, Dirb, Uniscan, WhatWeb, DNSRecon, Fierce, WAFW00F, and more**. It supports both non-intrusive and aggressive execution paths. 

With a single unified command, it covers **Web App Testing** (XSS, SQLi, LFI/RFI, Shellshock, Heartbleed, POODLE, CCS Injection, FREAK, LOGJAM, OCSP, and session configuration issues); **Network Reconnaissance** (TCP/UDP port scanning, OS detection, service enumeration, and vulnerability scripts via Nmap NSE); **DNS Analysis** (zone transfers, subdomain brute-forcing, DNSWalk, WHOIS, and IPv6 audits); **Information Gathering** (email harvesting, web fingerprinting, load-balancer detection, and internal IP leaks); and **Directory Discovery** via Dirb, Uniscan, and Nikto. 

Featuring fully verbose tracing (`-v`), it provides transparent, auditable results ideal for pen-testers, bug-bounty hunters, and engineers demanding rapid, multi-threaded asset evaluations.

---

## 🚀 Capabilities at a Glance

| Category | Capabilities Included |
| :--- | :--- |
| **Web Application** | XSS, SQLi, LFI, RFI, RCE, Shellshock, HTTP Options, PUT/DEL methods, Header analysis, X‑XSS‑Protection, Internal IP leaks |
| **SSL/TLS Hardening** | Heartbleed, POODLE, CCS Injection, FREAK, LOGJAM, OCSP Stapling, Zlib compression, Secure Renegotiation, Session Resumption |
| **Network Recon** | Full TCP/UDP port scanning, OS detection, service versioning, SMB, FTP, Telnet, RDP, SNMP, MS‑SQL, MySQL, Oracle |
| **DNS Analysis** | Zone transfers, subdomain brute‑force (Amass, DNSEnum, Fierce, DNSMap), DNSWalk, WHOIS, IPv6 existence validation |
| **Information Gathering** | Email harvesting (TheHarvester, DMitry), Web fingerprinting, WAF detection, Load‑balancer detection, Internal IP disclosure |
| **Directory & File** | Directory brute‑force (Dirb, Uniscan, Nikto), File discovery, WebDAV detection |
| **Aggressive Mode Extras** | Full Nmap (`-A -p- --script vuln`), Nikto all tests, Wapiti `-m all`, Amass `-active -brute`, DNSEnum full, Dnsrecon brute, Fierce wide, WhatWeb level 4, Golismero all plugins, Uniscan all checks, TheHarvester all sources |

---

## 🛠️ Tools Used (Dashboard)

| Tool | Purpose | Command Context (Aggressive Mode) |
| :--- | :--- | :--- |
| **Nmap** | Port scanning, OS detection, vulnerability scripts | `nmap -A -T4 -p- --script vuln -Pn -n -sT` |
| **Nikto** | Web server vulnerability scanning | `nikto -h <target> -Tuning x -ssl` |
| **Wapiti** | Web application vulnerability scanner (SQLi, XSS, etc.) | `wapiti -u <target> -m all -S aggressive` |
| **Amass** | DNS enumeration and subdomain brute‑forcing | `amass enum -active -brute -d <domain>` |
| **DNSEnum** | DNS zone transfers and subdomain brute‑forcing | `dnsenum --enum <domain>` |
| **Dnsrecon** | DNS reconnaissance with brute‑force | `dnsrecon -d <domain> -t brt` |
| **Fierce** | Subdomain brute‑forcing with DNS scanning | `fierce --domain <domain> --wide` |
| **WhatWeb** | Web technology fingerprinting | `whatweb -a 4 <target>` |
| **Golismero** | All‑in‑one security scanner with plugins | `golismero scan <target> --plugins all` |
| **Uniscan** | File/directory brute‑force, stress, LFI/RFI/XSS/SQLi | `uniscan -u <target> -qwedj` |
| **TheHarvester** | Email and subdomain harvesting from public sources | `theHarvester -d <domain> -b all -l 500` |
| **SSLyze** | SSL/TLS configuration auditing | `sslyze --regular <target>` |
| **WAFW00F** | Web Application Firewall detection | `wafw00f <target>` |
| **LBD** | Load‑balancer detection | `lbd <domain>` |
| **Dirb** | Directory brute‑force | `dirb http://<target>` |
| **Davtest** | WebDAV vulnerability testing | `davtest -url http://<target>` |
| **DNSWalk** | DNS zone transfer and misconfiguration check | `dnswalk <domain>.` |
| **DNSMap** | Subdomain brute‑forcing | `dnsmap <domain>` |
| **DMitry** | Email and subdomain harvesting (passive) | `dmitry -e/-s <target>` |
| **Host** | DNS record lookup (IPv6, etc.) | `host -v <domain>` |
| **Whois** | WHOIS lookup for administrative info | `whois <domain>` |
| **Wget** | Web file retrieval (for misconfiguration checks) | `wget -O /tmp/... <target>/path` |

---

## 📦 Setup & Installation

### 🔹 Prerequisites
* **Python 3.8+** along with `pip`
* **Linux / macOS** operating system (Ubuntu/Debian recommended)
* *Root privileges are not explicitly required* (Nmap defaults to `-sT` TCP connect scans to avoid raw socket requirement)

### 🔹 Installation Workflow

| Step | Scope | Command |
| :--- | :--- | :--- |
| **1. Update Repositories** | System | `sudo apt update` |
| **2. Install Global Tools** | System | `sudo apt install -y nmap nikto wapiti amass dnsenum dnsrecon fierce whatweb golismero uniscan theharvester sslyze wafw00f lbd dirb davtest dnswalk dnsmap dmitry whois wget host` |
| **3. Clone Repository** | Local | `git clone https://github.com/SYLHETYHACKVENGER/vuln-hunter.git` |
| **4. Navigate & Setup** | Local | `cd vuln-hunter && pip install -r requirements.txt` |
| **5. Execute Tool** | Local | `python3 vuln_hunter.py --help` |

---

## ⚖️ Disclaimer
This tool is built strictly for educational purposes, authorized security auditing, and penetration testing. The author assumes no liability for misuse, unauthorized targets, or malicious actions executed with this framework. Always ensure you have written permission before conducting scans.

---
<p align="center">
  <b>Developed with ❤️ by <a href="https://github.com/SYLHETYHACKVENGER">SYLHETYHACKVENGER (THE-ERROR808)</a></b><br>
  <sub>Empowering security researchers with scalable orchestration.</sub>
</p>
