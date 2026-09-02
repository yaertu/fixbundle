# FixBundle Roadmap

Roadmap özelliğe değil **kanıt kalitesine ve kullanıcı sonucuna** göre önceliklendirilir.

## v0.2.0 — Evidence Foundation ✅
- Stack auto-detection: Node/Python/Rust/.NET/Go/Java
- `--recommend` doğrulama komutları
- Git `HEAD` + branch evidence
- Turkish/English CLI output
- stronger secret patterns (JWT, credential URL, provider tokens)
- project/home path masking
- capture size guard + `.fixbundle` recursion guard

## v0.3.0 — Temporal Debugging
**Sonuç:** “Bug eski commit'te oldu” problemi için doğru kod anını yakala.
- `--commit <sha>` historical snapshot metadata
- safe temporary `git worktree` capture
- current vs incident commit identity
- detached/worktree cleanup guarantees
- uncommitted user workspace remains untouched

## v0.4.0 — GitHub Native
**Sonuç:** failed CI job → paylaşılabilir AI-ready evidence.
- GitHub Actions job metadata/log adapter
- issue-ready Markdown handoff
- workflow/commit/run identity
- CI artifact-friendly output

## v0.5.0 — Production Evidence
- Sentry event adapter
- structured JSON/log ingestion
- bounded time-window capture
- configurable privacy allow/deny rules

## v0.6.0 — Regression Fingerprints
- bundle-vs-bundle comparison
- dependency drift
- environment drift
- changed failure signature

## v1.0 — Stable Evidence Protocol
- versioned public schema
- plugin SDK
- signed manifest option
- organization policy packs
- compatibility contract

## Ticari katman ilkesi
Core local workflow kullanılabilir kalır. İleride cloud/team katmanı gelirse ücretli değer; encrypted sharing, history, team policy, hosted integrations ve collaboration kolaylığı üzerinden kurulur. Core kanıt üretimini kilitlemez.
