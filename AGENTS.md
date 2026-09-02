# FixBundle repository steward protocol

Bu dosya Codex, Claude Code, Cursor ve diğer kodlama ajanlarının projeyi aynı kurallarla sürdürebilmesi için repo-local çalışma sözleşmesidir.

## Ürün cümlesi
**Package local failures, historical Git bugs, and failed GitHub Actions runs into redacted AI-ready evidence bundles.**

Ürün sınırı: repository context packer veya vendor-specific “explain error” aracı değil, **portable failure evidence**.

## Her bakım turunun sırası
1. Güncel `main`, CI, açık issue/PR, README ve canlı repo metadata'sını oku.
2. `docs/product/METRICS.md`, `REPO_HOME.md`, `NEXT.md` ve mevcut evidence belgelerini kontrol et.
3. Yeni geliştirme için gerçek kullanıcı problemi veya tekrarlanabilir failure kanıtı ara; komşu araçları ve resmi platform yeteneklerini yok sayma.
4. Davranış değişikliği test gerektirir.
5. Lokal gate:
   ```bash
   python -m pytest -q
   python scripts/demo.py
   fixbundle --version
   fixbundle . --recommend --lang tr
   ```
6. GitHub Native davranışı değişirse ayrıca live gate'i koru:
   ```bash
   export GITHUB_TOKEN=<actions-read-contents-read-token>
   fixbundle github --repo yaertu/fixbundle --run 33587184675 --output .fixbundle-live --lang en
   python scripts/verify_live_github.py .fixbundle-live
   ```
7. CI sonucunu görmeden cross-platform veya live PASS yazma.
8. Star/download/benchmark/user quote/sponsor/novelty iddiası uydurma.
9. Secret veya proprietary bundle içeriğini repoya koyma.
10. Sırf aktivite görünsün diye commit atma.

## GitHub ana sayfa senkronu
Her positioning/release değişiminde README ve `docs/product/REPO_HOME.md` birlikte kontrol edilir.

v0.4 sonrası hedef açıklama:
`Package local failures, historical Git bugs, and failed GitHub Actions runs into redacted AI-ready evidence bundles.`

Hedef topics:
`ai-debugging`, `developer-tools`, `devtools`, `production-debugging`, `temporal-debugging`, `support-bundle`, `diagnostics`, `bug-report`, `ai-coding-assistant`, `github-actions`, `codex`, `claude-code`, `cursor`, `reproducibility`, `git`, `llm`

Connector About/Topics yazamıyorsa yalnız bu UI adımı maintainer'a kısa görev olarak verilir. Değiştirildiğini görmeden değişti denmez.

## v0.4 kanıt ankrajı
- source failed run: `33587184675`
- proof run: `33589138174`
- proof commit: `d15385a7f9ecd0a0dbd1c67b0caad6f7aa21bb95`
- expected: platform matrix 9/9 + Live GitHub failure evidence PASS
- evidence: `docs/evidence/V04_LIVE_GITHUB.md`

## Sürüm kararı
- docs-only: version bump yok
- backward-compatible behavior: minor
- bug fix: patch
- stable schema kırılması (v1+): semver major

## Devam promptu

```text
Continue as FixBundle repository steward for yaertu/fixbundle.
Start from current main and read AGENTS.md, README, ROADMAP, docs/product/NEXT.md, REPO_HOME.md, METRICS.md, open issues/PRs and latest CI before changing anything.
Run /truth + /audit discipline. Search current GitHub/Reddit/web and official docs for actual failure-evidence pain, competing tools and platform-native capabilities. Never build a wrapper that merely duplicates a vendor's existing LLM/debugging feature.
Current v0.4 anchor is the real failed GitHub Actions run 33587184675 and successful proof run 33589138174. Preserve the live verification gate when touching GitHub capture.
The researched v0.5 direction is vendor-neutral Production Evidence Import, starting with OpenTelemetry Protocol File Exporter JSON/JSONL logs/traces. Normalize trace/span/service/environment/release/exception evidence into the existing FixBundle schema family, with bounded selection, redaction, checksums and tests. Sentry should be an optional adapter only where it adds portability/correlation beyond Sentry's own llmFormat/event APIs.
Make only evidence-backed changes. Keep README/CHANGELOG/ROADMAP/evidence/repo-home metadata recommendations synchronized. Never fabricate users, stars, benchmarks, tests, compatibility, screenshots or novelty. Check CI after changes and repair failures caused by the change before claiming success.
End with: what changed, proof, current CI, live public metrics, repo-home metadata status, and the single highest-value next move.
```
