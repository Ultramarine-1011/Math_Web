"""Shared page metadata used by navigation and the home guide."""

from dataclasses import dataclass

SITE_BLURB = "交互式数学、概率统计与机器学习实验室。"
HOME_INTRO = (
    "从数学结构到数据与 AI 的基础原理：调整参数，观察模拟与优化过程，"
    "用理论结果检验直觉。保留随机种子与实验数据，让每一次探索都可以重现。"
)


@dataclass(frozen=True, slots=True)
class FeatureCard:
    title: str
    path: str
    icon: str
    summary: str
    detail: str


FEATURE_CARDS = (
    FeatureCard(
        "数学与优化",
        "interactive-lab",
        ":material/science:",
        "通过傅里叶级数、梯度下降和伽尔顿板，连接分析、优化与概率。",
        "比较理论与模拟，查看损失变化，导出随机实验结果。",
    ),
    FeatureCard(
        "统计与学习",
        "data-lab",
        ":material/query_stats:",
        "重复抽样检验置信区间，用线性回归与岭回归理解监督学习。",
        "固定种子、区分训练与测试、对照解析解，观察不确定性与正则化。",
    ),
    FeatureCard(
        "数学动画",
        "animations",
        ":material/animation:",
        "让矩阵变换和极小曲面形变成为可观察的连续过程。",
        "从基向量、面积缩放到几何结构，理解数据变换背后的数学。",
    ),
    FeatureCard(
        "数学画廊",
        "gallery",
        ":material/auto_awesome:",
        "探索洛伦兹吸引子与经典参数曲线。",
        "旋转、缩放并调整动力系统参数，观察确定性规则下的复杂结构。",
    ),
    FeatureCard(
        "复变映射",
        "complex-lab",
        ":material/cyclone:",
        "通过网格变形和相位色域观察复函数。",
        "探索幂、反演、指数与 Möbius 映射，辨认极点、分支与局部结构。",
    ),
    FeatureCard(
        "分形天文台",
        "fractals",
        ":material/grain:",
        "探索 Mandelbrot 与 Julia 集的逃逸时间图。",
        "对照参数空间与初值空间，理解迭代、稳定性与计算精度。",
    ),
    FeatureCard(
        "笔记资料",
        "notes",
        ":material/menu_book:",
        "按专题整理的 PDF 笔记库，支持标签筛选、在线预览与下载。",
        "从分析、线性代数到拓扑与代数，为实验补充理论基础。",
    ),
)
