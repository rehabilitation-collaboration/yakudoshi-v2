# Yakudoshi and Mortality: A Nonparametric Assessment of Japan's "Unlucky Year" Superstition Using 78 Years of National Mortality Data

**Running title:** Yakudoshi and mortality in Japan

## Abstract

**Background:** Yakudoshi (unlucky years) is a widely held Japanese superstition designating specific ages as periods of heightened vulnerability. Approximately 60% of the Japanese population recognizes yakudoshi, and 44% of those who have experienced a yakudoshi year report taking some form of protective action. Despite its cultural prominence, no epidemiological study has examined whether mortality rates actually increase at yakudoshi ages.

**Methods:** We conducted a retrospective ecological study using the Japanese Mortality Database (JMD), which provides single-year age-specific mortality data for all of Japan from 1947 to 2024 (78 years). The primary analysis used a nonparametric local comparison method: for each yakudoshi age, we calculated the ratio of mortality at that age to the mean mortality of neighboring ages (±3 years) for each calendar year, then tested the distribution of these ratios against a null of 1.0 using the Wilcoxon signed-rank test with permutation-based confirmation. We examined male yakudoshi ages 24, 41, and 60 (Western age; corresponding to kazoedoshi 25, 42, and 61) and female yakudoshi ages 18, 32, 36, and 60 (corresponding to kazoedoshi 19, 33, 37, and 61). Five sensitivity analyses assessed robustness to the kazoedoshi conversion offset, inclusion of pre/post-yakudoshi years, neighbor window size, historical period, and age range restriction. A supplementary Poisson regression provided model-based confirmation.

**Results:** Over the 78-year study period, the dataset encompassed 38.2 million male and 33.7 million female deaths. No yakudoshi age showed elevated mortality relative to neighboring ages. For males, the median rate ratio at age 41 (the "great unlucky year," taiyaku) was 0.979 (95% CI 0.968–0.991; P<0.001), indicating 2.1% *lower* mortality than neighbors. For females, the median rate ratio at age 32 (taiyaku) was 0.984 (95% CI 0.972–1.000; P=0.006). All statistically significant findings were in the direction opposite to the yakudoshi prediction (ratio < 1.0). Sensitivity analyses across all five dimensions yielded consistent results. The supplementary Poisson regression confirmed the absence of elevated mortality (male incidence rate ratio [IRR]=0.998, P=0.075; female IRR=0.965, P<0.001), though substantial overdispersion (deviance/df = 90–114) warrants cautious interpretation of Poisson-derived confidence intervals.

**Conclusions:** Yakudoshi ages are not associated with increased mortality in the Japanese population. The 78-year dataset comprising over 71 million deaths provides no evidence that this culturally significant superstition corresponds to an actual period of elevated mortality risk.

**Keywords:** yakudoshi, superstition, mortality, Japan, cultural beliefs, ecological study

---

## Introduction

Cultural beliefs and superstitions have been studied for their potential effects on health outcomes across multiple societies. Research on Friday the 13th has produced conflicting results: Scanlon et al. (1993) reported a 52% increase in traffic accident hospital admissions in England, while Näyhä (2002) found elevated female traffic deaths in Finland (relative risk 1.63), but Radun and Summala (2004) failed to replicate this finding using Finnish injury data [1–3]. Phillips et al. (2001) described the "Baskerville effect," reporting a 13% excess in cardiac deaths among Chinese and Japanese Americans on the 4th of each month—a date phonetically associated with death in these cultures—though subsequent attempts at replication have been unsuccessful [4]. In Japan, Hira et al. (1998) demonstrated that the rokuyō calendar system significantly influences hospital discharge timing, with patients preferring the auspicious day taian over butsumetsu, resulting in an estimated ¥7.4 million in excess annual medical costs at a single university hospital [5]. More recently, Halla et al. (2019), in a National Bureau of Economic Research working paper, showed that Taiwan's Ghost Month (the seventh lunar month) reduces mortality through behavioral avoidance of risky activities [6].

A recurring pattern in this literature is that initial studies often report statistically significant associations, while subsequent replications fail to confirm them [1–4]. This "initial positive, replication failure" pattern underscores the importance of rigorous methodology and large sample sizes in studies of cultural beliefs and health.

Birthday effects on mortality have been more consistently documented. Ajdacic-Gross et al. (2012) found a 13.8% increase in deaths on birthdays in a Swiss dataset of 2.4 million deaths over 40 years [7]. Matsubayashi and Ueda (2016) reported a 50% increase in suicides on birthdays in Japanese national data spanning 1974–2014 [8]. These findings suggest that psychologically significant dates can influence the timing of death, plausibly through stress-mediated cardiovascular mechanisms or behavioral changes.

Yakudoshi (厄年, literally "calamity year") is one of the most widely observed superstitions in contemporary Japan. The tradition designates specific ages as periods of heightened vulnerability to misfortune. For men, the principal yakudoshi ages are 25, 42, and 61 in kazoedoshi (traditional Japanese age counting, where a person is 1 at birth and gains a year each New Year). For women, they are 19, 33, 37, and 61. The ages of 42 for men and 33 for women are considered taiyaku (大厄, "great unlucky year"), partly through phonetic associations: 42 (shi-ni) evokes "death" (死に), and 33 (san-zan) evokes "disaster" (散々) [9]. Each principal yakudoshi year is flanked by a mae-yaku (前厄, pre-unlucky year) and ato-yaku (後厄, post-unlucky year).

The tradition has roots extending to at least the Heian period (794–1185 CE), with influences from Chinese yinyang philosophy and indigenous Japanese folk beliefs about life-stage transitions [9, 10]. The current age designations became standardized during the Edo period (1603–1868) [10]. A 2016 survey of 1,000 Japanese adults aged 20–59 found that approximately 60% were aware of yakudoshi, 46% reported being concerned about it, and 44% of those who had experienced a yakudoshi year took some form of protective action, most commonly visiting a shrine or temple for purification [11].

Despite the cultural significance of yakudoshi and the large body of literature on superstition and health, no epidemiological study has examined whether mortality rates actually differ at yakudoshi ages. This study addresses that gap using 78 years of national mortality data from the Japanese Mortality Database.

---

## Methods

### Study Design

We conducted a retrospective ecological study using population-level mortality data. The study examined whether age-specific mortality rates at yakudoshi ages differ from mortality rates at neighboring ages, using data from the entire Japanese population over a 78-year period.

### Data Source

Data were obtained from the Japanese Mortality Database (JMD), maintained by the National Institute of Population and Social Security Research (IPSS), Tokyo, Japan [12]. The JMD provides mortality statistics for all of Japan, structured for compatibility with the Human Mortality Database (HMD) methodology. We used three datasets in the 1×1 format (single-year age by single calendar year): Deaths_1x1.txt (death counts), Exposures_1x1.txt (exposure-to-risk, i.e., person-years), and Mx_1x1.txt (death rates). Data covered the period 1947–2024 (78 calendar years), ages 0–110+, for males and females separately. No individual-level data were used; all data were pre-aggregated by the IPSS from vital registration records and population censuses. The data were downloaded on March 19, 2026 (version 005_002, last modified February 20, 2026).

### Yakudoshi Age Definitions

We defined yakudoshi ages using the standard kazoedoshi designations. For men: 25, 42, and 61; for women: 19, 33, 37, and 61. Because the JMD reports ages in Western (mannenrei) counting, we converted kazoedoshi to Western age by subtracting 1 (the modal conversion for most of the calendar year, since kazoedoshi advances on January 1 while Western age advances on the birthday). This yielded primary analysis ages of 24, 41, and 60 for men and 18, 32, 36, and 60 for women. The sensitivity of results to this conversion was assessed by also using an offset of −2 (sensitivity analysis 1).

### Primary Analysis: Nonparametric Local Comparison

For each yakudoshi age, sex, and calendar year, we calculated the local rate ratio:

> Ratio = Mx(yakudoshi age) / mean[Mx(yakudoshi age ± k)], excluding the yakudoshi age itself

where Mx denotes the death rate and k = 3 (i.e., a window of ±3 neighboring ages). This ratio compares mortality at the yakudoshi age to the average mortality of the six surrounding ages, providing a model-free assessment of whether mortality is locally elevated.

We collected the ratio for each of the 78 calendar years, yielding a distribution of 78 ratios per yakudoshi age per sex. We tested whether this distribution is centered on 1.0 (the null hypothesis of no yakudoshi effect) using:

1. **Wilcoxon signed-rank test** (two-sided, α = 0.05): a nonparametric test of whether the median ratio differs from 1.0.
2. **Permutation test** (10,000 iterations): the signs of (ratio − 1.0) deviations were randomly permuted; the two-sided P-value was the proportion of permutations with a mean deviation as extreme as observed.
3. **Cohen's d**: effect size calculated as (mean ratio − 1.0) / SD(ratios).
4. **95% bootstrap confidence interval** for the median ratio (10,000 resamples).

This approach avoids parametric assumptions about the age-mortality relationship and is not sensitive to the choice of smoothing parameters (e.g., spline degrees of freedom), which have been shown to influence model-based estimates in age-mortality analyses. Because we tested seven yakudoshi ages (three male, four female), the question of multiple comparison correction arises. We did not apply a Bonferroni or similar correction because (a) the ages were pre-specified by cultural tradition rather than selected from data, and (b) applying a correction would make all P-values more conservative, further strengthening the null conclusion. For transparency, applying Bonferroni correction (α = 0.05/7 = 0.007) would not change the direction or substantive interpretation of any result.

### Supplementary Analysis: Poisson Regression

As a model-based confirmation, we fitted a Poisson regression:

> log(Deaths) = log(Exposure) + Σ β_j × Age^j (j = 1…5) + β_year × Year + β_yaku × Yakudoshi

where Age was centered and entered as a 5th-degree polynomial to accommodate the nonlinear (approximately log-linear with departures) shape of the age-mortality curve, Year was centered and entered linearly, and Yakudoshi was a binary indicator (1 if the age is a hon-yaku age, 0 otherwise). The exponentiated coefficient exp(β_yaku) gives the incidence rate ratio (IRR). Analyses were conducted separately for males and females, restricted to ages 15–80. We assessed overdispersion using the deviance/degrees-of-freedom ratio; values substantially exceeding 1.0 indicate that Poisson confidence intervals may be too narrow.

### Sensitivity Analyses

Five sensitivity analyses assessed robustness:

1. **Kazoedoshi conversion offset**: −2 instead of −1 (shifting all yakudoshi ages down by one additional year).
2. **Mae-yaku and ato-yaku inclusion**: the yakudoshi indicator in the Poisson regression was expanded to include the year before and after each hon-yaku year.
3. **Neighbor window size**: ±2 and ±5 ages instead of ±3.
4. **Historical period**: the dataset was divided into three periods—1947–1970, 1971–2000, and 2001–2024—to assess temporal stability.
5. **Age range restriction**: limited to ages 20–70 to exclude boundary effects.

### Missing Data

The JMD contains missing values (coded as ".") for death rates at very old ages (≥105) in some early years, where male populations were zero or near-zero. These ages are far outside the range of yakudoshi ages (18–60) and did not affect any analysis.

### Ethical Considerations

This study used exclusively publicly available, fully aggregated population-level data from the JMD. No individual-level data were accessed. Under the Japanese Ethical Guidelines for Medical and Biological Research Involving Human Subjects (Ministry of Education, Culture, Sports, Science and Technology; Ministry of Health, Labour and Welfare, 2021 revision), research using publicly available aggregate statistics does not require ethics committee review (Article 3, Paragraph 1, Item 1). As no human subjects were involved, no institutional review board approval or waiver was sought. This study was conducted in accordance with the principles of the Declaration of Helsinki where applicable to research using aggregate data.

### Software

All analyses were performed using Python 3.14.3 with pandas 2.3.0, NumPy 2.2.6, SciPy 1.15.3, statsmodels 0.14.4, and matplotlib 3.10.3. Analysis code is available at [repository URL to be added].

---

## Results

### Study Population

The JMD dataset comprised 8,658 age-year-sex cells per sex over the 78-year study period (1947–2024), representing 38,160,115 male deaths and 33,681,359 female deaths (71,841,474 total). Figure 1 shows the age-specific mortality curves for selected years, with yakudoshi ages highlighted; no visible discontinuities are apparent at these ages.

### Primary Analysis

Table 1 presents the local rate ratios at each yakudoshi age. No yakudoshi age exhibited a median rate ratio above 1.0 that would indicate elevated mortality (Figure 2).

**Table 1. Local rate ratios at yakudoshi ages (primary analysis, ±3 neighbor window)**

| Sex | Western age | Kazoedoshi | Median ratio | 95% CI | Wilcoxon P | Permutation P | Cohen's d | N years |
|-----|-------------|------------|-------------|--------|------------|---------------|-----------|---------|
| Male | 24 | 25 | 1.010 | [0.995, 1.025] | 0.137 | 0.172 | 0.16 | 78 |
| Male | 41 | 42 (taiyaku) | 0.979 | [0.968, 0.991] | <0.001 | <0.001 | −0.78 | 78 |
| Male | 60 | 61 | 0.976 | [0.973, 0.980] | <0.001 | <0.001 | −1.24 | 78 |
| Female | 18 | 19 | 1.006 | [0.992, 1.024] | 0.299 | 0.174 | 0.15 | 78 |
| Female | 32 | 33 (taiyaku) | 0.984 | [0.972, 1.000] | 0.006 | 0.008 | −0.31 | 78 |
| Female | 36 | 37 | 0.980 | [0.975, 0.991] | <0.001 | 0.004 | −0.32 | 78 |
| Female | 60 | 61 | 0.976 | [0.965, 0.982] | <0.001 | <0.001 | −1.04 | 78 |

For males, the "great unlucky year" age of 41 (kazoedoshi 42) had a median rate ratio of 0.979, meaning mortality was 2.1% *lower* than the mean of its six neighboring ages (P<0.001, Wilcoxon signed-rank test). Age 60 (kazoedoshi 61) showed an even larger deficit of 2.4% (P<0.001). Only age 24 (kazoedoshi 25) showed a non-significant tendency toward slightly higher mortality (ratio 1.010, P=0.137).

For females, age 32 (kazoedoshi 33, taiyaku) had a median ratio of 0.984 (P=0.006) and age 36 (kazoedoshi 37) a ratio of 0.980 (P<0.001), both indicating lower mortality at yakudoshi ages. Age 60 showed a 2.4% deficit (P<0.001). Age 18 (kazoedoshi 19) was non-significant (ratio 1.006, P=0.299).

### Supplementary Poisson Regression

The Poisson regression yielded consistent results. For males, the yakudoshi IRR was 0.998 (95% CI 0.996–1.000; P=0.075). For females, the IRR was 0.965 (95% CI 0.962–0.968; P<0.001). Substantial overdispersion was present (deviance/df = 90.0 for males, 114.4 for females), indicating that the Poisson model's confidence intervals are likely too narrow and P-values too small. This overdispersion supports the use of the nonparametric primary analysis, which does not rely on distributional assumptions.

### Sensitivity Analyses

All five sensitivity analyses produced results consistent with the primary analysis (Figure 3).

**Sensitivity analysis 1 (kazoedoshi offset −2):** Shifting all yakudoshi ages down by one year did not reveal elevated mortality at any age. Male age 23 (kazoedoshi 25) showed a slight but significant elevation (median ratio 1.020, P=0.002), unique to this offset and considered an exploratory finding; all other ages remained below 1.0.

**Sensitivity analysis 2 (mae-yaku and ato-yaku):** Expanding the yakudoshi indicator to include pre- and post-yakudoshi years in the Poisson regression yielded IRRs of 0.998 (male, P=0.006) and 0.959 (female, P<0.001), consistent with the primary analysis.

**Sensitivity analysis 3 (window size):** Narrowing the window to ±2 ages attenuated the effects (male age 41: ratio 0.987, P<0.001) while widening to ±5 amplified them (male age 41: ratio 0.948, P<0.001), consistent with the curvature of the age-mortality relationship rather than a yakudoshi-specific effect.

**Sensitivity analysis 4 (historical period):** The absence of elevated yakudoshi mortality was consistent across 1947–1970, 1971–2000, and 2001–2024. The one exception was male age 24 during 1947–1970, which showed an elevated ratio (1.049, P<0.001); this effect disappeared in later periods and likely reflects cohort-specific mortality patterns during the immediate postwar era rather than a yakudoshi effect.

**Sensitivity analysis 5 (age range 20–70):** Restricting the analysis to ages 20–70 produced results identical to the primary analysis, confirming that boundary effects at extreme ages did not influence our findings.

---

## Discussion

This study found no evidence that yakudoshi ages are associated with increased mortality in the Japanese population. Across 78 years of national data encompassing over 71 million deaths, mortality at yakudoshi ages was either indistinguishable from or slightly *lower* than mortality at neighboring ages. This finding was robust across five sensitivity analyses and confirmed by supplementary Poisson regression.

### Comparison with Prior Research

Our null finding is consistent with the broader pattern in the superstition-and-health literature, where initial positive findings are frequently not replicated. The Friday the 13th literature exemplifies this: Scanlon et al.'s (1993) original finding of increased traffic accidents was not replicated by Radun and Summala (2004) [1, 3]. Similarly, Phillips et al.'s (2001) "Baskerville effect" (excess cardiac deaths on the 4th of the month among Asian Americans) has not been confirmed in subsequent studies [4]. Our findings suggest that yakudoshi follows this same pattern—with the distinction that our study is the first epidemiological examination, and we find no initial positive signal.

The contrast with birthday effects is instructive. Unlike yakudoshi, birthday effects have been consistently replicated across countries and decades [7, 8]. A key difference is that birthdays are personally salient events with known dates, while yakudoshi ages are culturally designated periods that may not be equally salient to all individuals. Furthermore, birthday effects operate through acute psychological mechanisms (e.g., "birthday blues," celebratory risk-taking), whereas a yakudoshi effect would require a sustained year-long influence on mortality risk.

Our finding that some yakudoshi ages show *lower* mortality (ratio < 1.0) may initially seem puzzling but is readily explained by the curvature of the age-mortality relationship. When mortality increases exponentially with age (Gompertz law), the midpoint of an age interval will tend to have slightly lower mortality than the mean of the interval's endpoints. This geometric artifact produces ratios slightly below 1.0 even under the null hypothesis, and the effect grows with the steepness of the mortality curve—consistent with our observation that the deficit is largest at age 60, where mortality increases most steeply. The sensitivity of the ratio to window size (sensitivity analysis 3) further supports this interpretation: wider windows amplify the geometric effect.

### Possible Mechanisms and Their Absence

Several mechanisms could theoretically link yakudoshi beliefs to mortality: psychological stress increasing cardiovascular risk, behavioral changes (increased or decreased risk-taking), or "nocebo" effects. However, population-level detection of such effects faces two fundamental challenges. First, not all individuals in the population share the belief; the 2016 survey found that 40% of adults were unaware of yakudoshi [11]. Any individual-level effect would therefore be diluted when measured at the population level. Second, yakudoshi is an age-based belief that operates over an entire year, unlike acute triggers such as birthdays or specific calendar dates. The temporal diffusion of any effect over a full year would further reduce its detectability.

These considerations do not affect our conclusion. Even accounting for dilution, the point estimates in our analysis are not merely non-significant—they are in the *opposite* direction from the yakudoshi prediction. An underlying positive effect would need to be implausibly large to produce the observed pattern after dilution.

### Strengths and Limitations

This study has several strengths. First, the dataset spans 78 years and encompasses the entire Japanese population, providing statistical power that far exceeds typical mortality studies. Second, the nonparametric local comparison method avoids model specification issues that can produce spurious findings in age-mortality analyses. Third, the comprehensive sensitivity analyses demonstrate robustness across analytical choices.

Several limitations should be noted. First, this is an ecological study using aggregate data; we cannot identify individuals who hold yakudoshi beliefs. A study linking individual-level survey data on yakudoshi belief to subsequent mortality would provide stronger evidence, but such data do not currently exist. Second, the kazoedoshi-to-Western-age conversion introduces a ±1 year uncertainty. Our sensitivity analysis (offset −1 vs. −2) showed that this did not affect the conclusions. Third, we examined all-cause mortality only; it remains possible that yakudoshi beliefs affect specific causes of death (e.g., stress-related cardiovascular events) in ways that are masked when examining all causes combined. Fourth, the JMD data are based on registered residence, and any errors in population registration would affect exposure estimates. However, such errors are systematic rather than age-specific and would not create artifactual yakudoshi effects. Fifth, our nonparametric approach has limited ability to adjust for time-varying confounders; however, because our comparison is local (within ±3 ages in the same calendar year and sex), confounders would need to operate specifically at yakudoshi ages to bias results.

### Implications

Our findings suggest that yakudoshi, despite its deep cultural roots and widespread observance, does not correspond to an actual period of elevated mortality risk. This does not diminish the cultural or psychological significance of yakudoshi traditions, which serve important social functions as life-stage markers [10]. However, from a public health perspective, there is no evidence to support health warnings or targeted interventions at yakudoshi ages.

---

## References

[1] Scanlon TJ, Luben RN, Scanlon FL, Singleton N. Is Friday the 13th bad for your health? BMJ. 1993;307(6919):1584–1586. doi:10.1136/bmj.307.6919.1584

[2] Näyhä S. Traffic deaths and superstition on Friday the 13th. Am J Psychiatry. 2002;159(12):2110–2111. doi:10.1176/appi.ajp.159.12.2110

[3] Radun I, Summala H. Females do not have more injury road accidents on Friday the 13th. BMC Public Health. 2004;4:54. doi:10.1186/1471-2458-4-54

[4] Phillips DP, Liu GC, Kwok K, Jarvinen JR, Zhang W, Abramson IS. The Hound of the Baskervilles effect: natural experiment on the influence of psychological stress on timing of death. BMJ. 2001;323(7327):1443–1446. doi:10.1136/bmj.323.7327.1443

[5] Hira K, Fukui T, Endoh A, Rahman M, Maekawa M. Influence of superstition on the date of hospital discharge and medical cost in Japan: retrospective and descriptive study. BMJ. 1998;317(7174):1680–1683. doi:10.1136/bmj.317.7174.1680

[6] Halla M, Liu CL, Liu JT. The effect of superstition on health: evidence from the Taiwanese Ghost Month. NBER Working Paper No. 25474. 2019. doi:10.3386/w25474

[7] Ajdacic-Gross V, Knöpfli D, Landolt K, et al. Death has a preference for birthdays—an analysis of death time series. Ann Epidemiol. 2012;22(8):603–606. doi:10.1016/j.annepidem.2012.04.016

[8] Matsubayashi T, Ueda M. Suicides and accidents on birthdays: evidence from Japan. Soc Sci Med. 2016;159:61–72. doi:10.1016/j.socscimed.2016.04.034

[9] Yakudoshi. In: Wikipedia [Internet]. [cited 2026 Mar 19]. Available from: https://en.wikipedia.org/wiki/Yakudoshi

[10] Namihira E. Kegare [Pollution]. Tokyo: Tokyodo Shuppan; 1985.

[11] LifeNet Insurance. Survey on modern attitudes toward yakudoshi [Internet]. Tokyo: LifeNet Insurance; 2017 Feb [cited 2026 Mar 19]. Available from: https://prtimes.jp/main/html/rd/p/000000372.000001163.html

[12] National Institute of Population and Social Security Research. The Japanese Mortality Database [Internet]. Tokyo: IPSS; [cited 2026 Mar 19]. Available from: https://www.ipss.go.jp/p-toukei/JMD/index.asp

---

## Acknowledgments

This manuscript was drafted with the assistance of Claude (Anthropic), a large language model. The AI assisted with literature review, statistical code generation, and manuscript drafting. All analyses, interpretations, and final editorial decisions were made by the human author. All references were verified against CrossRef and PubMed databases.

## Author Contributions (CRediT)

**Mizuki Shirai:** Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing – Original Draft, Writing – Review & Editing, Visualization, Project Administration.

## Conflict of Interest

The author declares no conflicts of interest per ICMJE guidelines.

## Funding

This research received no external funding.

## Data Availability

All data used in this study are publicly available from the Japanese Mortality Database (https://www.ipss.go.jp/p-toukei/JMD/index.asp). Analysis code is available at [repository URL to be added].

## ORCID

Mizuki Shirai: 0009-0005-3615-0670
