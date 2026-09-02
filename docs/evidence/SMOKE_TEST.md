# v0.3.0 doğrulama kanıtı

README'deki davranış iddialarını yeniden üretmek için gereken kısa kanıt zinciri.

## 1. Unit / integration tests

GitHub Actions run #43 içindeki Windows Python 3.12 örneği:

```text
$ pytest -q
.....                                                                    [100%]
5 passed in 1.32s
```

Kapsanan ana davranışlar:
- bundle üretimi ve secret/path redaction
- stack detection
- provider/token redaction
- historical commit capture + dirty workspace preservation
- legacy Windows/CP1252-benzeri stdout koşulunda Türkçe CLI'nin çökmeden çalışması

## 2. Historical incident demo

```text
$ python scripts/demo.py
FixBundle historical demo
PASS  incident_commit_matches
PASS  current_head_preserved
PASS  dirty_workspace_preserved
PASS  old_buggy_source_captured
PASS  real_failure_captured
```

Demo iki commit üretir. İlk commit bilinçli olarak bozuk, ikinci commit düzeltilmiştir. Ayrıca current workspace'e commitlenmemiş `notes.txt` eklenir. FixBundle eski commit'i detached worktree içinde çalıştırır ve bundle içindeki `commands/01.log` dosyasına gerçek `AssertionError` koyar. Demo sonunda current HEAD ve `notes.txt` korunmuş olmalıdır.

## 3. CI

Doğrulanan behavior commit: `153dbecae075c6cc48e6375450ebf2493f263705`

GitHub Actions run: `33587276906`

`.github/workflows/ci.yml` matrisi:
- Ubuntu / Windows / macOS
- Python 3.10 / 3.12 / 3.13
- pytest
- CLI smoke
- historical demo

**9/9 job PASS.** Ayrıntı: [CI_MATRIX.md](CI_MATRIX.md).

## 4. Kanıt sınırı

Bu belge yalnız doğrulanmış test/demo sonuçlarını kaydeder. Star, download, performans veya “AI daha iyi çözer” gibi ölçülmemiş iddialar kanıt sayılmaz.
