# Review Report: Yakudoshi and Mortality

Date: 2026-03-19
System: Asura(Sonnet x3) + Monju(Opus x1)

## Critical Findings (P1)

None.

## Important Findings (P2)

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 1 | B-08 | 7 yakudoshi ages tested without multiple comparison correction or justification | Asura(3/3) | Add justification in Methods (null results make correction conservative — strengthens conclusion) |
| 2 | C-03 | No ethics approval/exemption number; self-asserted exemption only | Asura(3/3) | Add explicit statement that no IRB waiver document was obtained due to use of publicly available aggregate data |
| 3 | B-05 | 5th-degree polynomial choice not justified (no AIC/BIC comparison) | Asura(2/3) | Add brief justification or AIC comparison |
| 4 | B-04 | Poisson overdispersion assessed by deviance/df heuristic only; no formal test | Asura(2/3) | Add note that deviance/df >> 1 is sufficient given values of 90-114 |
| 5 | D-02 | Ref [10] publisher/year mismatch: 1985 original = Tokyodo Shuppan, Kodansha Gakujutsu Bunko edition = 2009 | Monju-independent | Fix reference: either cite 1985 Tokyodo or 2009 Kodansha edition |

## Minor Findings (P3)

| # | ID | Issue | Source | Action Required |
|---|-----|-------|--------|----------------|
| 6 | C-10 | ICMJE COI form not mentioned | Asura(3/3) | Add "per ICMJE guidelines" or similar |
| 7 | C-14 | Code repository URL is placeholder | Asura(3/3) | Replace after git push |
| 8 | E-04 | Figure 1 not referenced in text; Figures 2,3 only | Asura(3/3) | Add Figure 1 reference or renumber |
| 9 | B-20 | No outlier handling described | Asura(3/3) | Add brief statement (Wilcoxon is robust) |
| 10 | B-19 | No AIC/BIC for Poisson model | Asura(2/3) | Optional: add to supplementary |
| 11 | C-01 | Helsinki Declaration not mentioned | Asura(2/3) | Add reference or state N/A for aggregate data |
| 12 | E-03 | IRR undefined in Abstract | Asura(2/3) | Spell out "incidence rate ratio (IRR)" in Abstract |
| 13 | A-12 | No sample size/power justification | Asura(2/3) | Discussion already mentions "statistical power that far exceeds..."; add brief note in Methods |
| 14 | A-16 | SA1 male age 23 finding not labeled "exploratory" | Asura(2/3), Monju partial | Add "exploratory" label |
| 15 | D-02 | Ref [11] date: survey Dec 2016, publication Feb 2017 | Monju-independent | Change "2016 Dec" to "2017 Feb" or "2017" |
| 16 | B-25 | Female age 32 CI upper bound 1.0002 rounded to 1.000 | Monju-independent | Consider reporting as 1.000 (3dp) — acceptable but note |
| 17 | E-05 | Figure captions not in manuscript.md | Monju-independent | Add figure captions |
| 18 | D-08 | Ref [6] is NBER Working Paper (not peer-reviewed), no annotation | Monju-independent | Add "Working Paper" or note in text |
| 19 | B-24 | SA4/SA5 quantitative results sparse in text | Asura(1/3), Monju partial | Consider supplementary table |
| 20 | B-06 | alpha=0.05 stated only for Wilcoxon | Asura(1/3) | Minor: add to general statistical methods |

## Rejected by Monju

| # | Asura Finding | Rejection Reason |
|---|--------------|-----------------|
| 14 | A-22: Female 32 CI > 1.0 contradicts "all opposite direction" | The claim is about significant findings' point estimates, not CI bounds. CI crossing 1.0 is normal for P=0.006 |
| 18 | C-12: Sponsor absence not explicitly stated | "No external funding" is sufficient and standard |

## Review Statistics

- Asura: 49 items x 3 agents, 18 unique findings (13 after 2/3 filter)
- Monju verification: ACCEPT 15 / REJECT 2 (+ 1 partial accept)
- Monju independent: 6 findings (1 P2, 5 P3)
- Pre-processing: CrossRef run (PASS 10, MANUAL 1, FAIL 0)
- Numerical verification: All manuscript values match output files within rounding
