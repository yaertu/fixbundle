# FixBundle Roadmap

Roadmap, “daha fazla özellik” yerine **daha iyi hata kanıtı ve daha kısa çözüm süresi** hedefiyle sıralanır.

## v0.3.0 — Temporal Debugging ✅
**Sonuç:** “Bug eski commit'te oldu” durumunda AI'ya bugünkü kod yerine olay anındaki kodu ver.
- `--commit <sha/ref>`
- detached temporary `git worktree`
- incident vs current commit identity
- dirty workspace preservation
- cleanup/invariant testleri
- gerçek demo ve README GIF kanıtı

## v0.4.0 — GitHub Native
**Sonuç:** failed Actions job → tek komut/aksiyonla paylaşılabilir evidence.
- workflow/run/job/commit identity
- failed job log capture
- GitHub issue-ready handoff Markdown
- artifact-safe bundle output
- fork/PR secret-safety sınırları

## v0.5.0 — Production Evidence
**Sonuç:** “sadece production'da oldu” vakasında bounded runtime kanıtı.
- Sentry event adapter
- structured JSON/log ingestion
- time-window capture
- configurable privacy allow/deny rules

## v0.6.0 — Regression Fingerprints
**Sonuç:** “önceden çalışıyordu, şimdi neden bozuk?” sorusunu bundle-vs-bundle karşılaştır.
- failure signature diff
- dependency drift
- environment drift
- changed-file correlation

## v0.7.0 — Agent Handoff
- Codex / Claude Code / Cursor için tool-specific handoff adapters
- ortak kanıtı vendor-specific talimatlardan ayıran export profilleri
- prompt-injection-safe evidence boundaries

## v1.0 — Stable Evidence Protocol
- versioned public schema
- plugin SDK
- signed manifest option
- organization policy packs
- compatibility contract

## Ticari katman ilkesi
Local core kullanılabilir ve account gerektirmeyen durumda kalır. Ücretli değer ancak gerçek kullanım kanıtlandıktan sonra hosted integrations, encrypted sharing, team policy/history ve collaboration kolaylığına bağlanır. Core evidence üretimi paywall arkasına taşınmaz.
