# Next move

## v0.5 single highest-value milestone
**OpenTelemetry production event → portable FixBundle evidence packet.**

v0.4 artık gerçek GitHub Actions failure üzerinde doğrulandı. Sıradaki problem “CI'da değil, production'da oldu” vakası.

### Araştırma kararı
İlk v0.5 adapter'ı Sentry-specific olmayacak. OpenTelemetry'nin Protocol File Exporter'ı telemetry'yi standart OTLP JSON Lines olarak dosyaya yazabiliyor; exception semantiğinde `exception.type`, `exception.message` ve `exception.stacktrace` alanları tanımlı. Bu, FixBundle'ın vendor-independent ürün sınırına daha iyi uyuyor.

Sentry daha sonra desteklenecek fakat yalnızca gerçek ek değer sağladığı yerde. Sentry'nin issue-event API'si 2026 itibarıyla `llmFormat=markdown|xml` ile doğrudan LLM formatı sunuyor. Sadece “Sentry event'i Markdown'a çeviren” bir wrapper ürün farkı yaratmaz.

### Proposed CLI

```bash
fixbundle otlp --logs ./otel-logs.jsonl --traces ./otel-traces.jsonl --lang tr
```

Daha sonra:

```bash
fixbundle sentry --org <org> --issue <issue-id> --event recommended
```

### Definition of done
- OTLP JSON/JSONL dosyasını local ve account'suz okuyabilme,
- logs/traces içinden trace/span correlation,
- service/environment/release/deployment identity,
- exception type/message/stacktrace normalization,
- configurable bounded time/incident selection,
- secret/PII redaction katmanından geçirme,
- raw telemetry'yi körlemesine bundle'a doldurmak yerine seçilen kanıtı manifestte açıklama,
- SHA-256 integrity + AI handoff,
- malformed/oversized input için fail-closed testleri,
- gerçek veya spec-conformant OTLP fixture ile yeniden üretilebilir demo.

### Distribution hypothesis
CI evidence geliştiriciyi GitHub'dan yakalar; OTLP evidence ise backend/infra/agent geliştiricisini production telemetry'den yakalar. Eğer bu ikinci giriş gerçek kullanım üretirse FixBundle “bir CLI özelliği” olmaktan çıkıp ortak failure-evidence formatına yaklaşır.
