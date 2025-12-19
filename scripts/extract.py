import sys
import re
import os

def extract_urls_to_adblock(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    domains = set()
    # 匹配 "url":"域名" 格式的正则表达式
    url_pattern = re.compile(r'"url":"([^"]+)"')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 查找所有匹配的网址
        matches = url_pattern.findall(content)
        for url in matches:
            # 去掉协议头（如 http://）并只保留域名部分
            domain = url.split('/')[-1] if '://' not in url else url.split('://')[-1].split('/')[0]
            clean_domain = domain.strip().lower()
            if clean_domain:
                domains.add(clean_domain)

    # 写入 Adblock 格式
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("! Title: Extracted Adblock List\n")
        f.write("!\n")
        for domain in sorted(list(domains)):
            f.write(f"||{domain}^\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract.py <input_file> <output_file>")
    else:
        extract_urls_to_adblock(sys.argv[1], sys.argv[2])
