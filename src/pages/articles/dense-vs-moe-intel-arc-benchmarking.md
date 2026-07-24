---
title: "Dense vs. Mixture-of-Experts: Benchmarking Local LLMs on Intel Arc Battlemage"
date: "2026-07-23"
tags: ["machine learning", "large language models", "GPU benchmarking", "Intel Arc", "local inference"]
excerpt: "Why a mid-range Intel Arc B70 can run a 120B-parameter Mixture-of-Experts model faster than a dense model a quarter of its size — and what that says about memory bandwidth as the real bottleneck in local AI."
---

Intel's Arc Battlemage series of GPUs is doing something interesting for local AI enthusiasts: making it affordable to run models that, on paper, should be far out of a mid-range card's reach.

## Dense vs. Mixture-of-Experts

Most people who've worked with neural networks know the basic shape: inputs flow into hidden layers, which feed a loss function during training. What's less widely known is that large language models split into different architectural families on top of that shared skeleton — and two of the most common are **dense** and **Mixture-of-Experts (MoE)**.

**Dense models** are fairly linear. The entire model loads from VRAM, the input gets tokenized, and every token runs dot products against hidden layers across the *entire* network before streaming output.

**MoE models** are more distributed. The full model still sits in memory, but a routing gate selects only a fraction of the total parameters — the "experts" — to handle each token, bypassing the rest of the network. That's what makes it possible to run a 120-billion-parameter model without the token-per-second collapse you'd expect from a model that size.

<figure class="article-figure">
  <video autoplay muted loop playsinline aria-label="Animated diagram comparing dense and Mixture-of-Experts neural network architectures">
    <source src="/assets/video/dense-vs-moe.mp4" type="video/mp4">
  </video>
  <figcaption>Dense models route every token through the full network; MoE models route each token through a gated subset of "expert" parameters.</figcaption>
</figure>

## Benchmarking 21 models on an Arc B70

I ran a benchmark suite across 21 open-source LLMs on my own Intel Arc B70. The [full results are here](https://github.com/Wesley-Jakob-Gilbert/Intel-Arc-GPU-Benchmarks). The standout finding: high-parameter-count MoE models consistently outperformed low-parameter-count dense models — and the reason comes down to memory, not raw compute.

Battlemage cards ship with unusually high VRAM for their price point, so a huge model like GPT-OSS-120B can sit entirely in VRAM instead of streaming parameters over PCIe from system RAM, which is dramatically slower.

But VRAM capacity only explains part of it. Even at smaller sizes — where a dense model fits comfortably in memory — MoE still wins, because local text generation is bottlenecked by **memory bandwidth**: how fast the GPU can read weights out of memory, not how many weights it has. Since MoE only activates and reads a lightweight fraction of its total parameters per token, it cuts the load on the memory bus dramatically.

| Model | Architecture | Parameters | pp512 (tokens/s) |
|---|---|---|---|
| Qwen3 30B Instruct | MoE | 30B | 1188 |
| Qwen3 14B | Dense | 14B | 571 |

The MoE model has more than double the total parameter capacity of the dense model, yet it processes at roughly twice the speed — because it moves far less data per token.

## The real advantage: VRAM per dollar

MoE's efficiency advantage for local, single-user inference is well established at this point. What's more specific to this setup is that Intel's Arc Battlemage series makes 32GB of VRAM available at a fraction of the cost of Nvidia's 32GB RTX 5090 — which is what actually makes running a 120B-parameter MoE model at home practical, rather than merely theoretical.

## Links

- [Full benchmark results](https://github.com/Wesley-Jakob-Gilbert/Intel-Arc-GPU-Benchmarks) — all 21 models, Intel Arc B70
