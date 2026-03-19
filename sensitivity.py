"""Sensitivity analyses and Poisson regression (supplementary analysis)."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from analysis import format_results_table, run_main_analysis
from data_loader import load_analysis_data
from definitions import get_yakudoshi_ages

OUTPUT_DIR = Path(__file__).parent / "output"


def run_poisson_regression(offset: int = -1, include_mae_ato: bool = False) -> dict:
    """Run Poisson regression as a supplementary model-based analysis.

    Model: log(Deaths) = log(Exposure) + poly(Age, 5) + Yakudoshi + Year_trend

    Returns:
        Dictionary with IRR, 95% CI, p-value for the yakudoshi indicator.
    """
    df = load_analysis_data()
    results = {}

    for sex in ("male", "female"):
        sex_df = df[(df["sex"] == sex) & (df["age"] >= 15) & (df["age"] <= 80)].copy()
        sex_df = sex_df[sex_df["exposure"] > 0].copy()

        yaku_ages = get_yakudoshi_ages(sex, offset=offset, include_mae_ato=include_mae_ato)
        sex_df["yakudoshi"] = sex_df["age"].isin(yaku_ages).astype(int)
        sex_df["log_exposure"] = np.log(sex_df["exposure"])

        # Polynomial age terms (degree 5)
        age_centered = sex_df["age"] - sex_df["age"].mean()
        for deg in range(1, 6):
            sex_df[f"age_poly{deg}"] = age_centered ** deg

        # Year trend (linear)
        sex_df["year_centered"] = sex_df["year"] - sex_df["year"].mean()

        feature_cols = [f"age_poly{d}" for d in range(1, 6)] + ["year_centered", "yakudoshi"]
        X = sm.add_constant(sex_df[feature_cols])
        y = sex_df["deaths"]

        model = sm.GLM(y, X, family=sm.families.Poisson(), offset=sex_df["log_exposure"])
        fit = model.fit()

        beta = fit.params["yakudoshi"]
        se = fit.bse["yakudoshi"]
        irr = np.exp(beta)
        ci_lower = np.exp(beta - 1.96 * se)
        ci_upper = np.exp(beta + 1.96 * se)
        p_value = fit.pvalues["yakudoshi"]

        # Overdispersion check
        deviance = fit.deviance
        df_resid = fit.df_resid
        dispersion = deviance / df_resid

        results[sex] = {
            "irr": round(float(irr), 4),
            "ci_lower": round(float(ci_lower), 4),
            "ci_upper": round(float(ci_upper), 4),
            "p_value": round(float(p_value), 4) if p_value >= 0.0001 else "<0.0001",
            "beta": round(float(beta), 4),
            "se": round(float(se), 4),
            "deviance_df_ratio": round(float(dispersion), 2),
            "n_obs": len(sex_df),
            "include_mae_ato": include_mae_ato,
        }

    return results


def run_sensitivity_analyses() -> dict:
    """Run all 5 sensitivity analyses defined in the PLAN.

    1. Kazoedoshi offset: -1 vs -2
    2. Include mae-yaku and ato-yaku
    3. Window size: ±2, ±3, ±5
    4. Time period subsets
    5. Age range restriction (20-70)
    """
    all_results = {}

    # SA1: Kazoedoshi offset -2
    print("  SA1: Kazoedoshi offset -2...")
    all_results["sa1_offset_minus2"] = run_main_analysis(window=3, offset=-2)

    # SA2: Include mae-yaku and ato-yaku (via Poisson regression)
    print("  SA2: Include mae-yaku/ato-yaku (Poisson)...")
    all_results["sa2_mae_ato_poisson"] = run_poisson_regression(offset=-1, include_mae_ato=True)

    # SA3: Window sizes ±2 and ±5
    print("  SA3: Window ±2...")
    all_results["sa3_window2"] = run_main_analysis(window=2, offset=-1)
    print("  SA3: Window ±5...")
    all_results["sa3_window5"] = run_main_analysis(window=5, offset=-1)

    # SA4: Time period subsets
    df = load_analysis_data()
    periods = {
        "1947-1970": (1947, 1970),
        "1971-2000": (1971, 2000),
        "2001-2024": (2001, 2024),
    }
    all_results["sa4_periods"] = {}
    for period_name, (start, end) in periods.items():
        print(f"  SA4: Period {period_name}...")
        period_df = df[(df["year"] >= start) & (df["year"] <= end)]
        period_results = []
        for sex in ("male", "female"):
            yaku_ages = get_yakudoshi_ages(sex, offset=-1)
            for yaku_age in yaku_ages:
                from analysis import compute_local_ratios, test_ratio_distribution
                ratios_df = compute_local_ratios(period_df, sex, yaku_age, window=3)
                ratios = ratios_df["ratio"].values
                test_results = test_ratio_distribution(ratios)
                test_results["sex"] = sex
                test_results["yaku_age_mannenrei"] = yaku_age
                test_results["yaku_age_kazoedoshi"] = yaku_age + 1
                test_results["window"] = 3
                test_results["offset"] = -1
                period_results.append(test_results)
        all_results["sa4_periods"][period_name] = period_results

    # SA5: Age range restriction (20-70)
    print("  SA5: Age range 20-70...")
    restricted_df = df[(df["age"] >= 20) & (df["age"] <= 70)]
    sa5_results = []
    for sex in ("male", "female"):
        yaku_ages = get_yakudoshi_ages(sex, offset=-1)
        yaku_ages = [a for a in yaku_ages if 20 <= a <= 70]
        for yaku_age in yaku_ages:
            from analysis import compute_local_ratios, test_ratio_distribution
            ratios_df = compute_local_ratios(restricted_df, sex, yaku_age, window=3)
            ratios = ratios_df["ratio"].values
            test_results = test_ratio_distribution(ratios)
            test_results["sex"] = sex
            test_results["yaku_age_mannenrei"] = yaku_age
            test_results["yaku_age_kazoedoshi"] = yaku_age + 1
            test_results["window"] = 3
            test_results["offset"] = -1
            sa5_results.append(test_results)
    all_results["sa5_age_restricted"] = sa5_results

    return all_results


def format_sensitivity_report(sa_results: dict, poisson_results: dict) -> str:
    """Format all results into a comprehensive summary report."""
    lines = []

    # Main analysis header
    lines.append("=" * 100)
    lines.append("COMPREHENSIVE RESULTS SUMMARY")
    lines.append("=" * 100)
    lines.append("")

    # Poisson regression
    lines.append("-" * 100)
    lines.append("SUPPLEMENTARY: Poisson Regression (hon-yaku only, offset=-1)")
    lines.append("-" * 100)
    lines.append(f"{'Sex':<10} {'IRR':<10} {'95% CI':<22} {'p-value':<12} {'Deviance/df':<14} {'N obs':<8}")
    for sex in ("male", "female"):
        r = poisson_results[sex]
        ci = f"[{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]"
        lines.append(f"{sex:<10} {r['irr']:<10.4f} {ci:<22} {str(r['p_value']):<12} {r['deviance_df_ratio']:<14} {r['n_obs']:<8}")
    lines.append("")
    lines.append("NOTE: Deviance/df >> 1 indicates overdispersion. Poisson CIs may be too narrow.")
    lines.append("")

    # SA1: Offset -2
    lines.append("-" * 100)
    lines.append("SA1: Kazoedoshi offset = -2 (instead of -1)")
    lines.append("-" * 100)
    lines.append(format_results_table(sa_results["sa1_offset_minus2"]))

    # SA2: Mae-ato
    lines.append("-" * 100)
    lines.append("SA2: Including mae-yaku + ato-yaku (Poisson regression)")
    lines.append("-" * 100)
    r2 = sa_results["sa2_mae_ato_poisson"]
    lines.append(f"{'Sex':<10} {'IRR':<10} {'95% CI':<22} {'p-value':<12}")
    for sex in ("male", "female"):
        r = r2[sex]
        ci = f"[{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]"
        lines.append(f"{sex:<10} {r['irr']:<10.4f} {ci:<22} {str(r['p_value']):<12}")
    lines.append("")

    # SA3: Windows
    for w, key in [(2, "sa3_window2"), (5, "sa3_window5")]:
        lines.append("-" * 100)
        lines.append(f"SA3: Window = ±{w}")
        lines.append("-" * 100)
        lines.append(format_results_table(sa_results[key]))

    # SA4: Time periods
    for period_name, period_results in sa_results["sa4_periods"].items():
        lines.append("-" * 100)
        lines.append(f"SA4: Period {period_name}")
        lines.append("-" * 100)
        lines.append(format_results_table(period_results))

    # SA5: Age restricted
    lines.append("-" * 100)
    lines.append("SA5: Age range restricted to 20-70")
    lines.append("-" * 100)
    lines.append(format_results_table(sa_results["sa5_age_restricted"]))

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running Poisson regression...")
    poisson_results = run_poisson_regression(offset=-1, include_mae_ato=False)
    for sex, r in poisson_results.items():
        print(f"  {sex}: IRR={r['irr']}, 95%CI=[{r['ci_lower']}, {r['ci_upper']}], p={r['p_value']}, deviance/df={r['deviance_df_ratio']}")

    print("\nRunning sensitivity analyses...")
    sa_results = run_sensitivity_analyses()

    print("\nFormatting report...")
    report = format_sensitivity_report(sa_results, poisson_results)

    output_path = OUTPUT_DIR / "results_summary.txt"
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nSaved: {output_path}")

    # Save all raw results
    json_path = OUTPUT_DIR / "results_all.json"
    with open(json_path, "w") as f:
        json.dump({"poisson": poisson_results, "sensitivity": sa_results}, f, indent=2, default=str)
    print(f"Saved: {json_path}")
