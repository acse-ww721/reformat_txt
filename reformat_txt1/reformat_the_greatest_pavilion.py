# Author: wenqi
# Time: 2024/03/01

import re
import chardet


def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']


def read_txt_from_file(file_path):
    """read txt file from file_path"""
    encoding = detect_file_encoding(file_path)
    # with open(file_path,'r',encoding=encoding) as file:
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()


# def clean_and_merge_lines(lines):
#     """clean special character and merge lines which should not have a line break """
#     cleaned_lines=[]
#     for line in lines:
#         # clear redundant blanks and replace them with standard blanks
#         cleaned_line = ' '.join(line.strip().split())
#         # check whether the line meets the merge requirements
#         if cleaned_lines and not cleaned_line.endswith(('。', '？', '！', ',', '.', '?', '!',)):
#                 cleaned_lines[-1] += " " + cleaned_line
#         else:
#             cleaned_lines.append(cleaned_line)
#     return cleaned_lines

def clean_and_merge_lines(lines):
    """clean special character and merge lines which should not have a line break """
    cleaned_lines = []
    # chapter_pattern = re.compile(r'^\s*第[\u4e00-\u9fa5]+章[\u4e00-\u9fa5]*\(\d+\)')
    chapter_pattern = re.compile(r'^\s*第[\u4e00-\u9fa5]+章[\u4e00-\u9fa5]*[（(](\d+)[）)]')
    # chapter_pattern = re.compile(r'^\s*第[\u4e00-\u9fa5]+章[\u4e00-\u9fa5]*')
    for line in lines:
        # clear redundant blanks and replace them with standard blanks
        line = line.strip()

        if not line:
            continue
        # detect chapter
        if chapter_pattern.match(line):
            # print('yes!')
            cleaned_lines.append('\n' + line + '\n\n' + '    ')
            continue
        # for non-chapter
        # check whether the line meets the merge requirements
        if cleaned_lines and not cleaned_lines[-1].endswith(('。', '？', '！', ',', '.', '?', '!',)):
            cleaned_lines[-1] += line  # key point to merge irregular lines
        else:
            line = '    ' + line
            cleaned_lines.append(line)
    return cleaned_lines


def reformat_paragraph(paragraph):
    """reformat every single paragraph including clearing redundant blanks and indentation """
    cleaned_paragraph = ' ' + ' '.join(paragraph.split())
    return cleaned_paragraph


def reformat_text(text):
    lines = text.split('\n')
    processed_lines = clean_and_merge_lines(lines)
    # formatted_text = '\n'.join(processed_lines)
    formatted_text = '\n\n'.join(processed_lines)
    return formatted_text


def main():
    file_path = '/Users/ww721/JupyterNotebookPath/reformat_txt1/pavilion.txt'
    # read text
    original_text = read_txt_from_file(file_path)
    # reformat text
    formatted_text = reformat_text(original_text)

    # save file to the original path
    file_name = file_path.rstrip('.txt') + "_formatted" + ".txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(formatted_text)
    print(f"Formatted text saved to {file_name}")


if __name__ == '__main__':
    main()

"""Below is the test of the key function."""

original_text = """

第一章一（1）

    肉市口是北京前门外一条最热闹的胡同，路两边都是饭庄子。饭口的时候，各家饭庄忙着    
    煎、炒、烹、炸。这一年，是公元一九一七年，张勋的辫子兵，辅佐小皇上溥仪重登大宝，    
    清朝又复辟了。遗老遗少们翻腾出箱底的朝服，续起真真假假的辫子，满大街跑的都是祖宗    
    。按照我们中华民族的传统，表示心情愉快的唯一方式，就是“吃”。肉市里回光返照似的    
    闹腾起来，又行起请安礼的人们，相让着步入其中的饭庄。整条街上人声鼎沸，车水马龙。    
    正阳楼的涮羊肉，东兴楼的黄焖翅，丰泽园的红烧海参，福聚德的烧鸭子……各种色、香、    
    味俱全的菜肴出锅，菜香飘满街市。    
    各家饭庄子跑堂的招呼客人，伙计们站在门前，吆喝着自家的拿手菜肴及掌灶厨师的绰号大    
    名，食客们不时从各种车中轿中走出。    
    在肉市口，有两家经营烧鸭子的大饭馆（当时烤鸭叫烧鸭子，烤鸭是现代的叫法），除了著    
    名的老字号福聚德之外，另一家就是对门的适意居。那会儿，卢孟实还在适意居当账房    
    ，与福聚德只是隔街相望。  
"""

corrected_text = clean_and_merge_lines(original_text)
formatted_text = '\n'.join(corrected_text)
print(formatted_text)

text = original_text
# chapter_pattern = re.compile(r'^\s*第[\u4e00-\u9fa5]+章[\u4e00-\u9fa5]*')
chapter_pattern = re.compile(r'^\s*第[\u4e00-\u9fa5]+章[\u4e00-\u9fa5]*[（(](\d+)[）)]')
match = chapter_pattern.match(text)
if match:
    print("匹配成功")
else:
    print("匹配失败")

"""
小记
主要解决的问题:
1. 章节名前后单独列行 -- 正则匹配 + 章节名规则
2. 错误划分段落重新合并
3. 每段落后添加换行
4. 编码统一至"utf-8"
"""
