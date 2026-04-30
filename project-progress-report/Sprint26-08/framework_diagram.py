"""Generate framework_architecture.png — release-notes / news-digest version.

Re-run with:
    .venv/Scripts/python framework_diagram.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# ---------- typography ----------
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Segoe UI",
    "Inter",
    "Helvetica Neue",
    "Arial",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False

# ---------- palette ----------
BG = "#FAFBFC"  # very subtle off-white canvas
INK = "#1A202C"
MUTED = "#4A5568"
LINE = "#A0AEC0"
SUBTLE = "#CBD5E0"

LAYER_FILLS = {
    "ci": "#EBF4FF",
    "tests": "#F0FFF4",
    "domain": "#FFFAF0",
    "infra": "#F4F6F9",
}
LAYER_EDGES = {
    "ci": "#3182CE",
    "tests": "#38A169",
    "domain": "#DD6B20",
    "infra": "#A0AEC0",
}
ACCENT_NEW = "#D43F3A"  # marks the REST API path (this sprint)
ALLURE_EDGE = "#D69E2E"  # mustard — Allure / reporting
HERO_BLUE = "#3182CE"
HERO_GREEN = "#38A169"

# ---------- effects ----------
SHADOW_SOFT = patheffects.withSimplePatchShadow(
    offset=(2.5, -2.5),
    shadow_rgbFace="#0B1F3F",
    alpha=0.10,
)
SHADOW_HERO = patheffects.withSimplePatchShadow(
    offset=(3, -3),
    shadow_rgbFace="#0B1F3F",
    alpha=0.13,
)


# ----------------------------------------------------------------------------
# primitives
# ----------------------------------------------------------------------------


def card(
    ax,
    x,
    y,
    w,
    h,
    title,
    lines,
    *,
    edge=MUTED,
    fill="white",
    title_color=None,
    badge=None,
    title_size=11,
    body_size=9,
):
    """Card with drop shadow, accent ribbon at top, title and even body lines."""
    # Drop-shadow card
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.16",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=fill,
        zorder=2,
    )
    box.set_path_effects([SHADOW_SOFT])
    ax.add_patch(box)

    # Top accent ribbon — thin coloured stripe along the top edge
    ribbon_h = 0.12
    ax.add_patch(
        FancyBboxPatch(
            (x + 0.10, y + h - ribbon_h - 0.04),
            w - 0.20,
            ribbon_h,
            boxstyle="round,pad=0,rounding_size=0.06",
            linewidth=0,
            facecolor=edge,
            alpha=0.18,
            zorder=3,
        )
    )

    # Title
    ax.text(
        x + w / 2,
        y + h - 0.30,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=title_color or edge,
        zorder=4,
    )

    if badge:
        ax.text(
            x + w - 0.18,
            y + h - 0.16,
            badge,
            ha="right",
            va="top",
            fontsize=7.5,
            fontweight="bold",
            color="white",
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.30", fc=ACCENT_NEW, ec="none"),
        )

    n = len(lines)
    if n == 0:
        return

    body_top = y + h - 0.65
    body_bottom = y + 0.22
    if n == 1:
        ys = [(body_top + body_bottom) / 2]
    else:
        step = (body_top - body_bottom) / (n - 1)
        ys = [body_top - i * step for i in range(n)]

    for line, ly in zip(lines, ys):
        ax.text(
            x + w / 2,
            ly,
            line,
            ha="center",
            va="center",
            fontsize=body_size,
            color=INK,
            zorder=4,
        )


def band(ax, x, y, w, h, label, fill, edge, *, label_color="white"):
    """Layer band with a pill-style label sitting in the gap above."""
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.20",
        linewidth=0.8,
        edgecolor=edge,
        facecolor=fill,
        alpha=0.65,
        zorder=1,
    )
    ax.add_patch(rect)

    # Pill-style label — white text on coloured background, sits above band
    ax.text(
        x + 0.30,
        y + h + 0.20,
        label,
        ha="left",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color=label_color,
        bbox=dict(
            boxstyle="round,pad=0.42",
            fc=edge,
            ec="none",
        ),
        zorder=6,
    )


def arrow(ax, x1, y1, x2, y2, *, color=LINE, width=1.5, style="-|>", scale=16):
    a = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle=style,
        mutation_scale=scale,
        linewidth=width,
        color=color,
        shrinkA=2,
        shrinkB=2,
        zorder=3,
    )
    ax.add_patch(a)


def kpi_tile(ax, x, y, w, h, value, label_top, label_bottom, accent):
    """Hero tile: large numeral with a 2-line caption + drop shadow."""
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.24",
        linewidth=2.0,
        edgecolor=accent,
        facecolor="white",
        zorder=2,
    )
    box.set_path_effects([SHADOW_HERO])
    ax.add_patch(box)

    # Subtle inner accent stripe along the bottom of the tile
    ax.add_patch(
        Rectangle(
            (x + 0.12, y + 0.10),
            w - 0.24,
            0.06,
            facecolor=accent,
            edgecolor="none",
            alpha=0.85,
            zorder=3,
        )
    )

    ax.text(
        x + w / 2,
        y + h - 0.26,
        value,
        ha="center",
        va="top",
        fontsize=46,
        fontweight="bold",
        color=accent,
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + 0.62,
        label_top,
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color=INK,
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + 0.34,
        label_bottom,
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=MUTED,
        style="italic",
        zorder=4,
    )


def before_after_tile(ax, x, y, w, h):
    """Sprint headline — Katalon → pytest, with case count + drop shadow."""
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.24",
        linewidth=2.0,
        edgecolor=ACCENT_NEW,
        facecolor="#FFF7F6",
        zorder=2,
    )
    box.set_path_effects([SHADOW_HERO])
    ax.add_patch(box)

    # Header pill
    ax.text(
        x + w / 2,
        y + h - 0.20,
        "SPRINT HEADLINE",
        ha="center",
        va="top",
        fontsize=8,
        fontweight="bold",
        color="white",
        zorder=4,
        bbox=dict(boxstyle="round,pad=0.30", fc=ACCENT_NEW, ec="none"),
    )

    pill_y = y + 0.78
    pill_h = 0.55
    inner_pad = 0.20
    arrow_gap = 0.55
    pill_w = (w - 2 * inner_pad - arrow_gap) / 2

    # Katalon pill (left, muted)
    px1 = x + inner_pad
    ax.add_patch(
        FancyBboxPatch(
            (px1, pill_y),
            pill_w,
            pill_h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=1.0,
            edgecolor=MUTED,
            facecolor="#EDF2F7",
            zorder=3,
        )
    )
    ax.text(
        px1 + pill_w / 2,
        pill_y + pill_h / 2 + 0.07,
        "Katalon",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=MUTED,
        zorder=4,
    )
    ax.text(
        px1 + pill_w / 2,
        pill_y + pill_h / 2 - 0.13,
        "Groovy",
        ha="center",
        va="center",
        fontsize=7.8,
        color=MUTED,
        style="italic",
        zorder=4,
    )

    # Arrow
    ay = pill_y + pill_h / 2
    arrow(
        ax,
        px1 + pill_w + 0.05,
        ay,
        px1 + pill_w + arrow_gap - 0.05,
        ay,
        color=ACCENT_NEW,
        width=2.4,
        scale=18,
    )

    # pytest pill (right, accent, white background)
    px2 = px1 + pill_w + arrow_gap
    ax.add_patch(
        FancyBboxPatch(
            (px2, pill_y),
            pill_w,
            pill_h,
            boxstyle="round,pad=0.02,rounding_size=0.10",
            linewidth=1.6,
            edgecolor=ACCENT_NEW,
            facecolor="white",
            zorder=3,
        )
    )
    ax.text(
        px2 + pill_w / 2,
        pill_y + pill_h / 2 + 0.07,
        "pytest",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=ACCENT_NEW,
        zorder=4,
    )
    ax.text(
        px2 + pill_w / 2,
        pill_y + pill_h / 2 - 0.13,
        "+ Python",
        ha="center",
        va="center",
        fontsize=7.8,
        color=ACCENT_NEW,
        style="italic",
        zorder=4,
    )

    # Bottom captions
    ax.text(
        x + w / 2,
        y + 0.46,
        "REST API suite migrated",
        ha="center",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
        color=INK,
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + 0.22,
        "9 modules  ·  267 test cases",
        ha="center",
        va="bottom",
        fontsize=8.5,
        color=ACCENT_NEW,
        style="italic",
        zorder=4,
    )


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------


def main() -> None:
    fig, ax = plt.subplots(figsize=(16, 14), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(1.05, 14)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---------- top accent rule ----------
    ax.add_patch(
        Rectangle(
            (0, 13.85),
            16,
            0.05,
            facecolor=ACCENT_NEW,
            edgecolor="none",
            alpha=0.85,
            zorder=2,
        )
    )

    # ---------- header ----------
    ax.text(
        8,
        13.50,
        "vc-testing-module — Release Highlights",
        ha="center",
        fontsize=22,
        fontweight="bold",
        color=INK,
        zorder=4,
    )
    ax.text(
        8,
        13.13,
        "Sprint ending 2026-04-29   ·   404 active test cases   ·   "
        "Python 3.13 · pytest 9 · Playwright 1.58 · Pydantic 2 · Allure",
        ha="center",
        fontsize=10,
        color=MUTED,
        style="italic",
        zorder=4,
    )

    # ---------- HERO KPI strip ----------
    hero_y = 11.20
    hero_h = 1.75
    tiles = [
        # x,    w,    value,  label_top,                 label_bottom,                          accent
        (0.40, 3.55, "300+", "REST API cases migrated", "from Katalon Studio", ACCENT_NEW),
        (4.15, 3.55, "1", "Unified CI workflow", "auto-tests.yml · workflow_dispatch", HERO_BLUE),
        (7.90, 3.55, "3", "Test suites, one stack", "E2E · GraphQL · REST API", HERO_GREEN),
    ]
    for tx, tw, value, lt, lb, accent in tiles:
        kpi_tile(ax, tx, hero_y, tw, hero_h, value, lt, lb, accent)
    before_after_tile(ax, 11.65, hero_y, 3.95, hero_h)

    # ---------- Layer 1: CI / CD ----------
    band(
        ax,
        0.4,
        8.85,
        15.2,
        1.85,
        "CI / CD   ·   .github/workflows/auto-tests.yml",
        LAYER_FILLS["ci"],
        LAYER_EDGES["ci"],
    )
    card(
        ax,
        0.9,
        8.97,
        9.7,
        1.61,
        "Auto Tests Docker",
        [
            "workflow_dispatch  ·  manual trigger",
            "testSuites:  all  ·  graphql  ·  restapi  ·  e2e",
            "frontendZipUrl input  (default: latest)",
            "Reusable: VirtoCommerce/.github  ·  pytest-tests.yml @ v3.800.30",
            "Backend packages pinned via backend-packages.json",
        ],
        edge=LAYER_EDGES["ci"],
    )
    card(
        ax,
        10.8,
        8.97,
        4.4,
        1.61,
        "Allure Report",
        [
            "pytest --alluredir=allure-results",
            "Aggregated across all 3 suites",
            "Trends · history · attachments",
            "HAR · screenshots · request logs",
            "Drill-down per test, marker, suite",
        ],
        edge=ALLURE_EDGE,
    )
    arrow(ax, 10.6, 9.78, 10.8, 9.78, color=ALLURE_EDGE, width=1.8, scale=14)

    # ---------- Layer 2: Test Suites ----------
    band(
        ax,
        0.4,
        6.20,
        15.2,
        2.10,
        "Tests   ·   pytest markers: e2e · graphql · restapi",
        LAYER_FILLS["tests"],
        LAYER_EDGES["tests"],
    )
    card(
        ax,
        0.9,
        6.32,
        4.6,
        1.86,
        "E2E (Playwright UI)",
        ["50 active cases  ·  22 files", "cart · checkout · sign-in", "filters · i18n · pickup"],
        edge=LAYER_EDGES["tests"],
    )
    card(
        ax,
        5.7,
        6.32,
        4.6,
        1.86,
        "GraphQL (Storefront API)",
        ["87 active cases  ·  45 files", "cart · orders · quotes", "wishlist · contacts · seo"],
        edge=LAYER_EDGES["tests"],
    )
    card(
        ax,
        10.5,
        6.32,
        4.6,
        1.86,
        "REST API (Platform Admin)",
        ["267 active cases  ·  38 files", "platform · catalog · orders", "marketing · pricing · contacts"],
        edge=ACCENT_NEW,
        badge="NEW",
    )

    # ---------- Layer 3: Domain Layer ----------
    band(
        ax,
        0.4,
        3.55,
        15.2,
        2.10,
        "Domain Layer   ·   typed operations & UI model",
        LAYER_FILLS["domain"],
        LAYER_EDGES["domain"],
    )
    card(
        ax,
        0.9,
        3.67,
        4.6,
        1.86,
        "page_objects/",
        ["43 Python files", "10 pages · 29 components", "shared layouts"],
        edge=LAYER_EDGES["domain"],
    )
    card(
        ax,
        5.7,
        3.67,
        4.6,
        1.86,
        "gql/",
        ["13 operation classes", "42 .graphql fragments", "30+ Pydantic types"],
        edge=LAYER_EDGES["domain"],
    )
    card(
        ax,
        10.5,
        3.67,
        4.6,
        1.86,
        "restapi/",
        ["24 operation classes", "15 Pydantic type modules", "RestBaseOperations"],
        edge=ACCENT_NEW,
        badge="NEW",
    )

    # ---------- Layer 4: Shared Infrastructure (proper cards) ----------
    band(
        ax,
        0.4,
        1.15,
        15.2,
        1.85,
        "Shared Infrastructure   ·   core/  ·  dataset/  ·  utils/",
        LAYER_FILLS["infra"],
        LAYER_EDGES["infra"],
        label_color="white",
    )
    card(
        ax,
        0.50,
        1.27,
        3.55,
        1.61,
        "core/  —  Auth & Clients",
        [
            "AuthProvider · TokenInfo",
            "RestClient · GraphQLClient",
            "Per-suite admin auth",
            "ariadne-codegen typed client",
        ],
        edge=LAYER_EDGES["infra"],
    )
    card(
        ax,
        4.25,
        1.27,
        3.55,
        1.61,
        "dataset/  —  Seeder",
        [
            "DatasetManager · DatasetSeeder",
            "Topological sort by parent ref",
            "Manifest-driven  ·  5 HTTP verbs",
            "1 155 JSON  ·  27 entity types",
        ],
        edge=LAYER_EDGES["infra"],
    )
    card(
        ax,
        8.00,
        1.27,
        3.55,
        1.61,
        "core/logger/  —  Rich",
        [
            "RichLogger · NullLogger",
            "TRACE / DEBUG / INFO / WARN / ERROR",
            "Rich tracebacks  ·  markup colours",
            "Console + plain-text log file",
        ],
        edge=LAYER_EDGES["infra"],
    )
    card(
        ax,
        11.75,
        1.27,
        3.55,
        1.61,
        "utils/  —  Helpers",
        [
            "polling_utils  (poll_until)",
            "har_recorder  (per-test HAR)",
            "address_utils · line_item_utils",
            "Allure attachments",
        ],
        edge=LAYER_EDGES["infra"],
    )

    # ---------- Vertical arrows ----------
    for x in (3.2, 8.0, 12.8):
        arrow(ax, x, 8.97, x, 8.18)  # CI → Tests
        arrow(ax, x, 6.32, x, 5.53)  # Tests → Domain
    for x in (5.5, 10.5):
        arrow(ax, x, 3.67, x, 3.05)  # Domain → Foundation

    out = "framework_architecture.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
