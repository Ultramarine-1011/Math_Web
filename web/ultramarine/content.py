from __future__ import annotations

from dataclasses import dataclass


SITE_BLURB = (
    "A public-facing mathematics studio that combines visual essays, lecture notes,"
    " experiments, and a lightweight community board."
)

HOME_INTRO = (
    "The rebuilt site turns a collection of independent demos into a coherent mathematics portfolio."
    " Visualizations, notes, animations, and discussions now share one production-ready shell."
)


@dataclass(frozen=True, slots=True)
class FeatureCard:
    title: str
    icon: str
    path: str
    summary: str
    detail: str


FEATURE_CARDS = (
    FeatureCard(
        title="Interactive Lab",
        icon="LAB",
        path="interactive-lab",
        summary="Fourier drawing, gradient descent, and random simulation in one place.",
        detail="The page keeps the original mathematical ideas, but the implementation is now easier to extend.",
    ),
    FeatureCard(
        title="Gallery",
        icon="GAL",
        path="gallery",
        summary="A curated visual gallery for dynamical systems and iconic algebraic curves.",
        detail="Static exhibits now share one visual language and one chart stack.",
    ),
    FeatureCard(
        title="Animations",
        icon="ANM",
        path="animations",
        summary="Linear algebra and geometry presented as continuous motion rather than snapshots.",
        detail="The focus is on transformation and intuition, not only the final result.",
    ),
    FeatureCard(
        title="Notes",
        icon="PDF",
        path="notes",
        summary="A structured note library driven by PDF files and a catalog manifest.",
        detail="Each note can now carry tags, summaries, and featured ordering.",
    ),
    FeatureCard(
        title="Community",
        icon="MSG",
        path="community",
        summary="A small but durable discussion board for comments and appreciation.",
        detail="It supports either local JSON storage or a Supabase backend for deployment.",
    ),
)


PAGE_DESCRIPTIONS = {
    "home": "The public landing page for the rebuilt site.",
    "interactive": "An experiment-driven space for mathematical interaction.",
    "gallery": "A browseable visual gallery for mathematical forms.",
    "animations": "A motion-focused page for continuous transformations.",
    "notes": "A searchable and previewable notes library.",
    "community": "A lightweight, deployment-friendly discussion area.",
}