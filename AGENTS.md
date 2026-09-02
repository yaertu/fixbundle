# FixBundle repository steward protocol

Bu dosya Codex, Claude Code, Cursor ve diğer kodlama ajanlarının projeyi aynı kurallarla sürdürebilmesi için repo-local çalışma sözleşmesidir.

## Ürün cümlesi
**One command turns a broken project or historical Git commit into a redacted, AI-ready debugging bundle.**

## Her bakım turunun sırası
1. Güncel `main`, CI, açık issue/PR ve README iddialarını oku.
2. Yeni geliştirme için gerçek kullanıcı problemi veya tekrarlanabilir hata kanıtı ara.
3. Değişiklik davranışsal ise test ekle/değiştir.
4. Lokal gate çalıştır:
   ```bash
   python -m pytest -q
   python scripts/demo.py
   fixbundle --version
   fixbundle . --recommend --lang tr
   ```
5. Davranış değiştiyse `CHANGELOG.md`, `ROADMAP.md`, README sürümü/demo metni ve `docs/evidence/SMOKE_TEST.md` senkron olmalı.
6. CI sonucunu görmeden “cross-platform PASS” yazma.
7. Star/download/benchmark/user quote/sponsor gibi dış metrikleri uydurma.
8. Secret veya proprietary bundle içeriğini repoya koyma.
9. Sırf aktivite görünsün diye commit atma. Anlamlı değişiklik yoksa repo değişmeden kalabilir.

## GitHub ana sayfa senkronu
Her davranış sürümünde README'deki **GitHub About / Topics** bölümü kontrol edilir.

Hedef açıklama:
`One command turns a broken project or historical Git commit into a redacted, AI-ready debugging bundle.`

Hedef topics:
`ai-debugging`, `developer-tools`, `diagnostics`, `bug-report`, `support-bundle`, `codex`, `claude-code`, `cursor`, `reproducibility`, `git`

Connector/API repository About/Topics yazma yetkisi yoksa bu liste repo içinde güncel tutulur ve yalnız bu UI ayarı için maintainer'a kısa bir manuel görev verilir.

## Sürüm kararı
- docs-only: version bump yok
- backward-compatible behavior: minor
- bug fix: patch
- stable schema kırılması (v1+): semver major

## Devam promptu
Yeni bir ajan oturumu bu dosyayı okuyup aşağıdaki görevi çalıştırabilir:

```text
Continue as FixBundle repository steward for yaertu/fixbundle.
Start from current main. Run /truth + /audit discipline: inspect repository state, CI, issues/PRs, README claims and latest evidence before changing anything.
Research current GitHub/Reddit/web signals around AI debugging context, historical production bugs, support bundles, CI failure handoff, privacy/redaction and competing tools.
Make only one or a few evidence-backed improvements that materially improve usefulness, reliability or adoption. Preserve local-first/privacy-safe behavior. Add or update tests for behavior changes. Run python -m pytest -q and python scripts/demo.py. Sync README, CHANGELOG, ROADMAP, docs/evidence/SMOKE_TEST.md and GitHub About/Topics recommendations when behavior or positioning changes. Never fabricate metrics, testimonials, compatibility, benchmarks or test passes. Check CI after changes and repair failures caused by the change. End with: what changed, proof, current CI, current repo-home metadata, and the highest-value next move.
```
