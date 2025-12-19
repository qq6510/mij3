import sys
import re
import os

def extract_to_adblock(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"错误: 找不到输入文件 {input_file}")
        return

    domains = set()
    # 正则表达式：匹配 "url":"..." 括号里的网址
    url_pattern = re.compile(r'"url"\s*:\s*"([^"]+)"')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = url_pattern.findall(content)
        
        for item in matches:
            # 提取域名：去掉 http(s):// 和路径
            domain = item.split('://')[-1].split('/')[0]
            clean_domain = domain.strip().lower()
            if clean_domain:
                domains.add(clean_domain)

    # 写入 Adblock 格式 (||domain.com^)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("! Title: My Custom Adblock List\n")
        f.write(f"! Total Count: {len(domains)}\n\n")
        for d in sorted(list(domains)):
            f.write(f"||{d}^\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 extract.py <输入文件> <输出文件>")
    else:
        extract_to_adblock(sys.argv[1], sys.argv[2])
