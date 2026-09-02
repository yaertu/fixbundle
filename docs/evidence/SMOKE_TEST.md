# v0.2.0 doğrulama kanıtı

Bu belge, README'deki çalışabilirlik iddialarının kısa ve yeniden üretilebilir kanıtıdır.

## Test sonucu

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

> Not: Bu kanıt lokal doğrulamadan gelir. GitHub Actions, repository yayınlandıktan sonra aynı testleri Windows, macOS ve Ubuntu üzerinde yeniden çalıştırır.
