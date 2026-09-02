# Changelog

## 0.5.0 — 2026-09-02

### Added
- `fixbundle otlp --logs <file> [--traces <file>]` local production-evidence capture yolu.
- OpenTelemetry Protocol File Exporter JSON Lines için `resourceLogs/scopeLogs/logRecords` ve `resourceSpans/scopeSpans/spans` normalization.
- OTLP AnyValue + resource attribute normalization.
- Exact `traceId` / `spanId` evidence correlation.
- `service.name`, `service.version`, deployment environment/id ve telemetry SDK identity extraction.
- Stable exception evidence: `exception.type`, `exception.message`, `exception.stacktrace`.
- `--trace-id`, `--since`, `--until` bounded incident selection.
- `production/{incident,logs,traces,exceptions,services}.json` evidence shape.
- Selected/omitted input record provenance, `AI_HANDOFF.md` ve SHA-256 integrity.
- `scripts/demo_otlp.py` yeniden üretilebilir production incident demo.

### Safety / hardening
- OTLP core local/offline çalışır; network veya account istemez ve automatic upload yapmaz.
- Input absolute path'leri manifest'e serialize edilmez.
- Input başına byte guard ve total normalized record guard eklendi.
- Malformed JSONL, invalid time bounds, oversized input ve record overflow fail-closed davranır.
- Telemetry text serialization öncesi mevcut secret/path redaction katmanından geçer.
- Exact trace filter unrelated trace'leri sessizce evidence'e karıştırmaz.
- GitHub collector User-Agent ve `fixbundle_version` artık package `__version__` kaynağından gelir.
- Feature branch CI duplicate push + PR matrisleri kaldırıldı; branch PR bir kez, main push bir kez doğrulanır.

### Verification
- `tests/test_otlp.py`: exact trace selection, log/span correlation, exception normalization, service identity, unrelated-trace omission, secret redaction, checksums, malformed input, invalid time range ve record guard.
- `tests/test_otlp_cli.py`: gerçek `fixbundle otlp` CLI subprocess capture.
- `tests/test_otlp_limits.py`: oversized input fail-closed gate.
- `scripts/demo_otlp.py`: `PaymentGatewayError`, `payments-api`, secret redaction ve 7 checksum için yeniden üretilebilir PASS zinciri.
- v0.4 live GitHub failure evidence gate v0.5 CI içinde korunur.

## 0.4.0 — 2026-09-02

### Added
- `fixbundle github --repo owner/repo --run <id>` ile completed failed GitHub Actions run'ını local checkout olmadan evidence ZIP'e dönüştüren read-only capture yolu.
- Exact repository / workflow / run / commit / job / step identity normalization.
- Yalnız failed job loglarını bounded + redacted olarak `github/jobs/*.log` içine alma.
- Olay commit'inin bounded patch context'ini `github/commit.json` içine alma.
- Olay anındaki workflow config erişilebiliyorsa bundle'a ekleme.
- GitHub failure'a özel `AI_HANDOFF.md`, manifest ve SHA-256 integrity listesi.
- Recorded/synthetic API fixture testleri ve gerçek public failed-run verifier'ı.

### Safety / fixes
- `GITHUB_TOKEN` hiçbir output dosyasına serialize edilmez.
- GitHub job-log endpoint'inin signed blob redirect'inde Bearer Authorization header'ı redirect target'a taşınmaz.
- Redirect davranışını yerel HTTP server ile doğrulayan regression testi eklendi.
- Otomatik upload yoktur.
- `--repo` strict `owner/repo` formatıyla doğrulanır.
- Yalnız completed + failure run kabul edilir; belirsiz/in-progress run fail-closed davranır.
- Failed-job logları karakter guard ile sınırlandırılır ve secret redactor'dan geçirilir.

### Verified
- Kaynak incident: GitHub Actions run `33587184675` / run #41.
- Gerçek failure: üç Windows job, failed step `Historical demo`, log marker'ları `UnicodeEncodeError` + `cp1252`.
- Live proof: GitHub Actions run `33589138174` / run #63.
- Post-merge main proof: run `33589630906` / run #66, 9/9 platform matrix + live evidence job PASS.

## 0.3.0 — 2026-09-02
- `--commit <ref>` ile isolated historical worktree capture.
- Current workspace preservation ve gerçek historical failure demo.
- Windows legacy stdout encoding regression fix.

## 0.2.0 — 2026-09-02
- Node.js, Python, Rust, .NET, Go ve Java stack algılama.
- `fixbundle --recommend`, Türkçe/İngilizce CLI, Git identity ve genişletilmiş redaction.

## 0.1.0 — 2026-09-02
- İlk local AI-ready diagnostic bundle prototipi.
