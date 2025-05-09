import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来显示负号


def plot_combined_scores(excel_file, chart_output="combined_bar_chart.png"):
    """
    从 Excel 文件中读取两个 sheet (中文BLEU评分 和 英文BLEU评分)，
    提取每个 sheet 中每个平台的 combined 得分（即最后一行的对应列值），
    然后画出一个分组条形统计图。

    横坐标为：ours, 网易, 百度, Google, deepl, 腾讯翻译君
    每个平台对应两个条形，一个表示中文翻译的 combined 得分，另一个表示英文翻译的 combined 得分，
    纵坐标范围固定在 0-1。

    在每个条形顶部标注该条形的具体得分值，不绘制虚线。
    """
    # 读取 Excel 文件中两个 sheet
    df_chinese = pd.read_excel(excel_file, sheet_name="中文BLEU评分")
    df_english = pd.read_excel(excel_file, sheet_name="英文BLEU评分")

    # 获取每个 sheet 的最后一行，由于最后一行为平均行
    avg_chinese = df_chinese.tail(1)
    avg_english = df_english.tail(1)

    # 定义平台名称及对应的 combined 列名
    platforms = ['ours', '网易', '百度', 'Google', 'deepl', '腾讯翻译君']
    combined_columns = {
        'ours': 'ours_combined',
        '网易': '网易_combined',
        '百度': '百度_combined',
        'Google': 'Google_combined',
        'deepl': 'deepl_combined',
        '腾讯翻译君': '腾讯翻译君_combined'
    }

    # 从平均行中提取每个平台的得分，并转换为 float 型
    chinese_scores = []
    english_scores = []
    for plat in platforms:
        col = combined_columns[plat]
        try:
            ch_score = float(avg_chinese[col].iloc[0])
            en_score = float(avg_english[col].iloc[0])
        except Exception as e:
            raise Exception(f"读取列 {col} 时出错: {e}")
        chinese_scores.append(ch_score)
        english_scores.append(en_score)

    # 设置条形图属性
    x = np.arange(len(platforms))  # 各平台的索引位置
    width = 0.35  # 每个条形的宽度

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width / 2, chinese_scores, width, label='中文翻译', color='skyblue')
    rects2 = ax.bar(x + width / 2, english_scores, width, label='英文翻译', color='lightgreen')

    ax.set_ylabel('Average BLEU Score')
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(platforms)
    ax.set_title('各平台翻译 BLEU 平均得分--针对非向量化存储数据')
    ax.legend()

    def autolabel(rects):
        """
        为每个条形添加得分标签。
        """
        for rect in rects:
            height = rect.get_height()
            x_center = rect.get_x() + rect.get_width() / 2
            ax.annotate(f'{height:.2f}',
                        xy=(x_center, height),
                        xytext=(0, 3),  # 垂直偏移 3 个点
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig(chart_output)
    plt.show()
    print(f"条形统计图已保存为 {chart_output}")

    return platforms, chinese_scores, english_scores


def plot_average_scores(platforms, chinese_scores, english_scores, chart_output="average_bar_chart.png"):
    """
    根据传入的各平台中文和英文翻译的 combined 得分，
    计算每个平台的平均得分（中文和英文得分的平均值），
    并画出一个条形统计图。横坐标为各平台，纵坐标范围固定在 0-1，
    在每个条形顶部标注得分值。
    """
    # 计算各平台的平均值
    average_scores = [(ch + en) / 2 for ch, en in zip(chinese_scores, english_scores)]

    # 设置条形图属性
    x = np.arange(len(platforms))
    width = 0.6

    fig, ax = plt.subplots(figsize=(10, 6))
    rects = ax.bar(x, average_scores, width, color='mediumpurple')

    ax.set_ylabel('Average Combined BLEU Score')
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(platforms)
    ax.set_title('各平台翻译 中文+英文 得分平均值')

    def autolabel_single(rects):
        """
        为单个条形图中的每个条形添加得分标签。
        """
        for rect in rects:
            height = rect.get_height()
            x_center = rect.get_x() + rect.get_width() / 2
            ax.annotate(f'{height:.2f}',
                        xy=(x_center, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel_single(rects)

    plt.tight_layout()
    plt.savefig(chart_output)
    plt.show()
    print(f"平均得分条形统计图已保存为 {chart_output}")


if __name__ == "__main__":
    # 指定包含输出结果的 Excel 文件
    # 要求第一个 sheet 为中文BLEU评分，第二个 sheet 为英文BLEU评分，
    # 且每个 sheet 的列名为:
    # 标签, ours_1-gram, ours_2-gram, ours_combined,
    #      网易_1-gram, 网易_2-gram, 网易_combined,
    #      百度_1-gram, 百度_2-gram, 百度_combined,
    #      Google_1-gram, Google_2-gram, Google_combined,
    #      deepl_1-gram, deepl_2-gram, deepl_combined,
    #      腾讯翻译君_1-gram, 腾讯翻译君_2-gram, 腾讯翻译君_combined
    # 每个 sheet 的最后一行为平均值行，我们只提取其中每个平台的 combined 分数。
    excel_file = "score_output2.xlsx"
    # 画出原始中文和英文得分的分组条形图
    platforms, chinese_scores, english_scores = plot_combined_scores(excel_file, chart_output="非向量化存储数据 平均得分统计图.png")
    # 画出每个平台中文和英文得分的平均值图
    plot_average_scores(platforms, chinese_scores, english_scores, chart_output="非向量化存储数据 综合平均得分统计图.png")