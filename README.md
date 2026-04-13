# Ultramarine Mathematics Atelier

基于 **Streamlit** 的公开数学展示站：把可视化、互动实验、PDF 笔记与轻量留言放在同一站点里，用顶部导航在多个主题页面间切换。

---

## 功能概览

| 分组 | 页面 | 功能 |
|------|------|--------|
| **总览** | **首页** | 站点介绍、六页导览与快捷入口；展示笔记数量、推荐资料数等指标。 |
| **探索** | **互动实验室** | 可调参数的实验：**傅里叶级数**（Canvas 圆轮逼近波形）、**梯度下降**（3D 曲面与下降路径动画）、**伽尔顿板**（小球落槽与理论二项分布对比）。 |
| | **数学画廊** | 偏静态观赏的 **Plotly** 图形：**洛伦兹吸引子**（参数可调）、**心形参数曲线** 等，支持旋转缩放。 |
| | **数学动画** | 强调「过程」：**2×2 矩阵对平面与基向量的连续线性变换**（含行列式提示）、**曲面从悬链到螺旋的形变** 等动画。 |
| **资料与交流** | **笔记资料** | 由 `data/notes_catalog.json` + `note_resources/` 中的 **PDF** 驱动：标签筛选、推荐阅读、在线预览与下载。 |
| | **交流广场** | 发布留言、展示列表、点赞；存储可切换（见下文）。 |

留言后端支持三种策略（环境变量 `COMMENT_BACKEND`）：

- **`auto`（默认）**：若配置了 Supabase 凭证则走云端，否则使用本地 `data/comments.json`。
- **`json`**：始终使用本地 JSON。
- **`supabase`**：强制云端；若凭证缺失或初始化失败，会降级为**只读**本地展示，避免误写。

其他常用配置可通过环境变量覆盖，例如站点标题、头像路径、笔记目录等（见 `ultramarine/config.py` 中的 `load_settings`）。

---

## 技术栈

- **Python** 3.10+（推荐 3.12；依赖如 Streamlit 1.55 需 ≥3.10）
- **Streamlit**（`st.navigation` 多页顶栏路由）
- **NumPy / SciPy** 数值与微分方程
- **Plotly** 交互图与动画帧
- **Supabase**（可选）云端留言

---

## 仓库结构（精简）

```
app.py                 # 入口，调用 ultramarine.app.run
ultramarine/           # 应用包：配置、主题、导航、各 feature 页、数据层
data/
  notes_catalog.json   # 笔记清单（元数据）
  comments.json        # 未接 Supabase 时的本地留言（自动生成可为空数组）
note_resources/        # PDF 笔记文件
scripts/
  migrate_comments_to_supabase.py  # 历史留言从 JSON 迁到 Supabase
tests/                 # pytest；部分用例需从仓库根设置 PYTHONPATH
.streamlit/            # config.toml；secrets 见 secrets.example.toml
```

---

## 本地运行

### 1. 准备 Python 环境

需要 **Python 3.10 及以上**。若系统自带版本过旧，可使用 [uv](https://github.com/astral-sh/uv) 安装较新解释器并建虚拟环境：

```bash
cd /path/to/Math_Web
uv python install 3.12
uv venv --python 3.12 .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

或使用传统 `venv` + `pip`（在已安装 3.10+ 的前提下）：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 启动应用

```bash
streamlit run app.py
```

未配置 Supabase 时，交流广场会自动使用 **`data/comments.json`**（不存在时会按需创建）。

### 3. 运行测试

测试从仓库根导入包 `ultramarine`，需设置 **`PYTHONPATH`** 指向项目根目录：

```bash
cd /path/to/Math_Web
source .venv/bin/activate
PYTHONPATH=. pytest
```

代码风格检查（若已安装 ruff）：

```bash
ruff check .
```

---

## 可选配置：Supabase 留言

本地可把 `.streamlit/secrets.example.toml` 复制为 `.streamlit/secrets.toml` 并填入真实值；或通过环境变量提供：

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_COMMENTS_TABLE`（默认 `comments`）

建议在数据库中创建如下表（字段名与代码一致）：

```sql
create table if not exists comments (
  id text primary key,
  nickname text not null,
  content text not null,
  created_at timestamptz default now(),
  likes integer not null default 0
);
```

若此前使用本地 JSON 留言，可迁移到 Supabase（在 shell 中设置好环境变量后执行）：

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key"
python scripts/migrate_comments_to_supabase.py
```

---

## Streamlit Cloud 部署

1. 将仓库推送到 GitHub。
2. 在 Streamlit Cloud 中选择 **`app.py`** 作为入口。
3. 在 **Secrets** 中填写 Supabase 相关键值（模板见 `.streamlit/secrets.example.toml`）。

---

## 许可与说明

本站为个人数学展示与学习用途；可视化与交互逻辑集中在 `ultramarine/features/` 与 `ultramarine/theme.py` 中，可按页面逐步扩展或替换内容。
