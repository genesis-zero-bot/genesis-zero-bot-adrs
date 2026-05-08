---
id: adr.018
pageType: adr
title: "OCR Stack for Image Content Extraction in Genesis Pipeline"
status: Accepted
date: "2026-05-08"
authors: Genesis
domain: information
level: system
confidence: 0.85
updatedAt: "2026-05-08"
tags:
  - ocr
  - image-extraction
  - kreuzberg
  - document-intelligence
sourceIds:
  - source-kreuzberg-ocr
  - source-usls-ocr
  - source-ocrs-rust
relatedConcepts:
  - concept-kreuzberg
  - concept-usls
  - concept-ocrs
---

# OCR Stack for Image Content Extraction in Genesis Pipeline

## Status
Accepted

## Context

Genesis processes diverse document formats for RegenTribe community members. Images embedded in PDFs or uploaded as stand-alone files may contain text that standard parsing cannot extract. An OCR (Optical Character Recognition) pipeline is required.

Three candidate tools were evaluated: usls, ocrs, and Kreuzberg. Each targets a different niche: usls is a general vision/VLM library with OCR sub-models, ocrs is a dedicated Rust OCR engine, and Kreuzberg is a polyglot document intelligence framework with plugin-based OCR support.

## Decisions

### D1: Adopt Kreuzberg as the primary OCR engine for image content extraction

Kreuzberg provides the most production-ready path for Genesis use cases.

**Rationale:**

- **Native OCR integration.** Kreuzberg ships built-in Tesseract bindings (no external tesseract install required), plus optional EasyOCR and PaddleOCR backends. The Rust core handles format detection and extraction pipeline orchestration.

- **Document intelligence scope.** Kreuzberg extracts text, tables, metadata, and images from 97+ formats. OCR is one capability within a larger document pipeline — aligned with how Genesis uses extraction (ingestion of community documents for knowledge graph population).

- **Polyglot bindings.** Python, Node.js/TypeScript, Ruby, Go, Java, C#, PHP, Elixir, Rust, C FFI. Genesis operates primarily in Python (semantic-graph pipeline). The Python SDK is first-class and well-documented.

- **Plugin architecture.** OCR backend is swappable via configuration. Enables future migration to PaddleOCR or EasyOCR without code changes.

- **Existing Genesis integration.** Kreuzberg is already installed in the semantic-graph virtual environment. It is the standard extraction tool for the Genesis pipeline. No new dependencies required.

### D2: usls is not suited for standalone OCR text extraction

usls is a Rust library for vision and vision-language models powered by ONNX Runtime. It includes OCR sub-models (DB for text detection, SVTR for text recognition) as part of a broader model zoo covering object detection, segmentation, pose estimation, VLM, and embedding models.

**Rationale:**

- **Alpha-stage versioning.** Latest available version is `0.2.0-alpha.3`. Not production-ready.

- **Scope mismatch.** usls targets computer vision researchers and practitioners who need SOTA model inference (YOLO, SAM, GroundingDINO). The OCR models are incidental components of a much larger model portfolio, not a dedicated OCR engine.

- **Integration cost.** Requires ONNX Runtime management, model download/caching, and GPU/threading configuration. High operational overhead for the benefit of using a single OCR model from the usls ecosystem.

- **Rust-only.** No Python bindings, no CLI tool for quick extraction. Requires Rust compilation and custom integration code.

### D3: ocrs is a promising Rust-native OCR engine but not yet viable for Genesis pipeline

ocrs is a Rust library and CLI tool for OCR using PyTorch models exported to ONNX, executed via the RTen engine. It targets modern OCR with minimal preprocessing and open training data.

**Rationale:**

- **Early preview state.** The README explicitly states "Expect more errors than commercial OCR engines." Behavior may change across versions.

- **Latin alphabet only.** ocrs currently recognizes only the Latin alphabet. Many RegenTribe community documents may involve non-Latin scripts (Māori, Pacific languages, technical symbols). Kreuzberg's Tesseract backend supports 100+ languages out of the box.

- **Language constraint.** The requirement for multilingual document support disqualifies ocrs at this stage.

## Consequences

**Positive:**

- Kreuzberg provides a unified extraction pipeline: documents, images, OCR, tables, metadata — one tool, consistent API, minimal operational overhead.
- The Python SDK integrates cleanly with the existing semantic-graph pipeline. No new runtime dependencies.
- Tesseract backend works without external tesseract installation (native Rust binding). Backends are swappable via config.
- Language coverage is broad: Tesseract supports 100+ languages, PaddleOCR supports Chinese, Japanese, Korean, Arabic, and more.

**Negative:**

- Tesseract (default backend) produces lower accuracy on complex layouts compared to dedicated OCR systems. For highly structured documents, PaddleOCR or VLM-based OCR (GPT-4o, Claude) may be needed as a future upgrade.
- Kreuzberg is Elastic License v2 (ELv2) — not fully open source (source available, but license restrictions apply). Acceptable for Genesis internal pipeline use.
- The current Kreuzberg Python package is version 4.4.3 with pre-compiled binaries. Newer versions (4.10.0-rc.15) exist but pip may lag behind releases.

## References

- [Kreuzberg on GitHub](https://github.com/kreuzberg-dev/kreuzberg)
- [Kreuzberg OCR Guide](https://docs.kreuzberg.dev/guides/ocr/)
- [usls on GitHub](https://github.com/jamjamjon/usls) — Alpha-stage vision library with OCR sub-models
- [ocrs on GitHub](https://github.com/robertknight/ocrs) — Rust-native OCR (Latin only, early preview)
- [Kreuzberg Python SDK — extract_file_sync](https://docs.kreuzberg.dev/reference/api-python/)
- [Source — OCR Stack Evaluation Notes](https://regentribes.github.io/genesis-zero-bot-wiki/sources/kreuzberg-ocr-stack.html)