# -*- coding: utf-8 -*-

import os
import os.path
import re


class Posts(dict):
    def __init__(self, root_path):
        self.drafts = True
        self.root_path = root_path
        dict.__init__(self, {})
        self.load_posts()

    @staticmethod
    def read_post_info(path, file_name):
        file_info = {}
        file_path = os.path.join(path, file_name)
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8')
            # 子表达式增加? 使用非贪婪匹配
            head_pattern = re.compile('---([\w\W]*?)---')
            rv = re.search(head_pattern, content)
            head = rv.group(1)

            # 匹配基本信息
            title = re.findall('title:(.*?)\r\n', head)
            author = re.findall('author:(.*?)\r\n', head)
            categories = re.findall('categories:(.*?)\r\n', head)
            tag = re.findall('tag:(.*?)\r\n', head)
            date = re.findall('date:(.*?)\r\n', head)

            file_info['title'] = title[0].strip()
            file_info['author'] = author[0].strip()
            file_info['categories'] = categories[0].strip()
            file_info['tag'] = tag[0].strip()
            file_info['date'] = date[0].strip()
            file_info['path'] = file_path
            file_info['name'] = file_name

        return file_info

    def load_posts(self):
        # posts
        posts_path = os.path.join(self.root_path, 'posts')
        # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for parent, dir_names, file_names in os.walk(posts_path):
            # 输出文件夹信息
            # for dirname in dirnames:
               # print("parent is:" + parent)
               # print("dirname is" + dirname)

            # 保存文章信息
            for file_name in file_names:
                file_name = file_name.decode('gbk')
                path = parent.decode('gbk')
                file_info = self.read_post_info(path, file_name)
                self[file_name] = file_info

        if self.drafts:
            drafts_path = os.path.join(self.root_path, 'drafts')
            for parent, dir_names, file_names in os.walk(drafts_path):
                # 保存文章信息
                for file_name in file_names:
                    file_name = file_name.decode('gbk')
                    path = parent.decode('gbk')
                    file_info = self.read_post_info(path, file_name)
                    self[file_name] = file_info
