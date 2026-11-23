# ojob-warehouse-id-searcher

Burp Suite uchun Ozon ombori yoki Ozon Fresh mini-omborining nomini uning ID raqami orqali topish imkonini beruvchi kengaytma.

Misol: `1020001234567890` → `Ombor nomi`

<div align="center">

🌐 **Tillar:** 🇬🇧 [English](README.md) | 🇷🇺 [Русский](README-RU.md) | 🇺🇿 [O'zbekcha](README-UZ.md)

</div>

## 1-qadam — Burp Suite dasturini o'rnatish va sozlash

Avval Burp Suite dasturi o'rnatilgan bo'lishi kerak. Burp Suite sozlamalarida Proxy Listener'ni `0.0.0.0` yoki mahalliy tarmog'ingizdagi IPv4 manzilida (masalan, `192.168.69.14`) tinglaydigan qilib sozlang. Standart portdan (`8080`) yoki o'zingizga qulay boshqa portdan foydalaning.

> **Eslatma:** `0.0.0.0` — Proxy Listener uchun bog'lanish (bind) manzili. Telefoningizda proxy sozlayotganda kompyuteringizning haqiqiy mahalliy IPv4 manzilini (masalan, `192.168.69.14`) va Burp Suite'da sozlangan portni kiriting.

### O'rnatish

#### Linux

**Kali Linux / Parrot OS:**

```bash
sudo apt update && sudo apt install burpsuite
```

**Ubuntu / Debian (rasmiy o'rnatuvchi):**

[PortSwigger](https://portswigger.net/burp/releases) saytidan Linux uchun o'rnatuvchini yuklab oling va quyidagi buyruqlarni bajaring:

```bash
chmod +x burpsuite_community_linux_v*.sh
./burpsuite_community_linux_v*.sh
```

**Arch Linux (AUR):**

```bash
yay -S burpsuite
```

#### macOS

[Homebrew](https://brew.sh/) yordamida:

```bash
brew install --cask burp-suite
```

## 2-qadam — Burp Suite kengaytmasini o'rnatish

[Jython 2.7.4 standalone JAR faylini](https://github.com/jython/jython/releases/download/v2.7.4/jython-standalone-2.7.4.jar) yuklab oling.

1. **Extensions → Extensions Settings → Python environment → Location of Jython standalone JAR file** bo'limini oching va `jython-standalone-2.7.4.jar` faylini tanlang.
2. **Extensions → Add** bo'limiga o'ting, **Extension type** qiymatini **Python** qilib belgilang va kengaytma fayli (`.py`) sifatida `ozon_id_to_get.py` faylini tanlang.

## Qo'shimcha — Burp Suite uchun Match and Replace qoidalari

Quyidagi qoidalarni qo'shish uchun **Proxy → Match and replace → Add** bo'limini oching.

### 1. OJob ilovasida ombor ID raqamini uning nomi yonida ko'rsatish

**Type:** Request body  
**Match:**

```regex
("warehouse"\s*:\s*\\{\s*"id"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*")([^"]*)(")
```

**Replace:**

```text
$1$3 (WH ID: $2)$4
```

**Regex match:** Enabled

### 2. Javob tanasida ombor ID raqamini uning nomi yonida ko'rsatish

**Type:** Response body  
**Match:**

```regex
("warehouse"\s*:\s*\\{\s*"id"\s*:\s*")([^"]+)("\s*,\s*"type"\s*:\s*"[^"]+"\s*,\s*"name"\s*:\s*")([^"]+)(")
```

**Replace:**

```text
$1$2$3$4\\\n(WH ID: $2)$5
```

**Regex match:** Enabled

### 3. Jamoa reytingi sahifasida xodimlarning to'liq familiyalarini ko'rsatish

Odatiy holatda ilova xodim familiyasining faqat birinchi harfini ko'rsatadi.

**Type:** Response body  
**Match:**

```regex
("firstName"\s*:\s*")([^"]*)("\s*,\s*"lastName"\s*:\s*")([^"]*)(")
```

**Replace:**

```text
$1$2 $4$3 $5
```

**Regex match:** Enabled

### 4. Ozon moderatsiyasi xodim reytingini e'lon qilgan aniq vaqtni ko'rsatish

**Type:** Response body  
**Match:**

```regex
("commentText"\s*:\s*")([^"]*)("\s*,[\s\S]*?"createdAt"\s*:\s*")(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z")
```

**Replace:**

```text
$1$2\\\n$6.$5.$4 $7:$8:$9$3$4-$5-$6T$7:$8:$9$10$11
```

**Regex match:** Enabled

> **Eslatma:** Ushbu Match and Replace qoidalari so'rov va javob JSON ma'lumotlaridagi maydonlar tuzilishi hamda ularning joylashish tartibiga bog'liq. Agar Ozon API formatini o'zgartirsa, qoidalarni qayta sozlash talab qilinishi mumkin.

## 3-qadam — Android telefoniga PortSwigger CA sertifikatini o'rnatish

1. `.der` sertifikatini Android **Sozlamalari** orqali o'rnating.
2. Magisk root huquqi talab qilinadi. [AlwaysTrustUserCerts](https://github.com/NVISOsecurity/AlwaysTrustUserCerts) modulini o'rnating.
3. Telefoningizni qayta yuklang.

## 4-qadam — Proxy sozlamalarini sozlash

Men [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid) ilovasidan foydalanaman. Siz VPN rejimida HTTP proxy'ni qo'llab-quvvatlaydigan boshqa ilovadan ham foydalanishingiz mumkin.

1. Yangi **HTTP** ulanishini qo'shing. Masalan, mening konfiguratsiyamda `192.168.69.14:8080` manzili ishlatiladi, foydalanuvchi nomi va parol talab qilinmaydi (`nouser nopass`).
2. **Ixtiyoriy:** NekoBox'ni proxy orqali faqat Ozon Job ilovasi (`ru.ozon.hire`) trafikini yo'naltiradigan qilib sozlang.

**Proxy'ni yoqing.**

## Kengaytmadan foydalanish

Ombor qidiruv maydoniga kerakli ID raqamini kiritishni boshlang.

Shuningdek, jamoa reytingi sahifasida xodimlarning mavjud to'liq ismlarini ko'rishingiz mumkin.
