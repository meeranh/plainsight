<script lang="ts">
	function goBack() {
		history.back();
	}
</script>

<svelte:head>
	<title>how it works - pq-stego</title>
</svelte:head>

<main class="min-h-screen px-6 py-12 max-w-2xl mx-auto">
	<button
		onclick={goBack}
		class="text-fg-muted hover:text-fg transition-colors duration-100 mb-12"
	>
		&larr; back
	</button>

	<article class="space-y-16">
		<!-- Header -->
		<header>
			<h1 class="text-fg text-xl mb-4">how it works</h1>
			<div class="h-px bg-border mb-6"></div>
			<p class="text-fg-muted leading-relaxed">
				a technical overview of how pq-stego combines post-quantum
				cryptography with steganography to hide encrypted messages
				inside ordinary images.
			</p>
		</header>

		<!-- The Big Picture -->
		<section>
			<h2 class="text-fg mb-4">the big picture</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-6 leading-relaxed">
				the system combines three cryptographic techniques to ensure
				your message is both encrypted and hidden:
			</p>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │             │   │             │   │             │
  │   ML-KEM    │ + │  AES-256    │ + │    LSB      │
  │   (keys)    │   │  (encrypt)  │   │  (hide)     │
  │             │   │             │   │             │
  └─────────────┘   └─────────────┘   └─────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
   quantum-safe      symmetric        invisible
   key exchange      encryption       embedding
`}
			</pre>

			<p class="text-fg-muted leading-relaxed">
				even if someone intercepts the image, they see nothing
				suspicious. even if they suspect hidden data, they can't
				decrypt it without the private key. even with a quantum
				computer, the encryption remains secure.
			</p>
		</section>

		<!-- Key Generation -->
		<section>
			<h2 class="text-fg mb-4">1. key generation</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-6 leading-relaxed">
				the receiver generates an ML-KEM-768 keypair. this is a
				lattice-based cryptographic system that resists attacks
				from both classical and quantum computers.
			</p>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌────────────────────────────────────────────────┐
  │                   RECEIVER                     │
  └────────────────────────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │    ML-KEM-768   │
              │     keygen()    │
              └─────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
  ┌─────────────────┐       ┌─────────────────┐
  │   public key    │       │   private key   │
  │   (1,184 bytes) │       │   (2,400 bytes) │
  │                 │       │                 │
  │   share this    │       │   keep secret   │
  └─────────────────┘       └─────────────────┘
`}
			</pre>

			<div class="border border-border p-4 bg-bg-card">
				<p class="text-fg-muted text-sm">
					<span class="text-yellow">why ML-KEM?</span> RSA and ECC can be
					broken by Shor's algorithm on a quantum computer. ML-KEM is
					based on the hardness of lattice problems, which remain hard
					even for quantum computers. NIST standardized it in 2024.
				</p>
			</div>
		</section>

		<!-- Encryption Flow -->
		<section>
			<h2 class="text-fg mb-4">2. encryption (sender)</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-6 leading-relaxed">
				the sender uses the receiver's public key to encrypt a message.
				this happens in three steps:
			</p>

			<h3 class="text-fg-muted mb-4">step 2.1: key encapsulation</h3>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌─────────────────┐
  │  receiver's     │
  │  public key     │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    ML-KEM       │
  │  encapsulate()  │
  └────────┬────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  ┌──────┐   ┌──────────────┐
  │shared│   │kem ciphertext│
  │secret│   │ (1,088 bytes)│
  │(32 B)│   │              │
  └──────┘   └──────────────┘
`}
			</pre>

			<p class="text-fg-muted mb-8 leading-relaxed">
				the shared secret is random and known only to sender and
				receiver. the kem ciphertext is sent along with the message.
			</p>

			<h3 class="text-fg-muted mb-4">step 2.2: symmetric encryption</h3>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌──────────┐   ┌──────────┐
  │  shared  │   │   your   │
  │  secret  │   │  message │
  └────┬─────┘   └────┬─────┘
       │              │
       ▼              │
  ┌─────────┐         │
  │  HKDF   │         │
  │ derive  │         │
  └────┬────┘         │
       │              │
       ▼              ▼
  ┌─────────────────────┐
  │     AES-256-GCM     │
  │      encrypt        │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │     ciphertext      │
  │    + auth tag       │
  └─────────────────────┘
`}
			</pre>

			<div class="border border-border p-4 bg-bg-card mb-8">
				<p class="text-fg-muted text-sm">
					<span class="text-yellow">why AES-GCM?</span> ML-KEM is a key
					encapsulation mechanism, not an encryption algorithm. we use
					the shared secret to derive an AES key for actual encryption.
					GCM mode provides both confidentiality and integrity.
				</p>
			</div>

			<h3 class="text-fg-muted mb-4">step 2.3: steganography</h3>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌──────────────┐   ┌──────────────┐
  │kem ciphertext│   │  encrypted   │
  │ (1,088 bytes)│   │   message    │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         └────────┬─────────┘
                  │
                  ▼
         ┌───────────────┐
         │   serialize   │
         │   & combine   │
         └───────┬───────┘
                 │
                 ▼
  ┌────────────────────────────────────┐
  │         cover image                │
  │  ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐   │
  │  │▓▓│░░│▓▓│░░│▓▓│░░│▓▓│░░│▓▓│░░│   │
  │  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘   │
  │         LSB embedding              │
  └────────────────┬───────────────────┘
                   │
                   ▼
  ┌────────────────────────────────────┐
  │         stego image                │
  │                                    │
  │     (visually identical)           │
  │                                    │
  └────────────────────────────────────┘
`}
			</pre>

			<p class="text-fg-muted leading-relaxed">
				LSB (Least Significant Bit) steganography modifies the least
				important bit of each color channel. changing 10110100 to
				10110101 is invisible to the human eye but encodes one bit
				of hidden data.
			</p>
		</section>

		<!-- Decryption Flow -->
		<section>
			<h2 class="text-fg mb-4">3. decryption (receiver)</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-6 leading-relaxed">
				the receiver extracts and decrypts the message using their
				private key. the process is reversed:
			</p>

			<pre class="text-aqua text-sm overflow-x-auto mb-6 leading-relaxed">
{`
  ┌────────────────────────────────────┐
  │           stego image              │
  └────────────────┬───────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │  LSB extract   │
          └────────┬───────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  ┌──────────────┐   ┌──────────────┐
  │kem ciphertext│   │  encrypted   │
  │              │   │   message    │
  └──────┬───────┘   └──────┬───────┘
         │                  │
         ▼                  │
  ┌──────────────┐          │
  │ private key  │          │
  └──────┬───────┘          │
         │                  │
         ▼                  │
  ┌──────────────┐          │
  │   ML-KEM     │          │
  │ decapsulate  │          │
  └──────┬───────┘          │
         │                  │
         ▼                  ▼
  ┌──────────────┐   ┌──────────────┐
  │    shared    │──▶│  AES-256-GCM │
  │    secret    │   │   decrypt    │
  └──────────────┘   └──────┬───────┘
                            │
                            ▼
                   ┌────────────────┐
                   │  your message  │
                   └────────────────┘
`}
			</pre>

			<p class="text-fg-muted leading-relaxed">
				only the holder of the private key can recover the shared
				secret and decrypt the message. the GCM auth tag ensures
				the message wasn't tampered with.
			</p>
		</section>

		<!-- Security Properties -->
		<section>
			<h2 class="text-fg mb-4">security properties</h2>
			<div class="h-px bg-border mb-6"></div>

			<div class="space-y-4">
				<div class="border border-border p-4 bg-bg-card">
					<p class="text-green text-sm mb-2">quantum resistance</p>
					<p class="text-fg-muted text-sm">
						ML-KEM-768 provides NIST security level 3, equivalent to
						AES-192. safe against known quantum algorithms.
					</p>
				</div>

				<div class="border border-border p-4 bg-bg-card">
					<p class="text-green text-sm mb-2">forward secrecy</p>
					<p class="text-fg-muted text-sm">
						each message uses a fresh shared secret. compromising one
						message doesn't compromise others.
					</p>
				</div>

				<div class="border border-border p-4 bg-bg-card">
					<p class="text-green text-sm mb-2">authenticated encryption</p>
					<p class="text-fg-muted text-sm">
						AES-GCM provides integrity verification. any tampering
						with the ciphertext will be detected.
					</p>
				</div>

				<div class="border border-border p-4 bg-bg-card">
					<p class="text-green text-sm mb-2">plausible deniability</p>
					<p class="text-fg-muted text-sm">
						the stego image looks like any other image. without
						knowing to look, no one knows there's hidden data.
					</p>
				</div>
			</div>
		</section>

		<!-- Data Sizes -->
		<section>
			<h2 class="text-fg mb-4">data sizes</h2>
			<div class="h-px bg-border mb-6"></div>

			<pre class="text-fg-muted text-sm overflow-x-auto leading-relaxed">
{`
  component              size
  ─────────────────────────────────────
  ML-KEM public key      1,184 bytes
  ML-KEM private key     2,400 bytes
  ML-KEM ciphertext      1,088 bytes
  AES-GCM IV                12 bytes
  AES-GCM auth tag          16 bytes
  ─────────────────────────────────────
  overhead per message   ~1,116 bytes

  a 500×500 image can hide ~93 KB
  a 1000×1000 image can hide ~375 KB
`}
			</pre>
		</section>

		<!-- Footer -->
		<footer class="border-t border-dashed border-border pt-8">
			<p class="text-fg-muted/50 text-sm">
				implementation uses
				<span class="text-fg-muted">@noble/post-quantum</span> for ML-KEM,
				<span class="text-fg-muted">Web Crypto API</span> for AES-GCM, and
				<span class="text-fg-muted">Canvas API</span> for steganography.
				all cryptographic operations run client-side in your browser.
			</p>
		</footer>
	</article>
</main>
