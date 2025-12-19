import sys
import re
import ipaddress

def clean_domain(text):
    # 移除 Adblock 前缀和后缀
    text = re.sub(r'^\|\|', '', text)
    text = re.sub(r'^\|', '', text)
    text = re.sub(r'\^.*$', '', text)
    # 移除 URL 协议和路径
    text = re.sub(r'^https?://', '', text)
    text = re.sub(r'/.*$', '', text)
    # 移除端口
    text = re.sub(r':\d+$', '', text)
    return text.strip().lower()

def is_valid_domain(domain):
    if not domain or len(domain) > 253:
        return False
    if domain == "localhost":
        return False
    # 排除 IP 地址
    try:
        ipaddress.ip_address(domain)
        return False
    except:
        pass
    # 基本域名正则
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain) is not None

def process(input_file, output_file):
    domains = set()
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line: continue
                
                parts = line.split()
                # 处理 Hosts 格式 (0.0.0.0 example.com)
                if len(parts) >= 2 and re.match(r'^\d', parts[0]):
                    raw_domain = parts[1]
                else:
                    raw_domain = parts[0]
                
                domain = clean_domain(raw_domain)
                domain = re.sub(r'^www\.', '', domain)
                
                if is_valid_domain(domain):
                    domains.add(domain)
                    
        with open(output_file, 'w', encoding='utf-8') as f:
            for d in sorted(domains):
                f.write(f"{d}\n")
        print(f"Success: {len(domains)} domains saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inf = sys.argv[1] if len(sys.argv) > 1 else "reward.txt"
    outf = sys.argv[2] if len(sys.argv) > 2 else "domains.txt"
    process(inf, outf)
