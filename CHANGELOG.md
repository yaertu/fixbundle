# Changelog

## 0.3.0 — 2026-09-02

### Added
- `--commit <ref>` ile eski bir Git commit'ini izole, detached worktree içinde capture etme.
- `incident.json`: requested ref, incident commit ve current HEAD kimliği.
- Current vs incident commit ayrımını `manifest.json` içine taşıyan `fixbundle/0.3` schema.
- `scripts/demo.py`: eski production commit'ini yeniden üreten gerçek, tek komutlu demo.
- README içine gerçek çalışma akışından üretilen GIF kanıtı.

### Safety
- Historical capture mevcut branch'i checkout etmez.
- Commitlenmemiş çalışma alanı capture öncesi/sonrası karşılaştırılır.
- Geçici worktree hata halinde de temizlenir.
- Output klasörü workspace dirty-state karşılaştırmasından ayrıştırılır.

### Verified
- 4/4 local tests PASS.
- Historical demo 5/5 invariant PASS.
- Demo, eski kaynakta gerçek `AssertionError` yakaladı ve current HEAD'i korudu.

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
