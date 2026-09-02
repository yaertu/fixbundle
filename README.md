<p align="center">
  <img src="assets/fixbundle-logo.svg" width="112" alt="FixBundle logo">
</p>

<h1 align="center">FixBundle 🧰</h1>

<p align="center"><strong>Hatanın hikâyesini değil, kanıtını paketle.</strong></p>

<p align="center">
  <a href="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version 0.5.0" src="https://img.shields.io/badge/version-0.5.0-8B5CF6">
  <img alt="Local first" src="https://img.shields.io/badge/privacy-local--first-0EA5E9">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-22C55E">
</p>

<p align="center"><img src="assets/hero.svg" width="100%" alt="FixBundle: failure to portable debugging evidence"></p>

Bir hata dört farklı yerde ortaya çıkabilir: **local command**, **eski Git commit'i**, **GitHub Actions** veya **production telemetry**. FixBundle bunları aynı fikre indirger: bounded + redacted + checksum'lı bir evidence ZIP. Paketi Codex'e, Claude Code'a, Cursor'a, ChatGPT'ye veya insan destek ekibine verebilirsin.

## ⚡ 4 giriş, 1 evidence paketi

```bash
# Local failure
fixbundle . --lang tr --run "pytest -q"

# Historical failure
fixbundle . --commit <incident-sha> --run "python app.py" --lang tr

# GitHub Actions failure
fixbundle github --repo owner/repo --run <failed-run-id> --lang tr

# Production OpenTelemetry evidence
fixbundle otlp \
  --logs ./otel-logs.jsonl \
  --traces ./otel-traces.jsonl \
  --trace-id <trace-id> \
  --lang tr
```

PyPI yayını yapılana kadar kurulum:

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
```

GitHub capture için mümkün olan en dar **Actions: Read + Contents: Read** token'ı kullan. OTLP capture tamamen localdir; account veya network istemez.

## 🔭 v0.5: production olayı artık dışarıda kalmıyor

`fixbundle otlp`, OpenTelemetry Protocol File Exporter JSON Lines girdisini doğrudan okur:

- `resourceLogs → scopeLogs → logRecords`
- `resourceSpans → scopeSpans → spans`
- exact `traceId` / `spanId` correlation
- `service.name`, service version ve deployment environment evidence
- `exception.type`, `exception.message`, `exception.stacktrace`
- `--trace-id`, `--since`, `--until` ile bounded selection
- input byte + record guards
- selected / omitted record provenance
- redaction + SHA-256 integrity

Üretilen production paketi:

```text
AI_HANDOFF.md
manifest.json
SHA256SUMS.txt
production/
  incident.json
  exceptions.json
  services.json
  traces.json
  logs.json
```

### Tek komutlu OTLP kanıt demosu

```bash
python scripts/demo_otlp.py
```

CI'da doğrulanan demo çıktısı:

```text
PASS trace_id=4bf92f3577b34da6a3ce929d0e0e4736
PASS correlated_logs=1
PASS correlated_spans=1
PASS exception=PaymentGatewayError
PASS service=payments-api
PASS secret_redacted
PASS checksums=7
```

Demo sentetik bir ürün hikâyesi değil, gerçek OTLP nested shape'ini kullanan yeniden üretilebilir bir capture senaryosudur.

## 🎬 Historical Git kanıtı

<p align="center">
  <img src="docs/demo/fixbundle-v0.3-demo.svg" width="100%" alt="FixBundle historical debugging demo">
</p>

`python scripts/demo.py`, eski commit'teki gerçek `AssertionError`'ı yakalar ve current HEAD + dirty workspace'in değişmediğini doğrular.

## 🧪 GitHub Actions canlı kanıtı

v0.4 fixture ile bırakılmadı. FixBundle'ın kendi geçmişindeki gerçek failed run `33587184675` tekrar capture edildi:

```text
PASS live_run=33587184675
PASS failed_jobs=3
PASS log_files=3
PASS failed_step=Historical demo
PASS real_failure=UnicodeEncodeError/cp1252
PASS checksums=9
PASS token_not_serialized
```

Ayrıntı: [`docs/evidence/V04_LIVE_GITHUB.md`](docs/evidence/V04_LIVE_GITHUB.md).

Bu live gate v0.5 CI içinde de korunur. GitHub capture bozulursa production özelliği yeşil görünemez.

## 🛡️ Privacy by default

- `.env`, `.npmrc`, `.pypirc` ve bilinen secret dosyaları local source capture'da dışlanır.
- API key, bearer token, GitHub/OpenAI/Google/AWS token kalıpları, JWT, private key ve URL credentials maskelenir.
- Local project/home path'leri anonimleştirilir.
- OTLP input absolute path'i manifest'e yazılmaz; yalnız dosya adı + byte/record provenance tutulur.
- Text, patch, log ve telemetry girdileri bound'larla sınırlandırılır.
- GitHub log redirect'lerinde bearer token signed blob URL'ye forward edilmez.
- Hiçbir mode bundle'ı otomatik upload etmez.

Redaction kusursuzluk garantisi değildir. Hassas/proprietary bir bundle'ı public paylaşmadan önce ZIP'i kontrol et.

## 🧩 Ne değil?

| Araç / yaklaşım | Ana iş |
|---|---|
| **Repomix** | repository → LLM context |
| **temporal-debug-skill** | historical worktree agent akışı |
| **GitHub Copilot** | GitHub içinde failed check açıklama |
| **Sentry / observability AI** | kendi telemetry backend'i içinde teşhis |
| **OTel MCP sunucuları** | canlı telemetry'yi agent'a sorgulatma |
| **FixBundle** | **failure evidence'i bounded, redacted, agent/vendor bağımsız artifact'e çevirme** |

FixBundle observability dashboard veya AI chat değildir. Ürün sınırı **portable failure evidence**.

## ✅ Doğrulama zinciri

Güncel gate:

```text
pytest -q
python scripts/demo.py
python scripts/demo_otlp.py
fixbundle --version
fixbundle . --recommend --lang en
Live GitHub failure evidence
Ubuntu / Windows / macOS × Python 3.10 / 3.12 / 3.13
```

CI sonucu görülmeden README'ye platform PASS iddiası eklenmez.

## 🌍 English quick summary

**Turn local failures, historical Git bugs, failed GitHub Actions runs, and OpenTelemetry production incidents into redacted, checksummed evidence bundles.** FixBundle is local-first and keeps the evidence portable across AI coding tools and human support.

```bash
fixbundle . --run "npm test"
fixbundle . --commit <incident-sha> --run "npm test"
fixbundle github --repo owner/repo --run <failed-run-id>
fixbundle otlp --logs otel-logs.jsonl --traces otel-traces.jsonl --trace-id <trace-id>
```

## 🗺️ Yol haritası

- **v0.3 ✅ Temporal Evidence**
- **v0.4 ✅ GitHub Native**
- **v0.5 Production Evidence Import:** OTLP core + bounded production incident normalization
- **v0.6 Regression Fingerprints:** bundle-vs-bundle failure/environment/dependency drift
- **v0.7 Agent Handoff:** tool-specific export profiles without changing evidence truth
- **v1.0 Stable Evidence Protocol:** public schema + plugin SDK + signed manifest option

Araştırma ve tasarım: [`docs/product/V05_PRODUCTION_EVIDENCE.md`](docs/product/V05_PRODUCTION_EVIDENCE.md).

## 🤝 Proje

- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Roadmap](ROADMAP.md)
- [Live v0.4 evidence](docs/evidence/V04_LIVE_GITHUB.md)
- [Landscape](docs/product/LANDSCAPE.md)
- [Monetization](docs/product/MONETIZATION.md)
- [Adoption scoreboard](docs/product/METRICS.md)
- [Repository steward protocol](AGENTS.md)

## 🔎 GitHub About / Topics

v0.5 hedef About:

> Package local, historical, CI, and OpenTelemetry production failures into redacted portable debugging evidence.

Hedef topics mevcut discovery setine `github-actions`, `opentelemetry` ve `observability` ekler. Canlı metadata ile öneri [`docs/product/REPO_HOME.md`](docs/product/REPO_HOME.md) içinde ayrı tutulur; UI'da gerçekten değişmeden “güncellendi” denmez.

## 📜 Lisans

MIT.
