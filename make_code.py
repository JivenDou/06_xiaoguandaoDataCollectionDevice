"""
@File  : make_code.py.py
@Author: lee
@Date  : 2022/4/7/0007 16:51:10
@Desc  :
"""
import wmi
from AES_crypt import encrypt

cpu_code = None
code_file_name = "activate_code.txt"
for cpu in wmi.WMI().Win32_Processor():
    cpu_code = cpu.ProcessorId.strip()
if cpu_code is not None:
    activate_code = encrypt(cpu_code)
    fo = open(code_file_name, "w")
    fo.write(f"activate code: {activate_code}")
    # 关闭打开的文件
    fo.close()
    print("CPU序列号为：", activate_code, ", 已存储到文件：", code_file_name)
    temps = input("按任意键关闭窗口。\n")
else:
    print('获取CPU序列号失败！')
