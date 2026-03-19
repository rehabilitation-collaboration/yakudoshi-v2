"""Publication-quality figures for the yakudoshi mortality paper."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = Path(__file__).parent / "output"
DPI = 300


def load_main_results() -> list[dict]:
    with open(OUTPUT_DIR / "results_main.json") as f:
        return json.load(f)


def load_all_results() -> dict:
    with open(OUTPUT_DIR / "results_all.json") as f:
        return json.load(f)


def figure1_mortality_curves():
    """Figure 1: Age-specific mortality rates with yakudoshi ages highlighted."""
    from data_loader import load_analysis_data
    from definitions import get_yakudoshi_ages

    df = load_analysis_data()
    sample_years = [1950, 1970, 1990, 2010, 2024]
    age_range = (15, 80)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(sample_years)))

    for ax, sex, title in zip(axes, ("male", "female"), ("Male", "Female")):
        yaku_ages = get_yakudoshi_ages(sex, offset=-1)

        for year, color in zip(sample_years, colors):
            s = df[(df["sex"] == sex) & (df["year"] == year)]
            s = s[(s["age"] >= age_range[0]) & (s["age"] <= age_range[1])]
            ax.semilogy(s["age"], s["rate"], color=color, label=str(year), linewidth=1.2)

        for age in yaku_ages:
            ax.axvline(age, color="crimson", linestyle="--", alpha=0.4, linewidth=0.8)

        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Age (Western)")
        ax.set_xlim(age_range)
        ax.legend(title="Year", fontsize=7, title_fontsize=8)

    axes[0].set_ylabel("Death rate (log scale)")
    fig.suptitle(
        "Figure 1. Age-specific mortality rates, Japan 1950-2024\n"
        "Red dashed lines indicate yakudoshi ages (Western age equivalent)",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure1.png", dpi=DPI, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "figure1.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved: figure1.png/pdf")


def figure2_forest_plot():
    """Figure 2: Forest plot of local rate ratios for all yakudoshi ages."""
    results = load_main_results()

    fig, ax = plt.subplots(figsize=(8, 5))

    labels = []
    y_positions = []
    pos = 0

    for sex_label, sex in [("Male", "male"), ("Female", "female")]:
        sex_results = [r for r in results if r["sex"] == sex]
        for r in sex_results:
            label = f"{sex_label}, age {r['yaku_age_mannenrei']} (K:{r['yaku_age_kazoedoshi']})"
            labels.append(label)
            y_positions.append(pos)

            median = r["median_ratio"]
            ci_lo = r["ci_lower"]
            ci_hi = r["ci_upper"]

            color = "steelblue" if sex == "male" else "coral"
            ax.plot([ci_lo, ci_hi], [pos, pos], color=color, linewidth=2, solid_capstyle="round")
            ax.plot(median, pos, "o", color=color, markersize=7, zorder=5)

            # p-value annotation
            p = r["wilcoxon_p"]
            if p is not None:
                p_str = f"P<0.001" if p < 0.001 else f"P={p:.3f}"
            else:
                p_str = ""
            ax.annotate(p_str, xy=(ci_hi + 0.002, pos), fontsize=7, va="center")

            pos += 1

        pos += 0.5  # gap between sexes

    ax.axvline(1.0, color="black", linestyle="-", linewidth=0.8)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Rate ratio (yakudoshi / neighbors, ±3 ages)", fontsize=10)
    ax.set_title(
        "Figure 2. Local rate ratios at yakudoshi ages\n"
        "Median with 95% bootstrap CI, Wilcoxon signed-rank test",
        fontsize=10,
    )
    ax.set_xlim(0.95, 1.05)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure2.png", dpi=DPI, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "figure2.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved: figure2.png/pdf")


def figure3_sensitivity_comparison():
    """Figure 3: Sensitivity analysis comparison — median ratios across specifications."""
    all_results = load_all_results()

    main_results = load_main_results()

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for ax, sex, title in zip(axes, ("male", "female"), ("Male", "Female")):
        analyses = {}

        # Main (window=3, offset=-1)
        analyses["Main (±3, -1)"] = [r for r in main_results if r["sex"] == sex]

        # SA1: offset=-2
        analyses["SA1: offset=-2"] = [r for r in all_results["sensitivity"]["sa1_offset_minus2"] if r["sex"] == sex]

        # SA3: window=2
        analyses["SA3: ±2 window"] = [r for r in all_results["sensitivity"]["sa3_window2"] if r["sex"] == sex]

        # SA3: window=5
        analyses["SA3: ±5 window"] = [r for r in all_results["sensitivity"]["sa3_window5"] if r["sex"] == sex]

        # SA5: age restricted
        analyses["SA5: age 20-70"] = [r for r in all_results["sensitivity"]["sa5_age_restricted"] if r["sex"] == sex]

        # Collect unique yakudoshi ages from main
        main_ages = [r["yaku_age_mannenrei"] for r in analyses["Main (±3, -1)"]]

        x = np.arange(len(main_ages))
        width = 0.15
        offsets = np.linspace(-2 * width, 2 * width, len(analyses))

        for i, (name, results_list) in enumerate(analyses.items()):
            medians = []
            for age in main_ages:
                match = [r for r in results_list if r["yaku_age_mannenrei"] == age]
                if match:
                    medians.append(match[0]["median_ratio"])
                else:
                    # SA1 uses different ages, find closest
                    closest = min(results_list, key=lambda r: abs(r["yaku_age_mannenrei"] - age), default=None)
                    medians.append(closest["median_ratio"] if closest else np.nan)

            ax.bar(x + offsets[i], medians, width, label=name, alpha=0.8)

        ax.axhline(1.0, color="black", linestyle="-", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([str(a) for a in main_ages], fontsize=9)
        ax.set_xlabel("Yakudoshi age (Western)")
        ax.set_ylabel("Median rate ratio")
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.legend(fontsize=7, loc="lower left")
        ax.set_ylim(0.92, 1.06)

    fig.suptitle(
        "Figure 3. Sensitivity analysis: median rate ratios across specifications",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "figure3.png", dpi=DPI, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "figure3.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved: figure3.png/pdf")


if __name__ == "__main__":
    figure1_mortality_curves()
    figure2_forest_plot()
    figure3_sensitivity_comparison()
    print("All figures generated.")
