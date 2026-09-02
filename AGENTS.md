# FixBundle repository steward protocol

Bu dosya Codex, Claude Code, Cursor ve diğer kodlama ajanlarının projeyi aynı kurallarla sürdürebilmesi için repo-local çalışma sözleşmesidir.

## Ürün cümlesi
**Capture failure evidence, keep it portable, and compare what changed without trusting one vendor or one AI tool.**

Ürün sınırı: repository context packer, observability dashboard, generic log diff veya vendor-specific “explain error” aracı değil. FixBundle'ın çekirdeği **portable failure evidence + deterministic evidence comparison**.

## Her bakım turunun sırası
1. Güncel `main`, CI, açık issue/PR, README ve canlı repo metadata'sını oku.
2. `docs/product/METRICS.md`, `REPO_HOME.md`, `NEXT.md` ve mevcut evidence belgelerini kontrol et.
3. Yeni geliştirme için gerçek kullanıcı problemi veya tekrarlanabilir failure kanıtı ara; komşu araçları ve resmi platform yeteneklerini yok sayma.
4. Davranış değişikliği test gerektirir.
5. Lokal gate:
   ```bash
   python -m pytest -q
   python scripts/demo.py
   python scripts/demo_otlp.py
   python scripts/demo_compare.py
   fixbundle --version
   fixbundle . --recommend --lang tr
   ```
6. GitHub Native davranışı değişirse live gate'i koru:
   ```bash
   export GITHUB_TOKEN=<actions-read-contents-read-token>
   fixbundle github --repo yaertu/fixbundle --run 33587184675 --output .fixbundle-live --lang en
   python scripts/verify_live_github.py .fixbundle-live
   ```
7. Compare input/archive/security davranışı değişirse checksum, hostile ZIP ve cross-source tests geçmeden merge etme.
8. CI sonucunu görmeden cross-platform veya live PASS yazma.
9. Star/download/benchmark/user quote/sponsor/novelty iddiası uydurma.
10. Secret veya proprietary bundle içeriğini repoya koyma.
11. Sırf aktivite görünsün diye commit atma.

## Kanıt ankrajları
### v0.4 GitHub Native
- source failed run: `33587184675`
- proof run: `33589138174`
- expected: platform matrix + Live GitHub failure evidence PASS
- evidence: `docs/evidence/V04_LIVE_GITHUB.md`

### v0.5 Production Evidence
- OTLP Protocol File Exporter JSON/JSONL
- exact trace/span correlation
- local/offline, bounded, redacted, checksummed
- demo: `scripts/demo_otlp.py`

### v0.6 Cross-source Compare
- CLI: `fixbundle compare baseline.zip incident.zip [--format json]`
- input schemas: `fixbundle/0.3`, `0.4`, `0.5`
- integrity is validated before evidence interpretation
- ZIPs are never extracted or mutated
- no network/LLM required
- demo: `scripts/demo_compare.py`
- design: `docs/product/V06_COMPARE.md`

## GitHub ana sayfa senkronu
Her positioning/release değişiminde README ve `docs/product/REPO_HOME.md` birlikte kontrol edilir.

v0.6 target description:
`Package failures into redacted evidence bundles and compare what changed across local, CI, and OpenTelemetry incidents.`

Target topics are maintained in `docs/product/REPO_HOME.md`. Connected tools About/Topics yazamıyorsa yalnız bu UI adımı maintainer'a kısa görev olarak verilir. Değiştirildiğini görmeden değişti denmez.

## Sürüm kararı
- docs-only: version bump yok
- backward-compatible behavior: minor
- bug fix: patch
- stable schema kırılması (v1+): semver major

## Current product gate
v0.6 sonrası varsayılan hareket yeni adapter veya panel yazmak değildir. Önce `docs/product/NEXT.md` içindeki **distribution / repeat-use gate** sınanır. Amaç, unrelated bir maintainer'ın bir FixBundle artifact'ını saklayıp sonraki incident'ta compare için yeniden kullanmasıdır.

## Devam promptu

```text
Continue as FixBundle repository steward for yaertu/fixbundle.
Start from current main and read AGENTS.md, README, ROADMAP, docs/product/NEXT.md, REPO_HOME.md, METRICS.md, open issues/PRs and latest CI before changing anything.
Run /truth + /audit discipline. Preserve the proven local, historical, live GitHub, OTLP and compare evidence gates. Compare must validate bundle integrity before interpretation and must remain read-only, local and deterministic.
Search current GitHub/Reddit/web and official docs for actual failure-evidence pain, competing tools, repeat-use signals and distribution friction. Never build a wrapper that merely duplicates a vendor's existing LLM/debugging feature.
The current highest-value gate is distribution and repeat use: prove that an unrelated maintainer can install FixBundle, capture a real failure, retain the artifact, and use compare when the next incident changes or recurs. Do not start v0.7 merely to increase version count.
Make only evidence-backed changes. Keep README/CHANGELOG/ROADMAP/evidence/repo-home metadata recommendations synchronized. Never fabricate users, stars, downloads, benchmarks, tests, compatibility, screenshots or novelty. Check CI after changes and repair failures caused by the change before claiming success.
End with: what changed, proof, current CI, live public metrics, repo-home metadata status, and the single highest-value next move.
```
