# ojob-warehouse-id-searcher

Расширение для Burp Suite, позволяющее находить название склада Ozon или мини-склада Ozon Fresh по ID склада.

Пример: `1020001234567890` → `Название склада`

<div align="center">

🌐 **Языки:** 🇬🇧 [English](README.md) | 🇷🇺 [Русский](README-RU.md) | 🇺🇿 [O'zbekcha](README-UZ.md)

</div>

## Шаг 1 — Установка и настройка Burp Suite

У вас должен быть установлен Burp Suite. Настройте Proxy Listener в Burp Suite так, чтобы он прослушивал адрес `0.0.0.0` или локальный IPv4-адрес вашей сети (например, `192.168.69.14`). Используйте порт по умолчанию (`8080`) или любой другой удобный для вас порт.

> **Примечание:** `0.0.0.0` — это адрес, используемый для привязки Proxy Listener. При настройке прокси на телефоне необходимо указывать фактический локальный IPv4-адрес вашего компьютера (например, `192.168.69.14`) и порт, настроенный в Burp Suite.

### Установка

#### Linux

**Kali Linux / Parrot OS:**

```bash
sudo apt update && sudo apt install burpsuite
```

**Ubuntu / Debian (официальный установщик):**

Скачайте установщик для Linux с сайта [PortSwigger](https://portswigger.net/burp/releases) и выполните:

```bash
chmod +x burpsuite_community_linux_v*.sh
./burpsuite_community_linux_v*.sh
```

**Arch Linux (AUR):**

```bash
yay -S burpsuite
```

#### macOS

С помощью [Homebrew](https://brew.sh/):

```bash
brew install --cask burp-suite
```

## Шаг 2 — Установка расширения для Burp Suite

Скачайте [автономный JAR-файл Jython 2.7.4](https://github.com/jython/jython/releases/download/v2.7.4/jython-standalone-2.7.4.jar).

1. Откройте **Extensions → Extensions Settings → Python environment → Location of Jython standalone JAR file** и укажите файл `jython-standalone-2.7.4.jar`.
2. Перейдите в **Extensions → Add**, установите **Extension type** в значение **Python** и выберите `ozon_id_to_get.py` в качестве файла расширения (`.py`).

## Дополнительно — Правила Match and Replace для Burp Suite

Откройте **Proxy → Match and replace → Add**, чтобы добавить следующие правила.

### 1. Отображение ID склада рядом с его названием в приложении OJob

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

### 2. Отображение ID склада рядом с его названием в теле ответа

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

### 3. Отображение полных фамилий сотрудников на странице рейтинга команды

По умолчанию приложение отображает только первую букву фамилии сотрудника.

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

### 4. Отображение точного времени публикации оценки сотрудника модерацией Ozon

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

> **Примечание:** Эти выражения Match and Replace зависят от структуры JSON и порядка расположения полей в запросах и ответах. Если Ozon изменит формат API, правила может потребоваться скорректировать.

## Шаг 3 — Установка сертификата PortSwigger CA на Android

1. Установите сертификат `.der` через **Настройки Android**.
2. Необходим root-доступ через Magisk. Установите модуль [AlwaysTrustUserCerts](https://github.com/NVISOsecurity/AlwaysTrustUserCerts).
3. Перезагрузите телефон.

## Шаг 4 — Настройка прокси

Я использую приложение [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid). Вы можете использовать любое приложение, поддерживающее HTTP-прокси в режиме VPN.

1. Добавьте новое подключение типа **HTTP**. Например, в моей конфигурации используется `192.168.69.14:8080`, без имени пользователя и пароля (`nouser nopass`).
2. **Необязательно:** Настройте NekoBox так, чтобы прокси использовался только приложением Ozon Job: `ru.ozon.hire`.

**Включите прокси.**

## Использование расширения

Начните вводить нужный ID в строку поиска склада.

Также вы сможете просматривать актуальные полные имена сотрудников на странице рейтинга команды.
