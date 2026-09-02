# Changelog

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
- Local bundle `system.json` paket sürümünü `__version__` üzerinden alır.

### Verified
- Kaynak incident: GitHub Actions run `33587184675` / run #41.
- Gerçek failure: üç Windows job, failed step `Historical demo`, log marker'ları `UnicodeEncodeError` + `cp1252`.
- Live proof: GitHub Actions run `33589138174` / run #63, commit `d15385a7f9ecd0a0dbd1c67b0caad6f7aa21bb95`.
- Live verifier: 3 failed job, 3 real log, failed-step identity, 9 checksum ve token-not-serialized gate'leri PASS.
- Aynı proof run'da Ubuntu/Windows/macOS × Python 3.10/3.12/3.13 platform matrisi 9/9 PASS ve ayrı live GitHub evidence job PASS.

## 0.3.0 — 2026-09-02

### Added
- `--commit <ref>` ile eski bir Git commit'ini izole, detached worktree içinde capture etme.
- `incident.json`: requested ref, incident commit ve current HEAD kimliği.
- Current vs incident commit ayrımını `manifest.json` içine taşıyan `fixbundle/0.3` schema.
- `scripts/demo.py`: eski production commit'ini yeniden üreten gerçek, tek komutlu demo.
- README içine gerçek demo transcript'inden üretilen animasyonlu SVG kanıtı.
- Legacy Windows stdout encoding koşulunu yeniden üreten `tests/test_cli.py` regression testi.

### Safety
- Historical capture mevcut branch'i checkout etmez.
- Commitlenmemiş çalışma alanı capture öncesi/sonrası karşılaştırılır.
- Geçici worktree hata halinde de temizlenir.
- Output klasörü workspace dirty-state karşılaştırmasından ayrıştırılır.
- CLI stdout/stderr UTF-8 + replacement fallback ile yapılandırılarak legacy Windows code-page çökmesi giderildi.

### Verified
- Ubuntu, Windows ve macOS üzerinde Python 3.10 / 3.12 / 3.13 doğrulandı.
- Historical demo 5/5 invariant PASS.

## 0.2.0 — 2026-09-02
- Node.js, Python, Rust, .NET, Go ve Java stack algılama.
- `fixbundle --recommend` ile doğrulama komutu önerileri.
- Türkçe/İngilizce CLI.
- Git identity, stack evidence ve genişletilmiş redaction/path masking.

## 0.1.0 — 2026-09-02
- İlk local AI-ready diagnostic bundle prototipi.
