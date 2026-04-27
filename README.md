# Ultramarine Mathematics Atelier 项目教程

这是一个用 **Streamlit + Plotly + NumPy/SciPy** 构建的数学可视化网站。它把个人主页、数学实验、图形画廊、动画、笔记资料、留言区和 AI 助教放在同一个网页应用中，适合作为网页开发初学者理解“一个小型但完整的 Web 项目如何组织”的学习案例。

如果你是第一次读这个项目，可以先记住一句话：

> 这个项目的核心不是复杂后端，而是把数学计算、交互控件、可视化图表和页面组织方式整合成一个可持续扩展的 Streamlit 应用。

## 1. 项目能做什么

网站当前包含 9 个主要页面：

- **首页**：展示站点介绍、统计数据和页面导览。
- **互动实验室**：包含傅里叶级数、梯度下降、伽尔顿板等可调参数实验。
- **数学画廊**：展示洛伦兹吸引子、心形参数曲线等图形。
- **数学动画**：展示线性变换动画、悬链曲面到螺旋曲面的连续形变。
- **复变映射**：把复函数看成平面变形，用动画观察幂映射、反演、指数映射和 Mobius 映射。
- **分形天文台**：实时生成 Mandelbrot 集和 Julia 集的逃逸时间图。
- **笔记资料**：读取本地 PDF 笔记清单，支持标签筛选、预览和下载。
- **交流广场**：支持留言、点赞，本地 JSON 和 Supabase 云端两种存储方式。
- **AI 助教**：可接入 OpenAI 兼容接口，围绕数学概念、证明思路和学习路线进行问答。

从初学者角度看，它覆盖了网页项目里常见的几个主题：

- 页面入口和导航如何组织。
- 配置、数据、业务逻辑和 UI 如何分层。
- 如何把计算结果变成图表。
- 如何用缓存避免重复计算。
- 如何做输入校验、错误降级和测试。
- 如何把可选外部服务接入项目，而不让项目离线时崩溃。

## 2. 快速运行项目

### 2.1 环境准备

建议使用 Python 3.13 或与依赖兼容的较新 Python 版本。项目依赖写在 `requirements.txt` 中，主要包括：

- `streamlit`：快速构建网页交互界面。
- `plotly`：绘制交互式二维、三维图表和动画。
- `numpy`：向量化数学计算。
- `scipy`：数值积分和概率分布工具。
- `supabase`：可选的云端留言存储。
- `pytest` 和 `ruff`：测试与代码检查。

### 2.2 安装依赖

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 启动网页

```powershell
streamlit run app.py
```

启动后，Streamlit 会在终端输出本地访问地址，通常类似：

```text
http://localhost:8501
```

浏览器打开该地址即可访问网站。

### 2.4 运行测试

```powershell
pytest
```

如果只想检查代码风格：

```powershell
ruff check .
```

## 3. 项目结构总览

项目最重要的代码集中在 `ultramarine/` 目录中：

```text
web/
├── app.py                         # Streamlit 入口，只负责调用 ultramarine.app.run()
├── requirements.txt               # 运行依赖
├── pyproject.toml                 # pytest 与 ruff 配置
├── data/
│   └── notes_catalog.json          # PDF 笔记元数据清单
├── ultramarine/
│   ├── app.py                      # 应用初始化与运行流程
│   ├── navigation.py               # 页面注册与顶部导航
│   ├── config.py                   # 读取环境变量、secrets 和默认配置
│   ├── models.py                   # AppSettings、NoteEntry、Comment 等数据模型
│   ├── layout.py                   # 侧边栏、页面标题、调试面板等布局组件
│   ├── theme.py                    # 全局 CSS、颜色系统、Plotly 主题
│   ├── ui.py                       # 卡片、标签、洞察面板等可复用 UI
│   ├── ai.py                       # OpenAI 兼容接口调用与 Markdown 清洗
│   ├── data/
│   │   ├── notes.py                # 笔记清单读取
│   │   └── comments.py             # 留言仓储、校验、本地/云端存储
│   ├── math/
│   │   ├── complex_maps.py         # 复变映射算法
│   │   └── fractals.py             # Mandelbrot 与 Julia 逃逸算法
│   └── features/
│       ├── home.py                 # 首页
│       ├── interactive.py          # 互动实验室
│       ├── gallery.py              # 数学画廊
│       ├── animations.py           # 数学动画
│       ├── complex_lab.py          # 复变映射页面
│       ├── fractals.py             # 分形页面
│       ├── notes.py                # 笔记页面
│       ├── community.py            # 留言页面
│       └── tutor.py                # AI 助教页面
└── tests/                          # 单元测试与 Streamlit smoke tests
```

根目录下还有一个 `modules/` 目录，里面也有一些页面实现文件。从当前入口看，真正运行的网站使用的是 `ultramarine/` 这套模块化结构。学习和维护时应优先阅读 `ultramarine/`。

## 4. 一次请求是如何跑起来的

整个应用的入口非常短：

```python
from ultramarine.app import run

run()
```

这是一种常见设计：根目录的 `app.py` 保持干净，只负责启动；真正逻辑放进包内，方便测试、复用和维护。

核心运行流程在 `ultramarine/app.py`：

1. `load_settings()` 读取站点标题、头像路径、笔记路径、Supabase 配置、LLM 配置等。
2. `st.set_page_config()` 设置 Streamlit 页面标题、图标和宽屏布局。
3. `_initialize_session_state()` 初始化会话状态，例如动画速度、图表质量、已点赞留言等。
4. `configure_plotly_theme()` 设置 Plotly 全局主题。
5. `apply_global_styles()` 注入全局 CSS，让 Streamlit 默认界面变成暗黑玻璃风格。
6. `build_navigation(settings)` 注册所有页面。
7. `render_sidebar(settings)` 渲染侧边栏。
8. `render_debug_panel(settings)` 在调试模式下显示配置状态。
9. `current_page.run()` 执行当前页面的 `render()` 函数。

可以把它理解成一条流水线：

```text
读取配置 -> 初始化状态 -> 设置主题 -> 注册导航 -> 渲染公共布局 -> 渲染当前页面
```

这个顺序很重要。比如页面渲染前必须先有配置，图表出现前必须先有 Plotly 主题，导航链接出现前必须先注册页面。

## 5. Streamlit 在这里扮演什么角色

传统 Web 开发通常需要前端、后端、路由、模板、接口等多层结构。Streamlit 的思路不同：你主要用 Python 写页面，Streamlit 自动把控件和图表变成网页。

例如：

- `st.slider()` 生成滑块。
- `st.tabs()` 生成标签页。
- `st.columns()` 生成多列布局。
- `st.plotly_chart()` 把 Plotly 图表放到页面上。
- `st.session_state` 保存一次浏览会话中的状态。
- `@st.cache_data` 缓存计算结果。
- `@st.cache_resource` 缓存资源对象，例如数据库仓储。

这使得项目非常适合数学可视化：页面控件改变参数，Python 重新计算数据，Plotly 重新绘图，用户立即看到结果。

## 6. 配置系统：让项目既能本地跑，也能部署

配置集中在 `ultramarine/config.py`，返回一个 `AppSettings` 对象。这个对象定义在 `ultramarine/models.py` 中。

它主要读取三类信息：

- 操作系统环境变量，例如 `SITE_TITLE`、`PROFILE_NAME`。
- Streamlit secrets，例如部署时使用的 Supabase 或 LLM 密钥。
- 本地 `.env` 文件里的可选大模型配置。

常用配置项包括：

- `SITE_TITLE`：网站标题。
- `PROFILE_NAME`：侧边栏显示的名称。
- `PHOTO_PATH`：头像图片路径，默认 `photo.jpg`。
- `NOTES_DIR`：PDF 笔记目录，默认 `note_resources`。
- `NOTES_CATALOG_PATH`：笔记清单路径，默认 `data/notes_catalog.json`。
- `COMMENT_BACKEND`：留言后端，可设为 `auto`、`json` 或 `supabase`。
- `DEBUG`：是否显示开发自检面板。
- `SUPABASE_URL`、`SUPABASE_KEY`、`SUPABASE_COMMENTS_TABLE`：留言云端存储配置。
- `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`：AI 助教配置。

这里的设计思想是：**功能可以依赖外部服务，但项目不能因为外部服务缺失就无法启动。**

例如没有 Supabase 时，留言区会自动使用本地 JSON；没有 LLM API key 时，AI 助教会进入离线演示模式。

## 7. 页面模块：每个页面都是一个 render 函数

`ultramarine/features/` 目录下的每个文件对应一个页面。它们都遵循同一种结构：

```python
def render(settings: AppSettings) -> None:
    ...
```

这种约定让导航系统很容易统一调用页面。

在 `ultramarine/navigation.py` 中，`build_navigation()` 用 `st.Page` 把每个页面注册成 Streamlit 页面，并给它们设置标题、图标和 URL 路径。

这种结构有两个优点：

- 页面之间互相独立，修改某个页面时不容易影响其他页面。
- 新增页面很简单：写一个新的 `features/xxx.py`，再在 `navigation.py` 里注册即可。

## 8. UI 与主题：为什么页面看起来不像默认 Streamlit

Streamlit 默认界面比较朴素。这个项目通过两层方式重塑视觉风格：

1. `ultramarine/theme.py` 定义颜色、字体、卡片阴影、按钮、输入框、标签页等全局 CSS。
2. `ultramarine/ui.py` 封装可复用组件，例如卡片、指标、图表标题和洞察面板。

例如项目里很多页面都有“数学原理 / 算法逻辑 / 哲学意味”的解释面板，这不是 Streamlit 原生组件，而是 `render_insight_panel()` 统一生成的 HTML 结构。

值得注意的是，项目在渲染自定义 HTML 时使用了 `escape()` 对文本进行转义。这样可以减少用户输入或动态内容带来的 HTML 注入风险。对初学者来说，这是一个很重要的安全意识：**只要你允许 HTML，就必须思考内容是否可信。**

## 9. 数学可视化的基本模式

项目中很多页面都遵循同一个模式：

```text
用户调参数 -> Python 计算数组 -> Plotly 生成图表 -> Streamlit 显示图表
```

以梯度下降为例：

1. 用户通过滑块设置学习率和起点。
2. `compute_gradient_descent()` 计算函数曲面和下降路径。
3. `build_gradient_descent_figure()` 把曲面、路径、当前点和动画帧组装成 Plotly 3D 图。
4. `st.plotly_chart()` 在页面中显示。

这种拆分很值得学习：

- `compute_*` 函数只管数学计算。
- `build_*_figure` 函数只管图表构造。
- `render()` 函数只管页面交互和布局。

这是“关注点分离”的实践。代码越长，越要避免所有逻辑都堆在一个函数里。

## 10. 缓存：为什么重复拖动参数不会太慢

数学图形通常计算量较大。项目大量使用：

```python
@st.cache_data(show_spinner=False)
```

它的含义是：如果函数参数没变，Streamlit 会复用上一次计算结果，而不是重新计算。

典型例子包括：

- 傅里叶 Canvas HTML。
- 梯度下降曲面和路径。
- 伽尔顿板模拟。
- 洛伦兹系统数值解。
- 线性变换动画帧。
- 分形逃逸时间矩阵。
- PDF 文件读取和 Base64 编码。

这里的经验是：**缓存适合纯计算函数，不适合带有副作用的函数。**

例如读取图表数据、生成数组可以缓存；发布留言、点赞这种会改变外部状态的操作不应该用 `cache_data` 缓存。

## 11. 互动实验室：从公式到体验

`ultramarine/features/interactive.py` 展示了三类实验。

### 11.1 傅里叶级数

傅里叶级数的思想是把复杂周期函数拆成许多简单正弦函数的叠加。

页面中用 HTML Canvas 和 JavaScript 绘制旋转圆轮：

- 每个圆轮代表一个频率项。
- 圆轮半径由傅里叶系数决定。
- 最后一个圆轮的端点形成右侧波形轨迹。

这说明 Streamlit 不只能显示 Python 图表，也可以嵌入少量前端代码实现更灵活的动画。

### 11.2 梯度下降

项目使用的目标函数是：

```text
f(x, y) = (x^2 + y^2) / 10 + sin(x) + cos(y)
```

梯度是：

```text
∇f = (x/5 + cos(x), y/5 - sin(y))
```

每一步更新：

```text
(x, y) <- (x, y) - η∇f
```

这里的 `η` 就是学习率。学习率太小会走得慢，太大可能越过合适位置。页面让用户亲自调参数，比静态公式更容易理解优化算法。

### 11.3 伽尔顿板

伽尔顿板模拟每个小球每层向左或向右的随机选择。单个小球路径不可预测，但大量小球会形成接近二项分布的稳定形状。

页面中既画模拟结果，也画理论二项分布曲线。这是一种很好的教学方式：**把实验数据和理论模型放在同一张图里比较。**

## 12. 数学画廊：静态图形也需要算法

`ultramarine/features/gallery.py` 主要展示两类图形。

### 12.1 洛伦兹吸引子

洛伦兹系统是一个经典混沌系统：

```text
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

项目用 `scipy.integrate.odeint` 数值求解微分方程，再用 Plotly 画出三维轨迹。

这体现了一个常见工作流：数学模型并不直接等于图形，通常要先做数值求解，再把求解结果映射到视觉元素上。

### 12.2 心形曲线

心形曲线使用参数方程生成：

```text
x = 16 sin^3(t)
y = 13 cos(t) - 5 cos(2t) - 2 cos(3t) - cos(4t)
```

这类曲线适合帮助初学者理解“参数化”的思想：图形不是由 `y=f(x)` 唯一表示，也可以由一个共同参数 `t` 同时控制 `x` 和 `y`。

## 13. 数学动画：过程比结果更重要

`ultramarine/features/animations.py` 强调“变化过程”。

### 13.1 线性变换

页面允许用户输入 2x2 矩阵：

```text
A = [[a11, a12],
     [a21, a22]]
```

程序会把平面网格和两个基向量 `i`、`j` 一起变换。行列式 `det(A)` 用来解释面积缩放和方向翻转：

- `det(A) > 0`：方向保持。
- `det(A) < 0`：方向翻转。
- `det(A)` 接近 0：平面被压扁，信息丢失严重。

动画不是直接跳到目标矩阵，而是在单位矩阵和目标矩阵之间插值。这让用户看到“从原始空间到变换后空间”的连续过程。

### 13.2 曲面形变

页面还展示了悬链曲面到螺旋曲面的连续形变。代码中使用 `smoothstep`：

```text
progress = t^2(3 - 2t)
```

它比简单线性插值更平滑，起点和终点不会突然加速或减速。这个细节体现了动画设计中的一个原则：**数学上正确还不够，视觉运动也要自然。**

## 14. 复变映射：把函数看成平面变形

复变映射页面由两个部分配合完成：

- `ultramarine/features/complex_lab.py` 负责页面控件、图表和说明。
- `ultramarine/math/complex_maps.py` 负责复数网格、映射计算和动画帧生成。

页面支持几类映射：

- 幂映射：`f(z)=s z^n + b`
- 反演型映射：`f(z)=s/(z-p)+b`
- 指数映射：`f(z)=exp(s z)+b`
- Mobius 型映射：`f(z)=s(z-a)/(z-p)+b`

算法步骤是：

1. 生成复平面网格线。
2. 对每条线上的点计算目标复函数值。
3. 对过大或无穷的值做裁剪或设为 `NaN`，避免图表崩坏。
4. 在原始网格和映射后网格之间用 smoothstep 插值。
5. 把每一帧交给 Plotly 动画播放。

初学者可以从这里学到一个关键思想：**复函数不仅是数字到数字的计算，也可以理解为空间到空间的变形规则。**

## 15. 分形天文台：用简单规则生成复杂图像

分形相关算法在 `ultramarine/math/fractals.py`，页面在 `ultramarine/features/fractals.py`。

Mandelbrot 和 Julia 集都来自同一个迭代：

```text
z_{n+1} = z_n^2 + c
```

区别是：

- Mandelbrot 集：把每个像素当作参数 `c`，初值 `z=0`。
- Julia 集：固定参数 `c`，把每个像素当作初值 `z`。

项目使用“逃逸时间算法”：

1. 对每个像素构造一个复数。
2. 反复执行 `z = z^2 + c`。
3. 如果 `|z| > 2`，认为它已经逃逸。
4. 记录首次逃逸所需的迭代次数。
5. 把迭代次数映射成颜色。

这段实现使用 NumPy 数组一次性处理整张图，而不是对每个像素写 Python 循环。对图像计算来说，向量化非常重要。

## 16. 笔记资料：用 JSON 管理内容

笔记页面由 `ultramarine/features/notes.py` 和 `ultramarine/data/notes.py` 组成。

`data/notes_catalog.json` 是笔记清单。每条记录包含：

- `slug`：唯一标识。
- `title`：标题。
- `summary`：摘要。
- `file_name`：PDF 文件名。
- `tags`：标签。
- `featured`：是否推荐。
- `sort_order`：排序值。

页面启动时会读取这份清单，然后检查对应 PDF 是否存在。如果文件缺失，会跳过该条目并给出提示，而不是让整个页面报错。

这是一种稳健设计：**外部内容可能不完整，页面应该尽量优雅降级。**

如果要添加一份新笔记：

1. 把 PDF 放进 `note_resources/` 目录。
2. 在 `data/notes_catalog.json` 中增加一条记录。
3. 确保 `file_name` 与 PDF 文件名完全一致。
4. 重启或刷新页面。

当前仓库中没有检测到 PDF 文件，因此笔记清单中的文件需要你在本地补齐后才能显示。

## 17. 交流广场：本地 JSON 与 Supabase 的仓储模式

留言逻辑集中在 `ultramarine/data/comments.py`。

这里有一个很值得学习的设计：项目定义了 `CommentRepository` 协议。无论底层存储是本地 JSON 还是 Supabase，只要实现下面几个方法，就可以被页面统一使用：

```python
class CommentRepository(Protocol):
    def list_comments(self, limit: int) -> list[Comment]: ...
    def create_comment(self, nickname: str, content: str) -> Comment: ...
    def increment_like(self, comment_id: str) -> int: ...
    def is_writable(self) -> bool: ...
```

这叫“面向接口编程”。页面不需要关心评论存在哪里，只需要调用仓储方法。

### 17.1 本地 JSON 模式

默认情况下，项目会在 `data/comments.json` 中保存留言。这个模式适合本地开发和轻量演示。

### 17.2 Supabase 模式

部署到公开网站时，可以配置 Supabase。配置项包括：

```text
SUPABASE_URL
SUPABASE_KEY
SUPABASE_COMMENTS_TABLE
```

一个可参考的表结构是：

```sql
create table comments (
  id uuid primary key default gen_random_uuid(),
  nickname text not null,
  content text not null,
  created_at timestamptz not null default now(),
  likes integer not null default 0
);
```

如果指定 Supabase 但缺少凭证，页面会进入只读模式，避免用户以为留言已经成功写入。

### 17.3 输入校验

`validate_comment_input()` 会检查：

- 昵称不能为空。
- 昵称长度不能超过 24。
- 留言不能为空。
- 留言长度不能超过 1200。
- 不允许提交 `<script` 或 `javascript:` 这类明显脚本内容。

页面层还使用冷却时间 `COMMENT_COOLDOWN_SECONDS` 防止连续刷屏。

## 18. AI 助教：可选的 OpenAI 兼容接口

AI 助教页面由 `ultramarine/features/tutor.py` 和 `ultramarine/ai.py` 组成。

它的设计重点是“可选”：

- 有 `LLM_API_KEY` 时，调用在线模型。
- 没有 API key 时，仍展示界面和推荐问题，并给出离线提示。

模型调用使用标准 Chat Completions 风格接口：

```text
POST {LLM_BASE_URL}/chat/completions
```

默认模型是 `gpt-4o-mini`。如果 `.env` 中配置了 `DEEPSEEK_API_KEY`，默认 base URL 会切到 DeepSeek 接口，并使用 `deepseek-chat`。

`normalize_markdown()` 用来清洗模型返回内容。有些模型会把整段答案包在 Markdown 代码围栏里，这个函数会把多余围栏去掉，让页面渲染更自然。

## 19. 测试体系：项目不是只能“看起来能跑”

测试位于 `tests/`。

项目测试覆盖了几类风险：

- `test_app_smoke.py`：使用 Streamlit 的 `AppTest` 跑每个页面，确保页面不会启动时报错。
- `test_notes.py`：检查笔记清单读取、缺失文件跳过、坏 JSON 处理。
- `test_comments.py`：检查留言输入校验、本地 JSON 仓储、Supabase 仓储和只读降级。
- `test_fractals.py`：检查 Mandelbrot 和 Julia 算法输出形状与数值范围。
- `test_complex_maps.py`：检查复变映射相关计算。
- `test_ai.py`：检查 Markdown 清洗函数。

对初学者来说，这里的启发是：测试不一定一开始就覆盖所有视觉细节，但应该覆盖“最容易坏、坏了影响最大”的逻辑。

## 20. 如何新增一个页面

假设你想新增一个“数论实验”页面，可以按下面步骤做。

### 20.1 新建页面文件

在 `ultramarine/features/number_theory.py` 中写：

```python
from __future__ import annotations

import streamlit as st

from ultramarine.layout import render_page_intro
from ultramarine.models import AppSettings


def render(settings: AppSettings) -> None:
    del settings
    render_page_intro(
        "数论实验",
        "用交互图形理解同余、素数和算术函数。",
        kicker="Number Theory",
    )
    n = st.slider("选择整数 n", 2, 200, 30)
    st.write(f"{n} 的平方是 {n * n}")
```

### 20.2 注册页面

在 `ultramarine/navigation.py` 中导入新模块，并在 `pages` 字典中新增：

```python
"number-theory": _page(
    number_theory,
    settings,
    title="数论实验",
    icon=":material/functions:",
    url_path="number-theory",
),
```

然后把它放入导航分组即可。

### 20.3 思考是否需要拆分算法

如果页面只是展示简单文本，可以直接写在页面里；如果涉及计算，例如筛法、同余类统计、图结构，建议把算法放到 `ultramarine/math/` 或单独模块中，再由页面调用。

## 21. 如何维护和扩展这个项目

### 21.1 保持当前分层

建议继续遵循：

```text
features/ 负责页面
math/     负责数学计算
data/     负责数据读写
ui.py     负责可复用 UI 组件
theme.py  负责视觉系统
config.py 负责配置读取
```

这样项目即使继续增加页面，也不会变成一个巨大的单文件应用。

### 21.2 新增重计算功能时先考虑缓存

如果函数输入固定、输出固定、没有副作用，可以考虑加 `@st.cache_data`。例如：

- 数值积分。
- 大数组生成。
- 分形计算。
- 文件读取。

但下面这些不适合缓存：

- 发布留言。
- 点赞。
- 调用在线模型。
- 写入数据库。

### 21.3 用户输入永远要校验

留言区已经做了基础校验。以后如果添加上传、搜索、导入文件等功能，也应遵循同样原则：

- 限制长度。
- 限制类型。
- 给出清晰错误提示。
- 不信任用户输入里的 HTML 或脚本。

### 21.4 把“能运行”升级为“可解释”

这个项目的一大优点是很多页面不仅展示图，还解释“数学原理、算法逻辑、哲学意味”。如果继续扩展，建议保留这种风格。它能让网站从作品展示变成学习工具。

## 22. 初学者阅读代码的推荐路线

如果你还不熟悉项目，不建议从最复杂的页面开始。可以按下面顺序读：

1. `app.py`：理解入口为什么很短。
2. `ultramarine/app.py`：理解应用初始化流程。
3. `ultramarine/navigation.py`：理解页面如何注册。
4. `ultramarine/models.py`：理解项目有哪些核心数据对象。
5. `ultramarine/config.py`：理解配置如何进入应用。
6. `ultramarine/theme.py` 和 `ultramarine/ui.py`：理解视觉风格如何复用。
7. `ultramarine/features/home.py`：从最简单页面开始。
8. `ultramarine/features/interactive.py`：学习控件、缓存、计算和图表如何结合。
9. `ultramarine/data/comments.py`：学习本地存储、云端存储和接口抽象。
10. `ultramarine/math/fractals.py`：学习如何把数学算法写成可测试函数。

读代码时可以问自己三个问题：

- 这个函数的输入和输出是什么？
- 它是在做页面、做计算，还是做数据读写？
- 如果它出错，会影响哪个页面？

这三个问题比逐行死记更有效。

## 23. 这个项目的设计思路总结

这个项目可以概括为四个关键词。

**模块化**：入口、导航、页面、算法、数据、主题分开写。每个模块承担清晰职责。

**交互式**：用 Streamlit 控件让用户参与数学实验，而不是只看静态图片。

**可降级**：没有 PDF、没有 Supabase、没有 LLM key 时，页面仍尽量保持可用。

**可测试**：把关键算法和数据逻辑拆出来，让它们可以被 `pytest` 独立检查。

对网页开发初学者来说，这个项目最大的价值不只是“做了一个漂亮网站”，而是展示了一种可持续的开发方式：先让功能跑起来，再逐步把入口、配置、页面、算法和数据拆清楚，让项目从 Vibe Coding 走向可理解、可维护和可扩展。
