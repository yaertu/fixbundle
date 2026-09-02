<p align="center">
  <img src="assets/fixbundle-logo.svg" width="112" alt="FixBundle logo">
</p>

<h1 align="center">FixBundle 🧰</h1>

<p align="center"><strong>Bozuk projeyi, failed command'i, eski Git commit'ini veya failed GitHub Actions run'ını taşınabilir hata kanıtına çevir.</strong></p>

<p align="center">
  <a href="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yaertu/fixbundle/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="Version 0.4.0" src="https://img.shields.io/badge/main-0.4.0-8B5CF6">
  <img alt="CI matrix 9/9" src="https://img.shields.io/badge/CI_matrix-9%2F9_pass-22C55E">
  <img alt="Privacy" src="https://img.shields.io/badge/privacy-redaction_first-0EA5E9">
  <img alt="License MIT" src="https://img.shields.io/badge/license-MIT-22C55E">
</p>

<p align="center"><img src="assets/hero.svg" width="100%" alt="FixBundle: failure to portable AI debugging evidence"></p>

**Hata ayıklarken asıl zaman kaybı çoğu kez hatayı açıklamak değil, kanıtı toplamaktır.** FixBundle; failure output, exact Git identity, diff, runtime/stack bilgisi ve ilgili config/source parçalarını aynı pakete koyar, yaygın secret/path kalıplarını maskeler ve sonucu checksum'lı ZIP olarak verir. Aynı kanıtı Codex'e, Claude Code'a, Cursor'a, ChatGPT'ye veya insan destek ekibine taşıyabilirsin.

## 🎬 Gerçek çalışma demosu

<p align="center">
  <img src="docs/demo/fixbundle-v0.3-demo.svg" width="100%" alt="FixBundle historical debugging demo">
</p>

Demoda hata **eski bir commit'te**, güncel branch ise düzeltilmiş durumda. Çalışma alanında commitlenmemiş dosya da var. `--commit` eski commit'i geçici detached Git worktree içinde çalıştırıyor, gerçek `AssertionError` çıktısını bundle'a koyuyor ve güncel HEAD/dirty workspace'i değiştirmiyor.

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

## ⚡ Kurulum

PyPI yayını yapılana kadar doğrudan GitHub'dan:

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
```

Güncel proje:

```bash
fixbundle . --lang tr --run "pytest -q" --run "python -m build"
```

Eski commit'teki production hatası:

```bash
fixbundle . --commit <commit-sha> --run "python app.py" --lang tr
```

## 🛰️ GitHub Actions failure capture — v0.4

Bir failed Actions run'ın loglarını elle indirip sohbet kutusuna yapıştırmak yerine:

```bash
export GITHUB_TOKEN=<read-only-token>
fixbundle github --repo owner/repo --run 123456789 --lang tr
```

Windows PowerShell:

```powershell
$env:GITHUB_TOKEN = "<read-only-token>"
fixbundle github --repo owner/repo --run 123456789 --lang tr
```

Token için mümkün olan en dar **Actions: Read + Contents: Read** yetkisini kullan. Token bundle içine yazılmaz ve FixBundle üretilen ZIP'i kendiliğinden hiçbir yere yüklemez.

Remote capture şunları normalize eder:

```text
AI_HANDOFF.md
github/
  run.json             # repo / workflow / run / commit identity
  jobs.json            # job + step sonuçları
  jobs/<job-id>.log    # yalnız failed job logları, bounded + redacted
  commit.json          # ilgili commit + bounded patch context
  workflow.yml         # olay anındaki workflow config, erişilebiliyorsa
manifest.json
SHA256SUMS.txt
```

Bu yol **local checkout gerektirmez**. v0.4 çekirdeği recorded/synthetic fixture testleriyle exact run/job/step identity, secret redaction, workflow config ve commit patch capture davranışını doğruluyor. **Gerçek public failed-run → ZIP demo, v0.4 release gate'i olarak hâlâ açık; tamamlanmadan README'de “live verified” iddiası kullanmıyoruz.** Takip: [issue #2](https://github.com/yaertu/fixbundle/issues/2).

## 📦 Local bundle'ın içinde ne var?

```text
AI_HANDOFF.md
manifest.json
incident.json          # --commit kullanıldıysa
stack.json
system.json
tree.txt
SHA256SUMS.txt
git/
  head.txt
  branch.txt
  status.txt
  diff.patch
  recent.txt
commands/
  01.log
project/
  ...
```

## 🧩 FixBundle neyin yerine geçmiyor?

| Araç / yaklaşım | Ana iş |
|---|---|
| **Repomix** | repository'yi LLM-friendly code context'e paketlamak |
| **temporal-debug-skill** | agent'a eski commit'i worktree ile inceleme akışı öğretmek |
| **GitHub Actions + Copilot** | GitHub içindeki failed check/log'u açıklamak |
| **FixBundle** | **failure event'i agent/vendor bağımsız, redacted ve checksum'lı kanıt paketine çevirmek** |

FixBundle başka bir “AI chat” veya tüm repository'yi tek dosyaya çeviren context packer olmaya çalışmıyor. Ürün sınırı: **portable failure evidence**. Ayrıntı: [`docs/product/LANDSCAPE.md`](docs/product/LANDSCAPE.md).

## 🛡️ Privacy by default

- `.env`, `.npmrc`, `.pypirc`, credential/secrets dosyaları local capture'da varsayılan olarak alınmaz.
- API key, bearer token, GitHub/OpenAI/Google/AWS token kalıpları, JWT, private key ve URL credential kalıpları maskelenir.
- Local project/home path'leri anonimleştirilir.
- Vendor/build/cache klasörleri dışlanır.
- Text, diff ve log capture'ları boyut sınırıyla tutulur.
- GitHub token output'a serialize edilmez.
- Otomatik cloud upload yoktur.

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

Önerilen doğrulama komutlarını yalnızca görmek için:

```bash
fixbundle . --recommend --lang tr
```

## ✅ Kanıt zinciri

v0.3 historical behavior için cross-platform matrix doğrulandı: **Ubuntu + Windows + macOS × Python 3.10 / 3.12 / 3.13 = 9/9 job PASS.** v0.4 GitHub Native fixture testleri de aynı CI matrisine eklendi. Güncel CI badge'i üstteki workflow'un canlı sonucudur; ayrıntı: [`docs/evidence/CI_MATRIX.md`](docs/evidence/CI_MATRIX.md) · [`docs/evidence/SMOKE_TEST.md`](docs/evidence/SMOKE_TEST.md).

## 🌍 English quick summary

**Package a broken repo, failed command, historical Git commit, or failed GitHub Actions run into a redacted, portable debugging bundle.** FixBundle captures failure output and exact incident identity, adds bounded source/config/diff context, redacts common secrets, and produces checksummed evidence that can move between coding agents and human support.

```bash
pipx install git+https://github.com/yaertu/fixbundle.git
fixbundle . --run "npm test"
fixbundle . --commit <incident-sha> --run "npm test"
fixbundle github --repo owner/repo --run <failed-run-id>
```

## 🗺️ Yol haritası

- **v0.3 ✅ Temporal evidence:** historical commit/worktree capture + workspace preservation.
- **v0.4 🚧 GitHub Native:** collector + CLI + fixture tests hazır; real public failed-run proof release gate'i bekliyor.
- **v0.5 Production Evidence:** Sentry/structured log adapter + bounded time window.
- **v0.6 Regression Fingerprints:** bundle-vs-bundle failure/environment/dependency drift.
- **v1.0 Stable Evidence Protocol:** versioned schema + plugin SDK + signed manifest option.

Sıradaki tek hedef: [`docs/product/NEXT.md`](docs/product/NEXT.md) · detaylı yol haritası: [`ROADMAP.md`](ROADMAP.md).

## 🤝 Proje / büyüme notları

- Katkı: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Güvenlik: [`SECURITY.md`](SECURITY.md)
- Rakip/komşu araçlar: [`docs/product/LANDSCAPE.md`](docs/product/LANDSCAPE.md)
- Launch planı: [`docs/product/LAUNCH_PLAYBOOK.md`](docs/product/LAUNCH_PLAYBOOK.md)
- Gelir yaklaşımı: [`docs/product/MONETIZATION.md`](docs/product/MONETIZATION.md)
- Adoption baseline: [`docs/product/METRICS.md`](docs/product/METRICS.md)
- Repo bakım protokolü/continuation: [`AGENTS.md`](AGENTS.md)

## 🔎 GitHub About / Topics

Canlı About açıklaması:

> Package a broken repo, failed command, or historical Git commit into a redacted AI-ready debugging bundle.

Canlı discovery topics:

`ai-debugging` · `developer-tools` · `devtools` · `production-debugging` · `temporal-debugging` · `support-bundle` · `diagnostics` · `bug-report` · `ai-coding-assistant` · `codex` · `claude-code` · `cursor` · `reproducibility` · `git` · `llm`

Bu metadata 2026-09-02'de GitHub API üzerinden doğrulandı. Kaynak/senkron kuralı: [`docs/product/REPO_HOME.md`](docs/product/REPO_HOME.md).

## 📜 Lisans

MIT.
