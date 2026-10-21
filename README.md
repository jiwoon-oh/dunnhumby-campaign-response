# Did Campaign Response Differ by Campaign Type and Prior Spending Level?

[한국어](README.ko.md)

Full case study: https://jiwoon-oh.github.io/portfolio/projects/dunnhumby-customer/case2/

This repository covers the campaign-by-tier analysis, my contribution to a team project. Other hypotheses were handled by other team members.

## Research question

Using Dunnhumby's household transactions and campaign records, I examined whether changes in weekly spending during campaign periods differed across **low-, medium-, and high-spending households**. A comparison of households that received campaigns with those that did not would be misleading: a retailer might send more offers to customers who already spend a lot.

I defined spending tiers using pre-campaign data, built a household-week panel, and estimated campaign-by-tier associations using household and week fixed effects with household-clustered standard errors. I then checked pre-trends, applied a multiple-comparison correction, and ran a placebo-style comparison and a lead-effect test.

**The main finding was a negative association between Type C campaigns and weekly spending among high-spending households.** It survived the multiple-comparison correction. The pooled +242% difference for low spenders (any campaign active versus quiet weeks, no fixed effects) is a different quantity from the fixed-effects estimates, which compare one campaign type with a household's own other weeks; none of the three campaign-type estimates for low spenders under fixed effects is distinguishable from zero (smallest raw p = 0.163). The Type C estimate also cannot be read as a campaign effect. In the four weeks just before a household's first Type C week, its spending was already lower (Lead4 −9.02), though not in weeks five to eight, and I cannot separate how households were selected, anticipation, and the Type A and B campaigns running at that time. I therefore report an association, not a campaign effect.

## 0. Analysis decisions made in advance

| Decision | Reason |
|---|---|
| Fix tiers using Weeks 17–32 | Segmenting on post-campaign spending would introduce look-ahead bias |
| Household fixed effects | Account for persistent differences in average spending between households |
| Week fixed effects | Account for common seasonal and calendar-related changes |
| Cluster standard errors by household | Weekly observations within one household are correlated |
| Use three tiers for the main model and five quintiles as a check | Small campaign-by-tier cells become unstable with too much segmentation |
| Correct nine statistical comparisons | Reduce false discoveries from testing many campaign interactions |

Fixed effects do not remove every type of selection bias. Unobserved factors that change within a household over time and affect both campaign targeting and spending can still influence the estimates.

---

## Step 1. Assign spending tiers before the campaigns begin

The first campaign started in Week 33. I used each household's average weekly spend over **Weeks 17–32** to group the 2,500 households. I kept those assignments unchanged throughout the study.

| Tier | Households | Mean weekly spending | Range |
|---|---:|---:|---:|
| Low | 834 | $3.85 | $0.00–$10.03 |
| Medium | 834 | $20.36 | $10.05–$33.88 |
| High | 832 | $72.75 | $33.88–$378.60 |

There were **142 households (5.7%)** without purchases during this pre-period. Their measured spending was zero, placing them in the lowest tier. This creates a possible floor effect: a household with no recorded activity may behave differently from an otherwise active but low-spending customer.

With five quintiles, mean spending in the top and bottom groups was approximately **$93.14 versus $1.61**, a nearly 58-fold gap. This describes how different the groups were before exposure; it is not evidence of a campaign effect.

## Step 2. Map campaign type and campaign-active weeks

I mapped `START_DAY` and `END_DAY` from `campaign_desc` to weekly periods.

| Item | Result |
|---|---|
| First campaign | Week 33; none started beforehand |
| Last campaign ended | Week 102 |
| Campaigns by type | Type A: 5; Type B: 19; Type C: 6 |
| Distinct Type A recipients | 1,513 |
| Distinct Type B recipients | 1,023 |
| Distinct Type C recipients | 397 |
| Never received any campaign | 916 |
| Received more than one type | 1,008, or 63.6% of recipients |

Type A reached **60.5%** of all 2,500 households, with recipients receiving it an average of **2.63 times**. That is broad reach for something described as a personalized campaign. The content may have been personalized, but its audience was not particularly narrow.

Different campaigns also overlapped. This complicates any attempt to isolate the response to one type.

![Timeline of the 30 campaigns by week: 5 Type A, 19 Type B and 6 Type C campaigns, the first starting in week 33 and two continuing past week 101](images/campaign-timeline.png)

## Step 3. Construct the household-week panel

The main panel covered **Weeks 33–101** and contained **172,500 rows**. Week 102 is not in the panel: the data end on day 711, so that week holds only 6 days of transactions. For each household and week, I aligned spending with indicators for whether each campaign type was active.

### Overlapping exposure

- Among the **1,008 households** receiving multiple types, **869 (86.2%)** experienced at least one week when multiple types overlapped.
- Type A + Type B accounted for **3,530** simultaneous-exposure records, the most common combination.

I therefore checked variance inflation before interpreting a regression containing all campaign-by-tier indicators.

### Pooled comparison of campaign-active and campaign-inactive weeks

A simple comparison of household-weeks in which **any** of the three campaign types was active with household-weeks in which none was, pooled across households and without fixed effects, gave **+242%** for low spenders ($11.54 → $39.49; 2,924 campaign-active versus 54,622 campaign-inactive household-weeks), **+60%** for medium spenders and **+23%** for high spenders ($61.68 → $75.61). These comparisons mix households that differ in their usual spending and do not separate campaign types, so they are not estimates of campaign lift. They are also **not the unadjusted version of the Step 6 estimates**: those compare each household's weeks with a given campaign type active against its own other weeks, one type at a time (the Type C estimate applies to high spenders only).

## Step 4. Check campaign-by-tier sample sizes

| Tier | Type A | Type B | Type C |
|---|---:|---:|---:|
| Low | 187 | 90 | **28** |
| Medium | 554 | 305 | 74 |
| High | 772 | 628 | 295 |

Only 28 low-spending households received Type C. With five spending quintiles, the lowest two Type C cells had only **16 and 25 households**. This confirmed that a three-tier model was more appropriate for the main analysis.

![Heatmap of households receiving each campaign type by spending tier: Type A 187, 554 and 772; Type B 90, 305 and 628; Type C 28, 74 and 295 for low, medium and high spenders, with Type C × Low (28) flagged as below 30](images/sample-heatmap.png)

Targeting was strongly related to pre-campaign spending:

- Campaign reach among low spenders: **25.2%**
- Campaign reach among high spenders: **94.1%**

The retailer was far more likely to contact high-spending customers, so raw recipient/non-recipient comparisons are not credible as causal estimates.

Among the 28 low-spending Type C households, two had zero pre-campaign spending (7.1%). This limits one particular floor-effect concern but does not solve the small-cell problem.

![Share of households receiving a campaign by baseline spending tier: 25.2% low, 70.9% medium and 94.1% high; Type C reached 3.4%, 8.9% and 35.5%](images/reach-rate.png)

### Multicollinearity check: VIF

| Predictors | VIF range |
|---|---:|
| Three campaign activity indicators | 1.06–1.09 |
| Nine Type × tier interaction indicators | 1.02–1.12 |

Although overlapping types were common among multi-type recipients, simultaneously active campaigns appeared in only **4.1%** of all panel rows. The large share of rows without simultaneous exposure helps explain the low pooled VIF values.

I did not find serious linear multicollinearity in this specification. Low VIF does **not** resolve treatment-selection or overlapping-campaign interpretation issues.

## Step 5. Check pre-campaign trends

Before using post-campaign differences, I tested whether future recipients and non-recipients were already following different spending trends during **Weeks 17–32**.

During this step I found a denominator error: counting only households with observed purchases dropped the **142 zero-spending households**. I corrected the denominator to all **2,500 households** and repeated the test.

| Comparison | Trend interaction | p-value | Interpretation |
|---|---:|---:|---|
| Full sample | 0.296 | 0.087 | Not significant at 5%; borderline at 10% |
| Low spenders | 0.025 | 0.764 | No detected difference |
| Medium spenders | 0.308 | 0.053 | Just above 5% |
| High spenders | 0.333 | 0.613 | Low power; only 49 controls |

This was not a clean confirmation of parallel trends. The full sample and medium tier were borderline, while the high-tier comparison was based on a small number of controls. A pre-trend test that is not significant does not establish that the trends truly match.

![Weekly mean spending of future recipients and non-recipients in weeks 17–32 for low, medium and high spenders; the high-spender comparison group has only 49 households, and the trend-difference p-values are 0.764, 0.053 and 0.613](images/pretrend.png)

## Step 6. Two-way fixed-effects model

Weekly household spending was regressed on the nine campaign-by-tier indicators, household fixed effects, and week fixed effects.

```text
weekly_spend ~ TypeA × (low, medium, high)
             + TypeB × (low, medium, high)
             + TypeC × (low, medium, high)
             + household fixed effects
             + week fixed effects
```

I clustered standard errors at the household level because multiple observations from the same household are not independent.

| Diagnostic | Result | Interpretation |
|---|---|---|
| Within R² | 0.0004 | Campaign indicators explain very little within-household weekly variation |
| Poolability F-test | 38.138, `p < 0.0001` | Supports accounting for fixed effects |
| F-test without clustering | 11.544, `p < 0.0001` | Treats within-household errors more optimistically |
| F-test with household clustering | 2.313, `p = 0.0135` | Less overstated significance after allowing dependence |

The F-statistic is lower with household clustering than without it, so unclustered standard errors would overstate significance given the repeated measures within households.

### All nine campaign-by-tier estimates

| Campaign type | Spending tier | Households | Coefficient | Clustered SE | 95% CI | Raw p | BH-adjusted p |
|---|---|---:|---:|---:|---|---:|---:|
| Type A | Low | 187 | 1.06 | 1.43 | [−1.75, 3.86] | 0.4607 | 0.8055 |
| Type A | Medium | 554 | 0.82 | 0.69 | [−0.53, 2.17] | 0.2333 | 0.5249 |
| Type A | High | 772 | −0.16 | 0.77 | [−1.68, 1.35] | 0.8337 | 0.8337 |
| Type B | Low | 90 | 1.44 | 2.34 | [−3.14, 6.02] | 0.5370 | 0.8055 |
| Type B | Medium | 305 | 0.42 | 1.36 | [−2.25, 3.09] | 0.7591 | 0.8337 |
| Type B | High | 628 | −2.43 | 0.97 | [−4.32, −0.54] | 0.0118 | 0.0532 |
| Type C | Low | 28† | 9.68 | 6.94 | [−3.93, 23.28] | 0.1633 | 0.4898 |
| Type C | Medium | 74 | −1.22 | 4.36 | [−9.77, 7.33] | 0.7798 | 0.8337 |
| **Type C** | **High** | 295 | **−6.25** | 1.76 | [−9.70, −2.81] | 0.0004 | **0.0033** |

Coefficients are dollars of weekly spending per household-week with the campaign type active, relative to the household's other weeks. Intervals are 95% intervals **without** multiple-comparison correction; seven of the nine include zero. Only the bold row remains significant after Benjamini–Hochberg correction. † Fewer than 30 households; read as reference only.

### Two interactions with unadjusted p-values below 0.05

| Interaction | Coefficient | Raw p-value | Households | Relative to baseline spend |
|---|---:|---:|---:|---:|
| **Type C × high spenders** | **−6.25** | **0.0004** | 295 | approximately **−8.6%** |
| Type B × high spenders | −2.43 | 0.0118 | 628 | approximately −3.3% |

The other seven comparisons did not pass the 5% threshold. Type C × low spenders, for example, had only 28 households and `p = 0.163`; its estimated coefficient should not be read without its uncertainty.

The pooled comparison in Step 3 and the fixed-effects estimates are different quantities, so they should not be read as the same group before and after adjusting for fixed effects. The pooled comparison pools every active week of any campaign type within a tier; the fixed-effects model compares a household's Type C weeks with its own other weeks, holding week effects and the other campaign types fixed. Showing what fixed effects change for one group would need a model with a single "any campaign" indicator per tier, which I did not estimate. The estimates do not prove that fixed effects removed all targeting bias.

![Fixed-effects coefficients with 95% confidence intervals for the nine campaign type by spending tier combinations: seven of the nine intervals include zero, and only Type C × High (−6.25, 295 households) passes the Benjamini–Hochberg correction](images/forest-plot.png)

## Step 7. Multiple-comparison correction for nine interactions

Testing nine hypotheses raises the risk of chance discoveries. I used the Benjamini–Hochberg procedure to control the false discovery rate.

| Rank | Interaction | Raw p | BH threshold | Adjusted p | Result |
|---|---|---:|---:|---:|---|
| 1 | Type C × high | 0.000371 | 0.00556 | **0.0033** | Remains significant |
| 2 | Type B × high | 0.011832 | 0.01111 | 0.0532 | No longer below 0.05 |

**Only Type C × high spenders** remained statistically significant after correcting for nine comparisons. Type B × high is an exploratory finding, not a confirmed second result.

![Raw and Benjamini–Hochberg-adjusted p-values for the nine combinations: only Type C × High stays below 0.05 (0.0004 raw, 0.0033 adjusted), while Type B × High moves from 0.0118 to 0.0532](images/bh-correction.png)

## Step 8. Non-recipient comparison and lead-effect test

There is a competing explanation for the negative Type C result. The retailer might have sent Type C specifically to high-spending households **whose purchases were already declining**. If so, the timing of the campaign would coincide with the decline without causing it. I ran two checks: a comparison among households that never received a campaign, and a lead-effect test on the weeks just before each household's first Type C week.

### Early-versus-late spending among non-recipients

I used the **916 households that never received a campaign**.

| Tier | Mean, Weeks 33–42 | Mean, Weeks 92–101 | Change |
|---|---:|---:|---:|
| Low | $4.61 | $12.25 | +165.5% |
| Medium | $11.27 | $17.33 | +53.8% |
| High | $43.96 | $43.54 | −1.0% |

Average high-tier spending was nearly flat in this descriptive comparison. But there were only **49 high-spending non-recipient households**, making it difficult to distinguish different plausible explanations.

### Placebo-style regression among non-recipients

| Term (among non-recipients) | Coefficient | p-value | 95% CI | Households in tier |
|---|---:|---:|---|---:|
| Medium × later period | 0.05 | 0.9510 | [−1.60, 1.70] | 243 |
| High × later period | −4.74 | 0.2609 | [−13.00, 3.52] | 49 |

These coefficients are measured **against the low tier**, and week fixed effects absorb the change common to everyone. Each one is the later-period change of that tier minus the later-period change of low spenders (weeks 67–101 versus earlier weeks). Low-spending non-recipients rose by 165.5% above, so much of the High × later period coefficient can come from low-tier growth rather than from a high-tier decline. It is **not the same quantity as the Step 6 estimate**, which compares a household's Type C weeks with its own other weeks, so I do not compare the two numbers.

### Lead-effect test: spending just before the first Type C week

This test uses the same households and the same kind of comparison as Step 6. For the 295 high-spending households that received Type C, I added two indicators to the main model: **Lead4** (the four weeks before a household's first Type C week) and **Lead8** (weeks five to eight before it). They are estimated with household and week fixed effects, household-clustered standard errors and the same nine campaign-by-tier indicators, so Type A and B activity is controlled as in Step 6. I fixed the reading rule before running it: a 95% interval that includes zero means no evidence of a pre-existing decline; a negative coefficient whose interval excludes zero means reverse targeting is possible.

| Term | Coefficient | Clustered SE | 95% CI | p-value | Households | Reading |
|---|---:|---:|---|---:|---:|---|
| Lead4 (weeks −4 to −1) | **−9.02** | 2.26 | [−13.46, −4.58] | <0.0001 | 295 | Reverse targeting is possible |
| Lead8 (weeks −8 to −5) | −1.69 | 2.11 | [−5.82, 2.44] | 0.4233 | 286 | No evidence of a pre-existing decline |

Spending in the four weeks just before a household's first Type C week was about $9.02 lower per week than in its other weeks, with an interval that excludes zero. The weeks five to eight before showed no detectable difference. The two lead coefficients together differ from zero (joint Wald test p = 0.0003). With the leads included, the Type C × high coefficient is −7.12 (95% CI [−10.75, −3.48]) rather than −6.25. I ran two tests and did not adjust for multiple comparisons.

Limitation: 260 of the 295 households had a Type A or B campaign active in the Lead4 weeks (82% of those household-weeks), so a dip before Type C cannot be separated from anticipation or from the effect of those campaigns. For 9 households the lead windows begin before Week 33, outside the panel.

![Coefficients with 95% intervals around the first Type C week: −1.69 for weeks 5–8 before (interval includes zero), −9.02 for weeks 1–4 before (interval excludes zero), and −7.12 for Type C weeks with the lead weeks included](images/lead-effect.png)

## Additional robustness check: first versus repeat exposure

I separated initial Type C exposure from repeat exposure within the high-spending group.

| Exposure | Households | Coefficient | p-value |
|---|---:|---:|---:|
| First exposure | 295 | −4.89 | 0.009 |
| Repeat exposure | 131 | −9.09 | 0.003 |

The negative association appeared in both subsets. The more negative repeat-exposure coefficient does not establish an accumulating campaign effect. Households already experiencing a decline could have been targeted more often.

## Interpretation

**Observed result:** In Type C weeks, high-spending households spent an estimated **$6.25 less per week** than in their other weeks, after accounting for common week effects and the other campaign types. This association remained statistically significant after BH correction (`adjusted p = 0.0033`).

**What the lead-effect test adds:** in the four weeks before a household's first Type C week, its spending was already about $9.02 lower per week than in its other weeks (95% CI [−13.46, −4.58]); weeks five to eight showed no difference. With those lead weeks accounted for, the Type C coefficient is −7.12. Type C was targeted, so its timing is not random. The dip before exposure could come from how households were selected, from anticipation, or from the Type A and B campaigns that were active in 82% of those household-weeks, and the data cannot tell these apart. The estimate therefore cannot be read as the effect of Type C.

**Plausible competing explanations:**

1. Type C may encourage customers to postpone purchases or wait for discounts.
2. Type C may have been sent to households that were already reducing their spending. The lead-effect test in Step 8 found lower spending in the four weeks before exposure, which fits this explanation but also fits anticipation.
3. Other time-varying conditions may affect both campaign selection and spending.
4. Type A or B campaigns running in the weeks just before Type C may have changed spending; they were active in 82% of the Lead4 household-weeks.

The data do not separate these explanations convincingly. The result is a **statistically detectable association**, not an established causal campaign effect.

## Limitations and next steps

| Limitation | Implication |
|---|---|
| Small comparison cells | Type C × low has 28 households; the high-spending non-recipient comparison has 49 |
| Pre-trend uncertainty | The full sample and medium tier were near conventional significance thresholds |
| Unknown targeting criteria | Cannot reconstruct why a specific household received an offer in a specific week |
| Spending dip before exposure | Spending was already lower in the four weeks before a household's first Type C week (Lead4 −9.02); selection, anticipation and Type A/B campaigns cannot be separated |
| Concurrent campaigns | Several types can be active in the same household-week |
| Campaigns start and end at different times | Comparison groups under simple two-way fixed effects can be hard to interpret |
| Within R² = 0.0004 | Even a significant coefficient explains little of total within-household spending variation |
| Observational data | Household and week fixed effects cannot replace random assignment |

The literature on two-way fixed effects has shown that staggered treatment timing can cause misleading estimates in certain designs. This panel also contains recurring campaigns that switch on and off, rather than a single permanently adopted treatment; it is not identical to the textbook staggered-adoption case. A stronger follow-up would define exposure timing and comparison groups more carefully, or ideally run a randomized holdout with some households not receiving the campaign.

## How to run

```
pip install -r requirements.txt
pip install jupyter
```

The pinned versions are those of the Python 3.11 environment the notebooks were run in.

1. Download the Dunnhumby *The Complete Journey* CSVs into `data/` (see `data/README.md`). They are git-ignored.
2. Run the notebooks from the repository root in this order. `config.py` sets all paths and `SEED = 42`. Later notebooks reuse CSVs that earlier ones wrote to `outputs/`.

   ```
   python -m nbconvert --to notebook --execute --inplace <notebook>.ipynb
   ```

   `dunnhumby_data_overview`, `h2_stage1_2_tier_campaign_mapping`, `h2_stage3_panel`, `h2_stage4_cell_size`, `h2_stage5_pretrend`, `h2_stage6_main_regression`, `h2_stage7_multiple_comparison`, `h2_stage8_placebo_test`, then `h2_figures` (draws every figure in `images/` from `outputs/`; set `TRANSPARENT = True` for transparent versions).
3. Result CSVs go to `outputs/`. Household-level intermediate files go to `outputs/intermediate/` and are not committed.

## Methods covered

- Pre-campaign spending segmentation
- Campaign timing and household-week panel construction
- Exposure overlap, reach, and VIF checks
- Pre-trend testing and correction of a denominator bug
- Household and week fixed effects with household-clustered standard errors
- Nine interaction estimates and Benjamini–Hochberg correction
- Non-recipient comparison, lead-effect test, and first versus repeat exposure checks

**Bottom line:** Type C exposure coincided with lower weekly purchases among high-spending households, but their spending had already dropped in the four weeks before the first Type C week (Lead4 −9.02), and selection, anticipation and Type A/B campaigns cannot be separated. The pooled +242% difference for low spenders is not an estimate of campaign lift, and the low-spender fixed-effects estimates are not distinguishable from zero. I report an association, not a Type C effect.
