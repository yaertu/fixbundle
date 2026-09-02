# Changelog

## 0.6.0 — 2026-09-02

### Added
- `fixbundle compare baseline.zip incident.zip` deterministic evidence comparison.
- `--format json` machine-readable compare output.
- `fixbundle/0.3`, `fixbundle/0.4` ve `fixbundle/0.5` input normalization.
- Fixed-order comparison for capture identity, project/repository/workflow/run, Git commit + changed files, failed commands/jobs/steps, OTLP exceptions/services/traces and runtime identity.
- `changed`, `added`, `removed`, `unavailable` detailed statuses + `unchanged` summary count.
- `scripts/demo_compare.py`: iki gerçek OTLP FixBundle artifact'ı üretip service version / exception / trace drift'ini doğrulayan reproducible demo.
- `docs/product/V06_COMPARE.md`: compare integrity, normalization and semantic contract.

### Safety / hardening
- Compare, evidence interpretation'dan önce her iki bundle'ın `SHA256SUMS.txt` dosyasını strict doğrular.
- Exact checksum coverage zorunlu; missing/extra/malformed entries ve checksum mismatch fail-closed.
- Absolute ZIP path, Windows drive path, `..`, backslash, NUL, duplicate members, symlink ve encrypted members reddedilir.
- ZIP member count, per-member byte ve total uncompressed byte bounds uygulanır.
- Input ZIP hiçbir zaman extract edilmez veya mutate edilmez.
- Unknown FixBundle schema fail-closed davranır.
- Compare core LLM/network gerektirmez ve causal root-cause iddiası üretmez.

### Verification
- `tests/test_compare.py`: local↔local, GitHub↔GitHub, GitHub↔OTLP, checksum tamper, path traversal, duplicate member, symlink ve unsupported-schema regression coverage.
- `tests/test_compare_cli.py`: real CLI JSON output + invalid ZIP fail-closed subprocess coverage.
- `scripts/demo_compare.py`: real v0.5 bundle generation → integrity validation → deterministic compare.
- GitHub Actions PR run `33591450004`: Ubuntu + Windows + macOS × Python 3.10 / 3.12 / 3.13 ve Live GitHub evidence job PASS; compare demo platform matrix içinde PASS.
- Existing historical, OTLP production ve live GitHub evidence gates korunur.

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
