# Ultramarine Mathematics Atelier

一个基于 Streamlit 的公开数学展示站，包含 Home、Interactive Lab、Gallery、Animations、Complex Lab、Fractals、Notes、Community、AI Tutor 等页面。

## 本次重构做了什么

- 用 `st.navigation` 把原来的单入口侧边栏路由改成原生多页面站点
- 新增 `ultramarine/` 应用包，拆分配置层、主题层、数据层和功能页
- 笔记模块改成 `PDF + JSON 清单` 的结构
- 留言模块改成仓储抽象，支持本地 JSON 与 Supabase 两种后端
- 统一了视觉主题、Plotly 样式和站点首页
- 升级为暗黑玻璃拟态界面，新增复变函数映射、分形探索器和可选 AI 数学助教
- 补充了迁移脚本、测试和部署说明

## 目录概览

- `app.py`: Streamlit 入口
- `ultramarine/`: 应用代码
- `data/notes_catalog.json`: 笔记清单
- `note_resources/`: PDF 笔记资源
- `scripts/migrate_comments_to_supabase.py`: 旧留言迁移脚本
- `tests/`: 单元测试与页面 smoke tests

## 本地运行

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

如果不配置 Supabase，留言页会自动回退到本地 `data/comments.json`。

## Streamlit Cloud 部署

1. 把仓库推到 GitHub。
2. 在 Streamlit Cloud 里选择 `app.py` 作为入口。
3. 在 Secrets 中填写：

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-key"
SUPABASE_COMMENTS_TABLE = "comments"

# 可选：启用 AI 数学助教
LLM_API_KEY = "your-model-api-key"
LLM_BASE_URL = "https://api.openai.com/v1"
LLM_MODEL = "gpt-4o-mini"
```

`.streamlit/secrets.example.toml` 提供了可复制模板。

## Supabase 表结构建议

```sql
create table if not exists comments (
  id text primary key,
  nickname text not null,
  content text not null,
  created_at timestamptz default now(),
  likes integer not null default 0
);
```

## 迁移旧留言

如果你之前在 `data/comments.json` 里有历史数据，可以执行：

```bash
set SUPABASE_URL=https://your-project.supabase.co
set SUPABASE_KEY=your-key
python scripts/migrate_comments_to_supabase.py
```

## 测试

```bash
pytest
```

## 新增数学功能

- **复变映射实验室**：用相位色域和网格变形展示 `z^2`、`1/z`、`exp(z)` 与圆盘自同构。
- **分形天文台**：以逃逸时间算法探索 Mandelbrot 集，并联动展示 Julia 集。
- **AI 数学助教**：通过可选 LLM API 提供概念解释、证明提示和站内笔记导航；未配置密钥时自动进入离线演示模式。
