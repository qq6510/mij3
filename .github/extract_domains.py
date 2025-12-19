#!/usr/bin/env python3
"""
提取域名脚本（Python 版本）
Usage: python3 extract_domains.py [INPUT_FILE] [OUTFILE]
默认 INPUT_FILE: reward.txt
"""
import sys, re, ipaddress

INPUT = sys.argv[1] if len(sys.argv) > 1 else "reward.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "domains_py.txt"

try:
    with open(INPUT, "r", encoding="utf-8", errors="ignore") as fh:
        data = fh.read()
except FileNotFoundError:
    print(f"输入文件 {INPUT} 不存在，退出")
    sys.exit(0)

domains = set()
domain_re = re.compile(r'^[a-z0-9.-]+$')

for raw in data.splitlines():
    line = raw.split('#', 1)[0].strip()
    if not line:
        continue
    parts = re.split(r'\s+', line)
    token = parts[0]
    if len(parts) >= 2 and re.match(r'^\d+\.\d+\.\d+\.\d+$', parts[0]):
        token = parts[1]
    token = re.sub(r'^\|\|', '', token)
    token = re.sub(r'^\|', '', token)
    token = re.sub(r'^https?://', '', token)
    token = re.sub(r':\d+($|/).*', '', token)
    token = re.sub(r'/.*$', '', token)
    token = re.sub(r'\^.*$', '', token)
    token = token.lstrip('.').strip()
    if not token:
        continue
    try:
        ipaddress.ip_address(token)
        continue
    except Exception:
        pass
    if token.lower() == "localhost":
        continue
    token = re.sub(r'^www\.', '', token, flags=re.IGNORECASE)
    token = token.lower()
    if domain_re.match(token) and not token.startswith('-') and not token.endswith('-') and '..' not in token:
        domains.add(token)

with open(OUT, 'w') as f:
    for d in sorted(domains):
        f.write(d + '\n')

print(f"Wrote {len(domains)} unique domains to {OUT}")
