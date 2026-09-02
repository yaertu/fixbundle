# Changelog

## 0.4.0 — 2026-09-02 (main)

### Added
- `fixbundle github --repo owner/repo --run <id>` ile completed failed GitHub Actions run'ını local checkout olmadan kanıt paketine dönüştüren read-only capture yolu.
- Exact repository / workflow / run / commit / job / step identity normalization.
- Yalnız failed job loglarını bounded + redacted olarak `github/jobs/*.log` içine alma.
- Olay commit'inin bounded patch context'ini `github/commit.json` içine alma.
- Olay anındaki workflow config erişilebiliyorsa bundle'a ekleme.
- GitHub failure'a özel `AI_HANDOFF.md`, manifest ve SHA-256 integrity listesi.
- Recorded/synthetic API fixture ile remote capture regression testleri.

### Safety
- `GITHUB_TOKEN` hiçbir output dosyasına serialize edilmez.
- Otomatik upload yoktur.
- `--repo` strict `owner/repo` formatıyla doğrulanır.
- Yalnız completed + failure run kabul edilir; belirsiz/in-progress run fail-closed davranır.
- Failed-job logları karakter guard ile sınırlandırılır ve mevcut secret redactor'dan geçirilir.
- Local bundle `system.json` paket sürümünü hard-code etmek yerine `__version__` üzerinden alır.

### Verified so far
- Yeni GitHub Native fixture testleri CI matrisinde çalışıyor ve gözlenen Ubuntu/Windows job'larında PASS.
- v0.3 historical + CLI regression testleri korunuyor.
- **Release gate açık:** gerçek public failed Actions run'ın FixBundle CLI ile capture edilip README kanıtına bağlanması henüz tamamlanmadı. Issue #2 bu gate kapanana kadar açık kalır.

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
- GitHub Actions run #43: **9/9 job PASS**.
- Ubuntu, Windows ve macOS üzerinde Python 3.10 / 3.12 / 3.13 doğrulandı.
- `pytest -q`: **5 passed**.
- Historical demo **5/5 invariant PASS**.
- Demo, eski kaynakta gerçek `AssertionError` yakaladı ve current HEAD/dirty workspace'i korudu.

## 0.2.0 — 2026-09-02

### Added
- Node.js, Python, Rust, .NET, Go ve Java stack algılama.
- `fixbundle --recommend` ile güvenli doğrulama komutu önerileri.
- Türkçe/İngilizce CLI (`--lang auto|tr|en`).
- `git/head.txt` ve `git/branch.txt` commit identity kanıtı.
- `stack.json` bundle kanıtı.
- URL credentials, JWT ve ek secret pattern redaction.
- Proje ve home absolute path masking.

### Hardened
- `.fixbundle` recursion dışlaması.
- `.npmrc`, `.pypirc`, `secrets.json` secret-file dışlaması.
- Büyük text/diff/log capture'ları için 200k karakter guard.

## 0.1.0 — 2026-09-02
- İlk local AI-ready diagnostic bundle prototipi.
