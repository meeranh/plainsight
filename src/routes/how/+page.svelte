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
			<div class="h-px bg-border"></div>
		</header>

		<!-- Introduction -->
		<section>
			<h2 class="text-fg mb-4">introduction</h2>
			<div class="h-px bg-border mb-6"></div>

			<h3 class="text-fg-muted mb-3">what is steganography?</h3>
			<p class="text-fg-muted mb-8 leading-relaxed">
				steganography is the art of hiding messages in plain sight.
				unlike encryption (which scrambles a message so it can't be
				read), steganography hides the message inside something
				ordinary — like an image. anyone looking at the image sees
				just a normal picture.
			</p>

			<h3 class="text-fg-muted mb-3">what is post-quantum encryption?</h3>
			<p class="text-fg-muted mb-8 leading-relaxed">
				today's encryption (RSA, elliptic curves) can be broken by
				quantum computers using Shor's algorithm. post-quantum
				cryptography uses mathematical problems that remain hard even
				for quantum computers. ML-KEM is a lattice-based algorithm
				standardized by NIST in 2024 specifically for this purpose.
			</p>

			<h3 class="text-fg-muted mb-3">what is LSB encoding?</h3>
			<p class="text-fg-muted mb-8 leading-relaxed">
				every pixel in an image has color values stored as 8-bit
				numbers (0-255). the least significant bit (LSB) is the
				rightmost bit — changing it only shifts the value by 1.
				for example, changing a red value from 180 to 181 is
				completely invisible to the human eye.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/lsb_diagram.svg" alt="lsb embedding" class="w-full max-w-lg" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				lsb embedding example
			</p>

			<p class="text-fg-muted my-8 leading-relaxed">
				each pixel has three color channels (red, green, blue), so
				each pixel can hide 3 bits of data. a 1000×1000 image has
				1 million pixels — that's 375 KB of hiding capacity.
			</p>

			<p class="text-fg-muted leading-relaxed">
				LSB steganography is hard to detect because the changes are
				statistically random and visually imperceptible. detection
				tools look for unusual patterns, but at low embedding rates
				the modifications blend into the natural noise of any image.
			</p>
		</section>

		<!-- The Big Picture -->
		<section>
			<h2 class="text-fg mb-4">the big picture</h2>
			<div class="h-px bg-border mb-6"></div>

			<p class="text-fg-muted mb-8 leading-relaxed">
				plainsight combines these ideas: your message is encrypted
				with ML-KEM-768 and AES-256-GCM, then hidden inside an image
				using LSB encoding. the image can be shared anywhere —
				social media, email, messaging apps — without raising suspicion.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/encryption_flow.svg" alt="encryption flow" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				encryption pipeline
			</p>

			<p class="text-fg-muted my-8 leading-relaxed">
				the receiver extracts and decrypts the message using their
				private key. if anyone tampers with the image, the decryption
				fails automatically — the system detects modifications.
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
				the receiver generates a keypair using ML-KEM-768. the public
				key can be shared with anyone who wants to send them a message.
				the private key is kept secret and used for decryption.
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
				finally, the encrypted data is hidden inside an image using
				LSB steganography.
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
				PSNR (peak signal-to-noise ratio) measures image quality —
				values above 40 dB are considered imperceptible to humans.
				even at 100% capacity, PSNR stays above 51 dB. in practice,
				a typical message uses less than 1% of capacity.
			</p>

			<div class="flex justify-center">
				<img src="/diagrams/psnr_chart.svg" alt="psnr chart" class="w-full max-w-sm" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-2">
				psnr vs embedding capacity
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
