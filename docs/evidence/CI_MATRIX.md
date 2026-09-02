# Cross-platform CI kanıtı ✅

Doğrulanan commit: `0885a5ae621f8b8769eca91ef1bcb765ae12dc1d`

GitHub Actions run: `33585835489`

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
3. editable FixBundle install
4. `pytest -q`
5. `fixbundle --version`
6. `fixbundle . --recommend --lang en`

Bu belge statik bir pazarlama iddiası değildir; GitHub Actions üzerindeki gerçek matrix run sonucunun kaydıdır. README'deki CI badge her yeni commit için güncel durumu gösterir.
