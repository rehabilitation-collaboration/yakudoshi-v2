"""Exploratory analysis and visualization of JMD mortality data."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from data_loader import load_analysis_data
from definitions import get_yakudoshi_ages

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DPI = 300
AGE_RANGE = (15, 80)
SAMPLE_YEARS = [1950, 1970, 1990, 2010, 2024]


def plot_mortality_curves(df, output_path: Path | None = None):
    """Plot age-specific mortality rates for selected years, with yakudoshi ages highlighted."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    for ax, sex in zip(axes, ("male", "female")):
        yaku_ages = get_yakudoshi_ages(sex, offset=-1)

        for year in SAMPLE_YEARS:
            subset = df[(df["sex"] == sex) & (df["year"] == year)]
            subset = subset[(subset["age"] >= AGE_RANGE[0]) & (subset["age"] <= AGE_RANGE[1])]
            ax.semilogy(subset["age"], subset["rate"], label=str(year), alpha=0.7)

        # Highlight yakudoshi ages
        for age in yaku_ages:
            ax.axvline(age, color="red", linestyle="--", alpha=0.3, linewidth=1)

        ax.set_title(f"{'Male' if sex == 'male' else 'Female'} mortality rates")
        ax.set_xlabel("Age")
        ax.set_ylabel("Death rate (log scale)")
        ax.legend(title="Year", fontsize=8)
        ax.set_xlim(AGE_RANGE)

        # Annotate yakudoshi ages
        for age in yaku_ages:
            ax.annotate(
                f"{age}",
                xy=(age, ax.get_ylim()[0]),
                xytext=(0, 5),
                textcoords="offset points",
                fontsize=7,
                color="red",
                ha="center",
            )

    fig.suptitle("Age-specific mortality rates with yakudoshi ages (red dashed lines)", fontsize=12)
    fig.tight_layout()

    path = output_path or OUTPUT_DIR / "figure1_mortality_curves.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


def plot_local_ratio_overview(df, output_path: Path | None = None):
    """Plot ratio of yakudoshi age mortality to neighboring ages across all years.

    This gives a visual overview of whether yakudoshi ages stand out.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    window = 3  # ±3 ages for neighbors

    for ax, sex in zip(axes, ("male", "female")):
        yaku_ages = get_yakudoshi_ages(sex, offset=-1)
        sex_df = df[(df["sex"] == sex) & (df["age"] >= AGE_RANGE[0]) & (df["age"] <= AGE_RANGE[1])]

        for yaku_age in yaku_ages:
            ratios = []
            years = []
            for year in sex_df["year"].unique():
                year_df = sex_df[sex_df["year"] == year]
                target = year_df[year_df["age"] == yaku_age]["rate"].values
                neighbors = year_df[
                    (year_df["age"] >= yaku_age - window)
                    & (year_df["age"] <= yaku_age + window)
                    & (year_df["age"] != yaku_age)
                ]["rate"].values

                if len(target) == 1 and len(neighbors) > 0:
                    ratio = target[0] / np.mean(neighbors)
                    ratios.append(ratio)
                    years.append(year)

            ax.scatter(years, ratios, s=5, alpha=0.4, label=f"Age {yaku_age}")

        ax.axhline(1.0, color="black", linestyle="-", linewidth=0.5)
        ax.set_title(f"{'Male' if sex == 'male' else 'Female'}: yakudoshi / neighbors ratio")
        ax.set_xlabel("Year")
        ax.set_ylabel("Rate ratio (yakudoshi / mean of ±3 neighbors)")
        ax.legend(fontsize=8)
        ax.set_ylim(0.8, 1.2)

    fig.suptitle("Local rate ratio at yakudoshi ages over time", fontsize=12)
    fig.tight_layout()

    path = output_path or OUTPUT_DIR / "figure_exploratory_ratios.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    print("Loading data...")
    df = load_analysis_data()
    print(f"Loaded {len(df):,} rows ({df['year'].min()}-{df['year'].max()}, ages {df['age'].min()}-{df['age'].max()})")

    print("\nBasic stats:")
    for sex in ("male", "female"):
        sex_df = df[df["sex"] == sex]
        total_deaths = sex_df["deaths"].sum()
        print(f"  {sex}: {total_deaths:,.0f} total deaths")

    print("\nGenerating plots...")
    plot_mortality_curves(df)
    plot_local_ratio_overview(df)
    print("Done.")
