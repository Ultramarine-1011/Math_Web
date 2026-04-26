from __future__ import annotations

from dataclasses import dataclass


SITE_BLURB = "一个面向公开展示的数学空间，收纳图形、动画、笔记与交流。"

HOME_INTRO = (
    "这里汇集数学可视化、课程笔记、交互实验与学习助教。"
    "它既是个人学术主页，也是一间可持续扩展的暗黑数学博物馆。"
)


@dataclass(frozen=True, slots=True)
class FeatureCard:
    title: str
    icon: str
    path: str
    summary: str
    detail: str


FEATURE_CARDS = (
    FeatureCard(
        title="互动实验室",
        icon="实验",
        path="interactive-lab",
        summary="把傅里叶级数、梯度下降和随机模拟放进同一个实验空间。",
        detail="可以调参数、看过程，也可以把它当成一间持续扩充的小型数学实验台。",
    ),
    FeatureCard(
        title="数学画廊",
        icon="画廊",
        path="gallery",
        summary="收纳动力系统与经典代数曲线，适合沉浸式浏览。",
        detail="更偏向静态观赏，但依然保留旋转、缩放和细看结构的空间。",
    ),
    FeatureCard(
        title="数学动画",
        icon="动画",
        path="animations",
        summary="用连续运动来呈现线性代数与几何中的变化过程。",
        detail="重点不只是结果，而是结构如何一步步变形、展开和过渡。",
    ),
    FeatureCard(
        title="笔记资料",
        icon="PDF",
        path="notes",
        summary="按专题整理的 PDF 笔记库，支持摘要、标签与在线预览。",
        detail="适合系统查阅，也适合按兴趣快速翻找某一门课程的资料。",
    ),
    FeatureCard(
        title="交流广场",
        icon="交流",
        path="community",
        summary="一个轻量的留言空间，用来分享想法、提问和留下阅读感受。",
        detail="不追求复杂功能，只保留最直接、最克制的交流方式。",
    ),
    FeatureCard(
        title="复变映射",
        icon="复变",
        path="complex-lab",
        summary="用相位色域和网格变形观察复函数如何扭曲平面。",
        detail="从 z²、反演、指数到圆盘自同构，把抽象映射变成可读图像。",
    ),
    FeatureCard(
        title="分形天文台",
        icon="分形",
        path="fractals",
        summary="实时探索 Mandelbrot 与 Julia 集的逃逸时间图。",
        detail="一条二次迭代公式生成无限层级的边界细节。",
    ),
    FeatureCard(
        title="AI 助教",
        icon="AI",
        path="tutor",
        summary="把数学问题、证明提示和站内笔记清单连接起来。",
        detail="没有 API key 时保持离线演示，有密钥时可作为学习对话框使用。",
    ),
)


PAGE_DESCRIPTIONS = {
    "home": "站点首页。",
    "interactive": "以实验为核心的互动页面。",
    "gallery": "适合浏览与观赏的数学图形页面。",
    "animations": "强调连续变化与动画过程的页面。",
    "complex_lab": "复变函数映射与相位色域页面。",
    "fractals": "Mandelbrot 与 Julia 分形探索页面。",
    "notes": "可筛选、可预览的笔记资料页。",
    "community": "轻量留言与交流页面。",
    "tutor": "可选的大模型数学助教页面。",
}