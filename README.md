Algoritma:Linkedin'e normal kullanıcı gibi browserdan gidilerek kullanıcı girişi yapılır, ilgili şirketin sayfasında çalışanlar html dosyası çekilir. 
Sonrasında gerekli parse işlemleri ve dönüşümler yapılark isim-soyisim ikilisi ile mail adresleri oluşturulur.

**Öncelikle manuel olarak hangi şirketin çalışanları bulunmak isteniyorsa şirket sayfasına girilir, kişiler sekmesine tıklanır ve url kopyalanır. -l parameteresi ile kullanılır.**

Örnek:

google şirketinin sayfasına linkedin üzerinden erişirseniz https://www.linkedin.com/company/google/ adresine gidersiniz. Sonrasında kişiler sekmesine tıklarsanız
https://www.linkedin.com/company/google/people adresine gidersiniz. Kullanıcıların çekildiği yer burasıdır.

Bu sayfada "lazy load" yani aşağıya doğru scroll yaptıkça  kullanıcılar eklendiği için, script otomatik olarak en aşağıya iner, her 5 saniyede bir bu işlemi tekrar ederek
sayfanın sonuna gelmeye çalışır, geldiğinde bunu tespit eder ve ilgili html kaynağını çeker. Sonrasında parse işlemleri yapılarak isim-soyisim ikilisinden ve verilen parameter ile
mail listesi çıkartılır.

Kullanım örneği:
python main.py -e gmail.com -l https://www.linkedin.com/company/google/people -s .

Örnek çıktı:
ahmet.karaagacli@gmail.com
....


- Kullanıcı profillerine girmez.
- 2fa kapatılması gerekir
- Kullanıcı ad soyad ve mail listesi olmak üzere iki farklı dosyaya çıktı alınır.
- Şirket büyüklüğüne göre / çalışan sayısına göre tüm kullanıcılara ulaşmak zaman alabilir.
- Script çalışırken arka planda işlerinize devam edebilirsiniz.
- 2 isme sahip kullanıcıların ilk isimleri ve soyadları dikkate alınır.
- Örnek olarak google'ı denemeyin. linkedin üzerinde 200 bin kullanıcı var. Script bitmez. Daha küçük işletmeler üzerinde deneme yapılabiir.
- Linkedinde şirketlerin kişiler sayfası Lazy Load özelliğine sahiptir. Yani kullanıcı aşağıya doğru scroll yaptıkça yeni kullanıcılar getirilir ve gösterilir. Her sayfa sonuna scroll yapıldığında 12 kullanıcı eklenir. Script 5 saniye de bir bu scroll işlemini yapar. dolayısıyla 60 kişilik bir şirket için tüm kullanıcıları çekmek yaklaşık 25 saniye sürer. Kullanıcı sayısına göre doğru orantı kurulabilir.
- Windows sistemlerde daha düzgün çalışır.
