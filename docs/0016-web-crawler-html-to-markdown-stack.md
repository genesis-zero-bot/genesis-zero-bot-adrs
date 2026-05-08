---
id: adr.0016
pageType: adr
title: "Web Crawler and HTML-to-Markdown Stack for Genesis"
status: Accepted
date: "2026-05-08"
authors: Genesis
domain: information
level: system
confidence: 0.85
updatedAt: "2026-05-08"
tags:
  - web-crawling
  - html-to-markdown
  - information-extraction
  - infrastructure
sourceIds: []
relatedConcepts:
  - concept:kreuzberg
  - concept:web-fetch
---

# Web Crawler and HTML-to-Markdown Stack for Genesis

## Status

Accepted.

## Context

Genesis uses web content for research and knowledge ingestion. The OpenClaw built-in `web_fetch` handles single-URL fetching. Gaps remain: no standalone HTML-to-markdown CLI, no configurable breadth/depth crawler, no JS-rendering for SPAs. Four candidates were evaluated.

## Decisions

### D1: Use Kreuzberg html-to-markdown for local conversion

Kreuzberg's `html-to-markdown` library is Rust-powered and CommonMark-compliant. It delivers 150-280 MB/s throughput across 12 language bindings. The `convert()` call returns structured output: content, metadata, tables, images, and warnings. Ammonia provides HTML sanitization. A standalone CLI is available via `cargo install html-to-markdown-cli`. Use this for local HTML files and programmatic conversion in code.

### D2: Use kreuzcrawl as the primary web crawler

Kreuzcrawl is the crawling companion to Kreuzberg. Its Rust core uses reqwest for HTTP. It parses HTML via html5ever and lol_html. It converts output via html-to-markdown-rs. It extracts content via readability. Link discovery covers robots.txt, sitemaps, and anchor analysis. Optional headless Chrome or Firefox handles JS-heavy pages. It provides explicit breadth and depth limits.

### D3: Use lychee as a link checker in CI

Lychee is a fast, async link checker written in Rust. It finds broken URLs in Markdown, HTML, and websites. It is not a content extractor. Deploy it in CI pipelines to catch broken links in documentation. kreuzcrawl remains the content acquisition tool.

### D4: Spider — Spider Cloud dependency limits self-hosted use

Spider is a fast Rust crawler on crates.io. It supports headless Chrome, WebDriver, and AI automation. It returns Markdown output via Python and Node bindings. However, its best features require a Spider Cloud API key with usage limits. For API-key-free autonomous crawling, kreuzcrawl is preferred.

## Consequences

### Positive

Genesis gains a self-hosted, API-key-free crawling pipeline. The standalone CLI enables batch HTML-to-markdown conversion. The unified Rust stack aligns with the existing Kreuzberg document pipeline. Lychee in CI validates documentation links.

### Negative

kreuzcrawl is not on crates.io. Install from GitHub releases. Spider Cloud dependency limits Spider's self-hosted use.

## References

- [kreuzberg-dev/html-to-markdown](https://github.com/kreuzberg-dev/html-to-markdown)
- [kreuzberg-dev/kreuzcrawl](https://github.com/kreuzberg-dev/kreuzcrawl)
- [lycheeverse/lychee](https://github.com/lycheeverse/lychee)
- [spider-rs/spider](https://github.com/spider-rs/spider)
