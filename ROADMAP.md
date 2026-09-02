# FixBundle Roadmap

Roadmap, “daha fazla özellik” yerine **daha iyi failure evidence ve daha kısa çözüm süresi** hedefiyle sıralanır.

## v0.3.0 — Temporal Evidence ✅
**Sonuç:** bug eski commit'te olduysa olay anındaki kodu güvenli worktree içinde yakala.
- `--commit <sha/ref>`
- detached temporary `git worktree`
- incident vs current commit identity
- dirty workspace preservation
- gerçek historical demo

## v0.4.0 — GitHub Native ✅
**Sonuç:** failed GitHub Actions run → agent/vendor bağımsız portable evidence ZIP.
- `fixbundle github --repo owner/repo --run <id>`
- workflow/run/job/step/commit identity
- yalnız failed-job log capture
- bounded patch + workflow config
- redaction + checksums + AI handoff
- no local checkout
- bearer-token redirect hardening
- gerçek public failed-run ile live verification

Kanıt: `docs/evidence/V04_LIVE_GITHUB.md`.

## v0.5.0 — Production Evidence Import
**Sonuç:** “sadece production'da oldu” vakasını tek observability vendor'ına kilitlemeden FixBundle evidence protokolüne al.

Araştırma kararı: ilk giriş **OpenTelemetry Protocol File Exporter JSONL** olacak. Böylece local/offline, credential gerektirmeyen ve vendor-neutral bir production evidence yolu elde edilir. Sentry adapter ikinci katmandır; Sentry'nin kendi API'si event'i zaten LLM-friendly formatta verebildiği için yalnız aynı işi tekrar eden wrapper yazılmayacak.

Plan:
- OTLP JSON/JSONL logs + traces ingestion
- `traceId` / `spanId` correlation
- `service.name`, environment/release/deployment attributes
- stable `exception.type`, `exception.message`, `exception.stacktrace` normalization
- bounded incident/time window
- privacy allow/deny policy
- optional Sentry event/issue adapter when it adds portability/correlation value

## v0.6.0 — Regression Fingerprints
**Sonuç:** “önceden çalışıyordu, şimdi neden bozuk?” sorusunu bundle-vs-bundle karşılaştır.
- failure signature diff
- dependency drift
- environment drift
- changed-file correlation

## v0.7.0 — Agent Handoff
- Codex / Claude Code / Cursor için tool-specific export profiles
- ortak kanıtı vendor-specific talimatlardan ayırma
- prompt-injection-safe evidence boundaries

## v1.0 — Stable Evidence Protocol
- versioned public schema
- plugin SDK
- signed manifest option
- organization policy packs
- compatibility contract

## Ticari katman ilkesi
Local core account gerektirmeyen durumda kalır. Ücretli değer ancak gerçek kullanım kanıtlandıktan sonra hosted integrations, encrypted sharing, team policy/history ve collaboration kolaylığına bağlanır. Core evidence üretimi paywall arkasına taşınmaz.
