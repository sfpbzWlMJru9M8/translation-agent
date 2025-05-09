import nltk
import os

# 设置下载路径为当前目录下的 "nltk_data" 文件夹
download_dir = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(download_dir)

# 下载 punkt 模型
nltk.download('punkt', download_dir=download_dir)