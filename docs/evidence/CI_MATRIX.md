# Cross-platform CI kanıtı ✅

Doğrulanan davranış commit'i: `153dbecae075c6cc48e6375450ebf2493f263705`

GitHub Actions run: `33587276906` (#43)

## Sonuç

| OS | Python 3.10 | Python 3.12 | Python 3.13 |
|---|---:|---:|---:|
| Ubuntu | ✅ PASS | ✅ PASS | ✅ PASS |
| macOS | ✅ PASS | ✅ PASS | ✅ PASS |
| Windows | ✅ PASS | ✅ PASS | ✅ PASS |

**9/9 job PASS.**

Her job aşağıdaki kalite kapılarını geçti:

1. repository checkout
2. Python kurulumu
3. editable FixBundle 0.3.0 install
4. `pytest -q` → **5 passed**
5. `fixbundle --version`
6. `fixbundle . --recommend --lang en`
7. `python scripts/demo.py` → historical incident demo **5/5 invariant PASS**

## Windows regression kanıtı
Bir önceki v0.3 CI turunda Windows, `✅` karakterini CP1252 stdout'a yazarken `UnicodeEncodeError` ile kırıldı. Düzeltmede CLI stdout/stderr UTF-8 + replacement fallback ile yapılandırıldı ve `tests/test_cli.py` legacy `cp1252:strict` koşulunu yeniden üretilebilir teste çevirdi.

Run #43'te Windows Python 3.10, 3.12 ve 3.13 job'larının tamamı hem 5 testi hem historical demoyu geçti.

Bu belge statik bir pazarlama iddiası değildir; GitHub Actions üzerindeki gerçek matrix run sonucunun kaydıdır. README'deki CI badge her yeni commit için güncel durumu gösterir.
