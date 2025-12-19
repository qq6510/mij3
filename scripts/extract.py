import sys, re, os

def extract(input_p, output_p):
    if not os.path.exists(input_p): return
    with open(input_p, 'r', encoding='utf-8') as f:
        # 正则匹配 JSON 中的 url 字段内容
        urls = re.findall(r'"url"\s*:\s*"([^"]+)"', f.read())
    
    domains = set()
    for u in urls:
        # 提取域名：去掉协议和路径
        d = u.split('://')[-1].split('/')[0].strip().lower()
        if d: domains.add(d)
        
    with open(output_p, 'w', encoding='utf-8') as f:
        f.write("! Title: Adblock List\n")
        for d in sorted(list(domains)):
            f.write(f"||{d}^\n")

if __name__ == "__main__":
    if len(sys.argv) >= 3: extract(sys.argv[1], sys.argv[2])
