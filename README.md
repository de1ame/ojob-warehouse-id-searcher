# ojob-warehouse-id-searcher

Burp Suite extension for looking up the name of an Ozon warehouse or Fresh mini-warehouse using its warehouse ID.

Example: `1020001234567890` → `Warehouse Name`

<div align="center">

🌐 **Languages:** 🇬🇧 [English](README.md) | 🇷🇺 [Русский](README-RU.md) | 🇺🇿 [O'zbekcha](README-UZ.md)

</div>

## Step 1 — Install and configure Burp Suite

You need to have Burp Suite installed. Configure the proxy listener in Burp Suite to listen on `0.0.0.0` or on your local network IPv4 address (for example, `192.168.69.14`). Use the default port (`8080`) or any other port you prefer.

> **Note:** `0.0.0.0` is an address for the listener to bind to. When configuring the proxy on your phone, use your computer's actual local network IPv4 address (for example, `192.168.69.14`) and the port configured in Burp Suite.

### Installation

#### Linux

**Kali Linux / Parrot OS:**

```bash
sudo apt update && sudo apt install burpsuite
```

**Ubuntu / Debian (official installer):**

Download the Linux installer from [PortSwigger](https://portswigger.net/burp/releases) and run:

```bash
chmod +x burpsuite_community_linux_v*.sh
./burpsuite_community_linux_v*.sh
```

**Arch Linux (AUR):**

```bash
yay -S burpsuite
```

#### macOS

Using [Homebrew](https://brew.sh/):

```bash
brew install --cask burp-suite
```

## Step 2 — Install the Burp Suite extension

Download the [Jython 2.7.4 standalone JAR](https://github.com/jython/jython/releases/download/v2.7.4/jython-standalone-2.7.4.jar).

1. Open **Extensions → Extensions Settings → Python environment → Location of Jython standalone JAR file** and select `jython-standalone-2.7.4.jar`.
2. Open **Extensions → Add**, set **Extension type** to **Python**, and select `ozon_id_to_get.py` as the extension file (`.py`).

## Bonus — Additional Burp Suite Match and Replace rules

Open **Proxy → Match and replace → Add** to create the following rules.

### 1. Display the warehouse ID next to its name in the OJob app

**Type:** Request body  
**Match:**

```regex
("warehouse"\s*:\s*\{\s*"id"\s*:\s*"([^"]+)"[^}]*?"name"\s*:\s*")([^"]*)(")
```

**Replace:**

```text
$1$3 (WH ID: $2)$4
```

**Regex match:** Enabled

### 2. Display the warehouse ID next to its name in the response body

**Type:** Response body  
**Match:**

```regex
("warehouse"\s*:\s*\{\s*"id"\s*:\s*")([^"]+)("\s*,\s*"type"\s*:\s*"[^"]+"\s*,\s*"name"\s*:\s*")([^"]+)(")
```

**Replace:**

```text
$1$2$3$4\\\n(WH ID: $2)$5
```

**Regex match:** Enabled

### 3. Display workers' full last names on the team ratings page

By default, the app displays only the first letter of a worker's last name.

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

### 4. Display the exact time when Ozon moderation published a worker rating

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

> **Note:** These Match and Replace expressions rely on the response/request JSON having the field structure and order shown in the examples. If Ozon changes the API response format, a rule may need to be adjusted.

## Step 3 — Install the PortSwigger CA certificate on your Android phone

1. Install the `.der` certificate in Android **Settings**.
2. Magisk root access is required. Install the [AlwaysTrustUserCerts](https://github.com/NVISOsecurity/AlwaysTrustUserCerts) module.
3. Reboot your phone.

## Step 4 — Configure the proxy

I use the [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid) app. You can use any app that supports an HTTP proxy in VPN mode.

1. Add a new **HTTP** connection. For example, my proxy is `192.168.69.14:8080`, with no username or password (`nouser nopass`).
2. **Optional:** Configure NekoBox to proxy only the Ozon Job application: `ru.ozon.hire`.

**Enable the proxy.**

## Using the extension

Start entering the desired ID in the warehouse search bar.

You can also view workers' latest available full names on the team ratings page.
