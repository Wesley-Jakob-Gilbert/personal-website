"""
Static site builder: src/ → dist/

How it works
------------
1. Load site-wide metadata from src/data/site.json
2. Set up Jinja2 to render HTML templates (src/templates/)
3. Copy static assets (src/assets/) verbatim into dist/
4. Render the home page
5. Parse every Markdown file in src/pages/articles/ — YAML frontmatter
   becomes template variables, body becomes HTML
6. Render each article and the articles index page
7. Write a sitemap.xml for search engines

Running locally
---------------
    pip install -r requirements.txt
    python build.py
    # Open dist/index.html in a browser

The Dockerfile runs this automatically at image build time.
"""

import json
import shutil
from pathlib import Path
from datetime import date

import frontmatter          # pip: python-frontmatter  — reads YAML + markdown
import markdown as md_lib   # pip: markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

SRC  = Path("src")
DIST = Path("dist")

MD = md_lib.Markdown(
    extensions=["extra", "codehilite", "toc", "tables", "fenced_code"],
    extension_configs={"codehilite": {"css_class": "highlight"}},
)


def load_site() -> dict:
    with open(SRC / "data" / "site.json", encoding="utf-8") as f:
        return json.load(f)


def build_jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(SRC / "templates")),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def copy_assets() -> None:
    dest = DIST / "assets"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC / "assets", dest)


def parse_articles() -> list[dict]:
    articles = []
    articles_src = SRC / "pages" / "articles"
    if not articles_src.exists():
        return articles

    for md_file in sorted(articles_src.glob("*.md"), reverse=True):
        post = frontmatter.load(md_file)
        MD.reset()  # reset state between files (toc, etc.)
        html_body = MD.convert(post.content)

        article = {
            "slug": md_file.stem,
            "url":  f"/articles/{md_file.stem}/",
            "content": html_body,
            **post.metadata,  # title, date, tags, image, excerpt, ...
        }
        articles.append(article)

    return articles


def render_home(env: Environment, site: dict, articles: list[dict]) -> None:
    tmpl = env.get_template("home.html")
    (DIST / "index.html").write_text(
        tmpl.render(site=site, articles=articles[:5]), encoding="utf-8"
    )


def render_articles_index(env: Environment, site: dict, articles: list[dict]) -> None:
    (DIST / "articles").mkdir(exist_ok=True)
    tmpl = env.get_template("articles_index.html")
    (DIST / "articles" / "index.html").write_text(
        tmpl.render(site=site, articles=articles), encoding="utf-8"
    )


def render_article_pages(env: Environment, site: dict, articles: list[dict]) -> None:
    tmpl = env.get_template("article.html")
    for article in articles:
        out_dir = DIST / "articles" / article["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(
            tmpl.render(site=site, article=article), encoding="utf-8"
        )


def write_sitemap(site: dict, articles: list[dict]) -> None:
    base = site["url"].rstrip("/")
    today = date.today().isoformat()

    urls = [
        f"  <url><loc>{base}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>",
        f"  <url><loc>{base}/articles/</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>",
    ]
    for article in articles:
        urls.append(
            f"  <url><loc>{base}{article['url']}</loc>"
            f"<lastmod>{article.get('date', today)}</lastmod>"
            f"<priority>0.7</priority></url>"
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def write_robots(site: dict) -> None:
    base = site["url"].rstrip("/")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n",
        encoding="utf-8",
    )


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    site     = load_site()
    env      = build_jinja_env()
    articles = parse_articles()

    copy_assets()
    render_home(env, site, articles)
    render_articles_index(env, site, articles)
    render_article_pages(env, site, articles)
    write_sitemap(site, articles)
    write_robots(site)

    print(f"Built {1 + 1 + len(articles)} pages -> {DIST}/")


if __name__ == "__main__":
    build()
