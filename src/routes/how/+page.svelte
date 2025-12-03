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

	<article class="space-y-20">
		<!-- Header -->
		<header>
			<h1 class="text-fg text-xl mb-4">how it works</h1>
			<div class="h-px bg-border mb-6"></div>
			<p class="text-fg-muted leading-relaxed">
				post-quantum encryption meets steganography. your message is
				encrypted with ML-KEM-768 and AES-256-GCM, then hidden inside
				an ordinary image using LSB encoding.
			</p>
		</header>

		<!-- Encryption Flow -->
		<section>
			<div class="flex justify-center">
				<img src="/diagrams/encryption_flow.svg" alt="encryption flow" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				sender encrypts and embeds the message using the receiver's public key
			</p>
		</section>

		<!-- Decryption Flow -->
		<section>
			<div class="flex justify-center">
				<img src="/diagrams/decryption_flow.svg" alt="decryption flow" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				receiver extracts and decrypts using their private key
			</p>
		</section>

		<!-- Divider -->
		<div class="h-px bg-border"></div>

		<!-- Key Generation -->
		<section>
			<h2 class="text-fg mb-6">key generation</h2>
			<div class="flex justify-center">
				<img src="/diagrams/keygen.svg" alt="key generation" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				ml-kem-768 keypair generation — lattice-based, quantum-resistant
			</p>
		</section>

		<!-- Encapsulation -->
		<section>
			<h2 class="text-fg mb-6">key encapsulation</h2>
			<div class="flex justify-center">
				<img src="/diagrams/encapsulation.svg" alt="key encapsulation" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				encapsulation produces a shared secret and kem ciphertext
			</p>
		</section>

		<!-- Symmetric Encryption -->
		<section>
			<h2 class="text-fg mb-6">symmetric encryption</h2>
			<div class="flex justify-center">
				<img src="/diagrams/symmetric_encryption.svg" alt="symmetric encryption" class="w-full max-w-lg" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				shared secret derives an aes-256-gcm key for authenticated encryption
			</p>
		</section>

		<!-- Steganography -->
		<section>
			<h2 class="text-fg mb-6">steganography</h2>
			<div class="flex justify-center">
				<img src="/diagrams/steganography.svg" alt="steganography" class="w-full max-w-lg" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				lsb encoding hides ciphertext in the least significant bits of pixel values
			</p>
		</section>

		<!-- Full Decryption -->
		<section>
			<h2 class="text-fg mb-6">decryption</h2>
			<div class="flex justify-center">
				<img src="/diagrams/full_decryption.svg" alt="full decryption" class="w-full" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				complete decryption pipeline — only the private key holder can recover the message
			</p>
		</section>

		<!-- Divider -->
		<div class="h-px bg-border"></div>

		<!-- ML-KEM Performance -->
		<section>
			<h2 class="text-fg mb-6">ml-kem performance</h2>
			<div class="flex justify-center">
				<img src="/diagrams/mlkem_chart.svg" alt="ml-kem performance" class="w-full max-w-md" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				all operations complete in under 80 μs — benchmarked with 25,000 iterations
			</p>
		</section>

		<!-- Operation Times -->
		<section>
			<h2 class="text-fg mb-6">operation times</h2>
			<div class="flex justify-center">
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
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				amd ryzen 5 7535HS, rustc 1.90.0, arch linux
			</p>
		</section>

		<!-- PSNR Chart -->
		<section>
			<h2 class="text-fg mb-6">image quality</h2>
			<div class="flex justify-center">
				<img src="/diagrams/psnr_chart.svg" alt="psnr vs embedding rate" class="w-full max-w-sm" />
			</div>
			<p class="text-center text-fg-muted/50 text-sm italic mt-4">
				psnr stays above 51 db even at 100% capacity — 40 db is the visibility threshold
			</p>
		</section>

		<!-- Data Sizes -->
		<section>
			<h2 class="text-fg mb-6">data sizes</h2>
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
				all operations run client-side.
			</p>
		</footer>
	</article>
</main>
