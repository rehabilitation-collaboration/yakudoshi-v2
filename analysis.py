"""Main analysis: nonparametric local comparison of mortality at yakudoshi ages."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from data_loader import load_analysis_data
from definitions import get_yakudoshi_ages

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def compute_local_ratios(
    df: pd.DataFrame,
    sex: str,
    yaku_age: int,
    window: int = 3,
) -> pd.DataFrame:
    """Compute the ratio of yakudoshi age mortality to mean neighbor mortality.

    For each calendar year, ratio = Mx(yaku_age) / mean(Mx(yaku_age ± window, excluding yaku_age)).

    Args:
        df: Analysis data (long format with columns: year, age, sex, rate).
        sex: "male" or "female".
        yaku_age: Yakudoshi age in mannenrei.
        window: Number of neighboring ages on each side.

    Returns:
        DataFrame with columns: year, ratio, target_rate, neighbor_mean.
    """
    sex_df = df[df["sex"] == sex].copy()
    results = []

    for year in sorted(sex_df["year"].unique()):
        year_df = sex_df[sex_df["year"] == year]

        target = year_df[year_df["age"] == yaku_age]["rate"].values
        neighbors = year_df[
            (year_df["age"] >= yaku_age - window)
            & (year_df["age"] <= yaku_age + window)
            & (year_df["age"] != yaku_age)
        ]["rate"].values

        if len(target) == 1 and len(neighbors) > 0:
            target_rate = target[0]
            neighbor_mean = np.mean(neighbors)
            if neighbor_mean > 0 and not np.isnan(target_rate):
                ratio = target_rate / neighbor_mean
                results.append({
                    "year": year,
                    "ratio": ratio,
                    "target_rate": target_rate,
                    "neighbor_mean": neighbor_mean,
                })

    return pd.DataFrame(results)


def test_ratio_distribution(ratios: np.ndarray) -> dict:
    """Test whether the ratio distribution is significantly different from 1.0.

    Uses:
    1. Wilcoxon signed-rank test (H0: median ratio = 1.0)
    2. Permutation test (10,000 iterations)
    3. Cohen's d effect size

    Args:
        ratios: Array of yearly ratios.

    Returns:
        Dictionary with test statistics.
    """
    n = len(ratios)
    median_ratio = float(np.median(ratios))
    mean_ratio = float(np.mean(ratios))

    # Wilcoxon signed-rank test (two-sided, H0: median = 1.0)
    deviations = ratios - 1.0
    nonzero = deviations[deviations != 0]
    if len(nonzero) >= 10:
        wilcoxon_stat, wilcoxon_p = stats.wilcoxon(nonzero, alternative="two-sided")
    else:
        wilcoxon_stat, wilcoxon_p = np.nan, np.nan

    # Permutation test: randomly flip signs of (ratio - 1) deviations
    rng = np.random.default_rng(seed=42)
    observed_mean_dev = np.mean(deviations)
    n_perm = 10_000
    perm_count = 0
    for _ in range(n_perm):
        signs = rng.choice([-1, 1], size=n)
        perm_mean = np.mean(deviations * signs)
        if abs(perm_mean) >= abs(observed_mean_dev):
            perm_count += 1
    perm_p = perm_count / n_perm

    # Cohen's d (effect size relative to 1.0)
    std = np.std(ratios, ddof=1)
    cohens_d = (mean_ratio - 1.0) / std if std > 0 else 0.0

    # 95% CI for median (bootstrap)
    boot_medians = []
    for _ in range(10_000):
        boot_sample = rng.choice(ratios, size=n, replace=True)
        boot_medians.append(np.median(boot_sample))
    ci_lower = float(np.percentile(boot_medians, 2.5))
    ci_upper = float(np.percentile(boot_medians, 97.5))

    return {
        "n_years": n,
        "median_ratio": round(median_ratio, 4),
        "mean_ratio": round(mean_ratio, 4),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
        "wilcoxon_stat": round(float(wilcoxon_stat), 2) if not np.isnan(wilcoxon_stat) else None,
        "wilcoxon_p": round(float(wilcoxon_p), 4) if not np.isnan(wilcoxon_p) else None,
        "perm_p": round(perm_p, 4),
        "cohens_d": round(cohens_d, 4),
    }


def run_main_analysis(window: int = 3, offset: int = -1) -> list[dict]:
    """Run the main local comparison analysis for all yakudoshi ages.

    Args:
        window: Number of neighboring ages on each side.
        offset: Kazoedoshi-to-mannenrei conversion offset.

    Returns:
        List of result dictionaries (one per sex × yakudoshi age).
    """
    df = load_analysis_data()
    results = []

    for sex in ("male", "female"):
        yaku_ages = get_yakudoshi_ages(sex, offset=offset)
        for yaku_age in yaku_ages:
            ratios_df = compute_local_ratios(df, sex, yaku_age, window=window)
            ratios = ratios_df["ratio"].values

            test_results = test_ratio_distribution(ratios)
            test_results["sex"] = sex
            test_results["yaku_age_mannenrei"] = yaku_age
            test_results["yaku_age_kazoedoshi"] = yaku_age - offset
            test_results["window"] = window
            test_results["offset"] = offset
            results.append(test_results)

    return results


def format_results_table(results: list[dict]) -> str:
    """Format results as a readable text table."""
    lines = []
    lines.append("=" * 100)
    lines.append("LOCAL COMPARISON ANALYSIS: Yakudoshi age mortality vs. neighboring ages")
    lines.append("=" * 100)
    lines.append("")

    header = (
        f"{'Sex':<8} {'Age(M)':<8} {'Age(K)':<8} {'Window':<8} "
        f"{'Median':<10} {'95% CI':<18} {'Wilcoxon p':<12} {'Perm p':<10} {'Cohen d':<10} {'N':<5}"
    )
    lines.append(header)
    lines.append("-" * 100)

    for r in results:
        ci_str = f"[{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]"
        wilcoxon_str = f"{r['wilcoxon_p']:.4f}" if r["wilcoxon_p"] is not None else "N/A"
        line = (
            f"{r['sex']:<8} {r['yaku_age_mannenrei']:<8} {r['yaku_age_kazoedoshi']:<8} "
            f"±{r['window']:<7} {r['median_ratio']:<10.4f} {ci_str:<18} "
            f"{wilcoxon_str:<12} {r['perm_p']:<10.4f} {r['cohens_d']:<10.4f} {r['n_years']:<5}"
        )
        lines.append(line)

    lines.append("")
    lines.append("Interpretation:")
    lines.append("  Ratio > 1.0 = higher mortality at yakudoshi age than neighbors")
    lines.append("  Ratio < 1.0 = lower mortality at yakudoshi age than neighbors")
    lines.append("  Ratio ≈ 1.0 = no difference (null hypothesis)")
    lines.append("  Alpha = 0.05 (two-sided)")
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running main analysis (window=±3, offset=-1)...")
    results = run_main_analysis(window=3, offset=-1)

    table = format_results_table(results)
    print(table)

    # Save results
    output_path = OUTPUT_DIR / "results_main.txt"
    with open(output_path, "w") as f:
        f.write(table)
    print(f"Saved: {output_path}")

    # Save raw results as JSON
    json_path = OUTPUT_DIR / "results_main.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {json_path}")
