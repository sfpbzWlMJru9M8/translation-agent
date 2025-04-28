import os


def print_directory_tree(start_path, indent=""):
    """
    打印指定目录的树形结构
    """
    if not os.path.exists(start_path):
        print(f"路径不存在: {start_path}")
        return

    items = sorted(os.listdir(start_path))
    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        print(indent + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            print_directory_tree(path, indent + extension)


if __name__ == "__main__":
    # 设定你的项目根路径
    project_path = r"E:\竞赛\translation-agent"

    # 打印项目绝对路径
    abs_path = os.path.abspath(project_path)
    print(f"项目目录结构: {abs_path}\n")

    # 调用函数打印目录树
    print_directory_tree(abs_path)
