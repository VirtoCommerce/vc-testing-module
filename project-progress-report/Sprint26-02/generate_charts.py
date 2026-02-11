"""Generate separate test coverage report PNG charts for Sprint 26-02."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# === Output directory ===
OUT_DIR = r"C:\Users\mutyk\My Projects\vc-testing-module\project-progress-report\Sprint26-02\charts"
os.makedirs(OUT_DIR, exist_ok=True)

# === Data ===
dates = ["Dec 23\n2025", "Jan 22\n2026", "Feb 6\n2026"]
total_tests = [121, 161, 178]
active_tests = [118, 151, 177]

type_labels = ["E2E Tests", "GraphQL Tests"]
type_counts = [65, 113]

e2e_metrics = ["Test Files", "Test Functions", "Active Tests", "Ignored Tests"]
e2e_p1 = [27, 48, 45, 3]
e2e_p2 = [29, 65, 64, 3]

gql_metrics = ["Test Files", "Test Functions", "Active Tests", "Ignored Tests"]
gql_p1 = [58, 113, 106, 7]
gql_p2 = [58, 113, 113, 2]

# === Colors ===
C_BLUE = "#2563EB"
C_BLUE_LIGHT = "#93C5FD"
C_GREEN = "#16A34A"
C_GREEN_LIGHT = "#86EFAC"
C_RED = "#DC2626"
C_RED_LIGHT = "#FCA5A5"
C_ORANGE = "#EA580C"
C_PURPLE = "#7C3AED"
C_GRAY = "#6B7280"
C_BG = "#FAFBFC"
C_CARD_BG = "#FFFFFF"

DPI = 180


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  Saved: {path}")


# ─────────────────────────────────────────────────────
# 1. Test Growth Trend
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor=C_BG)
ax.set_facecolor(C_CARD_BG)

x = np.arange(len(dates))
ax.fill_between(x, active_tests, alpha=0.12, color=C_BLUE)
ax.plot(x, total_tests, "o-", color=C_BLUE, linewidth=3, markersize=12, label="Total Tests", zorder=5)
ax.plot(x, active_tests, "s--", color=C_GREEN, linewidth=3, markersize=12, label="Active Tests", zorder=5)

for i, (t, a) in enumerate(zip(total_tests, active_tests)):
    ax.annotate(
        str(t),
        (i, t),
        textcoords="offset points",
        xytext=(0, 16),
        ha="center",
        fontsize=14,
        fontweight="bold",
        color=C_BLUE,
    )
    if a != t:
        ax.annotate(
            str(a), (i, a), textcoords="offset points", xytext=(0, -20), ha="center", fontsize=13, color=C_GREEN
        )

ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=13)
ax.set_ylabel("Number of Tests", fontsize=14)
ax.set_title("Test Growth Trend — Sprint 26-02", fontsize=20, fontweight="bold", pad=16)
ax.legend(loc="upper left", fontsize=12, framealpha=0.9)
ax.set_ylim(90, 205)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

save(fig, "1_test_growth_trend.png")

# ─────────────────────────────────────────────────────
# 2. Period Comparison Overview
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6), facecolor=C_BG)
ax.set_facecolor(C_CARD_BG)

metrics_labels = ["Test Files", "Test Functions", "Active Tests", "Ignored Tests"]
vals_p1 = [85, 161, 151, 10]
vals_p2 = [87, 178, 177, 5]
changes = ["+2", "+17", "+22", "-5"]
bar_colors_p1 = [C_BLUE_LIGHT, C_BLUE_LIGHT, C_GREEN_LIGHT, C_RED_LIGHT]
bar_colors_p2 = [C_BLUE, C_BLUE, C_GREEN, C_RED]

y_pos = np.arange(len(metrics_labels))
bar_h = 0.35

bars1 = ax.barh(
    y_pos + bar_h / 2, vals_p1, bar_h, label="Sprint 26-01 (Jan 12-25)", color=bar_colors_p1, edgecolor="white"
)
bars2 = ax.barh(
    y_pos - bar_h / 2, vals_p2, bar_h, label="Sprint 26-02 (Jan 26-Feb 6)", color=bar_colors_p2, edgecolor="white"
)

for i, (b1, b2, ch) in enumerate(zip(bars1, bars2, changes)):
    ax.text(
        b1.get_width() + 2, b1.get_y() + b1.get_height() / 2, str(vals_p1[i]), va="center", fontsize=12, color=C_GRAY
    )
    color = C_GREEN if ch.startswith("+") else C_RED if ch.startswith("-") else C_GRAY
    ax.text(
        b2.get_width() + 2,
        b2.get_y() + b2.get_height() / 2,
        f"{vals_p2[i]}  ({ch})",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=color,
    )

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics_labels, fontsize=14)
ax.set_title("Period Comparison Overview — Sprint 26-02", fontsize=20, fontweight="bold", pad=16)
ax.legend(loc="lower left", fontsize=12, framealpha=0.9)
ax.invert_yaxis()
ax.set_xlim(0, 230)
ax.grid(axis="x", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

save(fig, "2_period_comparison_overview.png")

# ─────────────────────────────────────────────────────
# 3. Active vs Ignored Tests
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6), facecolor=C_BG)
ax.set_facecolor(C_CARD_BG)

categories = ["Sprint 26-01\n(Jan 12-25)", "Sprint 26-02\n(Jan 26-Feb 6)"]
active_vals = [151, 177]
ignored_vals = [10, 5]
active_pct = [93.8, 97.2]

x3 = np.arange(len(categories))
w = 0.5

ax.bar(x3, active_vals, w, label="Active", color=C_GREEN, edgecolor="white", linewidth=1.5)
ax.bar(x3, ignored_vals, w, bottom=active_vals, label="Ignored", color=C_RED, edgecolor="white", linewidth=1.5)

for i, (a, ig, pct) in enumerate(zip(active_vals, ignored_vals, active_pct)):
    ax.text(i, a / 2, f"{a}\n({pct:.1f}%)", ha="center", va="center", fontsize=15, fontweight="bold", color="white")
    ax.text(i, a + ig / 2, str(ig), ha="center", va="center", fontsize=13, fontweight="bold", color="white")

ax.annotate(
    "+3.4% active rate",
    xy=(1, 178),
    xytext=(0.15, 193),
    fontsize=14,
    fontweight="bold",
    color=C_GREEN,
    arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.5),
    ha="center",
)

ax.set_xticks(x3)
ax.set_xticklabels(categories, fontsize=13)
ax.set_ylabel("Number of Tests", fontsize=14)
ax.set_title("Active vs Ignored Tests — Sprint 26-02", fontsize=20, fontweight="bold", pad=16)
ax.legend(fontsize=12, framealpha=0.9)
ax.set_ylim(0, 205)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

save(fig, "3_active_vs_ignored.png")

# ─────────────────────────────────────────────────────
# 4. Test Distribution by Type (Donut)
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8), facecolor=C_BG)

donut_colors = [C_ORANGE, C_PURPLE]
wedges, texts, autotexts = ax.pie(
    type_counts,
    labels=type_labels,
    autopct="%1.1f%%",
    colors=donut_colors,
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=3),
    textprops=dict(fontsize=15),
)
for at in autotexts:
    at.set_fontsize(15)
    at.set_fontweight("bold")
    at.set_color("white")

ax.text(0, 0.05, "178", ha="center", va="center", fontsize=36, fontweight="bold", color="#1E293B")
ax.text(0, -0.12, "Total Tests", ha="center", va="center", fontsize=14, color=C_GRAY)
ax.set_title("Test Distribution by Type — Sprint 26-02", fontsize=20, fontweight="bold", pad=20)

save(fig, "4_test_distribution_donut.png")

# ─────────────────────────────────────────────────────
# 5. E2E Tests — Period Comparison
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor=C_BG)
ax.set_facecolor(C_CARD_BG)

x5 = np.arange(len(e2e_metrics))
w5 = 0.35
ax.bar(x5 - w5 / 2, e2e_p1, w5, label="Sprint 26-01 (Jan 12-25)", color=C_BLUE_LIGHT, edgecolor="white")
ax.bar(x5 + w5 / 2, e2e_p2, w5, label="Sprint 26-02 (Jan 26-Feb 6)", color=C_ORANGE, edgecolor="white")

for i, (v1, v2) in enumerate(zip(e2e_p1, e2e_p2)):
    ax.text(i - w5 / 2, v1 + 1.2, str(v1), ha="center", fontsize=12, color=C_GRAY)
    diff = v2 - v1
    sign = "+" if diff > 0 else ""
    color = C_GREEN if diff > 0 else C_RED if diff < 0 else C_GRAY
    suffix = f"\n({sign}{diff})" if diff != 0 else ""
    ax.text(i + w5 / 2, v2 + 1.2, f"{v2}{suffix}", ha="center", fontsize=12, fontweight="bold", color=color)

ax.set_xticks(x5)
ax.set_xticklabels(e2e_metrics, fontsize=13)
ax.set_ylabel("Count", fontsize=14)
ax.set_title("E2E Tests — Period Comparison", fontsize=20, fontweight="bold", pad=16)
ax.legend(loc="upper left", fontsize=12, framealpha=0.9)
ax.set_ylim(0, 82)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

save(fig, "5_e2e_tests_comparison.png")

# ─────────────────────────────────────────────────────
# 6. GraphQL Tests — Period Comparison
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor=C_BG)
ax.set_facecolor(C_CARD_BG)

x6 = np.arange(len(gql_metrics))
ax.bar(x6 - w5 / 2, gql_p1, w5, label="Sprint 26-01 (Jan 12-25)", color=C_BLUE_LIGHT, edgecolor="white")
ax.bar(x6 + w5 / 2, gql_p2, w5, label="Sprint 26-02 (Jan 26-Feb 6)", color=C_PURPLE, edgecolor="white")

for i, (v1, v2) in enumerate(zip(gql_p1, gql_p2)):
    ax.text(i - w5 / 2, v1 + 1.5, str(v1), ha="center", fontsize=12, color=C_GRAY)
    diff = v2 - v1
    sign = "+" if diff > 0 else ""
    color = C_GREEN if diff > 0 else C_RED if diff < 0 else C_GRAY
    suffix = f"\n({sign}{diff})" if diff != 0 else ""
    ax.text(i + w5 / 2, v2 + 1.5, f"{v2}{suffix}", ha="center", fontsize=12, fontweight="bold", color=color)

ax.set_xticks(x6)
ax.set_xticklabels(gql_metrics, fontsize=13)
ax.set_ylabel("Count", fontsize=14)
ax.set_title("GraphQL Tests — Period Comparison", fontsize=20, fontweight="bold", pad=16)
ax.legend(loc="upper left", fontsize=12, framealpha=0.9)
ax.set_ylim(0, 135)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

save(fig, "6_graphql_tests_comparison.png")

# ─────────────────────────────────────────────────────
# 7. Key Achievements Summary Cards
# ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 4), facecolor=C_BG)
ax.set_facecolor(C_BG)
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

achievements = [
    ("New Feature\nCoverage", "+10 tests", "Search history\nfully tested", C_BLUE),
    ("Test\nStabilization", "-50%", "Ignored tests\nreduced", C_GREEN),
    ("E2E\nGrowth", "+35.4%", "E2E test\nfunctions", C_ORANGE),
    ("Active\nTest Rate", "97.2%", "Up from\n93.8%", C_PURPLE),
    ("Growth\nVelocity", "1.13/day", "Tests added\nper day", C_GRAY),
    ("Component\nLibrary", "+8 new", "Reusable UI\ncomponents", C_RED),
]

n = len(achievements)
card_w = 0.14
gap = (1.0 - n * card_w) / (n + 1)

for i, (title, value, desc, color) in enumerate(achievements):
    cx = gap + i * (card_w + gap) + card_w / 2

    rect = mpatches.FancyBboxPatch(
        (cx - card_w / 2, 0.05),
        card_w,
        0.9,
        boxstyle="round,pad=0.02",
        facecolor="white",
        edgecolor=color,
        linewidth=3,
        transform=ax.transAxes,
    )
    ax.add_patch(rect)

    ax.text(
        cx,
        0.82,
        title,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#1E293B",
    )
    ax.text(
        cx, 0.50, value, transform=ax.transAxes, ha="center", va="center", fontsize=24, fontweight="bold", color=color
    )
    ax.text(cx, 0.20, desc, transform=ax.transAxes, ha="center", va="center", fontsize=10, color=C_GRAY)

fig.suptitle("Key Achievements — Sprint 26-02", fontsize=20, fontweight="bold", color="#1E293B", y=1.05)

save(fig, "7_key_achievements.png")

print(f"\nAll 7 charts saved to: {OUT_DIR}")
