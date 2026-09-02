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
**Sonuç:** “sadece production'da oldu” olayını tek observability vendor'ına kilitlemeden evidence protocolüne al.
- OpenTelemetry Protocol File Exporter JSON/JSONL
- exact trace/span correlation
- service/version/environment/deployment identity
- stable exception evidence
- explicit trace/time-window selection
- bounded input + redaction + checksums
- local/offline capture
- reproducible OTLP demo

## v0.6.0 — Cross-source Evidence Compare ✅
**Sonuç:** iki FixBundle ZIP'i ver, integrity-checked deterministic “ne değişti?” raporu al.
- `fixbundle compare baseline.zip incident.zip`
- `--format json` machine-readable output
- input `SHA256SUMS.txt` doğrulaması interpretation'dan önce
- path traversal, duplicate member, symlink, malformed/tampered ZIP fail-closed
- `fixbundle/0.3`, `0.4`, `0.5` normalization
- local↔local, GitHub↔GitHub, GitHub↔OTLP comparison tests
- commit / changed-file / failed-command / job / step / exception / service / trace / runtime drift
- deterministic `changed`, `added`, `removed`, `unavailable` semantics
- network/LLM yok, input extraction/mutation yok
- real FixBundle OTLP baseline→incident compare demo CI gate

Tasarım/güvenlik: `docs/product/V06_COMPARE.md`.

## Distribution gate
v0.7'ye geçmeden önce repeat-use hipotezini sınayacağız. Hedef daha fazla commit değil, gerçek bir maintainer'ın FixBundle artifact'ını saklayıp sonraki incident'ta tekrar kullanması.

Detay: `docs/product/NEXT.md`.

## v0.7.0 — Agent Handoff
- Codex / Claude Code / Cursor tool-specific export profiles
- ortak kanıtı vendor-specific instruction katmanından ayırma
- prompt-injection-safe evidence boundaries
- yalnız gerçek handoff friction kanıtlanırsa

## v0.8.0 — Source Adapters
Demand kanıtlanırsa Sentry ve diğer production source adapter'larını ortak evidence protocolüne bağla. Adapter sayısı başarı metriği değildir; mevcut vendor özelliğini tekrarlayan wrapper eklenmez.

## v1.0 — Stable Evidence Protocol
- versioned public schema
- plugin SDK
- signed manifest option
- organization policy packs
- compatibility contract

## Ticari katman ilkesi
Local core account gerektirmeyen durumda kalır. Ücretli değer ancak gerçek kullanım kanıtlandıktan sonra hosted integrations, encrypted sharing/history, team privacy policy, organization correlation ve collaboration kolaylığına bağlanır. Core evidence üretimi paywall arkasına taşınmaz.
