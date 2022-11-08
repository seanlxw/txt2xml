# filename:txt2xml.py
# author:李昕尉
# created:2022.11.9
# function:批量将文件夹中的江苏省史料txt格式文本构建为规范xml格式。
#          输入.txt文件路径：./江苏省史料（TXT格式）/
#          输出.xml文件定向到./江苏省史料（XML格式）/

import os
os.mkdir(r'./江苏省史料（XML格式）/')

for root, dirs, files in os.walk(r'./江苏省史料（TXT格式）/'):
    # 遍历文件
    for f in files:
        year = f[:f.index('.')]
        file_path = os.path.join(root, f)
        fi = open(file_path, 'r', encoding='utf-8')
        fo = open(f"./江苏省史料（XML格式）/{year}.xml", "w", encoding='utf-8')
        fo.write(f'<year_record year=\"{year}\">\n')
        province = fi.readline().strip()
        fo.write(f'<province_record year=\"{year}\" province=\"{province}\">\n')
        for line in fi:
            line = line.strip()
            if len(line) == 0:
                continue
            pointer = line.index(' ')+1
            county = line[0:pointer-1]
            fo.write(f'<county_record year=\"{year}\" province=\"{province}\" county=\"{county}\">\n')
            pointer += 1
            id_num = 1
            while pointer < len(line):
                a = line.find('。', pointer)
                b = line.find('：', pointer)
                # 若后续不存在"："则返回-1，需特殊处理！
                if b == -1 and a > 0:
                    #句号出现在最后
                    if a == len(line)-1:
                        fo.write(f'<s id=\"{id_num}\">{line[pointer:a + 1]}')
                        id_num += 1
                        pointer = a+1
                    elif line[a + 1] != '[':
                        fo.write(f'<s id=\"{id_num}\">{line[pointer:a + 1]}</s>\n')
                        id_num += 1
                        pointer = a + 1
                    else:
                        fo.write(f'<s id=\"{id_num}\">{line[pointer:a + 1]}')
                        pointer = a + 1
                        a = line.find(']', pointer)
                        fo.write(f'<reference>{line[pointer:a + 1]}</reference></s>\n')
                        id_num += 1
                        pointer = a + 1
                    continue
                if a < b:
                    if line[a + 1] != '[':
                        fo.write(f'<s id=\"{id_num}\">{line[pointer:a + 1]}</s>\n')
                        id_num += 1
                        pointer = a + 1
                    else:
                        fo.write(f'<s id=\"{id_num}\">{line[pointer:a + 1]}')
                        pointer = a + 1
                        a = line.find(']', pointer)
                        fo.write(f'<reference>{line[pointer:a + 1]}</reference></s>\n')
                        id_num += 1
                        pointer = a + 1
                else:
                    fo.write(f'<s id=\"{id_num}\"><report>{line[pointer:b + 1]}</report>')
                    pointer = b + 1
                    b = line.find('[', pointer)
                    #缺省参考文献
                    if b == -1:
                        b = line.find('。', pointer)
                        fo.write(line[pointer:b+1])
                        pointer = b + 1
                        id_num += 1
                        continue
                    fo.write(line[pointer:b])
                    pointer = b
                    b = line.find(']', pointer)
                    fo.write(f'<reference>{line[pointer:b + 1]}</reference></s>\n')
                    pointer = b + 1
                    id_num += 1
            fo.write('</county_record>\n')
        fo.write('</province_record>\n</year_record>')
        fi.close()
        fo.close()