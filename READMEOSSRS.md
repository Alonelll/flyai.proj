# OSSRS (SRS) Setup für macOS & Docker

Diese README beschreibt, wie man **OSSRS (SRS)** lokal auf macOS baut, startet, typische macOS-Probleme löst und optional SRS über Docker betreibt.

---

## 1. Voraussetzungen (macOS)

Installiere die benötigten Tools via **Homebrew**:

```bash
brew install automake libtool pkg-config cmake nasm yasm
xcode-select --install  # falls noch nicht installiert
```

---

## 2. SRS lokal bauen

1. Repository klonen:

```bash
git clone https://github.com/ossrs/srs.git
cd srs/trunk
```

2. Configure ausführen:

```bash
./configure
```

3. Kompilieren:

```bash
make
```

Das Binary befindet sich in `./objs/srs`.

---

## 3. macOS-spezifische Probleme

### 3.1 max_connections / ulimit

SRS bricht ab, wenn `max_connections` höher ist als das Systemlimit für offene Dateien:

```
[ERROR] max_connections=1000, system limit to 256, please run: ulimit -HSn 10000
```

#### Temporär erhöhen:

```bash
ulimit -n 10240
./objs/srs -c conf/srs.conf
```

#### Dauerhaft erhöhen:

```bash
sudo launchctl limit maxfiles 10240 10240
```

Danach Terminal neu starten.

### 3.2 SRS beenden

- Im Vordergrund gestartet: `Ctrl + C`
- Im Hintergrund gestartet (`&`):

```bash
ps aux | grep srs
kill <PID>
```

- Wenn mit `init.d` gestartet:

```bash
./etc/init.d/srs stop
```

---

## 4. Minimal funktionierende `srs.conf` für macOS

```conf
listen              1935;
max_connections     256;
daemon              off;
srs_log_tank        console;

vhost __defaultVhost__ {
    hls {
        enabled         on;
        hls_path        ./objs/nginx/html;
    }
}
```

Starten:

```bash
./objs/srs -c conf/minimal.conf
```

---

## 5. SRS mit Docker

### 5.1 Docker Image

```bash
docker pull ossrs/srs:5
```

### 5.2 Container starten

```bash
docker run -it --rm -p 1935:1935 -p 1985:1985 -p 8080:8080 ossrs/srs:5
```

- RTMP: `rtmp://localhost/live`
- HTTP: `http://localhost:8080`
- API: `http://localhost:1985/api/v1/versions`

> Vorteil: Docker umgeht macOS `ulimit`-Probleme und ist ideal für Tests.

---

## 6. OBS Setup

1. OBS → **Einstellungen → Stream**
2. Dienst: **Benutzerdefiniert**
3. Server: `rtmp://localhost/live`
4. Stream-Schlüssel: z.B. `test`
5. Auf **„Stream starten“** klicken
6. HLS im Browser testen: `http://localhost:8080/live/test.m3u8`

---

## 7. Troubleshooting macOS

- **Kamera wird in OBS nicht erkannt:**

  - Prüfen: `system_profiler SPCameraDataType`
  - Datenschutzrechte: Systemeinstellungen → Datenschutz → Kamera → OBS zulassen
  - Dock / Kabel: Direkt am Mac anschließen, UVC-kompatibles Kabel verwenden

- **SRS startet nicht:** `ulimit -n` erhöhen, minimal.conf testen

---

## 8. Nützliche Links

- [SRS GitHub](https://github.com/ossrs/srs)
- [HLS.js für Browser Playback](https://github.com/video-dev/hls.js)
