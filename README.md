<p align="center">
  <img src="assets/fixbundle-logo.svg" width="112" alt="FixBundle logo">
</p>

<h1 align="center">FixBundle 🧰</h1>

<p align="center"><strong>Bozuk projeyi, failed command'i veya eski Git commit'ini tek ZIP'lik hata kanıtına çevir.</strong></p>

<p align="center">
  <a href="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version 0.3.0" src="https://img.shields.io/badge/version-0.3.0-8B5CF6">
  <img alt="CI matrix 9/9" src="https://img.shields.io/badge/CI_matrix-9%2F9_pass-22C55E">
  <img alt="Local first" src="https://img.shields.io/badge/privacy-local--first-0EA5E9">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-22C55E">
</p>

<p align="center"><img src="assets/hero.svg" width="100%" alt="FixBundle: failure to portable AI debugging evidence"></p>

**Logları tek tek kopyalamak, hangi commit'te hata çıktığını anlatmak ve kaynak dosyalarını rastgele sohbete atmak yerine tek kanıt paketi üret.** FixBundle; Git identity/diff, gerçek test-build-runtime çıktıları, ortam bilgisi ve ilgili text/config dosyalarını toplar, yaygın secret/path kalıplarını maskeler ve aynı kanıt setini ChatGPT, Codex, Claude Code, Cursor veya insan destek ekibine verebileceğin checksum'lı bir ZIP'e dönüştürür.

## 🎬 Gerçek çalışma demosu

<p align="center">
  <img src="docs/demo/fixbundle-v0.3-demo.svg" width="100%" alt="FixBundle v0.3 historical debugging demo">
</p>

Demoda hata **eski bir commit'te**, güncel branch ise düzeltilmiş durumda. Çalışma alanında ayrıca commitlenmemiş bir dosya var. `--commit` eski commit'i geçici detached Git worktree içinde çalıştırıyor, gerçek `AssertionError` çıktısını bundle'a koyuyor ve güncel HEAD/dirty workspace'i değiştirmiyor.

Bunu kendin yeniden üret:

```bash
python scripts/demo.py
```

Beklenen invariant'lar:

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

Önce stack'e göre doğrulama komutu önerilerini görmek için:

```bash
fixbundle . --recommend --lang tr
```

## 📦 ZIP'in içinde ne var?

```text
AI_HANDOFF.md          # kanıt önceliği + beklenen çözüm formatı
manifest.json          # capture özeti + privacy sınırları
incident.json          # --commit kullanıldıysa incident/current commit kimliği
stack.json             # algılanan teknoloji yığını + önerilen komutlar
system.json            # OS/runtime kanıtı
tree.txt               # filtrelenmiş proje ağacı
SHA256SUMS.txt         # bütünlük hash'leri
git/
  head.txt
  branch.txt
  status.txt
  diff.patch
  recent.txt
commands/
  01.log               # gerçek command output + exit evidence
project/
  ...                  # seçilmiş text/source/config snapshotları
```

## 🧭 Neden `--commit` önemli?

Production bug'larında sık görülen sorun basit: **hata geçmişte oldu, debugger bugünkü kodu okuyor.** FixBundle v0.3 eski commit'i mevcut çalışma klasörüne checkout etmez. Geçici, detached bir Git worktree açar; kanıtı orada toplar; worktree'yi siler ve ana çalışma alanının HEAD/dirty durumunun aynı kaldığını doğrular.

Bu davranış testle korunuyor: [`tests/test_history.py`](tests/test_history.py).

## 🧩 FixBundle neyin yerine geçmiyor?

Komşu araçları yok saymak yerine sınırı net tutuyoruz:

| Araç / yaklaşım | Ana iş |
|---|---|
| **Repomix** | repository'yi LLM-friendly code context'e paketlamak |
| **temporal-debug-skill** | agent'a eski commit'i worktree ile inceleme akışı öğretmek |
| **GitHub Actions + Copilot** | GitHub içindeki failed check/log'u açıklamak |
| **FixBundle** | **failure event'i agent/vendor bağımsız, redacted ve checksum'lı kanıt paketine çevirmek** |

Ayrıntılı ve kaynak bağlantılı ürün sınırı: [`docs/product/LANDSCAPE.md`](docs/product/LANDSCAPE.md).

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

GitHub Actions run #43 / behavior commit `153dbec`:

```text
$ pytest -q
.....                                                                    [100%]
5 passed

$ python scripts/demo.py
PASS  incident_commit_matches
PASS  current_head_preserved
PASS  dirty_workspace_preserved
PASS  old_buggy_source_captured
PASS  real_failure_captured
```

**Ubuntu + Windows + macOS × Python 3.10 / 3.12 / 3.13 = 9/9 CI job PASS.** Windows'ta yakalanan legacy code-page hatası da regression testine dönüştürüldü. Kanıt: [`docs/evidence/CI_MATRIX.md`](docs/evidence/CI_MATRIX.md) · [`docs/evidence/SMOKE_TEST.md`](docs/evidence/SMOKE_TEST.md).

## 🌍 English quick summary

**Package a broken repo, failed command, or historical Git commit into a redacted AI-ready debugging bundle.** FixBundle captures failure output, exact Git identity, runtime/stack evidence and relevant source/config snapshots. v0.3 can reproduce an incident from an older commit in an isolated Git worktree without checking out over your current workspace.

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
fixbundle . --run "npm test" --run "npm run build"
fixbundle . --commit <incident-sha> --run "npm test"
```

## 🗺️ Yol haritası

- **v0.3 ✅ Temporal evidence:** historical commit/worktree capture + workspace preservation.
- **v0.4 GitHub Native:** failed Actions run → portable FixBundle evidence.
- **v0.5 Production Evidence:** Sentry/structured log adapter + bounded time window.
- **v0.6 Regression Fingerprints:** bundle-vs-bundle failure/environment/dependency drift.
- **v1.0 Stable Evidence Protocol:** versioned schema + plugin SDK + signed manifest option.

Sıradaki tek hedef: [`docs/product/NEXT.md`](docs/product/NEXT.md) · detaylı yol haritası: [`ROADMAP.md`](ROADMAP.md).

## 🤝 Proje / büyüme notları

- Katkı: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Güvenlik: [`SECURITY.md`](SECURITY.md)
- Neden şimdi?: [`docs/product/WHY_NOW.md`](docs/product/WHY_NOW.md)
- Rakip/komşu araçlar: [`docs/product/LANDSCAPE.md`](docs/product/LANDSCAPE.md)
- Launch metinleri: [`docs/product/LAUNCH_PLAYBOOK.md`](docs/product/LAUNCH_PLAYBOOK.md)
- Gelir yaklaşımı: [`docs/product/MONETIZATION.md`](docs/product/MONETIZATION.md)
- Gerçek adoption baseline: [`docs/product/METRICS.md`](docs/product/METRICS.md)
- Repo bakım protokolü/continuation: [`AGENTS.md`](AGENTS.md)

## 🔎 GitHub About / Topics

Önerilen açıklama:

> Package a broken repo, failed command, or historical Git commit into a redacted AI-ready debugging bundle.

Önerilen discovery topics:

`ai-debugging` · `developer-tools` · `devtools` · `production-debugging` · `temporal-debugging` · `support-bundle` · `diagnostics` · `bug-report` · `ai-coding-assistant` · `codex` · `claude-code` · `cursor` · `reproducibility` · `git` · `llm`

Kaynak: [`docs/product/REPO_HOME.md`](docs/product/REPO_HOME.md).

## 📜 Lisans

MIT.
