<p align="center">
  <img src="assets/fixbundle-logo.svg" width="112" alt="FixBundle logo">
</p>

<h1 align="center">FixBundle 🧰</h1>

<p align="center"><strong>Hatanın hikâyesini değil, kanıtını paketle. Sonra iki kanıtı karşılaştırıp ne değiştiğini gör.</strong></p>

<p align="center">
  <a href="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version 0.6.0" src="https://img.shields.io/badge/version-0.6.0-8B5CF6">
  <img alt="Local first" src="https://img.shields.io/badge/privacy-local--first-0EA5E9">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-22C55E">
</p>

<p align="center"><img src="assets/hero.svg" width="100%" alt="FixBundle: failure to portable debugging evidence"></p>

Bir hata **local command**, **eski Git commit'i**, **GitHub Actions** veya **production telemetry** içinde çıkabilir. FixBundle bunları bounded + redacted + checksum'lı evidence ZIP'lere çevirir. v0.6 ile iki FixBundle artifact'ını karşılaştırıp commit, failed step, exception, service, trace ve runtime evidence'ında ne değiştiğini deterministic olarak görebilirsin.

Aynı artifact Codex, Claude Code, Cursor, ChatGPT veya insan destek ekibine taşınabilir. Core evidence üretimi ve compare akışı otomatik upload yapmaz.

## ⚡ Kurulum

PyPI yayını yapılana kadar:

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
```

## 🧰 Capture + compare

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

# Before / after evidence comparison
fixbundle compare baseline.zip incident.zip
fixbundle compare baseline.zip incident.zip --format json
```

GitHub capture için mümkün olan en dar **Actions: Read + Contents: Read** token'ı kullan. OTLP capture ve compare local/offline çalışır; account veya network istemez.

## 🔬 v0.6 — Cross-source Evidence Compare

`fixbundle compare` iki ZIP'i satır satır log diff'ine çevirmek yerine önce evidence integrity'sini doğrular, sonra bilinen FixBundle schema'larını ortak alanlara normalize eder.

Karşılaştırılan evidence sınıfları:
- schema + capture mode
- project / repository / workflow / run identity
- Git commit + changed files
- failed local commands
- failed GitHub jobs + steps
- production exceptions
- service/version/environment/deployment identity
- trace IDs + span names
- stack + Python/platform runtime identity

Rapor statüleri sabittir:

```text
CHANGED      iki tarafta var, değer farklı
ADDED        baseline'da yok, incident'ta var
REMOVED      baseline'da var, incident'ta yok
UNAVAILABLE  iki tarafta da bu evidence yok
UNCHANGED    eşit; summary'de sayılır
```

Cross-source comparison'da `removed`, “gerçek dünyada silindi” anlamına gelmek zorunda değildir. Incident kaynağının o evidence türünü taşımadığı anlamına da gelebilir. Compare causal claim üretmez.

### Compare güvenlik sınırı

Input ZIP untrusted kabul edilir. `manifest.json` yorumlanmadan önce:
- `SHA256SUMS.txt` strict parse edilir ve tüm evidence dosyalarının hash'i doğrulanır,
- missing/extra checksum coverage reddedilir,
- checksum mismatch fail-closed olur,
- absolute path, `..`, Windows drive path, backslash ve NUL reddedilir,
- duplicate member, symlink ve encrypted member reddedilir,
- member count / per-member / total uncompressed size bound uygulanır,
- yalnız `fixbundle/0.3`, `fixbundle/0.4`, `fixbundle/0.5` input schema'ları kabul edilir,
- ZIP hiçbir zaman extract edilmez ve input bundle mutate edilmez.

Ayrıntı: [`docs/product/V06_COMPARE.md`](docs/product/V06_COMPARE.md).

### Gerçek artifact compare demosu

```bash
python scripts/demo_compare.py
```

Demo iki gerçek `build_otlp_bundle()` çıktısını üretir ve compare eder:

```text
PASS input_integrity=validated
PASS service_version=2.4.1->2.4.2
PASS exception=none->PaymentGatewayError
PASS trace_id=11111111111111111111111111111111->22222222222222222222222222222222
```

v0.6 compare gate GitHub Actions run `33591450004` içinde **Ubuntu + Windows + macOS × Python 3.10 / 3.12 / 3.13** ve Live GitHub evidence job ile doğrulandı.

## 🔭 v0.5 — Production Evidence Import

`fixbundle otlp`, OpenTelemetry Protocol File Exporter JSON/JSONL girdisini local olarak normalize eder:
- `resourceLogs → scopeLogs → logRecords`
- `resourceSpans → scopeSpans → spans`
- exact `traceId` / `spanId` correlation
- service/version/deployment identity
- `exception.type`, `exception.message`, `exception.stacktrace`
- `--trace-id`, `--since`, `--until` bounded selection
- input byte + record guards
- redaction + SHA-256 integrity

Tek komutlu kanıt demosu:

```bash
python scripts/demo_otlp.py
```

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

Ayrıntı: [`docs/evidence/V04_LIVE_GITHUB.md`](docs/evidence/V04_LIVE_GITHUB.md). Bu live gate sonraki sürümlerde de CI invariant'ı olarak korunur.

## 🛡️ Privacy by default

- `.env`, `.npmrc`, `.pypirc` ve bilinen secret dosyaları local source capture'da dışlanır.
- API key, bearer token, GitHub/OpenAI/Google/AWS token kalıpları, JWT, private key ve URL credentials maskelenir.
- Local project/home path'leri anonimleştirilir.
- OTLP input absolute path'i manifest'e yazılmaz.
- Text, patch, log ve telemetry girdileri bound'larla sınırlandırılır.
- GitHub log redirect'lerinde bearer token signed blob URL'ye forward edilmez.
- Compare input ZIP'lerini extract etmez.
- Hiçbir mode bundle'ı otomatik upload etmez.

Redaction kusursuzluk garantisi değildir. Hassas/proprietary bir bundle'ı public paylaşmadan önce ZIP'i kontrol et.

## 🧩 Ne değil?

| Araç / yaklaşım | Ana iş |
|---|---|
| **Repomix** | repository → LLM context |
| **GitHub Copilot** | GitHub içinde failed check açıklama |
| **Sentry / observability AI** | kendi telemetry backend'i içinde teşhis |
| **OTel MCP sunucuları** | canlı telemetry'yi agent'a sorgulatma |
| **Generic diff tools** | text/file difference |
| **FixBundle** | **failure evidence capture + portable integrity + cross-source evidence comparison** |

FixBundle observability dashboard, AI chat veya root-cause oracle değildir.

## ✅ Doğrulama zinciri

```text
pytest -q
python scripts/demo.py
python scripts/demo_otlp.py
python scripts/demo_compare.py
fixbundle --version
fixbundle . --recommend --lang en
Live GitHub failure evidence
Ubuntu / Windows / macOS × Python 3.10 / 3.12 / 3.13
```

CI sonucu görülmeden README'ye platform/live PASS iddiası eklenmez.

## 🌍 English quick summary

**Capture local, historical Git, GitHub Actions, and OpenTelemetry production failures as redacted checksummed evidence, then compare two FixBundle artifacts to see what changed.** The core workflow is local-first and portable across AI coding tools and human support.

```bash
fixbundle . --run "npm test"
fixbundle github --repo owner/repo --run <failed-run-id>
fixbundle otlp --logs otel-logs.jsonl --traces otel-traces.jsonl --trace-id <trace-id>
fixbundle compare baseline.zip incident.zip --format json
```

## 🗺️ Yol haritası

- **v0.3 ✅ Temporal Evidence**
- **v0.4 ✅ GitHub Native**
- **v0.5 ✅ Production Evidence Import**
- **v0.6 ✅ Cross-source Evidence Compare**
- **Distribution gate:** repeat-use kanıtı, packaging/discovery friction
- **v0.7 Agent Handoff:** yalnız gerçek tool-specific handoff ihtiyacı kanıtlanırsa
- **v1.0 Stable Evidence Protocol:** public schema + plugin SDK + signed manifest option

Sıradaki hedef: [`docs/product/NEXT.md`](docs/product/NEXT.md).

## 🤝 Proje

- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Roadmap](ROADMAP.md)
- [v0.6 compare design](docs/product/V06_COMPARE.md)
- [Live v0.4 evidence](docs/evidence/V04_LIVE_GITHUB.md)
- [Landscape](docs/product/LANDSCAPE.md)
- [Monetization](docs/product/MONETIZATION.md)
- [Adoption scoreboard](docs/product/METRICS.md)
- [Repository steward protocol](AGENTS.md)

## 🔎 GitHub About / Topics

v0.6 hedef About:

> Package failures into redacted evidence bundles and compare what changed across local, CI, and OpenTelemetry incidents.

Hedef topic seti [`docs/product/REPO_HOME.md`](docs/product/REPO_HOME.md) içinde tutulur. GitHub UI/API'de gerçekten değişmeden “güncellendi” denmez.

## 📜 Lisans

MIT.
