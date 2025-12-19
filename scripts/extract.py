import sys
import re
import os

def extract_to_adblock(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    domains = set()
    # [span_2](start_span)使用正则表达式匹配 {"url":"..."} 里的内容[span_2](end_span)
    url_pattern = re.compile(r'"url"\s*:\s*"([^"]+)"')

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = url_pattern.findall(content)
            
            for item in matches:
                # [span_3](start_span)提取域名部分：去掉协议(http/https)和路径[span_3](end_span)
                domain = item.split('://')[-1].split('/')[0]
                clean_domain = domain.strip().lower()
                if clean_domain:
                    domains.add(clean_domain)
    except Exception as e:
        print(f"Read error: {e}")
        return

    # [span_4](start_span)写入 Adblock 格式 (||domain.com^)[span_4](end_span)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("! Title: Adblock Custom List\n")
        f.write(f"! Total: {len(domains)}\n\n")
        for d in sorted(list(domains)):
            f.write(f"||{d}^\n")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        extract_to_adblock(sys.argv[1], sys.argv[2])
