import sys
import os

def generate_adblock_list(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    domains = set()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # [span_1](start_span)跳过注释、空行或以 [ 开头的行[span_1](end_span)
            if not line or line.startswith('#') or line.startswith('['):
                continue
            
            # [span_2](start_span)提取域名：通常在第二列[span_2](end_span)
            parts = line.split()
            domain = parts[1] if len(parts) >= 2 else parts[0]
            
            # [span_3](start_span)清洗域名并存入集合去重[span_3](end_span)
            clean_domain = domain.strip().lower()
            if clean_domain:
                domains.add(clean_domain)

    # [span_4](start_span)写入文件，转换为 ||domain.com^ 格式[span_4](end_span)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("! Title: Adblock List\n")
        f.write(f"! Last Updated: {os.popen('date').read()}")
        f.write("!\n")
        for domain in sorted(list(domains)):
            f.write(f"||{domain}^\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract.py <input_file> <output_file>")
    else:
        generate_adblock_list(sys.argv[1], sys.argv[2])
