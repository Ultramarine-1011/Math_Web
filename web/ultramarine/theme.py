from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


PALETTE = {
    "ink": "#162133",
    "muted": "#5A6475",
    "line": "#D7CFBE",
    "paper": "#F7F4ED",
    "panel": "#EEE6D8",
    "ultramarine": "#0F52BA",
    "azure": "#3F88FF",
    "coral": "#E86C4E",
    "jade": "#2F8F83",
    "gold": "#D2A44C",
}

COLORWAY = [
    PALETTE["ultramarine"],
    PALETTE["coral"],
    PALETTE["jade"],
    PALETTE["gold"],
    PALETTE["azure"],
]


def configure_plotly_theme() -> None:
    pio.templates["ultramarine"] = go.layout.Template(
        layout=go.Layout(
            colorway=COLORWAY,
            font={"family": "Space Grotesk, Segoe UI, sans-serif", "color": PALETTE["ink"]},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hoverlabel={
                "bgcolor": "#FFFFFF",
                "bordercolor": PALETTE["line"],
                "font": {"family": "Space Grotesk, Segoe UI, sans-serif"},
            },
        )
    )
    pio.templates.default = "ultramarine"


def apply_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

        :root {{
            --ink: {PALETTE["ink"]};
            --muted: {PALETTE["muted"]};
            --line: {PALETTE["line"]};
            --paper: {PALETTE["paper"]};
            --panel: {PALETTE["panel"]};
            --ultramarine: {PALETTE["ultramarine"]};
            --azure: {PALETTE["azure"]};
            --coral: {PALETTE["coral"]};
            --jade: {PALETTE["jade"]};
            --gold: {PALETTE["gold"]};
            --shadow: 0 22px 70px rgba(15, 82, 186, 0.08);
            --radius-lg: 28px;
            --radius-md: 18px;
        }}

        .stApp {{
            background:
                radial-gradient(circle at top right, rgba(63, 136, 255, 0.10), transparent 28%),
                radial-gradient(circle at top left, rgba(232, 108, 78, 0.08), transparent 25%),
                linear-gradient(180deg, #fcfbf8 0%, var(--paper) 100%);
        }}

        [data-testid="stHeader"] {{
            background: rgba(247, 244, 237, 0.72);
            backdrop-filter: blur(14px);
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(255,255,255,0.82) 0%, rgba(247,244,237,0.92) 100%);
            border-right: 1px solid rgba(215, 207, 190, 0.9);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.2rem;
        }}

        body, p, li, div, label, span {{
            font-family: "Space Grotesk", "Segoe UI", sans-serif;
            color: var(--ink);
        }}

        h1, h2, h3, h4 {{
            font-family: "Cormorant Garamond", Georgia, serif !important;
            letter-spacing: -0.02em;
            color: var(--ink);
        }}

        .hero-shell {{
            padding: 2.2rem 2rem 2rem;
            border: 1px solid rgba(215, 207, 190, 0.85);
            border-radius: var(--radius-lg);
            background:
                linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(247,244,237,0.94) 54%, rgba(63,136,255,0.09) 100%);
            box-shadow: var(--shadow);
            overflow: hidden;
        }}

        .hero-kicker {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: rgba(15, 82, 186, 0.1);
            color: var(--ultramarine);
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .hero-title {{
            margin: 0.8rem 0 0.7rem;
            font-size: clamp(2.7rem, 5vw, 4.8rem);
            line-height: 0.9;
        }}

        .hero-lead {{
            max-width: 48rem;
            font-size: 1.08rem;
            line-height: 1.8;
            color: var(--muted);
        }}

        .page-title {{
            margin: 0 0 0.35rem;
            font-size: clamp(2.2rem, 4vw, 3.4rem);
        }}

        .page-lead {{
            max-width: 44rem;
            margin-bottom: 1.15rem;
            color: var(--muted);
            line-height: 1.75;
        }}

        .meta-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.8rem;
            margin-top: 1.1rem;
        }}

        .metric-card, .feature-card, .note-card, .comment-card, .sidebar-card {{
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(215, 207, 190, 0.9);
            border-radius: var(--radius-md);
            box-shadow: 0 10px 28px rgba(22, 33, 51, 0.05);
        }}

        .metric-card {{
            padding: 1rem 1.1rem;
        }}

        .metric-label {{
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            color: var(--muted);
            text-transform: uppercase;
            font-weight: 700;
        }}

        .metric-value {{
            margin-top: 0.35rem;
            font-size: 1.6rem;
            font-weight: 700;
        }}

        .feature-card, .note-card, .comment-card {{
            padding: 1.25rem 1.2rem;
            height: 100%;
        }}

        .feature-title, .note-title {{
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin-bottom: 0.55rem;
            font-size: 1.4rem;
        }}

        .feature-summary, .note-summary, .comment-meta {{
            color: var(--muted);
            line-height: 1.7;
        }}

        .tag-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.8rem;
        }}

        .tag {{
            padding: 0.24rem 0.65rem;
            border-radius: 999px;
            background: rgba(15, 82, 186, 0.08);
            border: 1px solid rgba(15, 82, 186, 0.14);
            color: var(--ultramarine);
            font-size: 0.8rem;
            font-weight: 700;
        }}

        .sidebar-card {{
            padding: 1.1rem 1rem;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(247,244,237,0.85) 100%);
        }}

        .sidebar-photo {{
            width: 100%;
            border-radius: 22px;
            border: 1px solid rgba(215, 207, 190, 0.8);
            box-shadow: 0 16px 42px rgba(15, 82, 186, 0.08);
        }}

        .muted {{
            color: var(--muted);
        }}

        .section-spacer {{
            height: 0.8rem;
        }}

        .stButton > button, .stDownloadButton > button {{
            width: 100%;
            min-height: 2.9rem;
            border-radius: 999px;
            border: 1px solid rgba(15, 82, 186, 0.18);
            background: linear-gradient(180deg, rgba(15, 82, 186, 0.98) 0%, rgba(63, 136, 255, 0.95) 100%);
            color: white;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(15, 82, 186, 0.16);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }}

        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: rgba(15, 82, 186, 0.22);
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(15, 82, 186, 0.2);
        }}

        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            border-radius: 16px !important;
            border: 1px solid rgba(215, 207, 190, 0.95) !important;
            background: rgba(255,255,255,0.92) !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {{
            border-radius: 16px !important;
            border: 1px solid rgba(215, 207, 190, 0.95) !important;
            background: rgba(255,255,255,0.92) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.4rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 999px;
            background: rgba(255,255,255,0.7);
            border: 1px solid rgba(215, 207, 190, 0.85);
            padding: 0.45rem 0.95rem;
            min-height: 2.4rem;
        }}

        .stTabs [aria-selected="true"] {{
            background: rgba(15, 82, 186, 0.1);
            color: var(--ultramarine);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def transparent_plotly_layout(height: int = 520) -> dict[str, object]:
    return {
        "height": height,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
    }

