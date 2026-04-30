"""Generate test coverage report PNG charts from sprint data.

Usage:
    python project-progress-report/generate_charts.py Sprint26-03
    python project-progress-report/generate_charts.py Sprint26-02 --theme light

Each sprint directory must contain a sprint_data.json file.
Charts are saved to <sprint_dir>/charts/.
"""

import argparse
import json
import os
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# ── Theme presets ──────────────────────────────────────────────

THEMES = {
    "dark": {
        "style": "dark_background",
        "bg": "#1a1a2e",
        "card_bg": "#1a1a2e",
        "text": "white",
        "gray": "#95a5a6",
        "primary": "#0f3460",
        "secondary": "#e94560",
        "accent1": "#00b4d8",
        "accent2": "#48cae4",
        "green": "#2ecc71",
        "orange": "#f39c12",
        "edge": "#1a1a2e",
        "grid_alpha": 0.2,
        "legend_alpha": 0.3,
        "bar_prev_alpha": 0.6,
        "fill_alpha": 0.15,
        "marker_edge": "white",
        "bar_on_text": "white",
    },
    "light": {
        "style": None,
        "bg": "#FAFBFC",
        "card_bg": "#FFFFFF",
        "text": "#1E293B",
        "gray": "#6B7280",
        "primary": "#2563EB",
        "secondary": "#DC2626",
        "accent1": "#2563EB",
        "accent2": "#93C5FD",
        "green": "#16A34A",
        "orange": "#EA580C",
        "edge": "white",
        "grid_alpha": 0.3,
        "legend_alpha": 0.9,
        "bar_prev_alpha": 0.7,
        "fill_alpha": 0.12,
        "marker_edge": "white",
        "bar_on_text": "white",
    },
}

DPI = 180


# ── Helpers ────────────────────────────────────────────────────


def load_data(sprint_dir):
    """Load sprint_data.json from the given directory."""
    path = os.path.join(sprint_dir, "sprint_data.json")
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_theme(data, override=None):
    """Resolve the color theme."""
    name = override or data.get("theme", "dark")
    if name not in THEMES:
        print(f"Warning: unknown theme '{name}', falling back to 'dark'.")
        name = "dark"
    return THEMES[name]


def setup_style(theme):
    """Apply matplotlib style."""
    if theme["style"]:
        plt.style.use(theme["style"])
    else:
        plt.style.use("default")


def save(fig, out_dir, name, theme):
    """Save figure and print progress."""
    path = os.path.join(out_dir, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [OK] {name}")


def style_axes(ax, theme):
    """Apply common axis styling."""
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["bottom"].set_color(theme["gray"])
    ax.spines["left"].set_color(theme["gray"])
    ax.tick_params(colors=theme["text"])


def compute_changes(prev_vals, curr_vals):
    """Compute formatted change strings between two value lists."""
    changes = []
    for p, c in zip(prev_vals, curr_vals):
        diff = c - p
        if diff > 0:
            changes.append(f"+{diff}")
        elif diff < 0:
            changes.append(str(diff))
        else:
            changes.append("0")
    return changes


def auto_ylim(values, padding_ratio=0.25):
    """Compute a y-limit with reasonable padding."""
    max_val = max(values) if values else 100
    return max_val * (1 + padding_ratio)


def resolve_color(name, theme):
    """Map a color name like 'accent1' to the theme hex value, or pass through raw hex."""
    return theme.get(name, name)


# ── Chart generators ───────────────────────────────────────────


def chart_test_growth_trend(data, theme, out_dir):
    """1. Test Growth Trend (Line Chart)."""
    trend = data["trend"]
    dates = trend["dates"]
    total = trend["total_tests"]
    active = trend["active_tests"]
    sprint = data["sprint_name"]
    T = theme

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=T["bg"])
    ax.set_facecolor(T["bg"])

    x = np.arange(len(dates))
    ax.fill_between(x, active, alpha=T["fill_alpha"], color=T["accent1"])

    ax.plot(
        x,
        total,
        "o-",
        color=T["accent1"],
        linewidth=3,
        markersize=12,
        label="Total Tests",
        zorder=5,
        markerfacecolor=T["accent1"],
        markeredgecolor=T["marker_edge"],
        markeredgewidth=1.5,
    )
    ax.plot(
        x,
        active,
        "s--",
        color=T["green"],
        linewidth=3,
        markersize=12,
        label="Active Tests",
        zorder=5,
        markerfacecolor=T["green"],
        markeredgecolor=T["marker_edge"],
        markeredgewidth=1.5,
    )

    for i, (t, a) in enumerate(zip(total, active)):
        ax.annotate(
            str(t),
            (i, t),
            textcoords="offset points",
            xytext=(0, 18),
            ha="center",
            fontsize=14,
            fontweight="bold",
            color=T["accent1"],
        )
        if a != t:
            ax.annotate(
                str(a), (i, a), textcoords="offset points", xytext=(0, -22), ha="center", fontsize=13, color=T["green"]
            )

    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=13, color=T["text"])
    ax.set_ylabel("Number of Tests", fontsize=14, color=T["text"])
    ax.set_title(f"Test Growth Trend \u2014 {sprint}", fontsize=20, fontweight="bold", pad=16, color=T["text"])
    ax.legend(loc="upper left", fontsize=12, framealpha=T["legend_alpha"], facecolor=T["bg"], edgecolor=T["gray"])
    ax.set_ylim(min(active) * 0.65, max(total) * 1.18)
    ax.grid(axis="y", alpha=T["grid_alpha"], color=T["gray"])
    style_axes(ax, T)

    save(fig, out_dir, "1_test_growth_trend.png", T)


def chart_period_comparison(data, theme, out_dir):
    """2. Period Comparison Overview (Horizontal Bar Chart)."""
    curr = data["current"]["total"]
    prev = data["previous"]["total"]
    sprint = data["sprint_name"]
    prev_sprint = data["previous"]["sprint_name"]
    T = theme

    metrics_labels = ["Test Files", "Test Functions", "Active Tests", "Ignored Tests"]
    vals_prev = [prev["files"], prev["functions"], prev["active"], prev["ignored"]]
    vals_curr = [curr["files"], curr["functions"], curr["active"], curr["ignored"]]
    changes = compute_changes(vals_prev, vals_curr)

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=T["bg"])
    ax.set_facecolor(T["bg"])

    y_pos = np.arange(len(metrics_labels))
    bar_h = 0.35
    bar_colors_curr = [T["accent1"], T["accent1"], T["green"], T["secondary"]]

    bars1 = ax.barh(
        y_pos + bar_h / 2,
        vals_prev,
        bar_h,
        label=prev_sprint,
        color=T["accent2"],
        edgecolor=T["edge"],
        linewidth=1.5,
        alpha=T["bar_prev_alpha"],
    )
    bars2 = ax.barh(
        y_pos - bar_h / 2, vals_curr, bar_h, label=sprint, color=bar_colors_curr, edgecolor=T["edge"], linewidth=1.5
    )

    for i, (b1, b2, ch) in enumerate(zip(bars1, bars2, changes)):
        ax.text(
            b1.get_width() + 2,
            b1.get_y() + b1.get_height() / 2,
            str(vals_prev[i]),
            va="center",
            fontsize=12,
            color=T["gray"],
        )
        color = T["green"] if ch.startswith("+") else T["secondary"] if ch != "0" else T["gray"]
        ax.text(
            b2.get_width() + 2,
            b2.get_y() + b2.get_height() / 2,
            f"{vals_curr[i]}  ({ch})",
            va="center",
            fontsize=13,
            fontweight="bold",
            color=color,
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics_labels, fontsize=14, color=T["text"])
    ax.set_title(f"Period Comparison Overview \u2014 {sprint}", fontsize=20, fontweight="bold", pad=16, color=T["text"])
    ax.legend(loc="lower right", fontsize=12, framealpha=T["legend_alpha"], facecolor=T["bg"], edgecolor=T["gray"])
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals_curr + vals_prev) * 1.3)
    ax.grid(axis="x", alpha=T["grid_alpha"], color=T["gray"])
    style_axes(ax, T)

    save(fig, out_dir, "2_period_comparison_overview.png", T)


def chart_active_vs_ignored(data, theme, out_dir):
    """3. Active vs Ignored Tests (Stacked Bar Chart)."""
    curr = data["current"]["total"]
    prev = data["previous"]["total"]
    sprint = data["sprint_name"]
    prev_sprint = data["previous"]["sprint_name"]
    T = theme

    categories = [prev_sprint, sprint]
    active_vals = [prev["active"], curr["active"]]
    ignored_vals = [prev["ignored"], curr["ignored"]]
    active_pct = [
        prev["active"] / prev["functions"] * 100,
        curr["active"] / curr["functions"] * 100,
    ]

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=T["bg"])
    ax.set_facecolor(T["bg"])

    x = np.arange(len(categories))
    ax.bar(x, active_vals, 0.5, label="Active", color=T["green"], edgecolor=T["edge"], linewidth=2)
    ax.bar(
        x,
        ignored_vals,
        0.5,
        bottom=active_vals,
        label="Ignored",
        color=T["secondary"],
        edgecolor=T["edge"],
        linewidth=2,
    )

    for i, (a, ig, pct) in enumerate(zip(active_vals, ignored_vals, active_pct)):
        ax.text(
            i,
            a / 2,
            f"{a}\n({pct:.1f}%)",
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=T["bar_on_text"],
        )
        ax.text(
            i, a + ig / 2, str(ig), ha="center", va="center", fontsize=13, fontweight="bold", color=T["bar_on_text"]
        )

    rate_change = active_pct[1] - active_pct[0]
    sign = "+" if rate_change >= 0 else ""
    top_val = max(a + ig for a, ig in zip(active_vals, ignored_vals))
    ax.annotate(
        f"{sign}{rate_change:.1f}% active rate",
        xy=(1, curr["active"] + curr["ignored"]),
        xytext=(0.15, top_val * 1.07),
        fontsize=14,
        fontweight="bold",
        color=T["green"],
        arrowprops=dict(arrowstyle="->", color=T["green"], lw=2.5),
        ha="center",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=13, color=T["text"])
    ax.set_ylabel("Number of Tests", fontsize=14, color=T["text"])
    ax.set_title(f"Active vs Ignored Tests \u2014 {sprint}", fontsize=20, fontweight="bold", pad=16, color=T["text"])
    ax.legend(fontsize=12, framealpha=T["legend_alpha"], facecolor=T["bg"], edgecolor=T["gray"])
    ax.set_ylim(0, top_val * 1.15)
    ax.grid(axis="y", alpha=T["grid_alpha"], color=T["gray"])
    style_axes(ax, T)

    save(fig, out_dir, "3_active_vs_ignored.png", T)


def chart_distribution_donut(data, theme, out_dir):
    """4. Test Distribution by Type (Donut Chart)."""
    curr = data["current"]
    sprint = data["sprint_name"]
    T = theme

    e2e_count = curr["e2e"]["functions"]
    gql_count = curr["graphql"]["functions"]
    total = e2e_count + gql_count

    fig, ax = plt.subplots(figsize=(10, 10), facecolor=T["bg"])

    wedges, texts, autotexts = ax.pie(
        [e2e_count, gql_count],
        labels=[f"E2E Tests\n({e2e_count})", f"GraphQL Tests\n({gql_count})"],
        autopct="%1.1f%%",
        colors=[T["secondary"], T["accent1"]],
        startangle=90,
        pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor=T["edge"], linewidth=3),
        textprops=dict(fontsize=15, color=T["text"]),
    )
    for at in autotexts:
        at.set_fontsize(15)
        at.set_fontweight("bold")
        at.set_color(T["bar_on_text"])

    ax.text(0, 0.06, str(total), ha="center", va="center", fontsize=40, fontweight="bold", color=T["text"])
    ax.text(0, -0.12, "Total", ha="center", va="center", fontsize=16, color=T["gray"])
    ax.set_title(f"Test Distribution by Type \u2014 {sprint}", fontsize=20, fontweight="bold", pad=20, color=T["text"])

    save(fig, out_dir, "4_test_distribution_donut.png", T)


def _chart_type_comparison(label, curr_data, prev_data, bar_color, theme, sprint, prev_sprint, out_dir, filename):
    """Shared logic for E2E and GraphQL comparison charts."""
    T = theme
    metrics = ["Files", "Functions", "Active", "Ignored"]
    vals_prev = [prev_data["files"], prev_data["functions"], prev_data["active"], prev_data["ignored"]]
    vals_curr = [curr_data["files"], curr_data["functions"], curr_data["active"], curr_data["ignored"]]

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=T["bg"])
    ax.set_facecolor(T["bg"])

    x = np.arange(len(metrics))
    w = 0.35
    ax.bar(
        x - w / 2, vals_prev, w, label=prev_sprint, color=T["accent2"], edgecolor=T["edge"], alpha=T["bar_prev_alpha"]
    )
    ax.bar(x + w / 2, vals_curr, w, label=sprint, color=bar_color, edgecolor=T["edge"])

    for i, (v1, v2) in enumerate(zip(vals_prev, vals_curr)):
        ax.text(i - w / 2, v1 + 1.5, str(v1), ha="center", fontsize=12, color=T["gray"])
        diff = v2 - v1
        sign = "+" if diff > 0 else ""
        color = T["green"] if diff > 0 else T["secondary"] if diff < 0 else T["gray"]
        suffix = f"\n({sign}{diff})" if diff != 0 else ""
        ax.text(i + w / 2, v2 + 1.5, f"{v2}{suffix}", ha="center", fontsize=12, fontweight="bold", color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=13, color=T["text"])
    ax.set_ylabel("Count", fontsize=14, color=T["text"])
    ax.set_title(f"{label} Tests \u2014 Period Comparison", fontsize=20, fontweight="bold", pad=16, color=T["text"])
    ax.legend(loc="upper left", fontsize=12, framealpha=T["legend_alpha"], facecolor=T["bg"], edgecolor=T["gray"])
    ax.set_ylim(0, auto_ylim(vals_curr + vals_prev))
    ax.grid(axis="y", alpha=T["grid_alpha"], color=T["gray"])
    style_axes(ax, T)

    save(fig, out_dir, filename, T)


def chart_e2e_comparison(data, theme, out_dir):
    """5. E2E Tests - Period Comparison."""
    _chart_type_comparison(
        "E2E",
        data["current"]["e2e"],
        data["previous"]["e2e"],
        theme["secondary"],
        theme,
        data["sprint_name"],
        data["previous"]["sprint_name"],
        out_dir,
        "5_e2e_tests_comparison.png",
    )


def chart_graphql_comparison(data, theme, out_dir):
    """6. GraphQL Tests - Period Comparison."""
    _chart_type_comparison(
        "GraphQL",
        data["current"]["graphql"],
        data["previous"]["graphql"],
        theme["accent1"],
        theme,
        data["sprint_name"],
        data["previous"]["sprint_name"],
        out_dir,
        "6_graphql_tests_comparison.png",
    )


def chart_key_achievements(data, theme, out_dir):
    """7. Key Achievements Summary Cards."""
    sprint = data["sprint_name"]
    achievements = data["achievements"]
    T = theme

    fig, ax = plt.subplots(figsize=(12, 7), facecolor=T["bg"])
    ax.set_facecolor(T["bg"])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    n = len(achievements)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    card_w, card_h = 0.28, 0.38
    gap_x = (1.0 - cols * card_w) / (cols + 1)
    gap_y = (1.0 - rows * card_h) / (rows + 1)

    for idx, item in enumerate(achievements):
        title = item["title"]
        value = item["value"]
        color = resolve_color(item.get("color", "accent1"), T)
        row, col = idx // cols, idx % cols
        cx = gap_x + col * (card_w + gap_x) + card_w / 2
        cy_bottom = 1.0 - gap_y - (row + 1) * card_h - row * gap_y

        rect = mpatches.FancyBboxPatch(
            (cx - card_w / 2, cy_bottom),
            card_w,
            card_h,
            boxstyle="round,pad=0.02",
            facecolor=color,
            edgecolor="none",
            alpha=0.9,
            transform=ax.transAxes,
        )
        ax.add_patch(rect)
        cy_center = cy_bottom + card_h / 2
        ax.text(
            cx,
            cy_center + card_h * 0.22,
            title,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color=T["text"],
        )
        ax.text(
            cx,
            cy_center - card_h * 0.05,
            value,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=28,
            fontweight="bold",
            color=T["text"],
        )

    fig.suptitle(f"Key Achievements \u2014 {sprint}", fontsize=20, fontweight="bold", color=T["text"], y=0.98)

    save(fig, out_dir, "7_key_achievements.png", T)


# ── Main ───────────────────────────────────────────────────────

CHART_GENERATORS = [
    ("Test Growth Trend", chart_test_growth_trend),
    ("Period Comparison Overview", chart_period_comparison),
    ("Active vs Ignored Tests", chart_active_vs_ignored),
    ("Test Distribution Donut", chart_distribution_donut),
    ("E2E Tests Comparison", chart_e2e_comparison),
    ("GraphQL Tests Comparison", chart_graphql_comparison),
    ("Key Achievements", chart_key_achievements),
]


def main():
    parser = argparse.ArgumentParser(description="Generate sprint test coverage charts.")
    parser.add_argument("sprint", help="Sprint directory name (e.g. Sprint26-03)")
    parser.add_argument(
        "--theme", choices=["dark", "light"], default=None, help="Override theme (default: read from sprint_data.json)"
    )
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sprint_dir = os.path.join(base_dir, args.sprint)

    if not os.path.isdir(sprint_dir):
        print(f"Error: directory '{sprint_dir}' does not exist.")
        sys.exit(1)

    data = load_data(sprint_dir)
    theme = get_theme(data, args.theme)
    setup_style(theme)

    out_dir = os.path.join(sprint_dir, "charts")
    os.makedirs(out_dir, exist_ok=True)

    sprint_name = data["sprint_name"]
    report_date = data.get("report_date", "")
    print("=" * 60)
    print(f"  Generating {sprint_name} Charts")
    if report_date:
        print(f"  Report Date: {report_date}")
    print(f"  Theme: {args.theme or data.get('theme', 'dark')}")
    print("=" * 60)

    for i, (label, generator) in enumerate(CHART_GENERATORS, 1):
        print(f"\n[{i}/{len(CHART_GENERATORS)}] {label}...")
        generator(data, theme, out_dir)

    print("\n" + "=" * 60)
    print(f"  All {len(CHART_GENERATORS)} charts generated successfully!")
    print("=" * 60)
    print(f"\n  Output directory: {out_dir}")
    for f in sorted(os.listdir(out_dir)):
        if f.endswith(".png"):
            print(f"  - {f}")
    print()


if __name__ == "__main__":
    main()
