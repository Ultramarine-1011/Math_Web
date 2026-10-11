"""Two focused experiments linking statistical inference and supervised learning."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import gamma, norm

from ultramarine.config import AppSettings
from ultramarine.math.regression import fit_regression, generate_regression_data
from ultramarine.math.statistics import simulate_mean_intervals
from ultramarine.theme import PALETTE, transparent_plotly_layout
from ultramarine.ui import download_experiment, render_insight_panel, render_page_intro

cached_intervals = st.cache_data(show_spinner=False, max_entries=24)(simulate_mean_intervals)
cached_data = st.cache_data(show_spinner=False, max_entries=24)(generate_regression_data)
cached_fit = st.cache_data(show_spinner=False, max_entries=24)(fit_regression)


def render_inference() -> None:
    c1, c2, c3 = st.columns(3)
    sample_size = c1.slider("每组样本量 n", 2, 300, 30, key="inference_n")
    repetitions = c2.slider("重复抽样次数", 100, 3000, 1000, 100, key="inference_repetitions")
    confidence = c3.selectbox("置信水平", [0.90, 0.95, 0.99], index=1, key="inference_confidence")
    c1, c2, c3, c4 = st.columns(4)
    distribution = c1.selectbox(
        "总体分布",
        ["normal", "exponential"],
        key="inference_distribution",
        format_func=lambda value: {"normal": "正态", "exponential": "标准化指数（偏态）"}[value],
    )
    mean = c2.number_input("总体均值 μ", -5.0, 5.0, 0.0, 0.5, key="inference_mean")
    sigma = c3.number_input("总体标准差 σ", 0.1, 5.0, 1.0, 0.1, key="inference_sigma")
    seed = int(c4.number_input("随机种子", 0, 2**32 - 1, 42, key="inference_seed"))
    result = cached_intervals(sample_size, repetitions, confidence, seed, distribution, mean, sigma)
    coverage = float(result.covered.mean())
    mc_error = np.sqrt(coverage * (1 - coverage) / repetitions)
    st.latex(
        r"\bar X\pm t_{n-1,(1+c)/2}\frac{S}{\sqrt n},\qquad \mathrm{SE}(\bar X)=\sigma/\sqrt n"
    )
    render_insight_panel(
        "置信区间的长期覆盖率",
        principle="独立同分布正态样本下，(均值估计−μ)/(S/√n) 服从自由度 n−1 的 t 分布。",
        algorithm="反复生成新样本、计算均值和无偏样本方差，再检查区间是否覆盖固定的总体均值。",
        meaning="置信水平描述重复抽样下的覆盖比例；已观测到的区间和 μ 都是固定的。",
    )
    if distribution == "exponential":
        st.info(
            "偏态总体使用 μ+σ(E−1)，E 服从均值为 1 的指数分布。"
            "t 区间仅为近似，小样本覆盖率可能偏离名义水平。"
        )
    c1, c2, c3 = st.columns(3)
    c1.metric("名义置信水平", f"{confidence:.1%}")
    c2.metric("模拟覆盖率", f"{coverage:.1%}")
    c3.metric("覆盖率 MC 标准误（估计）", f"{mc_error:.2%}")
    st.caption("该标准误由模拟覆盖率估计，衡量有限次模拟的波动，不是总体均值估计的标准误。")

    figure = go.Figure()
    shown = min(60, repetitions)
    for covered, name, symbol, color in (
        (True, "覆盖 μ", "circle", PALETTE["jade"]),
        (False, "未覆盖 μ", "x", PALETTE["coral"]),
    ):
        indices = np.flatnonzero(result.covered[:shown] == covered)
        figure.add_trace(
            go.Scatter(
                x=result.means[indices],
                y=indices + 1,
                mode="markers",
                name=name,
                marker={"color": color, "symbol": symbol, "size": 7},
                error_x={
                    "type": "data",
                    "symmetric": False,
                    "array": result.upper[indices] - result.means[indices],
                    "arrayminus": result.means[indices] - result.lower[indices],
                },
            )
        )
    figure.add_vline(x=mean, line_dash="dash", line_color=PALETTE["gold"])
    figure.update_layout(
        **transparent_plotly_layout(550),
        xaxis_title="均值与置信区间",
        yaxis_title=f"抽样编号（前 {shown} 次）",
    )
    st.plotly_chart(figure, width="stretch")
    st.table(
        {
            "统计量": ["均值估计的平均值", "均值估计的标准差", "平均区间宽度"],
            "模拟值": [
                float(result.means.mean()),
                float(result.means.std(ddof=1)),
                float((result.upper - result.lower).mean()),
            ],
            "理论对照": [
                f"μ = {mean:.4f}",
                f"σ/√n = {sigma / np.sqrt(sample_size):.4f}",
                "由 n、σ 与置信水平共同决定",
            ],
        }
    )
    with st.expander("查看均值的抽样分布", expanded=False):
        se = sigma / np.sqrt(sample_size)
        x = np.linspace(
            min(mean - 4 * se, result.means.min()), max(mean + 4 * se, result.means.max()), 400
        )
        density = (
            norm.pdf(x, mean, se)
            if distribution == "normal"
            else gamma.pdf(
                x,
                a=sample_size,
                loc=mean - sigma,
                scale=sigma / sample_size,
            )
        )
        chart = go.Figure(
            [
                go.Histogram(
                    x=result.means, histnorm="probability density", nbinsx=40, name="模拟均值"
                ),
                go.Scatter(
                    x=x, y=density, mode="lines", name="精确抽样密度", line={"dash": "dash"}
                ),
            ]
        )
        chart.update_layout(
            **transparent_plotly_layout(360), xaxis_title="样本均值", yaxis_title="概率密度"
        )
        st.plotly_chart(chart, width="stretch")
    download_experiment(
        "mean_intervals",
        {
            "repetition": np.arange(1, repetitions + 1),
            "mean": result.means,
            "standard_error": result.standard_errors,
            "lower": result.lower,
            "upper": result.upper,
            "covered": result.covered.astype(int),
        },
        {
            "seed": seed,
            "distribution": distribution,
            "sample_size": sample_size,
            "repetitions": repetitions,
            "confidence": confidence,
            "population_mean": mean,
            "population_sigma": sigma,
        },
    )


def render_regression() -> None:
    c1, c2, c3 = st.columns(3)
    sample_size = c1.slider("数据量", 40, 400, 120, 20, key="regression_n")
    noise = c2.slider("噪声标准差", 0.0, 3.0, 0.8, 0.1, key="regression_noise")
    penalty = c3.slider("岭惩罚 λ", 0.0, 3.0, 0.0, 0.1, key="regression_penalty")
    c1, c2, c3 = st.columns(3)
    rate_fraction = c1.slider("学习率 / 稳定上界", 0.05, 1.2, 0.8, 0.05, key="regression_rate")
    steps = c2.slider("优化步数", 20, 300, 100, 10, key="regression_steps")
    seed = int(c3.number_input("随机种子", 0, 2**32 - 1, 42, key="regression_seed"))
    x_train, y_train, x_test, y_test = cached_data(sample_size, noise, seed)
    fit = cached_fit(x_train, y_train, penalty, rate_fraction, steps)
    weights = fit.weights[-1]
    train_prediction, test_prediction = (
        weights[0] + weights[1] * x_train,
        weights[0] + weights[1] * x_test,
    )
    st.latex(
        r"y=1+2x+\varepsilon,\ \varepsilon\sim N(0,\sigma^2),\qquad "
        r"J(b,w)=\frac{1}{n}\sum_i(b+wx_i-y_i)^2+\lambda w^2"
    )
    render_insight_panel(
        "从最小二乘到岭回归",
        principle="λ=0 时为最小二乘，λ>0 时只惩罚斜率，不惩罚截距；惩罚采用 MSE 的尺度。",
        algorithm="75% 数据训练，25% 独立数据测试。从零参数梯度下降，并与增广最小二乘解析解对照。",
        meaning="训练目标包含岭惩罚，测试 MSE 衡量预测误差。单次数据划分不能证明泛化优势。",
    )
    rate = rate_fraction * fit.stability_limit
    st.caption(
        f"实际学习率 η={rate:.4f}；稳定上界 2/L={fit.stability_limit:.4f}，"
        "L 为训练目标 Hessian 的最大特征值。"
    )
    if rate_fraction >= 1:
        st.warning("学习率已达到或超过稳定上界，迭代可能振荡或发散。目标值超过 1e12 时提前停止。")
    c1, c2, c3 = st.columns(3)
    c1.metric("训练 MSE", f"{np.mean((train_prediction - y_train) ** 2):.5f}")
    c2.metric("测试 MSE", f"{np.mean((test_prediction - y_test) ** 2):.5f}")
    c3.metric("与解析参数的距离", f"{np.linalg.norm(weights - fit.optimum):.6f}")
    x_grid = np.linspace(-2, 2, 150)
    chart = go.Figure(
        [
            go.Scatter(x=x_train, y=y_train, mode="markers", name="训练样本", marker={"size": 6}),
            go.Scatter(
                x=x_test,
                y=y_test,
                mode="markers",
                name="测试样本",
                marker={"symbol": "diamond", "size": 7},
            ),
            go.Scatter(
                x=x_grid, y=weights[0] + weights[1] * x_grid, mode="lines", name="梯度下降拟合"
            ),
            go.Scatter(
                x=x_grid,
                y=fit.optimum[0] + fit.optimum[1] * x_grid,
                mode="lines",
                name="解析最优解",
                line={"dash": "dash"},
            ),
            go.Scatter(
                x=x_grid, y=1 + 2 * x_grid, mode="lines", name="真实回归函数", line={"dash": "dot"}
            ),
        ]
    )
    chart.update_layout(**transparent_plotly_layout(440), xaxis_title="x", yaxis_title="y")
    st.plotly_chart(chart, width="stretch")
    optimum_loss = float(
        np.mean((fit.optimum[0] + fit.optimum[1] * x_train - y_train) ** 2)
        + penalty * fit.optimum[1] ** 2
    )
    loss_chart = go.Figure(go.Scatter(y=fit.losses, mode="lines", name="训练目标 J"))
    loss_chart.add_hline(y=optimum_loss, line_dash="dash", line_color=PALETTE["coral"])
    loss_chart.update_layout(
        **transparent_plotly_layout(300), xaxis_title="迭代", yaxis_title="MSE + λw²"
    )
    st.plotly_chart(loss_chart, width="stretch")
    st.table(
        {
            "参数": ["截距 b", "斜率 w"],
            "迭代解": weights,
            "解析解": fit.optimum,
            "真实参数": [1.0, 2.0],
        }
    )
    parameters = {
        "seed": seed,
        "sample_size": sample_size,
        "noise": noise,
        "penalty": penalty,
        "rate_fraction": rate_fraction,
        "learning_rate": rate,
        "steps": steps,
        "completed_steps": len(fit.losses) - 1,
    }
    download_experiment(
        "regression_samples",
        {
            "split": ["train"] * len(x_train) + ["test"] * len(x_test),
            "x": np.concatenate([x_train, x_test]),
            "y": np.concatenate([y_train, y_test]),
            "prediction": np.concatenate([train_prediction, test_prediction]),
        },
        parameters,
        label="下载样本 CSV（含参数）",
    )
    download_experiment(
        "regression_optimization",
        {
            "iteration": np.arange(len(fit.losses)),
            "intercept": fit.weights[:, 0],
            "slope": fit.weights[:, 1],
            "objective": fit.losses,
        },
        parameters,
        label="下载优化轨迹 CSV（含参数）",
    )


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "统计与学习",
        "通过重复抽样与简单监督学习，检验统计推断和机器学习的基础原理。",
        "Statistics & Machine Learning",
    )
    inference, regression = st.tabs(["均值置信区间", "线性回归与岭回归"])
    with inference:
        render_inference()
    with regression:
        render_regression()
