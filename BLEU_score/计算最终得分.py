# 模糊综合评价计算示例
# 定量赋值：优秀 = 3, 中等 = 2, 差 = 1
# 每个评价维度的得分 = 优秀隶属度 * 3 + 中等隶属度 * 2 + 差隶属度 * 1
# 最终得分 = 各维度得分（加权平均），此处假设所有维度同等重要

def compute_dimension_score(membership):
    """
    计算单个评价指标的得分.
    membership: [excellent, medium, poor]
    定量赋值: 优秀: 3, 中等: 2, 差: 1
    """
    scores = [3, 2, 1]
    dim_score = sum(m * s for m, s in zip(membership, scores))
    return dim_score


def compute_final_score(matrix, weights=None):
    """
    计算一个平台的最终得分.
    matrix: dict, 键为指标名称, 值为一个包含 [excellent, medium, poor] 的列表.
    weights: dict, 键为指标名称, 值为该指标的权重; 如果为None，则采用等权重.
    返回：
      (final_score, details) 其中 details 为各指标得分字典.
    """
    dimensions = list(matrix.keys())
    details = {}
    total_score = 0.0

    if weights is None:
        # 若未指定权重，等权所有指标
        weight = 1.0 / len(dimensions)
        weights = {dim: weight for dim in dimensions}

    for dim in dimensions:
        dim_membership = matrix[dim]
        dim_score = compute_dimension_score(dim_membership)
        details[dim] = dim_score
        total_score += dim_score * weights[dim]

    return total_score, details


# 表10: 网易隶属度矩阵 R
netease_matrix = {
    "准确性": [0.20, 0.55, 0.25],
    "文化语义": [0.10, 0.50, 0.40],
    "一致性": [0.15, 0.60, 0.25],
    "性能":   [0.9, 0.10, 0.0]
}

# 表11: 百度隶属度矩阵 R
baidu_matrix = {
    "准确性": [0.20, 0.65, 0.15],
    "文化语义": [0.10, 0.60, 0.30],
    "一致性": [0.20, 0.65, 0.15],
    "性能":   [0.60, 0.40, 0.0]
}

# 表12: Ours 隶属度矩阵 R
ours_matrix = {
    "准确性": [0.25, 0.60, 0.15],
    "文化语义": [0.30, 0.50, 0.20],
    "一致性": [0.40, 0.55, 0.05],
    "性能":   [0.50, 0.50, 0.0]
}

# 如果需要指定不同指标权重，可在此定义。比如，如果采用专家权重，
# 对于三个关键维度 [准确率, 文化适配, 一致性] 用 A = [0.7, 0.20, 0.10]
# 但此处有4个指标，暂时采用等权重，即每个指标权重为 0.25.
weights = None  # 使用等权重


def print_results(platform, final_score, details):
    print(f"{platform:10}: 最终得分 = {final_score:.3f}")
    for dim, score in details.items():
        print(f"    {dim:10}: {score:.3f}")
    print()


def main():
    netease_final, netease_details = compute_final_score(netease_matrix, weights)
    baidu_final, baidu_details = compute_final_score(baidu_matrix, weights)
    ours_final, ours_details = compute_final_score(ours_matrix, weights)

    print("模糊综合评价结果（定量值范围1～3，其中3表示最佳表现）:")
    print_results("网易翻译", netease_final, netease_details)
    print_results("百度翻译", baidu_final, baidu_details)
    print_results("Ours", ours_final, ours_details)

    # 汇总表
    print("汇总表:")
    print(f"{'平台':10s} {'最终得分':>10s}")
    print("-" * 25)
    print(f"{'网易翻译':10s} {netease_final:10.3f}")
    print(f"{'百度翻译':10s} {baidu_final:10.3f}")
    print(f"{'Ours':10s} {ours_final:10.3f}")


if __name__ == "__main__":
    main()