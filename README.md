<p align="center">
  <img src="assets/fixbundle-logo.svg" width="112" alt="FixBundle logo">
</p>

<h1 align="center">FixBundle 🧰</h1>

<p align="center"><strong>Bozuk projeyi tek komutla, paylaşılabilir ve AI-ready hata ayıklama paketine çevir.</strong></p>

<p align="center">
  <a href="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version 0.3.0" src="https://img.shields.io/badge/version-0.3.0-8B5CF6">
  <img alt="Local first" src="https://img.shields.io/badge/privacy-local--first-0EA5E9">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-22C55E">
</p>

<p align="center"><img src="assets/hero.svg" width="100%" alt="FixBundle: broken project to AI-ready debugging bundle"></p>

**Logları tek tek kopyalamak, hangi commit'te hata çıktığını anlatmak ve kaynak dosyalarını rastgele sohbete atmak yerine tek ZIP üret.** FixBundle; Git durumu, gerçek test/build çıktıları, ortam bilgisi ve ilgili metin dosyalarını toplar, yaygın secret kalıplarını maskeler ve aynı kanıt setini ChatGPT, Codex, Claude Code, Cursor veya insan destek ekibine verebileceğin hale getirir.

## 🎬 Gerçek çalışma demosu

<p align="center">
  <img src="docs/demo/fixbundle-v0.3-demo.gif" width="100%" alt="FixBundle v0.3 historical debugging demo">
</p>

Demoda hata **eski bir commit'te**, güncel branch ise düzeltilmiş durumda. Çalışma alanında ayrıca commitlenmemiş bir dosya var. `--commit` eski commit'i geçici Git worktree içinde çalıştırıyor, gerçek `AssertionError` çıktısını bundle'a koyuyor ve güncel çalışma alanını değiştirmiyor.

Bunu kendin yeniden üret:

```bash
python scripts/demo.py
```

Beklenen sonuç:

```text
PASS  incident_commit_matches
PASS  current_head_preserved
PASS  dirty_workspace_preserved
PASS  old_buggy_source_captured
PASS  real_failure_captured
```

## ⚡ Kurulum ve kullanım

PyPI yayını yapılana kadar doğrudan GitHub'dan:

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
```

Güncel proje için:

```bash
cd bozuk-proje
fixbundle . --lang tr --run "pytest -q" --run "python -m build"
```

Eski commit'te yaşanmış production hatası için:

```bash
fixbundle . --commit <commit-sha> --run "python app.py" --lang tr
```

Hangi doğrulama komutlarının mantıklı olduğunu görmek için:

```bash
fixbundle . --recommend --lang tr
```

## 📦 ZIP'in içinde ne var?

```text
AI_HANDOFF.md          # inceleme sırası ve beklenen çözüm formatı
manifest.json          # capture özeti + privacy sınırları
incident.json          # --commit kullanıldıysa incident/current commit kimliği
stack.json             # algılanan teknoloji yığını + önerilen komutlar
system.json            # işletim sistemi/runtime bilgisi
tree.txt               # filtrelenmiş proje ağacı
SHA256SUMS.txt         # dosya bütünlük hash'leri
git/
  head.txt
  branch.txt
  status.txt
  diff.patch
  recent.txt
commands/
  01.log               # gerçek test/build/runtime çıktısı
project/
  ...                  # seçilmiş text/source/config snapshotları
```

## 🧭 Neden `--commit` önemli?

Production bug'larında sık görülen sorun basit: **hata dün oldu, AI bugünkü kodu okuyor.** FixBundle v0.3 eski commit'i mevcut çalışma klasörüne checkout etmez. Geçici, detached bir Git worktree açar; kanıtı orada toplar; worktree'yi siler ve ana çalışma alanının HEAD/dirty durumunun aynı kaldığını doğrular.

Bu davranış testle korunuyor: [`tests/test_history.py`](tests/test_history.py).

## 🛡️ Privacy by default

FixBundle:

- `.env`, `.npmrc`, `.pypirc`, credential/secrets dosyalarını varsayılan olarak **almaz**.
- API key, bearer token, GitHub/OpenAI/Google/AWS token kalıpları, JWT, private key ve URL credential kalıplarını **maskeler**.
- Proje kökü ve kullanıcı home yolunu `<PROJECT>` / `<HOME>` olarak **anonimleştirir**.
- `node_modules`, `.git`, `target`, `dist`, `build`, `.fixbundle` gibi vendor/üretilmiş klasörleri **dışlar**.
- Metin, diff ve log capture'larını boyut sınırıyla **kontrol altında tutar**.
- Hiçbir şeyi kendiliğinden buluta yüklemez. **Local-first** çalışır.

Redaction kusursuzluk garantisi değildir. Hassas veya proprietary bir bundle'ı public paylaşmadan önce ZIP'i kontrol et.

## 🧩 Stack algılama

| Yığın | Kanıt örneği | Öneri örneği |
|---|---|---|
| 🟨 Node.js | `package.json` | `npm test`, `npm run build` |
| 🐍 Python | `pyproject.toml`, `requirements.txt` | `pytest -q`, `python -m build` |
| 🦀 Rust | `Cargo.toml` | `cargo test`, `cargo build --release` |
| 🟪 .NET | `.sln`, `.csproj` | `dotnet test`, `dotnet build -c Release` |
| 🐹 Go | `go.mod` | `go test ./...`, `go build ./...` |
| ☕ Java | `pom.xml`, Gradle | `mvn test`, package/build |

FixBundle öneri verir; önerilen komutları kullanıcı istemeden otomatik çalıştırmaz.

## ✅ Kanıt zinciri

Yerel v0.3 doğrulaması:

```text
$ python -m pytest -q
....                                                                     [100%]
4 passed

$ python scripts/demo.py
PASS  incident_commit_matches
PASS  current_head_preserved
PASS  dirty_workspace_preserved
PASS  old_buggy_source_captured
PASS  real_failure_captured
```

CI; Ubuntu, Windows ve macOS üzerinde Python 3.10 / 3.12 / 3.13 matrisini çalıştırır. Ayrıntılı ve yeniden üretilebilir kanıt: [`docs/evidence/SMOKE_TEST.md`](docs/evidence/SMOKE_TEST.md).

## 🌍 English quick summary

**One command turns a broken project into a redacted, AI-ready debugging bundle.** FixBundle captures Git identity, command failures, runtime/stack evidence and relevant source/config snapshots. v0.3 can reproduce an incident from an older commit in an isolated Git worktree without checking out over your current workspace.

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
fixbundle . --run "npm test" --run "npm run build"
fixbundle . --commit <incident-sha> --run "npm test"
```

## 🗺️ Yol haritası

- **v0.3 ✅ Temporal Debugging:** historical commit/worktree capture + workspace preservation.
- **v0.4 GitHub Native:** failed Actions run → AI-ready evidence bundle.
- **v0.5 Production Evidence:** Sentry/structured log adapter + bounded time window.
- **v0.6 Regression Fingerprints:** bundle-vs-bundle failure/environment/dependency drift.
- **v1.0 Stable Evidence Protocol:** versioned schema + plugin SDK + signed manifest option.

Detay: [`ROADMAP.md`](ROADMAP.md)

## 🤝 Katkı ve proje yönetimi

- Katkı: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Güvenlik: [`SECURITY.md`](SECURITY.md)
- Neden şimdi?: [`docs/product/WHY_NOW.md`](docs/product/WHY_NOW.md)
- Dağıtım/launch metinleri: [`docs/product/LAUNCH_PLAYBOOK.md`](docs/product/LAUNCH_PLAYBOOK.md)
- Sürdürülebilir gelir yaklaşımı: [`docs/product/MONETIZATION.md`](docs/product/MONETIZATION.md)
- Repo bakım protokolü ve devam komutları: [`AGENTS.md`](AGENTS.md)

## 🔎 GitHub About / Topics

Önerilen açıklama:

> One command turns a broken project or historical Git commit into a redacted, AI-ready debugging bundle.

Önerilen topics:

`ai-debugging` · `developer-tools` · `diagnostics` · `bug-report` · `support-bundle` · `codex` · `claude-code` · `cursor` · `reproducibility` · `git`

## 📜 Lisans

MIT.
