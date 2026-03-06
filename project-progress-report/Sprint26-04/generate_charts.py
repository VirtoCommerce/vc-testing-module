"""Generate separate test coverage report PNG charts for Sprint 26-04."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# === Output directory (relative to this script) ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "charts")
os.makedirs(OUT_DIR, exist_ok=True)

# === Style ===
plt.style.use("dark_background")

# === Color Scheme ===
C_PRIMARY = "#0f3460"
C_SECONDARY = "#e94560"
C_ACCENT1 = "#00b4d8"
C_ACCENT2 = "#48cae4"
C_BG = "#1a1a2e"
C_TEXT = "white"
C_GREEN = "#2ecc71"
C_ORANGE = "#f39c12"
C_GRAY = "#95a5a6"

DPI = 180


def save(fig, name):
    """Save figure and print progress."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [OK] Saved: {path}")


# === Historical Trend Data ===
dates = ["Dec 23\n2025", "Jan 22\n2026", "Feb 6\n2026", "Feb 20\n2026", "Mar 6\n2026"]
total_tests = [121, 161, 178, 183, 197]
active_tests = [118, 151, 173, 178, 192]

# === Current State (Sprint 26-04) ===
e2e_current = {"files": 32, "functions": 80, "active": 77, "ignored": 3}
gql_current = {"files": 60, "functions": 115, "active": 113, "ignored": 2}
webapi_current = {"files": 2, "functions": 2, "active": 2, "ignored": 0}
total_current = {"files": 94, "functions": 197, "active": 192, "ignored": 5, "active_rate": 97.5}

# === Previous State (Sprint 26-03) ===
e2e_prev = {"files": 30, "functions": 68, "active": 65, "ignored": 3}
gql_prev = {"files": 60, "functions": 115, "active": 113, "ignored": 2}
total_prev = {"files": 90, "functions": 183, "active": 178, "ignored": 5, "active_rate": 97.3}


print("=" * 60)
print("  Generating Sprint 26-04 Charts")
print("  Report Date: March 6, 2026")
print("=" * 60)

# ─────────────────────────────────────────────────────
# 1. Test Growth Trend (Line Chart)
# ─────────────────────────────────────────────────────
print("\n[1/7] Test Growth Trend...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

x = np.arange(len(dates))
ax.fill_between(x, active_tests, alpha=0.15, color=C_ACCENT1)

ax.plot(
    x,
    total_tests,
    "o-",
    color=C_ACCENT1,
    linewidth=3,
    markersize=12,
    label="Total Tests",
    zorder=5,
    markerfacecolor=C_ACCENT1,
    markeredgecolor=C_TEXT,
    markeredgewidth=1.5,
)
ax.plot(
    x,
    active_tests,
    "s--",
    color=C_GREEN,
    linewidth=3,
    markersize=12,
    label="Active Tests",
    zorder=5,
    markerfacecolor=C_GREEN,
    markeredgecolor=C_TEXT,
    markeredgewidth=1.5,
)

for i, (t, a) in enumerate(zip(total_tests, active_tests)):
    ax.annotate(
        str(t),
        (i, t),
        textcoords="offset points",
        xytext=(0, 18),
        ha="center",
        fontsize=14,
        fontweight="bold",
        color=C_ACCENT1,
    )
    if a != t:
        ax.annotate(
            str(a), (i, a), textcoords="offset points", xytext=(0, -22), ha="center", fontsize=13, color=C_GREEN
        )

ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=13, color=C_TEXT)
ax.set_ylabel("Number of Tests", fontsize=14, color=C_TEXT)
ax.set_title("Test Growth Trend \u2014 Sprint 26-04", fontsize=20, fontweight="bold", pad=16, color=C_TEXT)
ax.legend(loc="upper left", fontsize=12, framealpha=0.3, facecolor=C_BG, edgecolor=C_GRAY)
ax.set_ylim(80, 230)
ax.grid(axis="y", alpha=0.2, color=C_GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_color(C_GRAY)
ax.spines["left"].set_color(C_GRAY)
ax.tick_params(colors=C_TEXT)

save(fig, "1_test_growth_trend.png")

# ─────────────────────────────────────────────────────
# 2. Period Comparison Overview (Horizontal Bar Chart)
# ─────────────────────────────────────────────────────
print("[2/7] Period Comparison Overview...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

metrics_labels = ["Test Files", "Test Functions", "Active Tests", "Ignored Tests"]
vals_p1 = [total_prev["files"], total_prev["functions"], total_prev["active"], total_prev["ignored"]]
vals_p2 = [total_current["files"], total_current["functions"], total_current["active"], total_current["ignored"]]
changes = ["+4", "+14", "+14", "0"]

y_pos = np.arange(len(metrics_labels))
bar_h = 0.35
bar_colors_p2 = [C_ACCENT1, C_ACCENT1, C_GREEN, C_SECONDARY]

bars1 = ax.barh(
    y_pos + bar_h / 2, vals_p1, bar_h, label="Sprint 26-03", color=C_ACCENT2, edgecolor=C_BG, linewidth=1.5, alpha=0.6
)
bars2 = ax.barh(
    y_pos - bar_h / 2, vals_p2, bar_h, label="Sprint 26-04", color=bar_colors_p2, edgecolor=C_BG, linewidth=1.5
)

for i, (b1, b2, ch) in enumerate(zip(bars1, bars2, changes)):
    ax.text(
        b1.get_width() + 2, b1.get_y() + b1.get_height() / 2, str(vals_p1[i]), va="center", fontsize=12, color=C_GRAY
    )
    color = C_GREEN if ch.startswith("+") else C_SECONDARY if ch != "0" else C_GRAY
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
ax.set_yticklabels(metrics_labels, fontsize=14, color=C_TEXT)
ax.set_title("Period Comparison Overview \u2014 Sprint 26-04", fontsize=20, fontweight="bold", pad=16, color=C_TEXT)
ax.legend(loc="lower right", fontsize=12, framealpha=0.3, facecolor=C_BG, edgecolor=C_GRAY)
ax.invert_yaxis()
ax.set_xlim(0, 250)
ax.grid(axis="x", alpha=0.2, color=C_GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_color(C_GRAY)
ax.spines["left"].set_color(C_GRAY)
ax.tick_params(colors=C_TEXT)

save(fig, "2_period_comparison_overview.png")

# ─────────────────────────────────────────────────────
# 3. Active vs Ignored Tests (Stacked Bar Chart)
# ─────────────────────────────────────────────────────
print("[3/7] Active vs Ignored Tests...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

categories = ["Sprint 26-03\n(Period 1)", "Sprint 26-04\n(Period 2)"]
active_vals = [total_prev["active"], total_current["active"]]
ignored_vals = [total_prev["ignored"], total_current["ignored"]]
active_pct = [total_prev["active_rate"], total_current["active_rate"]]

x3 = np.arange(len(categories))
ax.bar(x3, active_vals, 0.5, label="Active", color=C_GREEN, edgecolor=C_BG, linewidth=2)
ax.bar(x3, ignored_vals, 0.5, bottom=active_vals, label="Ignored", color=C_SECONDARY, edgecolor=C_BG, linewidth=2)

for i, (a, ig, pct) in enumerate(zip(active_vals, ignored_vals, active_pct)):
    ax.text(i, a / 2, f"{a}\n({pct:.1f}%)", ha="center", va="center", fontsize=15, fontweight="bold", color=C_TEXT)
    ax.text(i, a + ig / 2, str(ig), ha="center", va="center", fontsize=13, fontweight="bold", color=C_TEXT)

rate_change = total_current["active_rate"] - total_prev["active_rate"]
ax.annotate(
    f"+{rate_change:.1f}% active rate",
    xy=(1, total_current["active"] + total_current["ignored"]),
    xytext=(0.15, 210),
    fontsize=14,
    fontweight="bold",
    color=C_GREEN,
    arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.5),
    ha="center",
)

ax.set_xticks(x3)
ax.set_xticklabels(categories, fontsize=13, color=C_TEXT)
ax.set_ylabel("Number of Tests", fontsize=14, color=C_TEXT)
ax.set_title("Active vs Ignored Tests \u2014 Sprint 26-04", fontsize=20, fontweight="bold", pad=16, color=C_TEXT)
ax.legend(fontsize=12, framealpha=0.3, facecolor=C_BG, edgecolor=C_GRAY)
ax.set_ylim(0, 230)
ax.grid(axis="y", alpha=0.2, color=C_GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_color(C_GRAY)
ax.spines["left"].set_color(C_GRAY)
ax.tick_params(colors=C_TEXT)

save(fig, "3_active_vs_ignored.png")

# ─────────────────────────────────────────────────────
# 4. Test Distribution by Type (Donut Chart)
# ─────────────────────────────────────────────────────
print("[4/7] Test Distribution Donut...")

fig, ax = plt.subplots(figsize=(10, 10), facecolor=C_BG)

wedges, texts, autotexts = ax.pie(
    [80, 115, 2],
    labels=["E2E Tests\n(80)", "GraphQL Tests\n(115)", "WebAPI Tests\n(2)"],
    autopct="%1.1f%%",
    colors=[C_SECONDARY, C_ACCENT1, C_ORANGE],
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(width=0.45, edgecolor=C_BG, linewidth=3),
    textprops=dict(fontsize=15, color=C_TEXT),
)
for at in autotexts:
    at.set_fontsize(15)
    at.set_fontweight("bold")
    at.set_color(C_TEXT)

ax.text(0, 0.06, "197", ha="center", va="center", fontsize=40, fontweight="bold", color=C_TEXT)
ax.text(0, -0.12, "Total", ha="center", va="center", fontsize=16, color=C_GRAY)
ax.set_title("Test Distribution by Type \u2014 Sprint 26-04", fontsize=20, fontweight="bold", pad=20, color=C_TEXT)

save(fig, "4_test_distribution_donut.png")

# ─────────────────────────────────────────────────────
# 5. E2E Tests - Period Comparison (Grouped Bar Chart)
# ─────────────────────────────────────────────────────
print("[5/7] E2E Tests Comparison...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

e2e_metrics = ["Files", "Functions", "Active", "Ignored"]
e2e_p1 = [e2e_prev["files"], e2e_prev["functions"], e2e_prev["active"], e2e_prev["ignored"]]
e2e_p2 = [e2e_current["files"], e2e_current["functions"], e2e_current["active"], e2e_current["ignored"]]

x5 = np.arange(len(e2e_metrics))
w5 = 0.35
ax.bar(x5 - w5 / 2, e2e_p1, w5, label="Sprint 26-03", color=C_ACCENT2, edgecolor=C_BG, alpha=0.7)
ax.bar(x5 + w5 / 2, e2e_p2, w5, label="Sprint 26-04", color=C_SECONDARY, edgecolor=C_BG)

for i, (v1, v2) in enumerate(zip(e2e_p1, e2e_p2)):
    ax.text(i - w5 / 2, v1 + 1.5, str(v1), ha="center", fontsize=12, color=C_GRAY)
    diff = v2 - v1
    sign = "+" if diff > 0 else ""
    color = C_GREEN if diff > 0 else C_SECONDARY if diff < 0 else C_GRAY
    suffix = f"\n({sign}{diff})" if diff != 0 else ""
    ax.text(i + w5 / 2, v2 + 1.5, f"{v2}{suffix}", ha="center", fontsize=12, fontweight="bold", color=color)

ax.set_xticks(x5)
ax.set_xticklabels(e2e_metrics, fontsize=13, color=C_TEXT)
ax.set_ylabel("Count", fontsize=14, color=C_TEXT)
ax.set_title("E2E Tests \u2014 Period Comparison", fontsize=20, fontweight="bold", pad=16, color=C_TEXT)
ax.legend(loc="upper left", fontsize=12, framealpha=0.3, facecolor=C_BG, edgecolor=C_GRAY)
ax.set_ylim(0, 100)
ax.grid(axis="y", alpha=0.2, color=C_GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_color(C_GRAY)
ax.spines["left"].set_color(C_GRAY)
ax.tick_params(colors=C_TEXT)

save(fig, "5_e2e_tests_comparison.png")

# ─────────────────────────────────────────────────────
# 6. GraphQL Tests - Period Comparison (Grouped Bar Chart)
# ─────────────────────────────────────────────────────
print("[6/7] GraphQL Tests Comparison...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)

gql_metrics = ["Files", "Functions", "Active", "Ignored"]
gql_p1 = [gql_prev["files"], gql_prev["functions"], gql_prev["active"], gql_prev["ignored"]]
gql_p2 = [gql_current["files"], gql_current["functions"], gql_current["active"], gql_current["ignored"]]

x6 = np.arange(len(gql_metrics))
ax.bar(x6 - w5 / 2, gql_p1, w5, label="Sprint 26-03", color=C_ACCENT2, edgecolor=C_BG, alpha=0.7)
ax.bar(x6 + w5 / 2, gql_p2, w5, label="Sprint 26-04", color=C_ACCENT1, edgecolor=C_BG)

for i, (v1, v2) in enumerate(zip(gql_p1, gql_p2)):
    ax.text(i - w5 / 2, v1 + 1.5, str(v1), ha="center", fontsize=12, color=C_GRAY)
    diff = v2 - v1
    sign = "+" if diff > 0 else ""
    color = C_GREEN if diff > 0 else C_SECONDARY if diff < 0 else C_GRAY
    suffix = f"\n({sign}{diff})" if diff != 0 else ""
    ax.text(i + w5 / 2, v2 + 1.5, f"{v2}{suffix}", ha="center", fontsize=12, fontweight="bold", color=color)

ax.set_xticks(x6)
ax.set_xticklabels(gql_metrics, fontsize=13, color=C_TEXT)
ax.set_ylabel("Count", fontsize=14, color=C_TEXT)
ax.set_title("GraphQL Tests \u2014 Period Comparison", fontsize=20, fontweight="bold", pad=16, color=C_TEXT)
ax.legend(loc="upper left", fontsize=12, framealpha=0.3, facecolor=C_BG, edgecolor=C_GRAY)
ax.set_ylim(0, 140)
ax.grid(axis="y", alpha=0.2, color=C_GRAY)
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_color(C_GRAY)
ax.spines["left"].set_color(C_GRAY)
ax.tick_params(colors=C_TEXT)

save(fig, "6_graphql_tests_comparison.png")

# ─────────────────────────────────────────────────────
# 7. Key Achievements Summary Cards (2x3 Grid)
# ─────────────────────────────────────────────────────
print("[7/7] Key Achievements Cards...")

fig, ax = plt.subplots(figsize=(12, 7), facecolor=C_BG)
ax.set_facecolor(C_BG)
ax.axis("off")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

achievements = [
    ("New Tests", "+14", C_ACCENT1),
    ("New Files", "+4", C_GREEN),
    ("Active Rate", "97.5%", C_ACCENT2),
    ("Files Refactored", "12+", C_SECONDARY),
    ("Growth", "+7.7%", C_ORANGE),
    ("VCST Tickets", "5", C_PRIMARY),
]

cols, rows_n = 3, 2
card_w, card_h = 0.28, 0.38
gap_x = (1.0 - cols * card_w) / (cols + 1)
gap_y = (1.0 - rows_n * card_h) / (rows_n + 1)

for idx, (title, value, color) in enumerate(achievements):
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
        color=C_TEXT,
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
        color=C_TEXT,
    )

fig.suptitle("Key Achievements \u2014 Sprint 26-04", fontsize=20, fontweight="bold", color=C_TEXT, y=0.98)

save(fig, "7_key_achievements.png")

# ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  All 7 charts generated successfully!")
print("=" * 60)
print(f"\n  Output directory: {OUT_DIR}")
for i, name in enumerate(
    [
        "1_test_growth_trend.png",
        "2_period_comparison_overview.png",
        "3_active_vs_ignored.png",
        "4_test_distribution_donut.png",
        "5_e2e_tests_comparison.png",
        "6_graphql_tests_comparison.png",
        "7_key_achievements.png",
    ],
    start=1,
):
    print(f"  {i}. {os.path.join(OUT_DIR, name)}")
print()
