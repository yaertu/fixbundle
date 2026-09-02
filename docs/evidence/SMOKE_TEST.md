# v0.3.0 doğrulama kanıtı

README'deki davranış iddialarını yeniden üretmek için gereken kısa kanıt zinciri.

## 1. Unit / integration tests

```text
$ python -m pytest -q
....                                                                     [100%]
4 passed
```

Kapsanan ana davranışlar:
- bundle üretimi ve secret/path redaction
- stack detection
- provider/token redaction
- historical commit capture + dirty workspace preservation

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

`.github/workflows/ci.yml` aşağıdaki matrisi çalıştırır:
- ubuntu-latest / windows-latest / macos-latest
- Python 3.10 / 3.12 / 3.13
- pytest
- CLI smoke
- historical demo

GitHub Actions sonucu README'deki CI badge üzerinden görülebilir.

## 4. Kanıt sınırı

Bu belge yalnız doğrulanmış test/demo sonuçlarını kaydeder. Star, download, performans veya “AI daha iyi çözer” gibi ölçülmemiş iddialar kanıt sayılmaz.
