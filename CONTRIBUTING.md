# FixBundle'a katkı 🧰

## Geliştirme

```bash
python -m pip install -e .
python -m pytest -q
fixbundle . --recommend
```

## PR kalite kapısı
- Yeni davranış test ister.
- Secret redaction gevşetilemez.
- Capture varsayılanları local-first ve bounded kalır.
- Kullanıcı workspace'i destructive biçimde değiştiren özellik kabul edilmez.
- README iddiası test/evidence ile desteklenir.

## İyi feature request
“Yeni panel ekle” yerine **kullanıcı sonucu** yaz:

> Failed GitHub Actions run'ını tek komutla AI-ready bundle'a dönüştürmek istiyorum; çünkü agent'ın workflow/commit/log ilişkisini elle topluyorum.
