"""Exercise parameter changes, including previously failing empty and extreme states."""

import pytest
from streamlit.testing.v1 import AppTest

from ultramarine.content import FEATURE_CARDS


def page(name: str) -> AppTest:
    return AppTest.from_file(f"tests/smoke_apps/{name}_app.py", default_timeout=15).run()


def test_home_registry_links_match_navigation() -> None:
    app = AppTest.from_file("app.py", default_timeout=15).run()
    assert not app.exception
    assert set(app.session_state["_page_registry"]) == {
        "home",
        *(card.path for card in FEATURE_CARDS),
    }
    links = app.get("page_link")
    assert len(links) == len(FEATURE_CARDS)
    assert len({link.proto.page_script_hash for link in links}) == len(FEATURE_CARDS)


def test_notes_empty_tag_intersection_and_recovery() -> None:
    app = page("notes")
    app.multiselect(key="notes_selected_tags").set_value(["数论", "测度论"]).run()
    assert not app.exception
    assert "没有同时匹配" in app.info[0].value
    app.multiselect(key="notes_selected_tags").set_value(["数论"]).run()
    assert not app.exception
    assert len(app.selectbox[0].options) == 1


def test_inference_skewed_distribution_and_seed_replay() -> None:
    app = page("data_lab")
    app.selectbox(key="inference_distribution").set_value("exponential")
    app.slider(key="inference_n").set_value(2).run()
    assert not app.exception
    assert "仅为近似" in app.info[0].value
    coverage = app.metric[1].value
    app.number_input(key="inference_seed").set_value(43).run()
    assert not app.exception
    app.number_input(key="inference_seed").set_value(42).run()
    assert app.metric[1].value == coverage


def test_regression_ridge_and_unstable_rate() -> None:
    app = page("data_lab")
    app.slider(key="regression_penalty").set_value(3.0).run()
    assert not app.exception
    assert float(app.metric[5].value) < 0.001
    app.slider(key="regression_rate").set_value(1.2)
    app.slider(key="regression_steps").set_value(300).run()
    assert not app.exception
    assert "振荡或发散" in app.warning[0].value


@pytest.mark.parametrize("probability", [0.0, 1.0])
def test_galton_probability_endpoints(probability: float) -> None:
    app = page("interactive")
    app.slider(key="galton_probability").set_value(probability).run()
    assert not app.exception
    table = app.table[0].value
    assert table["模拟"].iloc[1] == 0
    assert table["模拟"].iloc[2] == 1000


@pytest.mark.parametrize("name", ["power", "inverse_affine", "exponential", "mobius"])
def test_all_complex_mappings_render_with_parameter_changes(name: str) -> None:
    app = page("complex_lab")
    app.selectbox(key="complex_map_name").set_value(name)
    app.slider(key="complex_scale_real").set_value(2.0).run()
    assert not app.exception
    assert len(app.get("plotly_chart")) == 2


def test_fractal_zoom_and_highest_iteration_budget() -> None:
    app = page("fractals")
    app.selectbox(key="fractal_zoom").set_value("seahorse")
    app.slider(key="fractal_iter").set_value(180).run()
    assert not app.exception
