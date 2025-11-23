import re
import os

# 配置
MY_NAME = "Kuangzhi Ge"
BIB_FILE = "_data/references.bib"
YML_FILE = "_data/publications.yml"
BIB_OUTPUT_DIR = "assets/bibs"  # 存放生成的单独 bib 文件的目录

def parse_bibtex(bib_content):
    """
    简单的 BibTeX 解析器。
    假设格式比较标准，每个字段一行，用 = 分隔。
    """
    entries = []
    current_entry = {}

    # 匹配 @type{key,
    entry_start_pattern = re.compile(r'@(\w+)\{([^,]+),')
    # 匹配 field = {value} 或 field = "value"
    field_pattern = re.compile(r'\s*(\w+)\s*=\s*[\{"](.*)[\}"]\s*,?')

    lines = bib_content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        start_match = entry_start_pattern.match(line)
        if start_match:
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                'type': start_match.group(1),
                'key': start_match.group(2),
                'raw_bib': [line] # 保存原始 bib 行以便生成单独文件
            }
            continue

        if line == '}' and current_entry:
            current_entry['raw_bib'].append(line)
            entries.append(current_entry)
            current_entry = {}
            continue

        if current_entry:
            current_entry['raw_bib'].append(line)
            field_match = field_pattern.match(line)
            if field_match:
                key = field_match.group(1).lower()
                value = field_match.group(2)
                # 去除末尾可能的逗号
                if line.endswith(','):
                    # value 已经在正则里去掉了末尾的 }", 但如果正则没匹配好
                    pass
                current_entry[key] = value

    if current_entry:
        entries.append(current_entry)

    return entries

def format_authors(author_str):
    """
    格式化作者列表。
    1. 用 ' and ' 分割。
    2. 加粗 MY_NAME。
    3. 用 ', ' 连接。
    """
    if not author_str:
        return ""

    authors = author_str.split(' and ')
    formatted_authors = []

    for author in authors:
        author = author.strip()
        if MY_NAME in author:
            # 保持原有的标记（如 *），只加粗名字部分
            # 简单的替换可能不够，如果名字是 "Kuangzhi Ge*"
            if author.startswith(MY_NAME):
                author = author.replace(MY_NAME, f"<strong>{MY_NAME}</strong>")
            else:
                # 尝试查找名字位置
                author = author.replace(MY_NAME, f"<strong>{MY_NAME}</strong>")
        formatted_authors.append(author)

    return ", ".join(formatted_authors)

def generate_single_bib(entry, output_dir):
    """
    生成单独的 bib 文件。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{entry['key']}.bib"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(entry['raw_bib']))

    return f"/{output_dir}/{filename}"

def main():
    if not os.path.exists(BIB_FILE):
        print(f"Error: {BIB_FILE} not found.")
        return

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_bibtex(content)
    yml_data = []

    for entry in entries:
        yml_entry = {}

        # 必需字段
        yml_entry['title'] = entry.get('title', 'No Title')
        yml_entry['authors'] = format_authors(entry.get('author', ''))

        # 可选字段
        if 'url' in entry: yml_entry['url'] = entry['url']
        if 'code' in entry: yml_entry['code'] = entry['code']
        if 'page' in entry: yml_entry['page'] = entry['page']
        if 'image' in entry: yml_entry['image'] = entry['image']
        if 'notes' in entry: yml_entry['notes'] = entry['notes']
        if 'tags' in entry: yml_entry['tags'] = entry['tags']

        # 会议/期刊
        if 'booktitle' in entry:
            yml_entry['conference'] = entry['booktitle']
        elif 'journal' in entry:
            yml_entry['conference'] = entry['journal']

        # 生成单独的 bib 文件链接
        bib_link = generate_single_bib(entry, BIB_OUTPUT_DIR)
        yml_entry['bibtex'] = bib_link

        yml_data.append(yml_entry)

    # 写入 YAML
    # 手动生成 YAML 以避免依赖 pyyaml
    with open(YML_FILE, 'w', encoding='utf-8') as f:
        f.write("main:\n")
        for entry in yml_data:
            f.write(f"  - title: \"{entry['title']}\"\n")
            f.write(f"    authors: \"{entry['authors']}\"\n")

            # 可选字段
            for key in ['url', 'code', 'page', 'image', 'notes', 'tags', 'conference', 'bibtex']:
                if key in entry:
                    val = entry[key]
                    # 简单转义双引号
                    val = val.replace('"', '\\"')
                    f.write(f"    {key}: \"{val}\"\n")
            f.write("\n")

    print(f"Successfully generated {YML_FILE} from {BIB_FILE}")
    print(f"Generated {len(entries)} entries.")

if __name__ == "__main__":
    main()
