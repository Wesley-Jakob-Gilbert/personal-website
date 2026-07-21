# wesley-j-gilbert.com

Personal static site for `wesley-j-gilbert.com`.

## Tech stack

- Python static generator in `build.py`
- Jinja2 templates in `src/templates/`
- Markdown articles in `src/pages/articles/`
- Docker image served by nginx
- Fly.io deployment via `fly.toml`

## Local build

```bash
pip install -r requirements.txt
python build.py
```

The generated site is written to `dist/`.

## Deploy

```bash
flyctl deploy
```

## Roadmap

A future `/portfolio` subpage will host the Blender bird animation once the drawing-pad work is ready.
