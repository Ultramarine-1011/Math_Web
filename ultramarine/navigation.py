from __future__ import annotations

import streamlit as st

from ultramarine.features import animations, community, gallery, home, interactive, notes
from ultramarine.models import AppSettings


def _page(
    renderer,
    settings: AppSettings,
    *,
    title: str,
    icon: str,
    url_path: str,
    default: bool = False,
):
    return st.Page(
        lambda renderer=renderer: renderer.render(settings),
        title=title,
        icon=icon,
        url_path=url_path,
        default=default,
    )


def build_navigation(settings: AppSettings):
    pages = {
        "home": _page(home, settings, title="首页", icon=":material/home:", url_path="home", default=True),
        "interactive-lab": _page(
            interactive,
            settings,
            title="互动实验室",
            icon=":material/science:",
            url_path="interactive-lab",
        ),
        "gallery": _page(gallery, settings, title="数学画廊", icon=":material/auto_awesome:", url_path="gallery"),
        "animations": _page(
            animations,
            settings,
            title="数学动画",
            icon=":material/animation:",
            url_path="animations",
        ),
        "notes": _page(notes, settings, title="笔记资料", icon=":material/menu_book:", url_path="notes"),
        "community": _page(
            community,
            settings,
            title="交流广场",
            icon=":material/forum:",
            url_path="community",
        ),
    }
    current_page = st.navigation(
        {
            "总览": [pages["home"]],
            "探索": [pages["interactive-lab"], pages["gallery"], pages["animations"]],
            "资料与交流": [pages["notes"], pages["community"]],
        },
        position="top",
    )
    return current_page, pages