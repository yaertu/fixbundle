# Changelog

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
- Binary Git diff yerine bounded textual unified diff.

### Verified
- 3/3 local test PASS.
- Self-capture smoke test PASS.
- Python wheel 0.2.0 local build PASS.

## 0.1.0 — 2026-09-02
- İlk local AI-ready diagnostic bundle prototipi.
