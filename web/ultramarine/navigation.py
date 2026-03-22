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
        "home": _page(home, settings, title="Home", icon=":material/home:", url_path="home", default=True),
        "interactive-lab": _page(
            interactive,
            settings,
            title="Interactive Lab",
            icon=":material/science:",
            url_path="interactive-lab",
        ),
        "gallery": _page(gallery, settings, title="Gallery", icon=":material/auto_awesome:", url_path="gallery"),
        "animations": _page(
            animations,
            settings,
            title="Animations",
            icon=":material/animation:",
            url_path="animations",
        ),
        "notes": _page(notes, settings, title="Notes", icon=":material/menu_book:", url_path="notes"),
        "community": _page(
            community,
            settings,
            title="Community",
            icon=":material/forum:",
            url_path="community",
        ),
    }
    current_page = st.navigation(
        {
            "Overview": [pages["home"]],
            "Explore": [pages["interactive-lab"], pages["gallery"], pages["animations"]],
            "Library": [pages["notes"], pages["community"]],
        },
        position="top",
    )
    return current_page, pages
