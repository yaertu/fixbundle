# Security Policy 🔒

FixBundle'ın ana güvenlik sınırı **paylaşılacak diagnostic bundle**dır.

## Varsayılan korumalar
- Common secret/credential dosyaları capture edilmez.
- Known token/key/private-key kalıpları maskelenir.
- Project root ve home absolute paths anonimleştirilir.
- Symlink takip edilmez.
- Vendor/generated klasörleri ve önceki `.fixbundle` çıktıları dışlanır.
- Captured text boyutu sınırlandırılır.

## Önemli sınır
Redaction kusursuz değildir. Kaynak kodun kendisi ticari sır olabilir ve özel uygulamalar custom secret formatları kullanabilir. Public paylaşım öncesinde bundle içeriğini incele.

## Güvenlik açığı bildirimi
Public issue'ya gerçek API key, token, private source veya hassas bundle koyma. Repository sahibine güvenli bir kanal üzerinden bildirim yapılana kadar PoC'yi minimum ve sentetik tut.
