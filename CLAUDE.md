# Wesley Gilbert — Personal Website

## Project Goal

Replace the Carrd.co landing page at **wesley-j-gilbert.com** with a handcrafted site that:
- Signals real web dev / cloud infrastructure competency to potential employers
- Publicizes scientific research visuals, diagrams, and animations with good SEO so they appear in Google Images and get indexed by Googlebot
- Has personality, artistry, and character — not a generic portfolio template

## About Wesley

- **Current role:** Disaggregated Manufacturing Engineer at Intel Corporation (Albuquerque, since Sep 2024) — semiconductor packaging
- **Education:** Biophysics, UT Austin; senior thesis on cellular mechanobiology and bone tissue mechano-transduction; certificate in Scientific Computing & Data Science
- **Projects:** LNP-EE-Predictor (open-source dockerized API for lipid nanoparticle encapsulation efficiency prediction), Cranio-Facial-FEA (FEA bone remodeling model)
- **Interests:** Snowboarding, ice hockey, lacrosse, history, oil painting, museum visits (Goya, Gaudí)
- **Online:** YouTube (lipid nanoparticles, bone remodeling, genetic engineering, BMIs), GitHub, LinkedIn, X, Instagram
- **Motto:** *Aut inveniam viam aut faciam* — I shall find a way or make one

## Site Architecture

```
/                    → Home page (hero + brief bio + nav)
/articles            → Scientific articles, notebooks, papers, research visuals
```

The articles/notebooks page is the SEO core: research visuals, diagrams, and animations as standalone richly-tagged pages so Googlebot picks them up and they surface in Google Images.

## Hero Animation (Handled Separately)

The hero section features a full-viewport 2D bird-flock animation:
- Opens with a flock of birds small in the distance flying toward the camera
- As they get close they begin flying past; the camera then locks onto a single bird
- Remainder of scroll time: that bird is centered, gliding, slowly drifting, occasionally flapping
- **The animation itself is being created in Blender by Wesley — do not attempt to recreate it in code.** Expect to receive an exported file (e.g., `.webm`, `.mp4`, or a canvas/WebGL export) to embed.

## Tech Stack Preferences

- Vanilla HTML/CSS/JS or a lightweight framework (no heavy React SPA unless there's a real reason)
- Hosted on **Fly.io** (container-native — use Docker) — no Carrd dependency
- Semantic HTML, proper `<meta>` tags, Open Graph, structured data (JSON-LD) for SEO
- Images served with descriptive `alt` text and good filenames for Google Images indexing

## What to Signal to Employers

- Custom domain + self-hosted (not a site builder)
- Infrastructure knowledge: CI/CD, containerization references, cloud deployment
- Clean, intentional code — not WordPress or template soup
- Scientific credibility alongside engineering chops
