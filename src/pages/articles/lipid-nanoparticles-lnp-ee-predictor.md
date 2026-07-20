---
title: "Predicting LNP Encapsulation Efficiency from Formulation Parameters"
date: "2026-04-09"
tags: ["lipid nanoparticles", "drug delivery", "machine learning", "physics-informed neural networks", "biophysics"]
excerpt: "An open dataset, an XGBoost baseline, and a physics-informed neural network for predicting lipid nanoparticle encapsulation efficiency from formulation parameters — with an honest look at why cross-paper generalization is hard."
image: "lnp-dashboard.png"
image_alt: "Screenshot of the LNP-EE-Predictor Streamlit dashboard showing model comparison and interactive prediction interface"
image_caption: "The multipage Streamlit dashboard: data exploration, XGBoost baseline, PINN model, and interactive predictor."
---

## The problem

Lipid nanoparticles (LNPs) are the delivery vehicle behind mRNA therapeutics — including the COVID-19 vaccines. Every new formulation is characterized by its **encapsulation efficiency (EE%)**: the fraction of input nucleic acid that ends up inside the particle rather than free in solution. High EE is one of the first go/no-go metrics in LNP development, and it is measured empirically for nearly every new formulation.

That empirical bottleneck is the target here. If a predictive model can rank-order candidate formulations before synthesis, wet-lab teams can front-load the promising ones and skip the obvious losers. Even an imperfect model that narrows the search space is useful.

The catch is data. Published LNP literature is heterogeneous: different labs report different subsets of formulation parameters, assay conditions vary, and EE values reflect different measurement protocols. The signal is there, but so is a lot of noise.

## Approach

I'm developing **LNP-EE-Predictor** as an open-source pipeline in collaboration with Constantinos Skevofilax, trained on the [LNP Atlas](https://lnp-atlas.kisti.re.kr/) dataset — 1,092 formulations curated from peer-reviewed literature. The project explores two complementary strategies:

- **XGBoost baseline** — a high-capacity gradient-boosted tree that extracts signal from rich feature engineering across all 636 usable rows.
- **Physics-informed neural network (PINN)** — a smaller network trained on a 93-row subset with the full feature vector, plus three physics residual terms encoding domain constraints.

Both models are evaluated the same way: **GroupKFold cross-validation grouped by paper DOI**. Random-split validation on this data is misleading because rows from the same paper share confounders — measurement protocol, buffer composition, operator technique, lipid lot. GroupKFold forces the model to generalize across papers, which is what matters if you want to use it on a new formulation from a new lab.

## Results

| Model | OOF R² | OOF RMSE | Rows | Features | CV strategy |
|---|---|---|---|---|---|
| XGBoost | −0.032 | 21.88% | 636 | 88 | GroupKFold (paper DOI) |
| PINN, 7-feature | 0.438 | 11.25% | 93 | 7 | GroupKFold (paper DOI) |
| PINN, 7-feature | 0.580 | 10.12% | 93 | 7 | Random 80/20 (leakage-prone) |

The honest number is the middle row: **R² ≈ 0.44** on out-of-fold cross-paper prediction using the PINN. The XGBoost baseline is worse than the mean predictor on cross-paper splits, which is a real and instructive result — not a bug to hide.

## Why is XGBoost R² negative?

A previous iteration reported XGBoost R² ≈ 0.136. That number included a data leakage bug: the cleaned target column (`encapsulation_efficiency_clean`) was inadvertently retained as an input feature after the EE-cleaning step. Fixing the leak dropped honest R² to −0.032.

Both the XGBoost and the PINN results reveal the same underlying difficulty: **cross-paper generalization from heterogeneous LNP literature is hard.** Root-cause analysis suggests:

- Within-paper EE variance ≈ between-paper EE variance (both ~0.02 in fraction units)
- Roughly half of the EE variance is explained by unmeasured, paper-level confounders that no formulation feature can capture
- Feature coverage is uneven — many published papers omit key formulation details, so the model has to impute or drop

## Dataset cleaning

Getting the dataset from 523 usable rows to 636 involved:

- Fixing 174 rows with corrupt `±` encoding in the source CSVs
- Parsing range-formatted EE values (e.g. `"80–85%"`) and dual-assay reports
- Correcting 6 broken cKK-E12 SMILES against PubChem CID 71555845
- Nulling 32 DSPE-2armPEG2000 SMILES that had valence errors (falls back to frequency encoding)

Cleaned data is committed as `data/lnp_atlas_cleaned.csv` — the goal is that anyone reproducing the work starts from the same numbers.

## Physics-informed neural network

The PINN adds three physics residual terms (R1, R2, R3) to the loss function, encoding first-principles constraints on how formulation parameters should relate to EE. On the 93-row subset with full feature coverage, this halved RMSE relative to a comparable MLP without physics constraints. The tradeoff is the small labeled dataset — the physics prior is doing real work compensating for data scarcity.

Expanding the PINN training set is the next major work item. Every paper that reports a full formulation vector unlocks new training examples.

## Interactive dashboard

The Streamlit dashboard exposes data exploration, both model comparisons, and an interactive predictor where you can enter a formulation and get a predicted EE% back:

<div class="embed-frame">
  <iframe
    src="https://lipid-nanoparticle-ee-predictor.streamlit.app/?embed=true"
    title="LNP-EE-Predictor interactive dashboard"
    loading="lazy"
    allow="clipboard-read; clipboard-write"
    referrerpolicy="strict-origin-when-cross-origin"
  ></iframe>
</div>

<p class="muted">Hosted on Streamlit Community Cloud, which sleeps after inactivity — the first load can take 30–60 seconds. <a href="https://lipid-nanoparticle-ee-predictor.streamlit.app/" target="_blank" rel="noopener noreferrer">Open the dashboard in a new tab →</a></p>

## What's next

- **API endpoint** — Dockerized FastAPI service so the model is programmatically callable, not just interactive.
- **Expand the PINN dataset** — the 93-row subset is the current ceiling; growing it toward 300–500 rows would likely push honest R² past 0.6.
- **Public predictions log** — every prediction requested through the API gets logged (formulation + predicted EE), so if a user later measures the actual EE and reports it, we can grow the dataset from real usage.

## Links

- [Repository on GitHub](https://github.com/Wesley-Jakob-Gilbert/lipid-nanoparticle-ee-predictor) — code, cleaned data, notebooks
- [Live Streamlit dashboard](https://lipid-nanoparticle-ee-predictor.streamlit.app/) — cold-start warning above
- Data source: [LNP Atlas](https://lnp-atlas.kisti.re.kr/) at the Korea Institute for Science and Technology
