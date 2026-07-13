---
title: "Predicting Lipid Nanoparticle Encapsulation Efficiency"
date: "2025-01-15"
tags: ["lipid nanoparticles", "drug delivery", "machine learning", "biophysics"]
excerpt: "An overview of LNP-EE-Predictor — an open-source Dockerized API for predicting how efficiently lipid nanoparticles encapsulate nucleic acid cargo, trained on experimental formulation data."
image: "lnp-ee-diagram.png"
image_alt: "Diagram of a lipid nanoparticle cross-section showing ionizable lipid, helper lipids, PEG-lipid, and encapsulated mRNA"
---

## Background

Lipid nanoparticles (LNPs) are the delivery vehicles behind mRNA therapeutics — including the COVID-19 vaccines. Their ability to encapsulate nucleic acid cargo is measured as *encapsulation efficiency* (EE): what fraction of the input nucleic acid ends up inside the particle rather than free in solution. High EE (>80%) is generally required for therapeutic viability.

Formulating LNPs is still partly art, partly science. The four-component lipid mixture — ionizable lipid, helper lipid, cholesterol, PEG-lipid — interacts with the nucleic acid payload in ways that are difficult to predict from first principles. Labs rely on iterative experimental screening, which is slow and expensive.

## The Problem

There is no reliable, open, computational tool for predicting EE before running an experiment. Pharmaceutical companies have proprietary models, but the academic and startup communities lack access to them.

## LNP-EE-Predictor

With [Constantinos Skevofilax](PLACEHOLDER), I built an open-source solution:

- **Database**: curated dataset of LNP formulations with measured encapsulation efficiencies
- **Model**: trained regression model mapping formulation parameters (lipid ratios, N/P ratio, buffer conditions) to predicted EE
- **API**: Dockerized FastAPI endpoint — send a formulation, get a predicted EE back in milliseconds
- **Deployment**: runs locally or on any container host

```bash
docker pull PLACEHOLDER/lnp-ee-predictor
docker run -p 8000:8000 lnp-ee-predictor
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"ionizable_lipid_mol_fraction": 0.5, "np_ratio": 6, ...}'
```

## Results

Placeholder: add validation metrics, example predictions, and comparison to experimental outcomes here once paper is published.

## Why This Matters

Every failed formulation experiment costs time and reagents. A predictive tool that narrows the search space — even imperfectly — meaningfully accelerates the development of nucleic acid therapeutics.

---

*Code and database available on [GitHub](PLACEHOLDER). Paper in preparation.*
