# v0.2.0 doğrulama kanıtı

Bu belge, README'deki çalışabilirlik iddialarının kısa ve yeniden üretilebilir kanıtıdır.

## Yerel test sonucu

```text
$ python -m pytest -q
...                                                                      [100%]
3 passed in 1.58s
```

## Gerçek self-capture

```text
$ fixbundle . --lang tr --run "python -m pytest -q"
FixBundle hazır ✅
  Dosya: 24
  Komut: 1
  Gizleme/yol maskeleme: 7
```

Üretilen bundle içerisinde `AI_HANDOFF.md`, `manifest.json`, `stack.json`, `system.json`, `tree.txt`, `git/head.txt`, `git/status.txt`, `git/diff.patch`, komut logları ve `SHA256SUMS.txt` bulunur.

## Wheel

`fixbundle-0.2.0-py3-none-any.whl` yerel olarak `pip wheel --no-build-isolation` ile başarıyla üretildi.

## GitHub Actions matrix

Cross-platform doğrulama artık tamamlandı: **Windows + macOS + Ubuntu × Python 3.10/3.12/3.13 = 9/9 job PASS.** Her job install, `pytest -q`, `fixbundle --version` ve `fixbundle . --recommend --lang en` smoke adımlarını geçti.

Ayrıntılı matris: [CI_MATRIX.md](CI_MATRIX.md).
