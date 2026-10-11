# Ultramarine Lab

**交互式数学、概率统计与机器学习实验室**。基于 Streamlit、NumPy、SciPy 和 Plotly，用参数控制、模拟结果与理论对照连接数学结构、统计推断和 AI 的基础原理。

## 实验与资料

| 页面 | 内容 |
|---|---|
| 数学与优化 | 傅里叶圆轮与锯齿波、非凸梯度下降、可调层数与偏置概率的伽尔顿板 |
| 统计与学习 | 均值置信区间的覆盖率模拟；线性回归与岭回归、训练与测试误差、梯度下降与解析解对照 |
| 数学动画 | 平面线性变换、基向量与面积缩放；悬链曲面到螺旋曲面的共轭极小曲面族 |
| 数学画廊 | 洛伦兹吸引子与心形参数曲线 |
| 复变映射 | 幂、反演、指数、Möbius 映射的网格动画与相位色域 |
| 分形天文台 | Mandelbrot 参数空间、填充 Julia 集与边界、多个探索视窗 |
| 笔记资料 | 原有 10 份数学 PDF，标签交集筛选、推荐阅读、在线预览与下载 |

保留原有暗色界面与数学资源。所有实验在本地进程计算，无需账户、数据库或 API 密钥。

## 运行

推荐 Python **3.12**。固定依赖版本用于复现实验；NumPy 和 SciPy 的版本要求 Python 3.11 及以上。

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows 激活命令为 `.venv\Scripts\activate`。在 Streamlit Community Cloud 中选择 `app.py` 为入口即可。

## 实验约定与正确性

- **可复现随机实验**：显式输入随机种子，使用 NumPy `default_rng`。同一代码、依赖版本、参数与种子得到相同数值结果。缓存有容量限制，不改变实验结果。
- **结果导出**：伽尔顿板、梯度下降、置信区间与回归提供 CSV；每一行均附带参数。回归分别导出样本及优化轨迹。CSV 可用于外部绘图和重复计算。
- **伽尔顿板**：槽位为向右次数 `K ~ Binomial(m,p)`，均值 `mp`、方差 `mp(1-p)`；最后不足一批的小球也计入。正态近似需要合适的层数和概率，不把二项分布等同于正态分布。
- **梯度下降**：目标为 `(x²+y²)/10 + sin(x) + cos(y)`，梯度解析计算。Hessian 谱范数不超过 `1.2`，页面学习率位于下降的充分条件范围内。驻点和局部极小值不等同于全局最优解。
- **均值置信区间**：使用无偏样本方差与 Student t 分位数。独立正态样本下具有精确名义覆盖率；标准化指数总体下是近似方法，小样本可能欠覆盖。覆盖率的 Monte Carlo 标准误与样本均值的标准误分开显示。抽样分布图对照正态或平移 Gamma 的精确密度。
- **回归**：数据生成式为 `y=1+2x+ε`，独立正态噪声。固定 75% 训练、25% 测试；训练目标是 `MSE + λw²`，截距不惩罚。解析解使用增广最小二乘，避免显式求逆并支持奇异设计矩阵。学习率相对于 `2/L` 控制；故意使用不稳定学习率时，目标超过 `1e12` 会终止迭代。
- **复变映射**：计算真实复函数，不修改输入以压缩指数或幂函数。非整数幂采用主值分支；极点和视窗外目标隐藏，避免伪造边缘结构。动画中间的插值不保证共形；相位色域中的零点与极点留空。
- **分形**：逃逸次数从 1 计数，`max_iter+1` 表示预算内未逃逸；Julia 初值已在逃逸半径外时记为 0。Julia 使用适用于参数的安全半径。有限迭代无法证明永远有界。
- **动画**：提供播放与暂停。傅里叶 Canvas 在系统偏好减少动态效果时默认暂停。曲面族保持局部第一基本形式，不据此声称全局拓扑等价。

## 工程结构

```text
app.py                      # Streamlit 入口
ultramarine/
  app.py                    # 应用装配
  config.py                 # 公开配置与 AppSettings
  navigation.py             # 页面注册
  content.py                # 首页和导航共用的页面元数据
  ui.py / theme.py          # 共用 UI、结果导出、样式与图表主题
  features/                 # 页面、控件、图表与说明
  math/                     # 无 Streamlit 依赖的数值内核
    optimization.py         # 非凸目标、梯度与下降轨迹
    statistics.py           # 二项模拟与 t 区间
    regression.py           # 数据生成、岭回归与优化
    geometry.py             # 线性变换与极小曲面族
    dynamics.py             # 微分方程与参数曲线
    complex_maps.py         # 复变映射
    fractals.py             # 逃逸时间计算
  data/notes.py             # 笔记清单校验与本地 PDF 读取
data/notes_catalog.json    # 笔记元数据
note_resources/            # 保留的 PDF 资源
 tests/                     # 数值、回归与 Streamlit 冒烟测试
.streamlit/config.toml      # 暗色主题
requirements.txt            # 运行依赖
requirements-dev.txt        # 测试与检查依赖
```

数值内核不依赖 UI；页面组合计算、图表与说明；数据层仅处理本地笔记。新增实验优先复用这三层，无需增加服务框架。

## 配置

通过进程环境变量覆盖，相对路径以仓库根目录为基准：

| 环境变量 | 默认值 |
|---|---|
| `SITE_TITLE` | `Ultramarine Lab` |
| `PROFILE_NAME` | `Ultramarine` |
| `PHOTO_PATH` | `photo.jpg` |
| `NOTES_DIR` | `note_resources` |
| `NOTES_CATALOG_PATH` | `data/notes_catalog.json` |
| `DEBUG` | 关闭；`1` / `true` / `yes` / `on` 启用资源自检 |

笔记清单与文件缓存最长保留 60 秒。无效条目会跳过，缺失 PDF 会提示；目录之外的路径与非 PDF 文件不会加载。

## 验证

从仓库根目录执行，无需额外设置 `PYTHONPATH`：

```bash
pip install -r requirements-dev.txt
pytest
ruff check .
ruff format --check .
```

测试覆盖解析梯度、下降性、二项分布矩与数量守恒、Student t 区间与覆盖率、岭回归解析解和奇异设计、随机种子复现、复变极点与分支、分形已知轨道、曲面端点与局部度量、笔记路径和空筛选，以及全部页面与重要参数切换。

真实服务冒烟检查：

```bash
streamlit run app.py --server.headless=true --server.port=8501
curl --fail http://localhost:8501/_stcore/health
```

## 使用说明

本站用于数学学习与实验。训练数据由明确的概率模型生成；单次模拟或单次训练/测试划分用于观察原理，不能代替正式的数据分析与模型评估。
