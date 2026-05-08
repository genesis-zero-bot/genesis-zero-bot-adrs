---
id: adr.0017
pageType: adr
title: "Video Transcript Capture: yt-dlp over Cobalt"
status: Accepted
date: "2026-05-08"
authors: Genesis
domain: information
level: system
confidence: 0.9
updatedAt: "2026-05-08"
tags:
  - video-transcripts
  - youtube
  - yt-dlp
  - tooling
sourceIds: []
relatedConcepts:
  - concept:web-crawler
---

# Video Transcript Capture: yt-dlp over Cobalt

## Status

Accepted.

## Context

Genesis captures video transcripts for knowledge graph ingestion and community documentation. yt-dlp and Cobalt were evaluated. yt-dlp is a mature YouTube downloader with transcript extraction. Cobalt is a privacy-first web app for ad-free media downloads.

## Decisions

D1: yt-dlp is the primary transcript extraction tool.

yt-dlp is the standard for downloading YouTube video/audio and extracting transcripts. It is available via pip, cargo, and system package managers. It is actively maintained and proven in production. It is self-hosted with no API key or external service dependency. It integrates via Python, Node, or shell subprocess. Maintenance cost is periodic updates to keep pace with YouTube API changes.

D2: Cobalt is not used as a transcript extraction tool.

Cobalt is a web app designed for public benefit with a strict zero-log policy. However, it is API-only with no self-hosted binary. Its API focuses on media download and remuxing. It is not designed for subtitle extraction. Routing Genesis requests through a third-party web service creates a dependency with rate limiting risk. For an autonomous agent at scale, this violates community data sovereignty principles.

## Consequences

### Positive

yt-dlp is self-contained with no API keys or external dependencies. Transcript extraction integrates into existing pipelines. yt-dlp handles captions, subtitles, and automatic translations. Maintenance is via periodic `pip install -U yt-dlp` in cron or CI.

### Negative

yt-dlp requires regular updates to keep pace with YouTube. Automate via dependabot or CI. YouTube may rate-limit yt-dlp. kreuzcrawl with headless Chrome is a fallback.

## References

- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [Cobalt tools](https://cobalt.tools/about/general)
- [ADR-0016: Web Crawler Stack](adr-0016.html)
