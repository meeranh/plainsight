<script lang="ts">
	function goBack() {
		history.back();
	}
</script>

<svelte:head>
	<title>how it works - plainsight</title>
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
				plainsight combines post-quantum cryptography with steganography.
				your message is encrypted so that even quantum computers can't
				break it, then hidden inside an ordinary image that looks
				completely normal to anyone who sees it.
			</p>
		</header>

		<!-- The Big Picture -->
		<section>
			<h2 class="text-fg mb-4">the big picture</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				to send a secret message, you only need the receiver's public key.
				the system encrypts your message and hides it inside an image.
				the image can be shared anywhere — social media, email, messaging
				apps — without raising suspicion.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/encryption_flow.svg" alt="encryption flow" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				encryption pipeline
			</p>

			<p class="text-fg-muted my-8 leading-relaxed">
				the receiver extracts and decrypts the message using their private
				key. if anyone tampers with the image, the decryption fails
				automatically — the system detects modifications.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/decryption_flow.svg" alt="decryption flow" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				decryption pipeline
			</p>
		</section>

		<!-- Key Generation -->
		<section>
			<h2 class="text-fg mb-4">key generation</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				the receiver generates a keypair using ML-KEM-768, a lattice-based
				algorithm standardized by NIST in 2024. unlike RSA or elliptic
				curves, lattice problems remain hard even for quantum computers.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/keygen.svg" alt="key generation" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				ml-kem-768 keypair generation
			</p>
		</section>

		<!-- Encryption Steps -->
		<section>
			<h2 class="text-fg mb-4">encryption steps</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				encryption happens in three steps. first, the sender uses the
				receiver's public key to create a shared secret that only the
				receiver can recover.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/encapsulation.svg" alt="key encapsulation" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				key encapsulation
			</p>

			<p class="text-fg-muted my-8 leading-relaxed">
				the shared secret is used to derive an AES-256-GCM key. this
				symmetric cipher encrypts the actual message and adds an
				authentication tag that detects any tampering.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/symmetric_encryption.svg" alt="symmetric encryption" class="w-full max-w-lg" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				symmetric encryption
			</p>

			<p class="text-fg-muted my-8 leading-relaxed">
				finally, the encrypted data is hidden inside an image using LSB
				steganography. this modifies the least significant bit of each
				color channel — a change invisible to the human eye.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/steganography.svg" alt="steganography" class="w-full max-w-lg" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				lsb steganography
			</p>
		</section>

		<!-- Decryption -->
		<section>
			<h2 class="text-fg mb-4">decryption</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				the receiver reverses the process: extract the hidden data,
				recover the shared secret using their private key, and decrypt
				the message. only the private key holder can read it.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/full_decryption.svg" alt="full decryption" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				complete decryption process
			</p>
		</section>

		<!-- Performance -->
		<section>
			<h2 class="text-fg mb-4">performance</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				post-quantum cryptography has a reputation for being slow, but
				ML-KEM is remarkably fast. all operations complete in under
				100 microseconds — fast enough for real-time use.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/mlkem_chart.svg" alt="ml-kem performance" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				ml-kem operation times across variants
			</p>

			<div class="flex justify-center mt-8">
				<pre class="text-fg-muted text-sm leading-relaxed">
{`  operation                    time
  ─────────────────────────────────────
  ml-kem-768 key generation    44 μs
  ml-kem-768 encapsulation     41 μs
  ml-kem-768 decapsulation     53 μs
  aes-256-gcm encryption       < 1 μs
  lsb embedding                29 μs
  lsb extraction               17 μs
  ─────────────────────────────────────
  total encryption            ~115 μs
  total decryption             ~71 μs`}
				</pre>
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				benchmarks on amd ryzen 5 7535HS
			</p>
		</section>

		<!-- Image Quality -->
		<section>
			<h2 class="text-fg mb-4">image quality</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				LSB steganography changes pixel values by at most 1. the
				modifications are invisible to the human eye. PSNR (peak
				signal-to-noise ratio) measures image quality — values above
				40 dB are considered imperceptible.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/psnr_chart.svg" alt="psnr chart" class="w-full max-w-sm" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				psnr vs embedding capacity
			</p>

			<p class="text-fg-muted mt-8 leading-relaxed">
				even at 100% capacity, PSNR stays above 51 dB. in practice, a
				typical message uses less than 1% of capacity, resulting in
				PSNR well above 60 dB.
			</p>
		</section>

		<!-- Data Sizes -->
		<section>
			<h2 class="text-fg mb-4">data sizes</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				each message has about 1.1 KB of overhead for the cryptographic
				data. a typical photograph can hide tens or hundreds of
				kilobytes of data.
			</p>

			<div class="flex justify-center">
				<pre class="text-fg-muted text-sm leading-relaxed">
{`  component              size
  ─────────────────────────────────────
  ml-kem public key      1,184 bytes
  ml-kem private key     2,400 bytes
  ml-kem ciphertext      1,088 bytes
  aes-gcm iv                12 bytes
  aes-gcm auth tag          16 bytes
  ─────────────────────────────────────
  overhead per message   ~1,116 bytes

  500×500 image capacity     ~93 kb
  1000×1000 image capacity  ~375 kb`}
				</pre>
			</div>
		</section>

		<!-- Footer -->
		<footer class="border-t border-dashed border-border pt-8">
			<p class="text-fg-muted/50 text-sm">
				implementation uses
				<span class="text-fg-muted">@noble/post-quantum</span> for ml-kem,
				<span class="text-fg-muted">web crypto api</span> for aes-gcm, and
				<span class="text-fg-muted">canvas api</span> for steganography.
				all operations run client-side in your browser.
			</p>
		</footer>
	</article>
</main>
