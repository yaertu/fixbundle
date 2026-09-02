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
- failed-job logs + bounded patch/workflow config
- redaction + checksums + AI handoff
- no local checkout
- bearer-token redirect hardening
- gerçek public failed-run live verification

Kanıt: `docs/evidence/V04_LIVE_GITHUB.md`.

## v0.5.0 — Production Evidence Import ✅
**Sonuç:** “sadece production'da oldu” olayını tek observability vendor'ına kilitlemeden FixBundle evidence protokolüne al.

İlk core input: **OpenTelemetry Protocol File Exporter JSON Lines**.
- `fixbundle otlp --logs ... [--traces ...]`
- exact `traceId` / `spanId` correlation
- `service.name`, service version, deployment environment/id evidence
- stable `exception.type`, `exception.message`, `exception.stacktrace`
- explicit trace/time-window selection
- selected/omitted provenance
- input byte + record guards
- redaction + checksums + AI handoff
- local/offline, account'suz, auto-upload yok
- reproducible `scripts/demo_otlp.py`

Sentry adapter ancak portable normalization veya cross-source correlation gibi ek değer sağladığında gelecek; Sentry'nin mevcut LLM/event API'sini sırf wrapper olsun diye tekrar etmeyeceğiz.

## v0.6.0 — Regression Fingerprints
**Sonuç:** “önceden çalışıyordu, şimdi neden bozuk?” sorusunu evidence-vs-evidence karşılaştır.
- normalized failure signature
- exception/trace drift
- dependency/environment drift
- changed-file/release correlation
- deterministic before/after report

## v0.7.0 — Agent Handoff
- Codex / Claude Code / Cursor için tool-specific export profiles
- ortak kanıtı vendor-specific talimatlardan ayırma
- prompt-injection-safe evidence boundaries

## v0.8.0 — Source Adapters
Demand kanıtlanırsa Sentry ve diğer production source adapter'ları ortak evidence protocolüne bağla. Adapter sayısı başarı metriği değildir; aynı problemi tekrar eden wrapper eklenmez.

## v1.0 — Stable Evidence Protocol
- versioned public schema
- plugin SDK
- signed manifest option
- organization policy packs
- compatibility contract

## Ticari katman ilkesi
Local core account gerektirmeyen durumda kalır. Ücretli değer ancak gerçek kullanım kanıtlandıktan sonra hosted integrations, encrypted sharing/history, team privacy policy, organization correlation ve collaboration kolaylığına bağlanır. Core evidence üretimi paywall arkasına taşınmaz.
