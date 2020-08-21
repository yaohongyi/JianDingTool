#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import re
import winreg
from PyQt5 import QtCore


file_content = "/** -1：教育版, 0: 基础版, 1: 高级版, 2: 专家版 */\n" \
               "module.exports = {topLevel: 2,debug: 1,devTools: 1};"


class FileOperate(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, model_value, edition_text):
        super().__init__()
        self.model_value = model_value
        self.edition_text = edition_text

    def file_operate(self):
        # 获取鉴定系统安装磁盘
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
        key_num = winreg.QueryInfoKey(key)[0]
        finally_disk = ''
        for a in range(key_num):
            key_name = winreg.EnumKey(key, a)
            if key_name.startswith('{') and key_name.endswith('}'):
                new_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                         f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{key_name}')
                new_key_num = winreg.QueryInfoKey(new_key)[1]
                for b in range(new_key_num):
                    name, key_type, value = winreg.EnumValue(new_key, b)
                    if str(key_type).find('Uninstall 国音智能声纹鉴定专家系统.exe') != -1:
                        finally_disk = key_type[1:2]
                        break
        # 鉴定系统版本切换及模式调整
        edition = {'教学版': -1, '基础版': 0, '高级版': 1, '专家版': 2}
        edition_value = edition.get(self.edition_text)
        model_info = ['关闭', '打开']
        file_path = f'{finally_disk}:\\Program Files\\voice-identify\\locConf.js'
        try:
            with open(file_path, 'w+', encoding='utf-8') as file:
                file.read()
                file.seek(0)
                file.truncate()  # 清空文件
                result = re.sub(r'topLevel: (.*?),debug: (.*?),',
                                f'topLevel: {edition_value},debug: {self.model_value},',
                                file_content)
                file.write(result)
                info = f'开发者模式【{model_info[self.model_value]}】，版本为【{self.edition_text}】，重启鉴定系统后生效！'
                self.text.emit(info)
                return info
        except OSError:
            self.text.emit('切换失败，请手动将当前目录下的locConf.js拷贝到程序安装根目录！')
            with open('./locConf.js', 'w+', encoding='utf-8') as file:
                file.read()
                file.seek(0)
                file.truncate()  # 清空文件
                result = re.sub(r'topLevel: (.*?),debug: (.*?),',
                                f'topLevel: {edition_value},debug: {self.model_value},',
                                file_content)
                file.write(result)

    def run(self):
        self.file_operate()


if __name__ == '__main__':
    file_operate = FileOperate(1, 1)
    print(file_operate.get_identify_disk())
