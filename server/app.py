"""daesoop.sudden.ninja — renders the 대숲봇 information pages as HTML.

Markdown lives in this repository under ``pages/``; the app renders it on
request (cached per file mtime). Korean is the default language; English is
served when the visitor's ``Accept-Language`` prefers it or via the explicit
``/{page}/en`` URLs.

Routes:
    GET /               → pages/home.ko.md (locale-negotiated)
    GET /terms[/{lang}] → pages/legal/terms.{lang}.md
    GET /privacy[/{lang}] → pages/legal/privacy.{lang}.md
    GET /health         → liveness probe
"""

from __future__ import annotations

import html
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from markdown_it import MarkdownIt

DOCS_DIR = Path(os.getenv("DAESOOP_DOCS_DIR", "pages"))
SITE_NAME = os.getenv("DAESOOP_SITE_NAME", "대숲봇")

PAGES: dict[str, dict[str, str]] = {
    "home": {"ko": "home.ko.md", "en": "home.en.md"},
    "terms": {"ko": "legal/terms.ko.md", "en": "legal/terms.en.md"},
    "privacy": {"ko": "legal/privacy.ko.md", "en": "legal/privacy.en.md"},
}
PAGE_LABELS = {
    "home": {"ko": "홈", "en": "Home"},
    "terms": {"ko": "이용약관", "en": "Terms of Use"},
    "privacy": {"ko": "개인정보 처리방침", "en": "Privacy Policy"},
}
LANGS = ("ko", "en")

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
_md = MarkdownIt("commonmark", {"html": False}).enable("table")
_H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)

_PAGE_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site_name}</title>
<style>
body {{ margin: 0; color: #222; background: #f5f5f5;
       font-family: -apple-system, 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; }}
main {{ max-width: 46rem; margin: 0 auto; padding: 2.5rem 1.25rem 3rem; background: #fff; min-height: 100vh; }}
nav {{ font-size: .9rem; margin-bottom: 2rem; }}
nav a {{ margin-right: 1rem; }}
h1, h2, h3 {{ line-height: 1.35; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: .4rem .6rem; text-align: left; vertical-align: top; }}
code {{ background: #f0f0f0; padding: .1rem .3rem; border-radius: 3px; }}
footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; font-size: .85rem; color: #666; }}
</style>
</head>
<body><main>
<nav>{nav}</nav>
{body}
<footer><a href="/">대숲봇</a></footer>
</main></body></html>"""


def _negotiate_lang(header: str) -> str:
    """Pick ko/en from an Accept-Language header; Korean is the default."""
    tags = [part.split(";")[0].strip().lower() for part in header.split(",") if part.strip()]
    for tag in tags:
        if tag == "ko" or tag.startswith("ko-"):
            return "ko"
    for tag in tags:
        if tag == "en" or tag.startswith("en-"):
            return "en"
    return "ko"


@lru_cache(maxsize=64)
def _render_html(file: str, mtime_ns: int) -> str:
    return _md.render((DOCS_DIR / file).read_text(encoding="utf-8"))


def _page_body(page: str, lang: str) -> tuple[str, str]:
    """Return (html_body, lang) for a page, falling back to the other language."""
    for candidate in (lang, *(other for other in LANGS if other != lang)):
        file = PAGES[page].get(candidate)
        if file is None:
            continue
        path = DOCS_DIR / file
        if path.is_file():
            return _render_html(file, path.stat().st_mtime_ns), candidate
    raise HTTPException(status_code=404, detail="page not found")


def _title_of(body: str, fallback: str) -> str:
    match = _H1_RE.search(body)
    if match is None:
        return html.escape(fallback)
    return html.escape(re.sub(r"<[^>]+>", "", match.group(1)).strip())


def _nav(current: str, lang: str) -> str:
    links = []
    for page in PAGES:
        if page == current:
            continue
        file = PAGES[page].get(lang) or PAGES[page].get("ko")
        if file is not None and (DOCS_DIR / file).is_file():
            links.append(f'<a href="/{page}">{html.escape(PAGE_LABELS[page][lang])}</a>')
    return "".join(links)


def _serve(page: str, lang: str) -> HTMLResponse:
    if page not in PAGES or lang not in LANGS:
        raise HTTPException(status_code=404)
    body, actual_lang = _page_body(page, lang)
    return HTMLResponse(
        _PAGE_TMPL.format(
            lang=actual_lang,
            title=_title_of(body, PAGE_LABELS[page][actual_lang]),
            site_name=html.escape(SITE_NAME),
            nav=_nav(page, actual_lang),
            body=body,
        )
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return _serve("home", _negotiate_lang(request.headers.get("accept-language", "")))


@app.get("/terms", response_class=HTMLResponse)
def terms(request: Request) -> HTMLResponse:
    return _serve("terms", _negotiate_lang(request.headers.get("accept-language", "")))


@app.get("/terms/{lang}", response_class=HTMLResponse)
def terms_lang(lang: str) -> HTMLResponse:
    return _serve("terms", lang)


@app.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request) -> HTMLResponse:
    return _serve("privacy", _negotiate_lang(request.headers.get("accept-language", "")))


@app.get("/privacy/{lang}", response_class=HTMLResponse)
def privacy_lang(lang: str) -> HTMLResponse:
    return _serve("privacy", lang)


@app.get("/health")
def health() -> PlainTextResponse:
    return PlainTextResponse("ok")
