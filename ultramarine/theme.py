from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


PALETTE = {
    "ink": "#F7FBFF",
    "muted": "#9AA9C5",
    "line": "#223149",
    "paper": "#070A12",
    "panel": "#0D1424",
    "ultramarine": "#4D7CFF",
    "azure": "#38BDF8",
    "coral": "#FB7185",
    "jade": "#34D399",
    "gold": "#FBBF24",
    "violet": "#A78BFA",
}

COLORWAY = [
    PALETTE["ultramarine"],
    PALETTE["coral"],
    PALETTE["jade"],
    PALETTE["gold"],
    PALETTE["violet"],
    PALETTE["azure"],
]


def configure_plotly_theme() -> None:
    pio.templates["ultramarine"] = go.layout.Template(
        layout=go.Layout(
            colorway=COLORWAY,
            font={"family": "Inter, Space Grotesk, Segoe UI, sans-serif", "color": PALETTE["ink"]},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hoverlabel={
                "bgcolor": "#111827",
                "bordercolor": "#2F3B55",
                "font": {"family": "Inter, Space Grotesk, Segoe UI, sans-serif", "color": "#F7FBFF"},
            },
        )
    )
    pio.templates.default = "ultramarine"


def apply_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

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
            --violet: {PALETTE["violet"]};
            --glass: rgba(13, 20, 36, 0.72);
            --glass-strong: rgba(15, 23, 42, 0.86);
            --shadow: 0 24px 80px rgba(0, 0, 0, 0.34);
            --glow: 0 0 44px rgba(77, 124, 255, 0.24);
            --radius-lg: 30px;
            --radius-md: 20px;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 12% 12%, rgba(56, 189, 248, 0.18), transparent 30%),
                radial-gradient(circle at 86% 10%, rgba(167, 139, 250, 0.18), transparent 28%),
                radial-gradient(circle at 50% 100%, rgba(77, 124, 255, 0.14), transparent 34%),
                linear-gradient(180deg, #050812 0%, #08111F 46%, #05070D 100%);
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(180deg, rgba(0,0,0,0.62), transparent 78%);
            z-index: 0;
        }}

        .main .block-container {{
            position: relative;
            z-index: 1;
            max-width: 1240px;
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }}

        [data-testid="stHeader"] {{
            background: rgba(5, 8, 18, 0.72);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(8, 13, 25, 0.94) 0%, rgba(7, 10, 18, 0.98) 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.13);
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.2rem;
        }}

        body, p, li, div, label, span {{
            font-family: "Inter", "Space Grotesk", "Segoe UI", sans-serif;
            color: var(--ink);
        }}

        h1, h2, h3, h4 {{
            font-family: "Space Grotesk", "Inter", sans-serif !important;
            letter-spacing: -0.02em;
            color: var(--ink);
        }}

        code, pre {{
            font-family: "Fira Code", Consolas, monospace !important;
        }}

        .hero-shell {{
            position: relative;
            padding: clamp(1.35rem, 4vw, 3rem);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: var(--radius-lg);
            background:
                linear-gradient(135deg, rgba(15,23,42,0.94) 0%, rgba(13,20,36,0.72) 58%, rgba(77,124,255,0.18) 100%);
            box-shadow: var(--shadow);
            overflow: hidden;
            backdrop-filter: blur(18px);
        }}

        .hero-shell::after {{
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -120px;
            top: -140px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(56,189,248,0.26), transparent 68%);
        }}

        .hero-kicker {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            background: rgba(77, 124, 255, 0.14);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #BFE9FF;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .hero-title {{
            margin: 0.8rem 0 0.7rem;
            font-size: clamp(2.7rem, 5vw, 4.8rem);
            line-height: 0.92;
            background: linear-gradient(92deg, #FFFFFF 0%, #BFE9FF 46%, #A78BFA 100%);
            -webkit-background-clip: text;
            color: transparent;
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
            background: var(--glass);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
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

        .metric-detail {{
            margin-top: 0.35rem;
            color: var(--muted);
            font-size: 0.85rem;
        }}

        .feature-card, .note-card, .comment-card {{
            padding: 1.25rem 1.2rem;
            height: 100%;
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
        }}

        .feature-card:hover, .note-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(125, 211, 252, 0.34);
            box-shadow: var(--shadow), var(--glow);
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

        .card-kicker {{
            color: var(--azure);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
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
            background: rgba(77, 124, 255, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.18);
            color: #BFE9FF;
            font-size: 0.8rem;
            font-weight: 700;
        }}

        .sidebar-card {{
            padding: 1.1rem 1rem;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.88) 0%, rgba(8,13,25,0.76) 100%);
        }}

        .sidebar-photo {{
            width: 100%;
            border-radius: 22px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: var(--shadow);
        }}

        .muted {{
            color: var(--muted);
        }}

        .section-spacer {{
            height: 0.8rem;
        }}

        .chart-shell-title {{
            margin: 0.2rem 0 0.7rem;
            padding: 0.85rem 1rem;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.56);
            border: 1px solid rgba(148, 163, 184, 0.14);
        }}

        .chart-shell-title span {{
            font-weight: 800;
        }}

        .chart-caption {{
            margin: 0.25rem 0 0;
            color: var(--muted);
            font-size: 0.88rem;
        }}

        .insight-panel {{
            margin: 1rem 0 1.2rem;
            padding: 1.15rem 1.2rem;
            border-radius: var(--radius-md);
            border: 1px solid rgba(125, 211, 252, 0.18);
            background:
                radial-gradient(circle at top right, rgba(77, 124, 255, 0.16), transparent 42%),
                rgba(13, 20, 36, 0.72);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
        }}

        .insight-panel h3 {{
            margin: 0 0 0.8rem;
        }}

        .insight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 0.85rem;
        }}

        .insight-grid div {{
            padding: 0.85rem;
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.12);
            background: rgba(3, 7, 18, 0.34);
        }}

        .insight-grid span {{
            color: var(--azure);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .insight-grid p, .insight-panel li {{
            color: var(--muted);
            line-height: 1.7;
        }}

        .feed-header {{
            padding: 1rem 1.2rem;
            border-radius: var(--radius-md);
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: linear-gradient(135deg, rgba(15,23,42,0.84), rgba(77,124,255,0.12));
            margin: 1.2rem 0 0.8rem;
        }}

        .feed-header h3 {{
            margin: 0.1rem 0;
        }}

        .feed-header p {{
            margin: 0;
            color: var(--muted);
        }}

        .comment-body {{
            line-height: 1.75;
            color: var(--ink);
        }}

        .stMarkdown pre {{
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: rgba(3, 7, 18, 0.72) !important;
        }}

        .stButton > button, .stDownloadButton > button {{
            width: 100%;
            min-height: 2.9rem;
            border-radius: 999px;
            border: 1px solid rgba(125, 211, 252, 0.25);
            background: linear-gradient(135deg, rgba(77,124,255,0.98), rgba(56,189,248,0.88));
            color: white;
            font-weight: 700;
            box-shadow: 0 14px 34px rgba(37, 99, 235, 0.24);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }}

        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: rgba(191, 233, 255, 0.42);
            transform: translateY(-1px);
            box-shadow: 0 18px 42px rgba(37, 99, 235, 0.34);
        }}

        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            border-radius: 16px !important;
            border: 1px solid rgba(148, 163, 184, 0.22) !important;
            background: rgba(15,23,42,0.72) !important;
            color: var(--ink) !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {{
            border-radius: 16px !important;
            border: 1px solid rgba(148, 163, 184, 0.22) !important;
            background: rgba(15,23,42,0.72) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.4rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 999px;
            background: rgba(15,23,42,0.62);
            border: 1px solid rgba(148, 163, 184, 0.16);
            padding: 0.45rem 0.95rem;
            min-height: 2.4rem;
        }}

        .stTabs [aria-selected="true"] {{
            background: rgba(77, 124, 255, 0.18);
            color: #BFE9FF;
        }}

        iframe, canvas {{
            border-radius: var(--radius-md);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: var(--shadow);
        }}

        @media (max-width: 760px) {{
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .hero-title {{
                font-size: 2.45rem;
            }}

            .metric-card, .feature-card, .note-card, .comment-card {{
                padding: 1rem;
            }}
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
        "font": {"color": PALETTE["ink"]},
    }


def animation_button_menu(label: str, *, y: float = 1.05, duration: int = 70) -> list[dict[str, object]]:
    return [
        {
            "type": "buttons",
            "direction": "left",
            "showactive": False,
            "x": 0.5,
            "xanchor": "center",
            "y": y,
            "yanchor": "bottom",
            "bgcolor": "rgba(13, 20, 36, 0.92)",
            "bordercolor": "rgba(125, 211, 252, 0.34)",
            "borderwidth": 1,
            "font": {"color": "#E6F6FF", "size": 13},
            "pad": {"r": 12, "t": 8, "b": 8, "l": 12},
            "buttons": [
                {
                    "label": label,
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": duration, "redraw": True},
                            "transition": {"duration": max(20, duration // 2), "easing": "cubic-in-out"},
                            "fromcurrent": True,
                        },
                    ],
                }
            ],
        }
    ]

