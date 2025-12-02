<p align="center">
  <br>
  <br>
  <br>
</p>

<pre align="center">
██████╗ ██╗      █████╗ ██╗███╗   ██╗███████╗██╗ ██████╗ ██╗  ██╗████████╗
██╔══██╗██║     ██╔══██╗██║████╗  ██║██╔════╝██║██╔════╝ ██║  ██║╚══██╔══╝
██████╔╝██║     ███████║██║██╔██╗ ██║███████╗██║██║  ███╗███████║   ██║
██╔═══╝ ██║     ██╔══██║██║██║╚██╗██║╚════██║██║██║   ██║██╔══██║   ██║
██║     ███████╗██║  ██║██║██║ ╚████║███████║██║╚██████╔╝██║  ██║   ██║
╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝
</pre>

<p align="center">
  <br>
  <em>some things are hidden in plain sight</em>
  <br>
  <br>
</p>

<br>
<br>

---

<br>

### what

hide encrypted messages inside ordinary images.

no one knows they're there. not even quantum computers.

<br>

### why

because privacy shouldn't require trust.

because sometimes you need to send secrets through places that are watching.

because the best hiding spot is in plain sight.

<br>

### how

```
message ─── ML-KEM-768 ─── AES-256-GCM ─── LSB ─── image.png
```

**ml-kem-768** — post-quantum key encapsulation. safe from shor's algorithm.

**aes-256-gcm** — symmetric encryption with authentication.

**lsb steganography** — hides data in the least significant bits of pixels. invisible to the eye.

<br>

### run

```sh
git clone https://github.com/meeranh/plainsight.git
cd plainsight
pnpm install
pnpm dev
```

open `http://localhost:5173`

<br>

---

<p align="center">
  <br>
  <sub>
    the walls have eyes. make sure yours are hidden.
  </sub>
  <br>
  <br>
</p>
