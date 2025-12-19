#!/usr/bin/env bash
# 提取域名脚本（通用，支持 hosts / adblock / plain domain / URL 格式）
# Usage: ./extract_domains.sh [INPUT_FILE] [OUTFILE]
set -euo pipefail

INPUT="${1:-reward.txt}"
OUT="${2:-domains.txt}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

if [ ! -f "$INPUT" ]; then
  echo "输入文件 $INPUT 不存在，退出"
  exit 0
fi

cp "$INPUT" "$TMP"

awk '
function trim(s) { sub(/^[ \t\r\n]+/, "", s); sub(/[ \t\r\n]+$/, "", s); return s }
{
  line = $0
  sub(/#.*/,"",line)
  line = trim(line)
  if (line == "") next
  n = split(line, F, /[ \t]+/)
  token = F[1]
  if (token ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ || token == "127.0.0.1" || token == "::1") {
    if (n >= 2) token = F[2]; else next
  }
  gsub(/^\|\|/,"",token)
  gsub(/^\|/,"",token)
  gsub(/^https?:\/\//,"",token)
  sub(/:([0-9]+)($|\/)/, "", token)
  sub(/\/.*$/,"",token)
  sub(/\^.*$/,"",token)
  gsub(/^[ \t]+|[ \t]+$/,"",token)
  sub(/^[.]+/,"",token)
  gsub(/^[^A-Za-z0-9]+/, "", token)
  gsub(/[^A-Za-z0-9.-]+$/, "", token)
  if (token == "") next
  if (token ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) next
  if (tolower(token) == "localhost") next
  sub(/^www\./, "", token)
  print tolower(token)
}
' "$TMP" | sort -u > "$OUT"

echo "Wrote $(wc -l < "$OUT") unique domains to $OUT"
