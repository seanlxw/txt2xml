# txt2xml
文本处理，将有固定格式的文本txt文件转换为自定义固定格式的xml文件。

task：txt转xml,text to xml

【文本格式】  
文件名：年份.txt  
行1 ：省份  
每行：每个区县单独成行；【区县名】【空2格】 {【总括描述XX流行】【。】（【报道/载：】【内容】【[参考文献信息]】）重复}重复  
*重复部分格式不定，有的地方缺省总述and/or报道and/or参考文献信息。  
*部分文本格式不规范，【区县名】后统一【空2格】进行了处理。为了实现功能，其他不规范部分亦做了修改。  

【xml格式example】  
<year_record year="1912"\>  
<province_record year="1912" province="江苏省"\>  

<county_record year="1912" province="江苏省" county="吴县（今属苏州市）"\>  
<s id="1"\> 夏六月，疟疾流行。</s\>  

<s id="2"\>  
<report\>7月26日（六月十三日）报道：</report\>  
苏州城厢内外，疟疾颇多，染者无数。  
<reference\>[ “苏事杂闻”，《申报》1912年7月26日，第3版。]</reference\>  
</s\>  

<s id="3"\>秋七八月，霍乱流行。</s\>  

<s id="4"\>  
<report\>9月7日（七月廿六日）报道：</report\>  
夏秋以来，疫气渐行。  
<reference\>[ “设局防疫”，《申报》1912年9月7日，第6版。]</reference\>  
</s\>  
</county_record\>  

</province_record\>  
</year_record\>  

【变量定义】  
year  
province  
county  
sentence  
id_num  
report  
reference  
pointer  
a（临时指针1）  
b（临时指针2）  

【代码逻辑】注：以下{var}表示变量  
1.打开源文件，读取文件名，删除.txt后存入{year}变量。  
2.打开输出文件，输出fo.write(f'<year_record year=\"{year}\">\n ')  
3.读取第一行，存入{province}变量，输出fo.write(f'<province_record year=\"{year}\" province=\"{province}\">\n')  
4.循环读取每行至源文件结束，对每行（第一层循环）：  
4.1 读取空格前内容，存入{county}变量，输出fo.write(f'<county_record year=\"{year}\" province=\"{province}\" county=\"{county}\">\n')，pointer++， id_num = 1  
4.2读取段落字符直至结束（第二层循环）：  
4.2.1寻找最近的"。"(index=a)或"："(index=b)  
4.2.1.1若是"。"，判断其后有无"["  
4.2.1.1.1若无"["则为总述，直接输出fo.write(f'<s id=\"{id_num}\">{line[pointer+1:a+1]}</s>\n'),id_num++,pointer=a+1  
4.2.1.1.2若有"["则为具体内容，输出fo.write(f'<s id=\"{id_num}\">{line[pointer:a+1]}')，pointer = a+1，寻找"]"的下标更新为a，输出fo.write(f'<reference>{line[pointer:a+1]}</reference></s>\n')，id_num++,pointer = a+1，  
4.2.1.2若是"："  
4.2.1.2.1输出fo.write(f'<s id=\"{id_num}\"><report>{line[pointer+1:b+1]}</report>'),pointer=b+1  
4.2.1.2.2寻找"["的下标更新为b，输出fo.write(line[pointer:b]),pointer=b  
4.2.1.2.3寻找"]"的下标更新为b，输出fo.write(f'<reference>{line[pointer:b+1]}</reference></s>\n'),pointer=b+1，id_num++  
4.3输出fo.write('</county_record>\n')  
5.输出fo.write('</province_record>\n</year_record>')  
