#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================================
#  ██╗   ██╗██╗   ██╗██╗     ███╗   ██╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
#  ██║   ██║██║   ██║██║     ████╗  ██║    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
#  ██║   ██║██║   ██║██║     ██╔██╗ ██║    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
#  ██║   ██║██║   ██║██║     ██║╚██╗██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
#  ╚██████╔╝╚██████╔╝███████╗██║ ╚████║    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
#   ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
#
#  Tool       : Vuln Hunter v2.0
#  Author     : SYLHETYHACKVENGER (THE-ERROR808)
#  Description: Multi‑Tool Web Vulnerability Scanner with aggressive extras
#  Usage      : python3 vulnhunter.py example.com -v --extra
# ========================================================================

import sys
import argparse
import subprocess
import os
import time
import random
import threading
import re
import shutil
from urllib.parse import urlsplit

# ─── Terminal control ──────────────────────────────────────────────────────
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
CLEAR_SCREEN = '\x1b[2J'
CURSOR_HOME = '\x1b[H'

# ─── Color palette (neon/futuristic) ──────────────────────────────────────
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BADFAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_CRIT = '\033[45m'
    BG_HIGH = '\033[41m'
    BG_MED  = '\033[43m'
    BG_LOW  = '\033[44m'
    BG_INFO = '\033[42m'

# ─── Time formatter ──────────────────────────────────────────────────────
intervals = (('h', 3600), ('m', 60), ('s', 1))
def display_time(seconds, granularity=3):
    result = []
    seconds = seconds + 1
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append("{}{}".format(value, name))
    return ' '.join(result[:granularity])

def terminal_size():
    try:
        rows, columns = subprocess.check_output(['stty', 'size']).split()
        return int(columns)
    except:
        return 80

def url_maker(url):
    if not re.match(r'http(s?)\:', url):
        url = 'http://' + url
    parsed = urlsplit(url)
    host = parsed.netloc
    if host.startswith('www.'):
        host = host[4:]
    return host

def check_internet():
    os.system('ping -c1 github.com > /tmp/vh_net 2>&1')
    val = 1 if "0% packet loss" in open('/tmp/vh_net').read() else 0
    os.system('rm /tmp/vh_net 2>/dev/null')
    return val

# ─── Vulnerability helper ──────────────────────────────────────────────
def vul_info(val):
    if val == 'c': return Colors.BG_CRIT + " CRITICAL " + Colors.ENDC
    elif val == 'h': return Colors.BG_HIGH + " HIGH " + Colors.ENDC
    elif val == 'm': return Colors.BG_MED + " MEDIUM " + Colors.ENDC
    elif val == 'l': return Colors.BG_LOW + " LOW " + Colors.ENDC
    else: return Colors.BG_INFO + " INFO " + Colors.ENDC

proc_high = Colors.RED + "●" + Colors.ENDC
proc_med  = Colors.YELLOW + "●" + Colors.ENDC
proc_low  = Colors.GREEN + "●" + Colors.ENDC

def vul_remed_info(v1, v2, v3):
    print(Colors.BOLD + "██ Vulnerability Threat Level" + Colors.ENDC)
    print("  " + vul_info(v2) + " " + Colors.WARNING + str(tool_resp[v1][0]) + Colors.ENDC)
    print(Colors.BOLD + "██ Attacker Gain" + Colors.ENDC)
    print("  " + Colors.RED + str(tools_fix[v3-1][1]) + Colors.ENDC)
    print(Colors.BOLD + "██ Vulnerability Definition" + Colors.ENDC)
    print("  " + Colors.RED + str(tools_fix[v3-1][2]) + Colors.ENDC)
    print(Colors.BOLD + "██ Remediation" + Colors.ENDC)
    print("  " + Colors.GREEN + str(tools_fix[v3-1][3]) + Colors.ENDC)

# ─── Help ──────────────────────────────────────────────────────────────
def helper():
    print(Colors.CYAN + "█ Information:" + Colors.ENDC)
    print("  ./vulnhunter.py example.com            – Standard scan")
    print("  ./vulnhunter.py example.com --extra    – Add aggressive red‑team scans")
    print("  ./vulnhunter.py example.com -v --extra – Verbose + aggressive")
    print("  ./vulnhunter.py --update               – Update to latest")
    print("  ./vulnhunter.py --help                 – This help")
    print(Colors.CYAN + "█ Interactive:" + Colors.ENDC)
    print("  Ctrl+C  – Skip current test")
    print("  Ctrl+Z  – Quit")
    print(Colors.CYAN + "█ Legends:" + Colors.ENDC)
    print("  [" + proc_high + "] Long scan time")
    print("  [" + proc_med + "] Medium scan time")
    print("  [" + proc_low + "] Short scan time")
    print(Colors.CYAN + "█ Severity:" + Colors.ENDC)
    print("  " + vul_info('c') + " Immediate action required")
    print("  " + vul_info('h') + " High probability of compromise")
    print("  " + vul_info('m') + " Can be combined with other flaws")
    print("  " + vul_info('l') + " Recommended to fix")
    print("  " + vul_info('i') + " Informational only\n")

# ─── COLORFUL BANNER ──────────────────────────────────────────────────────
def banner():
    os.system('clear')
    colors = [Colors.CYAN, Colors.MAGENTA, Colors.YELLOW, Colors.GREEN, Colors.BLUE]
    banner_lines = [
        "⣤⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤",
        "⣿⣿⣿⠀⠀⠀⠀⠀⠀⢀⡠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠚⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿",
        "⠀⠀⠀⠀⠀⠀⠀⠠⠾⠉⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⠀⠀⠀⠀⠀⠀⠀⠉",
        "⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀",
        "⢦⣀⣀⣀⣀⣠⠴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣐⣄⣀⠀⠀⠀⣀⠔⠚⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢦⣄⠀⠀⠀⠀",
        "⠀⠻⢭⡉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠔⠛⠉⠀⢀⣤⠔⠚⠁⠀⠀⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⡀⠀",
        "⣶⣶⣶⡟⠲⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠖⢠⣾⡥⠖⠊⠉⡽⠉⠀⠀⢀⡀⠀⠀⠈⠓⠦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲",
        "⠁⠀⠈⡃⠀⠀⠀⠉⣩⠷⠃⠀⠀⠀⠀⠀⢀⡴⠋⠀⢠⠟⠁⠀⠀⠀⠀⠳⡄⠀⠀⠳⣝⠦⠤⣀⣀⣀⣀⣀⣉⣩⠤⠶⠚⠉⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⣀⢀⣀⣀⣤⡾",
        "⠀⠀⠀⡇⠀⠀⣠⠞⢁⣀⣠⠀⠀⠀⠀⣠⠛⠀⠀⣠⠟⠀⣠⠀⠀⠀⠀⠀⢈⠓⢤⣀⡈⠓⠦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣄⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠈⠻⢦⡀⢹⠁",
        "⠀⠀⠀⡇⣠⣾⣗⣚⣩⠟⠁⠀⠀⠀⡴⠁⠀⠀⡴⠃⢀⡼⠁⠀⡴⠀⠀⣠⠋⠀⠀⠈⠉⠑⠒⠚⠓⠒⠆⠰⣄⠀⠀⠰⣄⠀⠀⠈⢳⡀⠀⠀⠀⢳⡀⠀⠀⠀⠀⣤⣤⣀⠳⣌⠀",
        "⡀⠀⢸⡇⠀⠀⠀⣰⠃⠀⠀⠀⠀⣸⠁⠀⠀⡼⠁⢠⠎⠀⠀⡼⠁⠀⣰⠃⢀⡆⠀⠀⠀⡆⠀⠀⡀⠀⠀⠀⠈⢦⡀⠀⠈⢦⠀⠀⠀⠱⣄⠀⠀⠈⢧⠀⠀⠀⠀⠈⢣⡈⠑⢿⡂",
        "⣷⣶⣾⡇⢀⣠⠞⠁⠀⠀⠀⠀⣠⡇⠀⢀⣼⠁⢀⡎⠀⢀⣼⠁⢀⣼⡇⠀⣼⠃⠀⠀⣰⣧⠀⠀⣿⣦⡀⠀⠀⠈⣿⡶⡀⠀⢣⡀⠀⠀⢻⣷⡄⠀⠸⡀⠀⠀⠀⠀⠈⢳⡀⢸⣿",
        "⣿⣿⣯⣍⡉⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⣼⡏⠀⣸⠀⢀⣾⡿⠀⢼⣿⠀⠸⣿⡀⠀⠀⣿⣿⣄⠀⢻⡇⠹⣦⠀⠀⢸⣿⣽⣄⠈⢿⡄⠀⠀⣿⣿⡄⠀⣧⡈⢧⢄⠀⠀⠀⠙⢿⣻",
        "⣿⣿⣿⡇⠉⠛⠓⠒⣒⡶⠛⣠⣿⠀⣰⡿⡇⢰⣿⠀⡜⣼⢣⠀⣸⢻⠀⠀⣾⡇⠀⢰⠉⢹⣿⣄⠸⣿⡴⢛⣷⡀⠨⣟⠻⣿⡄⢸⣿⡄⠀⣿⠉⢿⠀⣿⣷⠈⢷⣝⣓⣦⣄⣀⣽",
        "⣿⣿⣿⡷⠚⠓⠒⠲⣾⠃⣼⣿⢿⡀⣿⠃⡇⡼⣿⠀⢠⣿⣾⣠⣿⣮⡇⠀⡿⢱⡄⢸⠀⣾⡟⢻⣮⡛⣿⠋⠉⣻⣤⣏⣅⣹⡁⢸⢿⣷⠀⣿⠶⣾⣷⡿⣷⠃⠸⡿⠿⠿⠯⢽⣿",
        "⣿⡟⢻⡇⠀⠀⠀⠀⣿⣴⢫⡇⠀⣇⣿⠤⣿⠀⣿⣿⣿⣿⣿⣿⡿⢿⣿⣾⣿⣦⡹⣄⠀⠸⣷⣻⠀⢙⣾⣿⣿⣾⢷⡿⣾⣿⣇⢸⣼⣇⡆⣯⣤⡜⣿⠀⢸⣧⡄⣷⠀⠀⠀⢸⣿",
        "⣋⣀⣸⡇⠀⠀⠀⠀⠿⠁⢸⡇⠀⠘⡇⣠⣼⣦⣿⠙⣿⠋⠁⠀⠀⠤⣶⣽⠋⢷⡅⠈⢦⡀⠹⣼⡇⢾⣿⠿⢯⣤⡈⠀⠈⠙⢻⡿⢋⣿⣼⣧⠰⠃⣯⠀⢸⢿⣿⡟⠀⠀⠀⢸⣿",
        "⣿⣿⣿⡇⠀⠀⠀⠀⠀⢠⠟⠀⠀⣸⠃⡗⣶⢿⣿⡇⠈⠀⠀⠀⣤⣀⣾⣿⣇⠀⠋⠀⠀⠉⠳⢿⡵⠋⢠⣄⣠⣿⣿⡆⠀⠀⠼⠁⣸⣿⠃⢸⠀⢀⡿⠀⢸⠈⠋⠀⠀⠀⠀⢸⣿",
        "⣿⣿⢿⡇⢠⡀⣀⣀⣼⣯⣤⣶⡒⣻⣆⠀⢻⣄⠻⢷⠀⠀⠘⢦⣻⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⢃⡠⠀⠀⢀⣿⣃⡴⠋⣀⣾⡧⣤⣘⡇⠀⠀⠀⠀⠀⠈⠀",
        "⣻⣿⣼⣿⣄⣿⣿⡟⠉⢉⣉⠙⣛⣁⣘⣷⣤⡈⠛⠾⣇⠀⠀⠀⠉⠛⠛⠉⠁⠀⠀⠀⣶⠀⠀⠀⠀⠀⠈⠙⠛⠛⠛⠉⠀⠀⠀⢸⠉⠉⣠⣾⣿⡟⣿⣿⣿⡿⠛⠛⠒⠒⠂⠰⠀",
        "⣿⣾⣿⡟⢻⣧⣿⣿⡲⡤⣿⣷⣾⣿⣿⠉⣿⣿⠦⣤⣼⣿⠉⠉⡇⠀⠀⠀⠀⠀⠀⢻⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⢲⣾⡏⠀⠉⢳⣾⣿⣿⣇⡀⠀⠀⠀⠀⠀⠀",
        "⣿⣶⣾⣷⡿⠻⢿⣷⣿⣋⣘⠃⣹⣿⣿⣾⣿⣿⣷⡿⠉⣿⡀⠀⢱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⢶⡀⢀⡼⣿⣾⣿⡟⠙⢿⣾⡇⠀⠉⠈⠙⠀⠀⣤⠀⠀⠀",
        "⣿⠙⢛⣿⣿⢶⣾⡻⣿⣿⣿⡿⢻⣿⣿⡟⠛⢿⡿⠷⣿⣿⣷⣤⡀⣹⠄⠀⠀⠀⠀⠠⢤⣀⠀⠀⠀⠀⠀⠀⠘⣇⢀⣠⣿⡟⣰⡟⣭⡟⠻⣼⣿⡿⠷⢾⡓⣠⡄⠀⠈⣉⡀⢸⣿",
        "⣛⣿⣿⣧⣹⡀⣿⣿⣿⣿⣿⣷⣾⠻⢿⣷⣺⣿⣿⣏⢉⡿⠻⡛⣿⣷⣤⡀⠀⠀⠀⠀⠤⡌⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠉⢹⣟⠻⠿⣿⣄⣐⣼⣿⣯⣰⠀⠀⣀⠀⢀⣍",
        "⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⡿⠶⣿⣿⡿⠛⠛⠛⠋⠀⢰⣧⣿⣿⣽⣿⣷⣦⣄⡀⠀⠀⠀⠀⢀⣤⠖⠋⠉⢿⣿⣇⣾⣽⣿⢰⠀⠘⢷⣤⣬⣿⣿⣿⠋⠛⣁⠛⣤⠉⠈⠈⠋",
        "⣿⣿⣿⣷⡀⣠⣿⣿⣿⣿⣿⣿⣶⣴⣿⣿⠁⠀⠀⠀⠀⠀⠈⣇⠹⣿⣿⣿⠉⠘⠆⠉⠓⠶⠶⠞⠉⠀⠀⠀⠀⠀⣼⣿⣿⣿⢿⡟⠀⠀⠀⠉⠁⠀⠈⠙⢷⠞⠻⡇⢀⠀⠀⢀⠰",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠶⠞⠉⠀⠀⠸⣆⠀⠀⠀⠀⠀⠀⢹⡄⠙⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⢛⣽⡿⢋⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣄⣛⠶⠀⠀⠲⠦",
        "⡿⣿⠷⠾⣯⡙⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀⢻⡀⠙⢿⣧⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣽⡿⠋⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠋⠉⠛⢾⣷⣤⠀⠀",
        "⠁⣶⣿⣶⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠙⢦⡀⠻⣿⣿⡶⣄⠀⠀⠀⣠⢾⣿⣿⠟⣉⣤⠞⠋⠀⠀⠀⠀⠠⠄⢀⣠⠖⠋⠀⠀⠀⠀⠀⠀⠙⣿⣆⣌",
        "⣶⣿⣿⣿⣿⠋⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⢀⣙⣦⣄⠀⠀⠀⠀⠀⠉⠛⠺⢿⣧⣬⣻⣶⣚⢅⣾⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⢠⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿",
        "⠿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠸⣿⡄⢄⣇⣀⡴⠞⠉⠁⠉⠉⠉⠉⠓⢦⣄⡀⢀⣀⠀⠹⣆⠀⠀⢠⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠋⠀⠀⠀⠀⠀⠀⠀⣦⠀⠀⠀⠀⠀⢸⣿",
        "⠶⠿⠋⠀⠀⠀⠀⠀⠀⠀⣤⠟⠉⠙⠿⣀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠈⠙⠻⣿⠿⢦⣸⡆⠀⡜⢀⣤⣶⣃⣤⣤⣤⠤⠤⠶⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠘⣿",
        "⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠓⠀⠀⠀⠀⠈⠳⢶⣿⠟⡛⡋⢙⣟⠓⠻⠷⢶⣛⡁⢀⡀⢉⡟⣿⡛⠛⣉⣿⣿⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⣿"
    ]
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        print(color + line + Colors.ENDC)
    print(Colors.MAGENTA + "  ════════════════════════════════════════════════════════════════════════" + Colors.ENDC)
    print(Colors.CYAN + "  █  Tool : Vuln Hunter v2.0   █  Author : SYLHETYHACKVENGER (THE-ERROR808)" + Colors.ENDC)
    print(Colors.MAGENTA + "  ════════════════════════════════════════════════════════════════════════" + Colors.ENDC + "\n")

# ─── Fiber‑Optic Spinner ──────────────────────────────────────────────
class FiberOptic:
    def __init__(self, disabled=False):
        self.busy = False
        self.delay = 0.05
        self.thread = None
        self.disabled = disabled
        self.beam_pos = 0
        self.beam_dir = 1

    def _animate(self):
        cols = terminal_size()
        while self.busy:
            if not self.disabled:
                line = ""
                for i in range(cols - 10):
                    if i == self.beam_pos:
                        line += Colors.CYAN + "█" + Colors.ENDC
                    else:
                        if random.random() < 0.1:
                            line += Colors.WARNING + "░" + Colors.ENDC
                        else:
                            line += Colors.BG_BLACK + " " + Colors.ENDC
                self.beam_pos += self.beam_dir
                if self.beam_pos >= cols - 10 or self.beam_pos <= 0:
                    self.beam_dir *= -1
                sys.stdout.write("\r" + line)
                sys.stdout.flush()
                time.sleep(self.delay)
            else:
                time.sleep(0.1)

    def start(self):
        self.busy = True
        self.beam_pos = 0
        self.beam_dir = 1
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.busy = False
        if self.thread:
            self.thread.join(timeout=0.3)
        sys.stdout.write("\r" + " " * terminal_size() + "\r")
        sys.stdout.flush()

# ─── MAIN TOOL DEFINITIONS ─────────────────────────────────────────────
# (Standard safe scans – unchanged)
tool_names = [
    ["host","Host - Checks for existence of IPV6 address.","host",1],
    ["aspnet_config_err","ASP.Net Misconfiguration - Checks for ASP.Net Misconfiguration.","wget",1],
    ["wp_check","WordPress Checker - Checks for WordPress Installation.","wget",1],
    ["drp_check", "Drupal Checker - Checks for Drupal Installation.","wget",1],
    ["joom_check", "Joomla Checker - Checks for Joomla Installation.","wget",1],
    ["uniscan","Uniscan - Checks for robots.txt & sitemap.xml","uniscan",1],
    ["wafw00f","Wafw00f - Checks for Application Firewalls.","wafw00f",1],
    ["nmap","Nmap - Fast Scan [Only Few Port Checks]","nmap",1],
    ["theHarvester","The Harvester - Scans for emails using Google's passive search.","theHarvester",1],
    ["dnsrecon","DNSRecon - Attempts Multiple Zone Transfers on Nameservers.","dnsrecon",1],
    ["dnswalk","DNSWalk - Attempts Zone Transfer.","dnswalk",1],
    ["whois","WHOis - Checks for Administrator's Contact Information.","whois",1],
    ["nmap_header","Nmap [XSS Filter Check] - Checks if XSS Protection Header is present.","nmap",1],
    ["nmap_sloris","Nmap [Slowloris DoS] - Checks for Slowloris Denial of Service Vulnerability.","nmap",1],
    ["sslyze_hbleed","SSLyze - Checks only for Heartbleed Vulnerability.","sslyze",1],
    ["nmap_hbleed","Nmap [Heartbleed] - Checks only for Heartbleed Vulnerability.","nmap",1],
    ["nmap_poodle","Nmap [POODLE] - Checks only for Poodle Vulnerability.","nmap",1],
    ["nmap_ccs","Nmap [OpenSSL CCS Injection] - Checks only for CCS Injection.","nmap",1],
    ["nmap_freak","Nmap [FREAK] - Checks only for FREAK Vulnerability.","nmap",1],
    ["nmap_logjam","Nmap [LOGJAM] - Checks for LOGJAM Vulnerability.","nmap",1],
    ["sslyze_ocsp","SSLyze - Checks for OCSP Stapling.","sslyze",1],
    ["sslyze_zlib","SSLyze - Checks for ZLib Deflate Compression.","sslyze",1],
    ["sslyze_reneg","SSLyze - Checks for Secure Renegotiation Support and Client Renegotiation.","sslyze",1],
    ["sslyze_resum","SSLyze - Checks for Session Resumption Support with [Session IDs/TLS Tickets].","sslyze",1],
    ["lbd","LBD - Checks for DNS/HTTP Load Balancers.","lbd",1],
    ["golismero_dns_malware","Golismero - Checks if the domain is spoofed or hijacked.","golismero",1],
    ["golismero_heartbleed","Golismero - Checks only for Heartbleed Vulnerability.","golismero",1],
    ["golismero_brute_url_predictables","Golismero - BruteForces for certain files on the Domain.","golismero",1],
    ["golismero_brute_directories","Golismero - BruteForces for certain directories on the Domain.","golismero",1],
    ["golismero_sqlmap","Golismero - SQLMap [Retrieves only the DB Banner]","golismero",1],
    ["dirb","DirB - Brutes the target for Open Directories.","dirb",1],
    ["xsser","XSSer - Checks for Cross-Site Scripting [XSS] Attacks.","xsser",1],
    ["golismero_ssl_scan","Golismero SSL Scans - Performs SSL related Scans.","golismero",1],
    ["golismero_zone_transfer","Golismero Zone Transfer - Attempts Zone Transfer.","golismero",1],
    ["golismero_nikto","Golismero Nikto Scans - Uses Nikto Plugin to detect vulnerabilities.","golismero",1],
    ["golismero_brute_subdomains","Golismero Subdomains Bruter - Brute Forces Subdomain Discovery.","golismero",1],
    ["dnsenum_zone_transfer","DNSEnum - Attempts Zone Transfer.","dnsenum",1],
    ["fierce_brute_subdomains","Fierce Subdomains Bruter - Brute Forces Subdomain Discovery.","fierce",1],
    ["dmitry_email","DMitry - Passively Harvests Emails from the Domain.","dmitry",1],
    ["dmitry_subdomains","DMitry - Passively Harvests Subdomains from the Domain.","dmitry",1],
    ["nmap_telnet","Nmap [TELNET] - Checks if TELNET service is running.","nmap",1],
    ["nmap_ftp","Nmap [FTP] - Checks if FTP service is running.","nmap",1],
    ["nmap_stuxnet","Nmap [STUXNET] - Checks if the host is affected by STUXNET Worm.","nmap",1],
    ["webdav","WebDAV - Checks if WEBDAV enabled on Home directory.","davtest",1],
    ["golismero_finger","Golismero - Does a fingerprint on the Domain.","golismero",1],
    ["uniscan_filebrute","Uniscan - Brutes for Filenames on the Domain.","uniscan",1],
    ["uniscan_dirbrute", "Uniscan - Brutes Directories on the Domain.","uniscan",1],
    ["uniscan_ministresser", "Uniscan - Stress Tests the Domain.","uniscan",1],
    ["uniscan_rfi","Uniscan - Checks for LFI, RFI and RCE.","uniscan",1],
    ["uniscan_xss","Uniscan - Checks for XSS, SQLi, BSQLi & Other Checks.","uniscan",1],
    ["nikto_xss","Nikto - Checks for Apache Expect XSS Header.","nikto",1],
    ["nikto_subrute","Nikto - Brutes Subdomains.","nikto",1],
    ["nikto_shellshock","Nikto - Checks for Shellshock Bug.","nikto",1],
    ["nikto_internalip","Nikto - Checks for Internal IP Leak.","nikto",1],
    ["nikto_putdel","Nikto - Checks for HTTP PUT DEL.","nikto",1],
    ["nikto_headers","Nikto - Checks the Domain Headers.","nikto",1],
    ["nikto_ms01070","Nikto - Checks for MS10-070 Vulnerability.","nikto",1],
    ["nikto_servermsgs","Nikto - Checks for Server Issues.","nikto",1],
    ["nikto_outdated","Nikto - Checks if Server is Outdated.","nikto",1],
    ["nikto_httpoptions","Nikto - Checks for HTTP Options on the Domain.","nikto",1],
    ["nikto_cgi","Nikto - Enumerates CGI Directories.","nikto",1],
    ["nikto_ssl","Nikto - Performs SSL Checks.","nikto",1],
    ["nikto_sitefiles","Nikto - Checks for any interesting files on the Domain.","nikto",1],
    ["nikto_paths","Nikto - Checks for Injectable Paths.","nikto",1],
    ["dnsmap_brute","DNSMap - Brutes Subdomains.","dnsmap",1],
    ["nmap_sqlserver","Nmap - Checks for MS-SQL Server DB","nmap",1],
    ["nmap_mysql", "Nmap - Checks for MySQL DB","nmap",1],
    ["nmap_oracle", "Nmap - Checks for ORACLE DB","nmap",1],
    ["nmap_rdp_udp","Nmap - Checks for Remote Desktop Service over UDP","nmap",1],
    ["nmap_rdp_tcp","Nmap - Checks for Remote Desktop Service over TCP","nmap",1],
    ["nmap_full_ps_tcp","Nmap - Performs a Full TCP Port Scan","nmap",1],
    ["nmap_full_ps_udp","Nmap - Performs a Full UDP Port Scan","nmap",1],
    ["nmap_snmp","Nmap - Checks for SNMP Service","nmap",1],
    ["aspnet_elmah_axd","Checks for ASP.net Elmah Logger","wget",1],
    ["nmap_tcp_smb","Checks for SMB Service over TCP","nmap",1],
    ["nmap_udp_smb","Checks for SMB Service over UDP","nmap",1],
    ["wapiti","Wapiti - Checks for SQLi, RCE, XSS and Other Vulnerabilities","wapiti",1],
    ["nmap_iis","Nmap - Checks for IIS WebDAV","nmap",1],
    ["whatweb","WhatWeb - Checks for X-XSS Protection Header","whatweb",1],
    ["amass","AMass - Brutes Domain for Subdomains","amass",1]
]

# Default commands (safe, Ubuntu‑friendly)
tool_cmd = [
    ["host ", ""],
    ["wget -O /tmp/vulnhunter_aspnet_config_err --tries=1 ", "/%7C~.aspx"],
    ["wget -O /tmp/vulnhunter_wp_check --tries=1 ", "/wp-admin"],
    ["wget -O /tmp/vulnhunter_drp_check --tries=1 ", "/user"],
    ["wget -O /tmp/vulnhunter_joom_check --tries=1 ", "/administrator"],
    ["uniscan -e -u ", ""],
    ["wafw00f ", ""],
    ["nmap -F --open -Pn -n -sT ", ""],
    ["theHarvester -l 50 -b censys -d ", ""],
    ["dnsrecon -d ", ""],
    ["dnswalk -d ", "."],
    ["whois ", ""],
    ["nmap -p80 --script http-security-headers -Pn -n -sT ", ""],
    ["nmap -p80,443 --script http-slowloris --max-parallelism 500 -Pn -n -sT ", ""],
    ["sslyze --heartbleed ", ""],
    ["nmap -p443 --script ssl-heartbleed -Pn -n -sT ", ""],
    ["nmap -p443 --script ssl-poodle -Pn -n -sT ", ""],
    ["nmap -p443 --script ssl-ccs-injection -Pn -n -sT ", ""],
    ["nmap -p443 --script ssl-enum-ciphers -Pn -n -sT ", ""],
    ["nmap -p443 --script ssl-dh-params -Pn -n -sT ", ""],
    ["sslyze --certinfo ", ""],
    ["sslyze --compression ", ""],
    ["sslyze --reneg ", ""],
    ["sslyze --resum ", ""],
    ["lbd ", ""],
    ["golismero -e dns_malware scan ", ""],
    ["golismero -e heartbleed scan ", ""],
    ["golismero -e brute_url_predictables scan ", ""],
    ["golismero -e brute_directories scan ", ""],
    ["golismero -e sqlmap scan ", ""],
    ["dirb http://", " -fi"],
    ["xsser --all=http://", ""],
    ["golismero -e sslscan scan ", ""],
    ["golismero -e zone_transfer scan ", ""],
    ["golismero -e nikto scan ", ""],
    ["golismero -e brute_dns scan ", ""],
    ["dnsenum ", ""],
    ["fierce --domain ", ""],
    ["dmitry -e ", ""],
    ["dmitry -s ", ""],
    ["nmap -p23 --open -Pn -n -sT ", ""],
    ["nmap -p21 --open -Pn -n -sT ", ""],
    ["nmap --script stuxnet-detect -p445 -Pn -n -sT ", ""],
    ["davtest -url http://", ""],
    ["golismero -e fingerprint_web scan ", ""],
    ["uniscan -w -u ", ""],
    ["uniscan -q -u ", ""],
    ["uniscan -r -u ", ""],
    ["uniscan -s -u ", ""],
    ["uniscan -d -u ", ""],
    ["nikto -Plugins 'apache_expect_xss' -host ", ""],
    ["nikto -Plugins 'subdomain' -host ", ""],
    ["nikto -Plugins 'shellshock' -host ", ""],
    ["nikto -Plugins 'cookies' -host ", ""],
    ["nikto -Plugins 'put_del_test' -host ", ""],
    ["nikto -Plugins 'headers' -host ", ""],
    ["nikto -Plugins 'ms10-070' -host ", ""],
    ["nikto -Plugins 'msgs' -host ", ""],
    ["nikto -Plugins 'outdated' -host ", ""],
    ["nikto -Plugins 'httpoptions' -host ", ""],
    ["nikto -Plugins 'cgi' -host ", ""],
    ["nikto -Plugins 'ssl' -host ", ""],
    ["nikto -Plugins 'sitefiles' -host ", ""],
    ["nikto -Plugins 'paths' -host ", ""],
    ["dnsmap ", ""],
    ["nmap -p1433 --open -Pn -n -sT ", ""],
    ["nmap -p3306 --open -Pn -n -sT ", ""],
    ["nmap -p1521 --open -Pn -n -sT ", ""],
    ["nmap -p3389 --open -sU -Pn -n ", ""],
    ["nmap -p3389 --open -sT -Pn -n ", ""],
    ["nmap -p1-65535 --open -Pn -n -sT ", ""],
    ["nmap -p1-65535 -sU --open -Pn -n ", ""],
    ["nmap -p161 -sU --open -Pn -n ", ""],
    ["wget -O /tmp/vulnhunter_aspnet_elmah_axd --tries=1 ", "/elmah.axd"],
    ["nmap -p445,137-139 --open -Pn -n -sT ", ""],
    ["nmap -p137,138 --open -Pn -n -sT ", ""],
    ["wapiti ", " -f txt -o /tmp/vulnhunter_wapiti"],
    ["nmap -p80 --script=http-iis-webdav-vuln -Pn -n -sT ", ""],
    ["whatweb ", " -a 1"],
    ["amass enum -d ", ""]
]

tool_resp = [
    ["Does not have an IPv6 Address. It is good to have one.","i",1],
    ["ASP.Net is misconfigured to throw server stack errors on screen.","m",2],
    ["WordPress Installation Found. Check for vulnerabilities corresponds to that version.","i",3],
    ["Drupal Installation Found. Check for vulnerabilities corresponds to that version.","i",4],
    ["Joomla Installation Found. Check for vulnerabilities corresponds to that version.","i",5],
    ["robots.txt/sitemap.xml found. Check those files for any information.","i",6],
    ["No Web Application Firewall Detected","m",7],
    ["Some ports are open. Perform a full-scan manually.","l",8],
    ["Email Addresses Found.","l",9],
    ["Zone Transfer Successful using DNSRecon. Reconfigure DNS immediately.","h",10],
    ["Zone Transfer Successful using dnswalk. Reconfigure DNS immediately.","h",10],
    ["Whois Information Publicly Available.","i",11],
    ["XSS Protection Filter is Disabled.","m",12],
    ["Vulnerable to Slowloris Denial of Service.","c",13],
    ["HEARTBLEED Vulnerability Found with SSLyze.","h",14],
    ["HEARTBLEED Vulnerability Found with Nmap.","h",14],
    ["POODLE Vulnerability Detected.","h",15],
    ["OpenSSL CCS Injection Detected.","h",16],
    ["FREAK Vulnerability Detected.","h",17],
    ["LOGJAM Vulnerability Detected.","h",18],
    ["Unsuccessful OCSP Response.","m",19],
    ["Server supports Deflate Compression.","m",20],
    ["Secure Client Initiated Renegotiation is supported.","m",21],
    ["Secure Resumption unsupported with (Sessions IDs/TLS Tickets).","m",22],
    ["No DNS/HTTP based Load Balancers Found.","l",23],
    ["Domain is spoofed/hijacked.","h",24],
    ["HEARTBLEED Vulnerability Found with Golismero.","h",14],
    ["Open Files Found with Golismero BruteForce.","m",25],
    ["Open Directories Found with Golismero BruteForce.","m",26],
    ["DB Banner retrieved with SQLMap.","l",27],
    ["Open Directories Found with DirB.","m",26],
    ["XSSer found XSS vulnerabilities.","c",28],
    ["Found SSL related vulnerabilities with Golismero.","m",29],
    ["Zone Transfer Successful with Golismero. Reconfigure DNS immediately.","h",10],
    ["Golismero Nikto Plugin found vulnerabilities.","m",30],
    ["Found Subdomains with Golismero.","m",31],
    ["Zone Transfer Successful using DNSEnum. Reconfigure DNS immediately.","h",10],
    ["Found Subdomains with Fierce.","m",31],
    ["Email Addresses discovered with DMitry.","l",9],
    ["Subdomains discovered with DMitry.","m",31],
    ["Telnet Service Detected.","h",32],
    ["FTP Service Detected.","c",33],
    ["Vulnerable to STUXNET.","c",34],
    ["WebDAV Enabled.","m",35],
    ["Found some information through Fingerprinting.","l",36],
    ["Open Files Found with Uniscan.","m",25],
    ["Open Directories Found with Uniscan.","m",26],
    ["Vulnerable to Stress Tests.","h",37],
    ["Uniscan detected possible LFI, RFI or RCE.","h",38],
    ["Uniscan detected possible XSS, SQLi, BSQLi.","h",39],
    ["Apache Expect XSS Header not present.","m",12],
    ["Found Subdomains with Nikto.","m",31],
    ["Webserver vulnerable to Shellshock Bug.","c",40],
    ["Webserver leaks Internal IP.","l",41],
    ["HTTP PUT DEL Methods Enabled.","m",42],
    ["Some vulnerable headers exposed.","m",43],
    ["Webserver vulnerable to MS10-070.","h",44],
    ["Some issues found on the Webserver.","m",30],
    ["Webserver is Outdated.","h",45],
    ["Some issues found with HTTP Options.","l",42],
    ["CGI Directories Enumerated.","l",26],
    ["Vulnerabilities reported in SSL Scans.","m",29],
    ["Interesting Files Detected.","m",25],
    ["Injectable Paths Detected.","l",46],
    ["Found Subdomains with DNSMap.","m",31],
    ["MS-SQL DB Service Detected.","l",47],
    ["MySQL DB Service Detected.","l",47],
    ["ORACLE DB Service Detected.","l",47],
    ["RDP Server Detected over UDP.","h",48],
    ["RDP Server Detected over TCP.","h",48],
    ["TCP Ports are Open","l",8],
    ["UDP Ports are Open","l",8],
    ["SNMP Service Detected.","m",49],
    ["Elmah is Configured.","m",50],
    ["SMB Ports are Open over TCP","m",51],
    ["SMB Ports are Open over UDP","m",51],
    ["Wapiti discovered a range of vulnerabilities","h",30],
    ["IIS WebDAV is Enabled","m",35],
    ["X-XSS Protection is not Present","m",12],
    ["Found Subdomains with AMass","m",31]
]

tool_status = [
    ["has IPv6",1,proc_low," < 15s","ipv6",["not found","has IPv6"]],
    ["Server Error",0,proc_low," < 30s","asp.netmisconf",["unable to resolve host address","Connection timed out"]],
    ["wp-login",0,proc_low," < 30s","wpcheck",["unable to resolve host address","Connection timed out"]],
    ["drupal",0,proc_low," < 30s","drupalcheck",["unable to resolve host address","Connection timed out"]],
    ["joomla",0,proc_low," < 30s","joomlacheck",["unable to resolve host address","Connection timed out"]],
    ["[+]",0,proc_low," < 40s","robotscheck",["Use of uninitialized value in unpack at"]],
    ["No WAF",0,proc_low," < 45s","wafcheck",["appears to be down"]],
    ["tcp open",0,proc_med," <  2m","nmapopen",["Failed to resolve"]],
    ["No emails found",1,proc_med," <  3m","harvester",["No hosts found","No emails found"]],
    ["[+] Zone Transfer was successful!!",0,proc_low," < 20s","dnsreconzt",["Could not resolve domain"]],
    ["0 errors",0,proc_low," < 35s","dnswalkzt",["!!!0 failures, 0 warnings, 3 errors."]],
    ["Admin Email:",0,proc_low," < 25s","whois",["No match for domain"]],
    ["XSS filter is disabled",0,proc_low," < 20s","nmapxssh",["Failed to resolve"]],
    ["VULNERABLE",0,proc_high," < 45m","nmapdos",["Failed to resolve"]],
    ["Server is vulnerable to Heartbleed",0,proc_low," < 40s","sslyzehb",["Could not resolve hostname"]],
    ["VULNERABLE",0,proc_low," < 30s","nmap1",["Failed to resolve"]],
    ["VULNERABLE",0,proc_low," < 35s","nmap2",["Failed to resolve"]],
    ["VULNERABLE",0,proc_low," < 35s","nmap3",["Failed to resolve"]],
    ["VULNERABLE",0,proc_low," < 30s","nmap4",["Failed to resolve"]],
    ["VULNERABLE",0,proc_low," < 35s","nmap5",["Failed to resolve"]],
    ["ERROR - OCSP response status is not successful",0,proc_low," < 25s","sslyze1",["Could not resolve hostname"]],
    ["VULNERABLE",0,proc_low," < 30s","sslyze2",["Could not resolve hostname"]],
    ["VULNERABLE",0,proc_low," < 25s","sslyze3",["Could not resolve hostname"]],
    ["VULNERABLE",0,proc_low," < 30s","sslyze4",["Could not resolve hostname"]],
    ["does NOT use Load-balancing",0,proc_med," <  4m","lbd",["NOT FOUND"]],
    ["No vulnerabilities found",1,proc_low," < 45s","golism1",["Cannot resolve domain name","No vulnerabilities found"]],
    ["No vulnerabilities found",1,proc_low," < 40s","golism2",["Cannot resolve domain name","No vulnerabilities found"]],
    ["No vulnerabilities found",1,proc_low," < 45s","golism3",["Cannot resolve domain name","No vulnerabilities found"]],
    ["No vulnerabilities found",1,proc_low," < 40s","golism4",["Cannot resolve domain name","No vulnerabilities found"]],
    ["No vulnerabilities found",1,proc_low," < 45s","golism5",["Cannot resolve domain name","No vulnerabilities found"]],
    ["FOUND: 0",1,proc_high," < 35m","dirb",["COULDNT RESOLVE HOST","FOUND: 0"]],
    ["Could not find any vulnerability!",1,proc_med," <  4m","xsser",["XSSer is not working propertly!","Could not find any vulnerability!"]],
    ["Occurrence ID",0,proc_low," < 45s","golism6",["Cannot resolve domain name"]],
    ["DNS zone transfer successful",0,proc_low," < 30s","golism7",["Cannot resolve domain name"]],
    ["Nikto found 0 vulnerabilities",1,proc_med," <  4m","golism8",["Cannot resolve domain name","Nikto found 0 vulnerabilities"]],
    ["Possible subdomain leak",0,proc_high," < 30m","golism9",["Cannot resolve domain name"]],
    ["AXFR record query failed:",1,proc_low," < 45s","dnsenumzt",["NS record query failed:","AXFR record query failed","no NS record for"]],
    ["Found 0 entries",1,proc_high," < 75m","fierce2",["Found 0 entries","is gimp"]],
    ["Found 0 E-Mail(s)",1,proc_low," < 30s","dmitry1",["Unable to locate Host IP addr","Found 0 E-Mail(s)"]],
    ["Found 0 possible subdomain(s)",1,proc_low," < 35s","dmitry2",["Unable to locate Host IP addr","Found 0 possible subdomain(s)"]],
    ["open",0,proc_low," < 15s","nmaptelnet",["Failed to resolve"]],
    ["open",0,proc_low," < 15s","nmapftp",["Failed to resolve"]],
    ["open",0,proc_low," < 20s","nmapstux",["Failed to resolve"]],
    ["SUCCEED",0,proc_low," < 30s","webdav",["is not DAV enabled or not accessible."]],
    ["No vulnerabilities found",1,proc_low," < 15s","golism10",["Cannot resolve domain name","No vulnerabilities found"]],
    ["[+]",0,proc_med," <  2m","uniscan2",["Use of uninitialized value in unpack at"]],
    ["[+]",0,proc_med," <  5m","uniscan3",["Use of uninitialized value in unpack at"]],
    ["[+]",0,proc_med," <  9m","uniscan4",["Use of uninitialized value in unpack at"]],
    ["[+]",0,proc_med," <  8m","uniscan5",["Use of uninitialized value in unpack at"]],
    ["[+]",0,proc_med," <  9m","uniscan6",["Use of uninitialized value in unpack at"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto1",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto2",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto3",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto4",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto5",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto6",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto7",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto8",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto9",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto10",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto11",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto12",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto13",["ERROR: Cannot resolve hostname","0 item(s) reported","No web server found","0 host(s) tested"]],
    ["0 item(s) reported",1,proc_low," < 35s","nikto14","ERROR: Cannot resolve hostname , 0 item(s) reported"],
    ["#1",0,proc_high," < 30m","dnsmap_brute",["[+] 0 (sub)domains and 0 IP address(es) found"]],
    ["open",0,proc_low," < 15s","nmapmssql",["Failed to resolve"]],
    ["open",0,proc_low," < 15s","nmapmysql",["Failed to resolve"]],
    ["open",0,proc_low," < 15s","nmaporacle",["Failed to resolve"]],
    ["open",0,proc_low," < 15s","nmapudprdp",["Failed to resolve"]],
    ["open",0,proc_low," < 15s","nmaptcprdp",["Failed to resolve"]],
    ["open",0,proc_high," > 50m","nmapfulltcp",["Failed to resolve"]],
    ["open",0,proc_high," > 75m","nmapfulludp",["Failed to resolve"]],
    ["open",0,proc_low," < 30s","nmapsnmp",["Failed to resolve"]],
    ["Microsoft SQL Server Error Log",0,proc_low," < 30s","elmahxd",["unable to resolve host address","Connection timed out"]],
    ["open",0,proc_low," < 20s","nmaptcpsmb",["Failed to resolve"]],
    ["open",0,proc_low," < 20s","nmapudpsmb",["Failed to resolve"]],
    ["Host:",0,proc_med," < 5m","wapiti",["none"]],
    ["WebDAV is ENABLED",0,proc_low," < 40s","nmapwebdaviis",["Failed to resolve"]],
    ["X-XSS-Protection[1",1,proc_med," < 3m","whatweb",["Timed out","Socket error","X-XSS-Protection[1"]],
    ["No names were discovered",1,proc_med," < 15m","amass",["The system was unable to build the pool of resolvers"]]
]

# Enhanced vulnerability data (Impact + Definition + Remediation) – same as before
tools_fix = [
    [1, "Attacker gains no direct foothold, but lack of IPv6 means missing out on built‑in IPSec security. IPv6 provides mandatory encryption and authentication, which increases the difficulty of eavesdropping and man‑in‑the‑middle attacks. Without it, you rely on separate security layers.", "Not a vulnerability, just an informational alert. The host does not have IPv6 support. IPv6 provides more security as IPSec (responsible for CIA - Confidentiality, Integrity and Availablity) is incorporated into this model. So it is good to have IPv6 Support.",
        "It is recommended to implement IPv6. More information on how to implement IPv6 can be found from this resource. https://www.cisco.com/c/en/us/solutions/collateral/enterprise/cisco-on-cisco/IPv6-Implementation_CS.html"],
    [2, "Attacker can read detailed stack trace and internal file paths, revealing the web framework, version, and potentially database credentials or connection strings. This information helps plan targeted exploits.", "Sensitive Information Leakage Detected. The ASP.Net application does not filter out illegal characters in the URL. The attacker injects a special character (%7C~.aspx) to make the application spit sensitive information about the server stack.",
        "It is recommended to filter out special charaters in the URL and set a custom error page on such situations instead of showing default error messages. This resource helps you in setting up a custom error page on a Microsoft .Net Application. https://docs.microsoft.com/en-us/aspnet/web-forms/overview/older-versions-getting-started/deploying-web-site-projects/displaying-a-custom-error-page-cs"],
    [3, "Attacker can exploit known vulnerabilities in the specific WordPress version or its plugins, potentially leading to remote code execution, database theft, or site defacement.", "It is not bad to have a CMS in WordPress. There are chances that the version may contain vulnerabilities or any third party scripts associated with it may possess vulnerabilities",
        "It is recommended to conceal the version of WordPress. This resource contains more information on how to secure your WordPress Blog. https://codex.wordpress.org/Hardening_WordPress"],
    [4, "Same as WordPress – attacker can target known Drupal vulnerabilities, which may allow full site compromise.", "It is not bad to have a CMS in Drupal. There are chances that the version may contain vulnerabilities or any third party scripts associated with it may possess vulnerabilities",
        "It is recommended to conceal the version of Drupal. This resource contains more information on how to secure your Drupal Blog. https://www.drupal.org/docs/7/site-building-best-practices/ensure-that-your-site-is-secure"],
    [5, "Attacker can target Joomla‑specific vulnerabilities, often leading to SQL injection or remote code execution.", "It is not bad to have a CMS in Joomla. There are chances that the version may contain vulnerabilities or any third party scripts associated with it may possess vulnerabilities",
        "It is recommended to conceal the version of Joomla. This resource contains more information on how to secure your Joomla Blog. https://www.incapsula.com/blog/10-tips-to-improve-your-joomla-website-security.html"],
    [6, "Attacker can discover hidden administrative endpoints or sensitive directories that are intentionally disallowed from crawling, gaining a roadmap to attack.", "Sometimes robots.txt or sitemap.xml may contain rules such that certain links that are not supposed to be accessed/indexed by crawlers and search engines. Search engines may skip those links but attackers will be able to access it directly.",
        "It is a good practice not to include sensitive links in the robots or sitemap files."],
    [7, "Attacker can send a wide range of attack vectors (SQLi, XSS, etc.) without being blocked or logged by a WAF, increasing the chance of successful exploitation.", "Without a Web Application Firewall, An attacker may try to inject various attack patterns either manually or using automated scanners. An automated scanner may send hordes of attack vectors and patterns to validate an attack, there are also chances for the application to get DoS`ed (Denial of Service)",
        "Web Application Firewalls offer great protection against common web attacks like XSS, SQLi, etc. They also provide an additional line of defense to your security infrastructure. This resource contains information on web application firewalls that could suit your application. https://www.gartner.com/reviews/market/web-application-firewall"],
    [8, "Attacker can probe open ports to discover running services and versions, then use known exploits for those services to gain initial access or pivot internally.", "Open Ports give attackers a hint to exploit the services. Attackers try to retrieve banner information through the ports and understand what type of service the host is running",
        "It is recommended to close the ports of unused services and use a firewall to filter the ports wherever necessary. This resource may give more insights. https://security.stackexchange.com/a/145781/6137"],
    [9, "Attacker can use harvested email addresses for phishing, social engineering, or password brute‑forcing across other services that use the same username pattern.", "Chances are very less to compromise a target with email addresses. However, attackers use this as a supporting data to gather information around the target. An attacker may make use of the username on the email address and perform brute-force attacks on not just email servers, but also on other legitimate panels like SSH, CMS, etc with a password list as they have a legitimate name.",
        "Since the chances of exploitation is feeble there is no need to take action. Perfect remediation would be choosing different usernames for different services will be more thoughtful."],
    [10, "Attacker obtains a full zone transfer, revealing all internal hostnames, IP addresses, and network topology. This enables precise targeting of internal systems and services.", "Zone Transfer reveals critical topological information about the target. The attacker will be able to query all records and will have more or less complete knowledge about your host.",
        "Good practice is to restrict the Zone Transfer by telling the Master which are the IPs of the slaves that can be given access for the query. This SANS resource  provides more information. https://www.sans.org/reading-room/whitepapers/dns/securing-dns-zone-transfer-868"],
    [11, "Attacker can use administrative contact information for social engineering or targeted spear‑phishing to gain initial access or sensitive data.", "The email address of the administrator and other information (address, phone, etc) is available publicly. An attacker may use these information to leverage an attack.",
        "Some administrators intentionally would have made this information public, in this case it can be ignored. If not, it is recommended to mask the information. This resource provides information on this fix. http://www.name.com/blog/how-tos/tutorial-2/2013/06/protect-your-personal-information-with-whois-privacy/"],
    [12, "Attacker can exploit the lack of X‑XSS‑Protection header to perform reflected XSS attacks on older browsers, stealing session cookies or redirecting users to malware sites.", "As the target is lacking this header, older browsers will be prone to Reflected XSS attacks.",
        "Modern browsers does not face any issues with this vulnerability (missing headers). However, older browsers are strongly recommended to be upgraded."],
    [13, "Attacker can keep multiple connections open with partial requests, eventually exhausting server resources and causing a denial of service (DoS) for legitimate users.", "This attack works by opening multiple simultaneous connections to the web server and it keeps them alive as long as possible by continously sending partial HTTP requests, which never gets completed. They easily slip through IDS by sending partial requests.",
        "If you are using Apache Module, `mod_antiloris` would help. For other setup you can find more detailed remediation on this resource. https://www.acunetix.com/blog/articles/slow-http-dos-attacks-mitigate-apache-http-server/"],
    [14, "Attacker can read up to 64 KB of memory from the server per heartbeat, potentially exposing private keys, user credentials, session tokens, and other sensitive data.", "This vulnerability seriously leaks private information of your host. An attacker can keep the TLS connection alive and can retrieve a maximum of 64K of data per heartbeat.",
        "PFS (Perfect Forward Secrecy) can be implemented to make decryption difficult. Complete remediation and resource information is available here. http://heartbleed.com/"],
    [15, "Attacker can perform a man‑in‑the‑middle attack by downgrading the connection to SSLv3, intercepting and decrypting encrypted session data, thus stealing cookies and impersonating users.", "By exploiting this vulnerability, an attacker will be able gain access to sensitive data in a n encrypted session such as session ids, cookies and with those data obtained, will be able to impersonate that particular user.",
        "This is a flaw in the SSL 3.0 Protocol. A better remediation would be to disable using the SSL 3.0 protocol. For more information, check this resource. https://www.us-cert.gov/ncas/alerts/TA14-290A"],
    [16, "Attacker can exploit the CCS injection to force the server into using a weak cipher or to perform a man‑in‑the‑middle attack, decrypting communications.", "This attacks takes place in the SSL Negotiation (Handshake) which makes the client unaware of the attack. By successfully altering the handshake, the attacker will be able to pry on all the information that is sent from the client to server and vice-versa",
        "Upgrading OpenSSL to latest versions will mitigate this issue. This resource gives more information about the vulnerability and the associated remediation. http://ccsinjection.lepidum.co.jp/"],
    [17, "Attacker can exploit the FREAK vulnerability to downgrade the encryption to weak export‑grade ciphers, allowing them to decrypt intercepted traffic.", "With this vulnerability the attacker will be able to perform a MiTM attack and thus compromising the confidentiality factor.",
        "Upgrading OpenSSL to latest version will mitigate this issue. Versions prior to 1.1.0 is prone to this vulnerability. More information can be found in this resource. https://bobcares.com/blog/how-to-fix-sweet32-birthday-attacks-vulnerability-cve-2016-2183/"],
    [18, "Attacker can downgrade the TLS connection to use weak Diffie‑Hellman parameters, enabling them to read and modify data passing between client and server.", "With the LogJam attack, the attacker will be able to downgrade the TLS connection which allows the attacker to read and modify any data passed over the connection.",
        "Make sure any TLS libraries you use are up-to-date, that servers you maintain use 2048-bit or larger primes, and that clients you maintain reject Diffie-Hellman primes smaller than 1024-bit. More information can be found in this resource. https://weakdh.org/"],
    [19, "Attacker can cause a denial of service or, in some cases, read sensitive memory contents by sending a malformed ClientHello handshake.", "Allows remote attackers to cause a denial of service (crash), and possibly obtain sensitive information in applications that use OpenSSL, via a malformed ClientHello handshake message that triggers an out-of-bounds memory access.",
        "OpenSSL versions 0.9.8h through 0.9.8q and 1.0.0 through 1.0.0c are vulnerable. It is recommended to upgrade the OpenSSL version. More resource and information can be found here. https://www.openssl.org/news/secadv/20110208.txt"],
    [20, "Attacker can use the BREACH attack to extract secrets like CSRF tokens or session IDs from compressed HTTPS responses by injecting known content and measuring the size.", "Otherwise termed as BREACH atack, exploits the compression in the underlying HTTP protocol. An attacker will be able to obtain email addresses, session tokens, etc from the TLS encrypted web traffic.",
        "Turning off TLS compression does not mitigate this vulnerability. First step to mitigation is to disable Zlib compression followed by other measures mentioned in this resource. http://breachattack.com/"],
    [21, "Attacker can perform a man‑in‑the‑middle attack by injecting data into a session during renegotiation, potentially stealing session identifiers or manipulating requests.", "Otherwise termed as Plain-Text Injection attack, which allows MiTM attackers to insert data into HTTPS sessions, and possibly other types of sessions protected by TLS or SSL, by sending an unauthenticated request that is processed retroactively by a server in a post-renegotiation context.",
        "Detailed steps of remediation can be found from these resources. https://securingtomorrow.mcafee.com/technical-how-to/tips-securing-ssl-renegotiation/ https://www.digicert.com/news/2011-06-03-ssl-renego/ "],
    [22, "Attacker can hijack an existing TLS session by resuming it, thereby bypassing authentication and impersonating a legitimate user.", "This vulnerability allows attackers to steal existing TLS sessions from users.",
        "Better advice is to disable session resumption. To harden session resumption, follow this resource that has some considerable information. https://wiki.crashtest-security.com/display/KB/Harden+TLS+Session+Resumption"],
    [23, "Attacker can more easily launch a denial‑of‑service attack because there is no load balancing to distribute traffic across multiple servers.", "This has nothing to do with security risks, however attackers may use this unavailability of load balancers as an advantage to leverage a denial of service attack on certain services or on the whole application itself.",
        "Load-Balancers are highly encouraged for any web application. They improve performance times as well as data availability on during times of server outage. To know more information on load balancers and setup, check this resource. https://www.digitalocean.com/community/tutorials/what-is-load-balancing"],
    [24, "Attacker can redirect users to a malicious site, serving malware or phishing pages, because the domain is spoofed or hijacked.", "An attacker can forwarded requests that comes to the legitimate URL or web application to a third party address or to the attacker's location that can serve malware and affect the end user's machine.",
        "It is highly recommended to deploy DNSSec on the host target. Full deployment of DNSSEC will ensure the end user is connecting to the actual web site or other service corresponding to a particular domain name. For more information, check this resource. https://www.cloudflare.com/dns/dnssec/how-dnssec-works/"],
    [25, "Attacker can read sensitive information (like configuration files, source code, or backup archives) that are inadvertently exposed, leading to data theft or further system compromise.", "Attackers may find considerable amount of information from these files. There are even chances attackers may get access to critical information from these files.",
        "It is recommended to block or restrict access to these files unless necessary."],
    [26, "Attacker can enumerate directory structure and possibly access files that are not meant to be public, such as admin panels or backup directories.", "Attackers may find considerable amount of information from these directories. There are even chances attackers may get access to critical information from these directories.",
        "It is recommended to block or restrict access to these directories unless necessary."],
    [27, "Attacker learns that the host uses a database backend, and the type (MySQL, MSSQL, etc.), which allows them to target specific database exploits.", "May not be SQLi vulnerable. An attacker will be able to know that the host is using a backend for operation.",
        "Banner Grabbing should be restricted and access to the services from outside would should be made minimum."],
    [28, "Attacker can inject malicious scripts into the web application, stealing cookies, session tokens, or redirecting users to malware or phishing sites.", "An attacker will be able to steal cookies, deface web application or redirect to any third party address that can serve malware.",
        "Input validation and Output Sanitization can completely prevent Cross Site Scripting (XSS) attacks. XSS attacks can be mitigated in future by properly following a secure coding methodology. The following comprehensive resource provides detailed information on fixing this vulnerability. https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet"],
    [29, "Attacker can exploit SSL/TLS weaknesses to eavesdrop on communication, steal session data, or perform man‑in‑the‑middle attacks.", "SSL related vulnerabilities breaks the confidentiality factor. An attacker may perform a MiTM attack, intrepret and eavesdrop the communication.",
        "Proper implementation and upgraded version of SSL and TLS libraries are very critical when it comes to blocking SSL related vulnerabilities."],
    [30, "Attacker can combine multiple findings to build a comprehensive attack strategy, potentially leading to full system compromise.", "Particular Scanner found multiple vulnerabilities that an attacker may try to exploit the target.",
        "Refer to RS-Vulnerability-Report to view the complete information of the vulnerability, once the scan gets completed."],
    [31, "Attacker can discover additional attack surfaces (subdomains) that may host applications with weak security, leading to lateral movement or data breaches.", "Attackers may gather more information from subdomains relating to the parent domain. Attackers may even find other services from the subdomains and try to learn the architecture of the target.",
        "It is sometimes wise to block sub domains like development, staging to the outside world, as it gives more information to the attacker about the tech stack. Complex naming practices also help in reducing the attack surface as attackers find hard to perform subdomain bruteforcing through dictionaries and wordlists."],
    [32, "Attacker can perform man‑in‑the‑middle attacks or eavesdrop on Telnet traffic, which is sent in cleartext, revealing credentials and commands.", "Through this deprecated protocol, an attacker may be able to perform MiTM and other complicated attacks.",
        "It is highly recommended to stop using this service and it is far outdated. SSH can be used to replace TELNET. For more information, check this resource https://www.ssh.com/ssh/telnet"],
    [33, "Attacker can capture FTP credentials (sent in cleartext) and potentially use known FTP exploits to gain shell access or upload malicious files.", "This protocol does not support secure communication and there are likely high chances for the attacker to eavesdrop the communication. Also, many FTP programs have exploits available in the web such that an attacker can directly crash the application or either get a SHELL access to that target.",
        "Proper suggested fix is use an SSH protocol instead of FTP. It supports secure communication and chances for MiTM attacks are quite rare."],
    [34, "Attacker (or a worm) can use this known vulnerability to propagate, steal data, or cause operational disruption, as Stuxnet is a sophisticated cyber‑weapon.", "The StuxNet is level-3 worm that exposes critical information of the target organization. It was a cyber weapon that was designed to thwart the nuclear intelligence of Iran.",
        "It is highly recommended to perform a complete rootkit scan on the host. For more information refer to this resource. https://www.symantec.com/security_response/writeup.jsp?docid=2010-071400-3123-99&tabid=3"],
    [35, "Attacker can upload malicious files via WebDAV and trick users into executing them, or exploit known WebDAV vulnerabilities to gain server control.", "WebDAV is supposed to contain multiple vulnerabilities. In some case, an attacker may hide a malicious DLL file in the WebDAV share however, and upon convincing the user to open a perfectly harmless and legitimate file, execute code under the context of that user",
        "It is recommended to disable WebDAV. Some critical resource regarding disbling WebDAV can be found on this URL. https://www.networkworld.com/article/2202909/network-security/-webdav-is-bad---says-security-researcher.html"],
    [36, "Attacker learns server type, software versions, and modification times, enabling them to target known vulnerabilities for that specific server stack.", "Attackers always do a fingerprint of any server before they launch an attack. Fingerprinting gives them information about the server type, content- they are serving, last modification times etc, this gives an attacker to learn more information about the target",
        "A good practice is to obfuscate the information to outside world. Doing so, the attackers will have tough time understanding the server's tech stack and therefore leverage an attack."],
    [37, "Attacker can launch a volumetric DDoS attack to make the service unavailable, causing business loss and reputational damage.", "Attackers mostly try to render web applications or service useless by flooding the target, such that blocking access to legitimate users.",
        "By ensuring proper load balancers in place, configuring rate limits and multiple connection restrictions, such attacks can be drastically mitigated."],
    [38, "Attacker can include remote shell files or execute arbitrary system commands, leading to full server compromise and data exfiltration.", "Intruders will be able to remotely include shell files and will be able to access the core file system or they will be able to read all the files as well. There are even higher chances for the attacker to remote execute code on the file system.",
        "Secure code practices will mostly prevent LFI, RFI and RCE attacks. The following resource gives a detailed insight on secure coding practices. https://wiki.sei.cmu.edu/confluence/display/seccode/Top+10+Secure+Coding+Practices"],
    [39, "Attacker can steal database contents (including user credentials and personal data), impersonate users, or delete entire databases.", "Hackers will be able to steal data from the backend and also they can authenticate themselves to the website and can impersonate as any user since they have total control over the backend. They can even wipe out the entire database. Attackers can also steal cookie information of an authenticated user and they can even redirect the target to any malicious address or totally deface the application.",
        "Proper input validation has to be done prior to directly querying the database information. A developer should remember not to trust an end-user's input. By following a secure coding methodology attacks like SQLi, XSS and BSQLi. The following resource guides on how to implement secure coding methodology on application development. https://wiki.sei.cmu.edu/confluence/display/seccode/Top+10+Secure+Coding+Practices"],
    [40, "Attacker can exploit the Bash vulnerability to execute arbitrary commands on the server, gaining full control over the system.", "Attackers exploit the vulnerability in BASH to perform remote code execution on the target. An experienced attacker can easily take over the target system and access the internal sources of the machine",
        "This vulnerability can be mitigated by patching the version of BASH. The following resource gives an indepth analysis of the vulnerability and how to mitigate it. https://www.symantec.com/connect/blogs/shellshock-all-you-need-know-about-bash-bug-vulnerability https://www.digitalocean.com/community/tutorials/how-to-protect-your-server-against-the-shellshock-bash-vulnerability"],
    [41, "Attacker can identify internal IP addressing schemes, which can be used to plan network‑level attacks or map internal infrastructure.", "Gives attacker an idea on how the address scheming is done internally on the organizational network. Discovering the private addresses used within an organization can help attackers in carrying out network-layer attacks aiming to penetrate the organization's internal infrastructure.",
        "Restrict the banner information to the outside world from the disclosing service. More information on mitigating this vulnerability can be found here. https://portswigger.net/kb/issues/00600300_private-ip-addresses-disclosed"],
    [42, "Attacker can upload or delete files on the server using HTTP PUT/DELETE, potentially allowing them to plant malicious content or deface the website.", "There are chances for an attacker to manipulate files on the webserver.",
        "It is recommended to disable the HTTP PUT and DEL methods incase if you don't use any REST API Services. Following resources helps you how to disable these methods. http://www.techstacks.com/howto/disable-http-methods-in-tomcat.html https://docs.oracle.com/cd/E19857-01/820-5627/gghwc/index.html https://developer.ibm.com/answers/questions/321629/how-to-disable-http-methods-head-put-delete-option/"],
    [43, "Attacker can gather information about the web server, programming language, and framework, making it easier to select and launch appropriate exploits.", "Attackers try to learn more about the target from the amount of information exposed in the headers. An attacker may know what type of tech stack a web application is emphasizing and many other information.",
        "Banner Grabbing should be restricted and access to the services from outside would should be made minimum."],
    [44, "Attacker can decrypt view state data, allowing them to tamper with session data or escalate privileges within the application.", "An attacker who successfully exploited this vulnerability could read data, such as the view state, which was encrypted by the server. This vulnerability can also be used for data tampering, which, if successfully exploited, could be used to decrypt and tamper with the data encrypted by the server.",
        "Microsoft has released a set of patches on their website to mitigate this issue. The information required to fix this vulnerability can be inferred from this resource. https://docs.microsoft.com/en-us/security-updates/securitybulletins/2010/ms10-070"],
    [45, "Attacker can exploit known vulnerabilities in outdated web server software, potentially gaining remote code execution or causing a denial of service.", "Any outdated web server may contain multiple vulnerabilities as their support would've been ended. An attacker may make use of such an opportunity to leverage attacks.",
        "It is highly recommended to upgrade the web server to the available latest version."],
    [46, "Attacker can inject arbitrary commands or scripts into URL parameters, leading to command injection or XSS attacks.", "Hackers will be able to manipulate the URLs easily through a GET/POST request. They will be able to inject multiple attack vectors in the URL with ease and able to monitor the response as well",
        "By ensuring proper sanitization techniques and employing secure coding practices it will be impossible for the attacker to penetrate through. The following resource gives a detailed insight on secure coding practices. https://wiki.sei.cmu.edu/confluence/display/seccode/Top+10+Secure+Coding+Practices"],
    [47, "Attacker can attempt default credentials or known vulnerabilities for that specific database type, possibly gaining access to sensitive data.", "Since the attacker has knowledge about the particular type of backend the target is running, they will be able to launch a targetted exploit for the particular version. They may also try to authenticate with default credentials to get themselves through.",
        "Timely security patches for the backend has to be installed. Default credentials has to be changed. If possible, the banner information can be changed to mislead the attacker. The following resource gives more information on how to secure your backend. http://kb.bodhost.com/secure-database-server/"],
    [48, "Attacker can launch brute‑force attacks or exploit known RDP vulnerabilities to gain access to the system, potentially leading to ransomware deployment.", "Attackers may launch remote exploits to either crash the service or tools like ncrack to try brute-forcing the password on the target.",
        "It is recommended to block the service to outside world and made the service accessible only through the a set of allowed IPs only really neccessary. The following resource provides insights on the risks and as well as the steps to block the service. https://www.perspectiverisk.com/remote-desktop-service-vulnerabilities/"],
    [49, "Attacker can read SNMP community strings, enumerate system information, and potentially exploit remote code execution vulnerabilities in SNMP services.", "Hackers will be able to read community strings through the service and enumerate quite a bit of information from the target. Also, there are multiple Remote Code Execution and Denial of Service vulnerabilities related to SNMP services.",
        "Use a firewall to block the ports from the outside world. The following article gives wide insight on locking down SNMP service. https://www.techrepublic.com/article/lock-it-down-dont-allow-snmp-to-compromise-network-security/"],
    [50, "Attacker can view detailed error logs and application status codes, which can reveal internal paths, database errors, and other sensitive information to plan attacks.", "Attackers will be able to find the logs and error information generated by the application. They will also be able to see the status codes that was generated on the application. By combining all these information, the attacker will be able to leverage an attack.",
        "By restricting access to the logger application from the outside world will be more than enough to mitigate this weakness."],
    [51, "Attacker can exploit SMB vulnerabilities (e.g., EternalBlue) to perform remote code execution, spread ransomware, or gain high‑level access.", "Cyber Criminals mainly target this service as it is very easier for them to perform a remote attack by running exploits. WannaCry Ransomware is one such example.",
        "Exposing SMB Service to the outside world is a bad idea, it is recommended to install latest patches for the service in order not to get compromised. The following resource provides a detailed information on SMB Hardening concepts. https://kb.iweb.com/hc/en-us/articles/115000274491-Securing-Windows-SMB-and-NetBios-NetBT-Services"]
]

# ─── EXTRA AGGRESSIVE SCANS ────────────────────────────────────────────
extra_tool_names = [
    ["nmap_aggressive", "AGGRESSIVE: Nmap Full Scan (all ports, OS, vuln scripts)", "nmap", 1],
    ["nikto_aggressive", "AGGRESSIVE: Nikto All Tests + SSL", "nikto", 1],
    ["wapiti_aggressive", "AGGRESSIVE: Wapiti all modules, aggressive", "wapiti", 1],
    ["amass_aggressive", "AGGRESSIVE: Amass active + brute subdomains", "amass", 1],
    ["dnsenum_aggressive", "AGGRESSIVE: DNSEnum full enum", "dnsenum", 1],
    ["dnsrecon_aggressive", "AGGRESSIVE: Dnsrecon brute force", "dnsrecon", 1],
    ["fierce_aggressive", "AGGRESSIVE: Fierce wide scan", "fierce", 1],
    ["whatweb_aggressive", "AGGRESSIVE: WhatWeb level 4", "whatweb", 1],
    ["golismero_aggressive", "AGGRESSIVE: Golismero all plugins", "golismero", 1],
    ["uniscan_aggressive", "AGGRESSIVE: Uniscan all checks", "uniscan", 1],
    ["theHarvester_aggressive", "AGGRESSIVE: TheHarvester all sources", "theHarvester", 1],
]

extra_tool_cmd = [
    ["nmap -A -T4 -p- --script vuln -Pn -n -sT ", ""],
    ["nikto -h ", " -Tuning x -ssl"],
    ["wapiti -u ", " -m all -S aggressive -f txt -o /tmp/vulnhunter_wapiti_extra"],
    ["amass enum -active -brute -d ", ""],
    ["dnsenum --enum ", ""],
    ["dnsrecon -d ", " -t brt"],
    ["fierce --domain ", " --wide"],
    ["whatweb -a 4 ", ""],
    ["golismero scan ", " --plugins all"],
    ["uniscan -u ", " -qwedj"],
    ["theHarvester -d ", " -b all -l 500"]
]

extra_resp = [
    ["AGGRESSIVE Nmap found multiple open ports/vulnerabilities.","h",30],
    ["AGGRESSIVE Nikto found multiple web vulnerabilities.","h",30],
    ["AGGRESSIVE Wapiti found multiple vulnerabilities.","h",30],
    ["AGGRESSIVE Amass found multiple subdomains.","m",31],
    ["AGGRESSIVE DNSEnum found zone transfer or subdomains.","m",31],
    ["AGGRESSIVE Dnsrecon found subdomains via brute force.","m",31],
    ["AGGRESSIVE Fierce found subdomains.","m",31],
    ["AGGRESSIVE WhatWeb identified web technologies.","i",36],
    ["AGGRESSIVE Golismero found multiple issues.","h",30],
    ["AGGRESSIVE Uniscan found directory/files or vulnerabilities.","h",30],
    ["AGGRESSIVE TheHarvester found many emails.","l",9]
]

extra_status = [
    ["open",0,proc_high," > 20m","nmapaggr",["Failed to resolve"]],
    ["0 item(s) reported",1,proc_med," > 10m","niktoaggr",["ERROR: Cannot resolve hostname","0 item(s) reported"]],
    ["Host:",0,proc_med," > 10m","wapitiaggr",["none"]],
    ["No names were discovered",1,proc_med," > 15m","amassaggr",["The system was unable to build"]],
    ["AXFR record query failed:",1,proc_low," < 2m","dnsenumaggr",["AXFR record query failed"]],
    ["No results",1,proc_low," < 2m","dnsreconaggr",["No results"]],
    ["Found 0 entries",1,proc_high," > 20m","fierceaggr",["Found 0 entries"]],
    ["X-XSS-Protection[1",1,proc_med," < 3m","whatwebaggr",["Timed out"]],
    ["No vulnerabilities found",1,proc_high," > 30m","golisaggr",["No vulnerabilities found"]],
    ["Use of uninitialized value",0,proc_med," < 5m","uniscanaggr",["Use of uninitialized value"]],
    ["No emails found",1,proc_med," < 5m","harvesteraggr",["No emails found"]]
]

# Tool pre‑check list
tools_precheck = [
    ["wapiti"], ["whatweb"], ["nmap"], ["golismero"], ["host"], ["wget"], ["uniscan"],
    ["wafw00f"], ["dirb"], ["davtest"], ["theHarvester"], ["xsser"], ["dnsrecon"],
    ["fierce"], ["dnswalk"], ["whois"], ["sslyze"], ["lbd"], ["golismero"],
    ["dnsenum"], ["dmitry"], ["davtest"], ["nikto"], ["dnsmap"], ["amass"]
]

# ─── Parser ──────────────────────────────────────────────────────────
def get_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    parser.add_argument('-u', '--update', action='store_true', help='Update tool')
    parser.add_argument('-s', '--skip', action='append', default=[], help='Skip tools', choices=[t[0] for t in tools_precheck])
    parser.add_argument('-n', '--nospinner', action='store_true', help='Disable animation')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--extra', action='store_true', help='Add aggressive red‑team scans')
    parser.add_argument('target', nargs='?', metavar='URL', help='Target URL', default='')
    return parser

# ─── Main ────────────────────────────────────────────────────────────
if len(sys.argv) == 1:
    banner()
    helper()
    sys.exit(1)

args_namespace = get_parser().parse_args()
verbose = args_namespace.verbose
nospinner = args_namespace.nospinner
extra = args_namespace.extra

if args_namespace.help or (not args_namespace.update and not args_namespace.target):
    banner()
    helper()
    sys.exit(1)

if args_namespace.update:
    banner()
    print(Colors.CYAN + "█ Updating Vuln Hunter ..." + Colors.ENDC)
    if not check_internet():
        print(Colors.RED + "No internet connection." + Colors.ENDC)
        sys.exit(1)
    old = subprocess.check_output("sha1sum vulnhunter.py | cut -c1-40", shell=True).strip()
    os.system("wget -N https://raw.githubusercontent.com/skavngr/rapidscan/master/rapidscan.py -O vulnhunter.py 2>/dev/null")
    new = subprocess.check_output("sha1sum vulnhunter.py | cut -c1-40", shell=True).strip()
    if old == new:
        print(Colors.GREEN + "Already latest version." + Colors.ENDC)
    else:
        print(Colors.GREEN + "Updated successfully." + Colors.ENDC)
    sys.exit(1)

if args_namespace.target:
    target = url_maker(args_namespace.target)
    os.system('rm /tmp/vulnhunter_* 2>/dev/null')
    banner()

    # If extra, append the aggressive scans
    if extra:
        print(Colors.WARNING + "█ Aggressive (red‑team) mode enabled – adding deep scans." + Colors.ENDC)
        tool_names.extend(extra_tool_names)
        tool_cmd.extend(extra_tool_cmd)
        tool_resp.extend(extra_resp)
        tool_status.extend(extra_status)
        tool_checks = len(tool_names)

    # Check available tools using shutil.which
    print(Colors.CYAN + "█ Scanning environment for available tools ..." + Colors.ENDC)
    unavail = []
    all_tool_binaries = set()
    for t in tool_names:
        all_tool_binaries.add(t[2])
    for bin_name in all_tool_binaries:
        path = shutil.which(bin_name)
        if path:
            print(Colors.GREEN + "  ✔ " + bin_name + " -> " + path + Colors.ENDC)
        else:
            print(Colors.RED + "  ✘ " + bin_name + " (not found in PATH)" + Colors.ENDC)
            for i, scanner in enumerate(tool_names):
                if scanner[2] == bin_name:
                    tool_names[i][3] = 0
                    unavail.append(bin_name)
    if unavail:
        print(Colors.YELLOW + "  Some tools unavailable – those checks will be skipped." + Colors.ENDC)
    print()

    # Start scanning
    fiber = FiberOptic(disabled=nospinner)
    tool = 0
    rs_total_elapsed = 0
    rs_skipped_checks = 0
    rs_vul_list = []

    print(Colors.MAGENTA + "╔════════════════════════════════════════════════════════════════════════╗" + Colors.ENDC)
    print(Colors.MAGENTA + "║" + Colors.CYAN + "  Initiating scan on " + Colors.WHITE + target + Colors.CYAN + "  (press Ctrl+C to skip current test)  " + Colors.MAGENTA + "║" + Colors.ENDC)
    print(Colors.MAGENTA + "╚════════════════════════════════════════════════════════════════════════╝" + Colors.ENDC)

    while tool < len(tool_names):
        print("\n" + Colors.OKBLUE + "[" + tool_status[tool][2] + tool_status[tool][3] + "] " + Colors.BOLD + "Test " + str(tool+1) + "/" + str(tool_checks) + Colors.ENDC + " | " + Colors.CYAN + tool_names[tool][1] + Colors.ENDC)
        if tool_names[tool][3] == 0:
            print(Colors.WARNING + "  → Tool unavailable – skipping." + Colors.ENDC)
            rs_skipped_checks += 1
            tool += 1
            continue

        try:
            fiber.start()
        except:
            pass
        scan_start = time.time()
        temp_file = "/tmp/vulnhunter_" + tool_names[tool][0]
        cmd = tool_cmd[tool][0] + target + tool_cmd[tool][1] + " > " + temp_file + " 2>&1"

        if verbose:
            print(Colors.OKBLUE + "  [CMD] " + cmd + Colors.ENDC)

        # Run the command, catch KeyboardInterrupt to skip
        try:
            ret = subprocess.call(cmd, shell=True)
        except KeyboardInterrupt:
            # User pressed Ctrl+C – skip this test
            fiber.stop()
            print(Colors.WARNING + "\n  ⏹ Skipped by user (Ctrl+C)." + Colors.ENDC)
            rs_skipped_checks += 1
            tool += 1
            continue

        elapsed = time.time() - scan_start
        rs_total_elapsed += elapsed
        fiber.stop()

        # Now check if we have output to process
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print(Colors.WARNING + "  ⚠ No output generated. Skipping vulnerability check." + Colors.ENDC)
            rs_skipped_checks += 1
            tool += 1
            continue

        # Read output
        rs_tool_output_file = open(temp_file).read()
        if verbose:
            print(Colors.WARNING + "  [OUTPUT]" + Colors.ENDC)
            if len(rs_tool_output_file) < 5000:
                print(rs_tool_output_file)
            else:
                print(rs_tool_output_file[:2000] + "\n... (truncated)")

        # Detection logic
        if tool_status[tool][1] == 0:   # positive detection expected
            if tool_status[tool][0].lower() in rs_tool_output_file.lower():
                if verbose:
                    print(Colors.RED + "  🔴 Vulnerability detected! (pattern: " + tool_status[tool][0] + ")" + Colors.ENDC)
                vul_remed_info(tool, tool_resp[tool][1], tool_resp[tool][2])
                rs_vul_list.append(tool_names[tool][0] + "*" + tool_names[tool][1])
            else:
                if verbose:
                    print(Colors.GREEN + "  ✅ No vulnerability found." + Colors.ENDC)
        else:   # negative detection – vulnerability if none of the bad patterns are found
            if any(i in rs_tool_output_file for i in tool_status[tool][5]):
                if verbose:
                    print(Colors.GREEN + "  ✅ No vulnerability found." + Colors.ENDC)
            else:
                if verbose:
                    print(Colors.RED + "  🔴 Vulnerability detected! (patterns: " + str(tool_status[tool][5]) + ")" + Colors.ENDC)
                vul_remed_info(tool, tool_resp[tool][1], tool_resp[tool][2])
                rs_vul_list.append(tool_names[tool][0] + "*" + tool_names[tool][1])

        print(Colors.OKBLUE + "  ⏱ Completed in " + display_time(int(elapsed)) + Colors.ENDC)
        tool += 1

    # Report
    print("\n" + Colors.MAGENTA + "╔════════════════════════════════════════════════════════════════════════╗" + Colors.ENDC)
    print(Colors.MAGENTA + "║" + Colors.CYAN + "  Scan completed. Generating reports ...                             " + Colors.MAGENTA + "║" + Colors.ENDC)
    print(Colors.MAGENTA + "╚════════════════════════════════════════════════════════════════════════╝" + Colors.ENDC)

    date = subprocess.Popen(["date", "+%Y-%m-%d"], stdout=subprocess.PIPE).stdout.read()[:-1].decode("utf-8")
    debuglog = "vh.dbg.%s.%s" % (target, date)
    vulreport = "vh.vul.%s.%s" % (target, date)

    if rs_vul_list:
        with open(vulreport, "w") as rp:
            for vuln in rs_vul_list:
                parts = vuln.split('*')
                rp.write(parts[1] + "\n" + "=" * 40 + "\n")
                with open("/tmp/vulnhunter_" + parts[0], 'r') as tf:
                    rp.write(tf.read() + "\n\n")
        print(Colors.GREEN + "  Vulnerability report : " + vulreport + Colors.ENDC)
    else:
        print(Colors.GREEN + "  No vulnerabilities detected." + Colors.ENDC)

    with open(debuglog, "w") as dbg:
        for t in tool_names:
            try:
                with open("/tmp/vulnhunter_" + t[0], 'r') as tf:
                    dbg.write(t[1] + "\n" + "=" * 40 + "\n" + tf.read() + "\n\n")
            except:
                pass
    print(Colors.CYAN + "  Debug log : " + debuglog + Colors.ENDC)

    print("\n" + Colors.MAGENTA + "═" * 50 + Colors.ENDC)
    print(Colors.BOLD + "  Summary" + Colors.ENDC)
    print("  Total checks            : " + str(len(tool_names)))
    print("  Skipped (unavailable)   : " + str(rs_skipped_checks))
    print("  Vulnerabilities found   : " + str(len(rs_vul_list)))
    print("  Total time              : " + display_time(int(rs_total_elapsed)))
    print(Colors.MAGENTA + "═" * 50 + Colors.ENDC)

    os.system('rm /tmp/vulnhunter_* 2>/dev/null')
    sys.exit(0)
