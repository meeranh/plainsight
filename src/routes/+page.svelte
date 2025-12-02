<script lang="ts">
	import {
		generateKeyPair,
		encryptMessage,
		decryptMessage,
		serializePayload,
		deserializePayload,
		toBase64,
		fromBase64,
		type KeyPair
	} from '$lib/crypto';
	import {
		loadImage,
		hideData,
		extractData,
		imageDataToBlob,
		downloadBlob,
		getCapacity
	} from '$lib/stego';
	import { saveKeyPair, loadKeyPair, hasKeyPair } from '$lib/storage';
	import { onMount } from 'svelte';

	type Mode = 'landing' | 'send' | 'receive';
	type ReceiveStep = 'init' | 'keys' | 'decrypt' | 'result';
	type SendStep = 'key' | 'compose' | 'result';

	let mode = $state<Mode>('landing');
	let receiveStep = $state<ReceiveStep>('init');
	let sendStep = $state<SendStep>('key');

	// Receiver state
	let keyPair = $state<KeyPair | null>(null);
	let showSecretKey = $state(false);
	let decryptedMessage = $state('');
	let decryptError = $state('');

	// Sender state
	let recipientPublicKey = $state('');
	let secretMessage = $state('');
	let coverImage = $state<File | null>(null);
	let coverImageUrl = $state('');
	let stegoImageUrl = $state('');
	let stegoBlob = $state<Blob | null>(null);
	let sendError = $state('');
	let imageCapacity = $state(0);
	let dataSize = $state(0);
	let processing = $state(false);
	let processingStep = $state('');

	// Stats for result display
	let stats = $state({
		kemBytes: 0,
		encryptedBytes: 0,
		totalBytes: 0,
		pixelsChanged: ''
	});

	onMount(() => {
		// Load existing key pair if available
		if (hasKeyPair()) {
			keyPair = loadKeyPair();
		}
	});

	function goBack() {
		if (mode === 'receive') {
			if (receiveStep === 'init' || receiveStep === 'keys') {
				mode = 'landing';
				receiveStep = 'init';
			} else if (receiveStep === 'decrypt' || receiveStep === 'result') {
				receiveStep = 'keys';
			}
		} else if (mode === 'send') {
			if (sendStep === 'key') {
				mode = 'landing';
			} else if (sendStep === 'compose') {
				sendStep = 'key';
			} else if (sendStep === 'result') {
				sendStep = 'compose';
			}
		} else {
			mode = 'landing';
		}
		// Reset errors
		decryptError = '';
		sendError = '';
	}

	function handleGenerateKeys() {
		keyPair = generateKeyPair();
		saveKeyPair(keyPair);
		receiveStep = 'keys';
	}

	function handleUseExistingKeys() {
		if (keyPair) {
			receiveStep = 'keys';
		}
	}

	async function copyToClipboard(text: string) {
		await navigator.clipboard.writeText(text);
	}

	function downloadKey(data: Uint8Array, filename: string) {
		const blob = new Blob([toBase64(data)], { type: 'text/plain' });
		downloadBlob(blob, filename);
	}

	async function handleDecryptImage(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file || !keyPair) return;

		decryptError = '';
		processing = true;
		processingStep = 'extracting...';

		try {
			const { imageData } = await loadImage(file);
			processingStep = 'decapsulating...';
			const extractedData = extractData(imageData);
			const payload = deserializePayload(extractedData);

			processingStep = 'decrypting...';
			decryptedMessage = await decryptMessage(payload, keyPair.secretKey);
			receiveStep = 'result';
		} catch (err) {
			decryptError = err instanceof Error ? err.message : 'failed to decrypt';
		} finally {
			processing = false;
			processingStep = '';
		}
	}

	function handleCoverImage(event: Event) {
		const input = event.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;

		coverImage = file;
		coverImageUrl = URL.createObjectURL(file);

		// Calculate capacity
		const img = new Image();
		img.onload = () => {
			imageCapacity = getCapacity(img.width, img.height);
			// Estimate data size (rough: 1088 + 12 + 4 + message length * 2)
			dataSize = 1104 + secretMessage.length * 2;
		};
		img.src = coverImageUrl;
	}

	async function handleEncryptAndHide() {
		if (!coverImage || !secretMessage || !recipientPublicKey) return;

		sendError = '';
		processing = true;

		try {
			processingStep = 'encapsulating...';
			const pubKeyBytes = fromBase64(recipientPublicKey.trim());

			processingStep = 'encrypting...';
			const payload = await encryptMessage(secretMessage, pubKeyBytes);
			const serialized = serializePayload(payload);

			processingStep = 'embedding...';
			const { imageData, width, height } = await loadImage(coverImage);
			const stegoImageData = hideData(imageData, serialized);
			stegoBlob = await imageDataToBlob(stegoImageData);
			stegoImageUrl = URL.createObjectURL(stegoBlob);

			// Calculate stats
			stats = {
				kemBytes: 1088,
				encryptedBytes: payload.ciphertext.length + payload.iv.length,
				totalBytes: serialized.length,
				pixelsChanged: ((serialized.length * 8) / (width * height * 3) * 100).toFixed(2)
			};

			sendStep = 'result';
		} catch (err) {
			sendError = err instanceof Error ? err.message : 'failed to encrypt';
		} finally {
			processing = false;
			processingStep = '';
		}
	}

	function handleDownloadStego() {
		if (stegoBlob) {
			downloadBlob(stegoBlob, 'stego-image.png');
		}
	}

	function resetSender() {
		sendStep = 'key';
		recipientPublicKey = '';
		secretMessage = '';
		coverImage = null;
		coverImageUrl = '';
		stegoImageUrl = '';
		stegoBlob = null;
		sendError = '';
	}

	function resetReceiver() {
		receiveStep = keyPair ? 'keys' : 'init';
		decryptedMessage = '';
		decryptError = '';
	}
</script>

<svelte:head>
	<title>pq-stego</title>
</svelte:head>

<main class="flex min-h-screen flex-col items-center justify-center px-6 py-12">
	{#if mode === 'landing'}
		<div class="max-w-md text-center animate-in">
			<p class="text-fg-muted leading-relaxed">
				encrypt and hide messages<br />
				in images using post-quantum<br />
				cryptography.
			</p>

			<div class="mt-12 flex gap-4 justify-center">
				<button
					onclick={() => { mode = 'send'; sendStep = 'key'; }}
					class="px-6 py-2 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100"
				>
					send
				</button>
				<button
					onclick={() => { mode = 'receive'; receiveStep = keyPair ? 'keys' : 'init'; }}
					class="px-6 py-2 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100"
				>
					receive
				</button>
			</div>

			<p class="mt-16 text-sm text-fg-muted/50">
				ml-kem-768 &middot; aes-256-gcm &middot; lsb steganography
			</p>
		</div>

	{:else if mode === 'receive'}
		<div class="w-full max-w-lg animate-in">
			<button
				onclick={goBack}
				class="text-fg-muted hover:text-fg transition-colors duration-100 mb-8"
			>
				&larr; back
			</button>

			{#if receiveStep === 'init'}
				<div>
					<h2 class="text-fg mb-2">receive mode</h2>
					<div class="h-px bg-border mb-6"></div>

					<p class="text-fg-muted mb-8">
						generate a keypair. share your public key<br />
						with anyone who wants to message you.
					</p>

					<div class="space-y-4">
						<button
							onclick={handleGenerateKeys}
							class="w-full px-6 py-3 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100"
						>
							generate keys
						</button>

						{#if keyPair}
							<button
								onclick={handleUseExistingKeys}
								class="w-full px-6 py-3 text-fg-muted/50 hover:text-fg-muted transition-colors duration-100"
							>
								use existing keys
							</button>
						{/if}
					</div>
				</div>

			{:else if receiveStep === 'keys'}
				<div>
					<h2 class="text-fg mb-2">your public key</h2>
					<div class="h-px bg-border mb-6"></div>

					<p class="text-fg-muted/70 text-sm mb-4">
						share this with senders. it's safe to post publicly.
					</p>

					<div class="border border-border p-4 mb-4 break-all text-sm text-fg-muted font-mono bg-bg-card">
						{keyPair ? toBase64(keyPair.publicKey) : ''}
					</div>

					<div class="flex gap-4 mb-8">
						<button
							onclick={() => keyPair && copyToClipboard(toBase64(keyPair.publicKey))}
							class="px-4 py-2 text-sm text-fg-muted hover:text-aqua transition-colors duration-100"
						>
							copy
						</button>
						<button
							onclick={() => keyPair && downloadKey(keyPair.publicKey, 'public-key.txt')}
							class="px-4 py-2 text-sm text-fg-muted hover:text-aqua transition-colors duration-100"
						>
							download
						</button>
					</div>

					<div class="border-t border-dashed border-border pt-8 mt-8">
						<h2 class="text-fg mb-2">your secret key</h2>
						<div class="h-px bg-border mb-6"></div>

						<p class="text-fg-muted/70 text-sm mb-4">
							never share this. stored locally in your browser.
						</p>

						<div class="border border-border p-4 mb-4 break-all text-sm text-fg-muted font-mono bg-bg-card">
							{#if showSecretKey}
								{keyPair ? toBase64(keyPair.secretKey) : ''}
							{:else}
								{'•'.repeat(64)}
							{/if}
						</div>

						<div class="flex gap-4 mb-8">
							<button
								onclick={() => (showSecretKey = !showSecretKey)}
								class="px-4 py-2 text-sm text-fg-muted hover:text-aqua transition-colors duration-100"
							>
								{showSecretKey ? 'hide' : 'reveal'}
							</button>
							<button
								onclick={() => keyPair && downloadKey(keyPair.secretKey, 'secret-key.txt')}
								class="px-4 py-2 text-sm text-fg-muted hover:text-aqua transition-colors duration-100"
							>
								download backup
							</button>
						</div>
					</div>

					<div class="border-t border-dashed border-border pt-8 mt-8">
						<h2 class="text-fg mb-2">decrypt an image</h2>
						<div class="h-px bg-border mb-6"></div>

						<p class="text-fg-muted/70 text-sm mb-4">
							upload an image someone sent you.
						</p>

						<label class="block border border-dashed border-border p-8 text-center cursor-pointer hover:border-aqua transition-colors duration-100">
							<input
								type="file"
								accept="image/png,image/jpeg"
								class="hidden"
								onchange={handleDecryptImage}
							/>
							{#if processing}
								<span class="text-fg-muted">{processingStep}<span class="animate-pulse">|</span></span>
							{:else}
								<span class="text-fg-muted">drop image here<br /><span class="text-fg-muted/50">png or jpg</span></span>
							{/if}
						</label>

						{#if decryptError}
							<p class="mt-4 text-red text-sm">{decryptError}</p>
						{/if}
					</div>
				</div>

			{:else if receiveStep === 'result'}
				<div>
					<h2 class="text-fg mb-2">decrypted message</h2>
					<div class="h-px bg-border mb-6"></div>

					<div class="border border-border p-6 mb-6 text-fg bg-bg-card whitespace-pre-wrap">
						{decryptedMessage}
					</div>

					<div class="flex gap-4 mb-8">
						<button
							onclick={() => copyToClipboard(decryptedMessage)}
							class="px-4 py-2 text-sm text-fg-muted hover:text-aqua transition-colors duration-100"
						>
							copy
						</button>
					</div>

					<p class="text-sm text-green mb-8">
						&check; extracted &nbsp; &check; decapsulated &nbsp; &check; decrypted &nbsp; &check; verified
					</p>

					<button
						onclick={resetReceiver}
						class="text-fg-muted hover:text-fg transition-colors duration-100"
					>
						decrypt another
					</button>
				</div>
			{/if}
		</div>

	{:else if mode === 'send'}
		<div class="w-full max-w-lg animate-in">
			<button
				onclick={goBack}
				class="text-fg-muted hover:text-fg transition-colors duration-100 mb-8"
			>
				&larr; back
			</button>

			{#if sendStep === 'key'}
				<div>
					<h2 class="text-fg mb-2">send mode</h2>
					<div class="h-px bg-border mb-6"></div>

					<p class="text-fg-muted/70 text-sm mb-4">
						paste the recipient's public key.
					</p>

					<textarea
						bind:value={recipientPublicKey}
						placeholder="paste public key here..."
						class="w-full border border-border p-4 mb-6 bg-bg-card text-fg placeholder-fg-muted/30 font-mono text-sm resize-none h-32 focus:outline-none focus:border-aqua transition-colors duration-100"
					></textarea>

					<button
						onclick={() => recipientPublicKey.trim() && (sendStep = 'compose')}
						disabled={!recipientPublicKey.trim()}
						class="px-6 py-2 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:border-border disabled:hover:text-fg-muted"
					>
						continue
					</button>
				</div>

			{:else if sendStep === 'compose'}
				<div>
					<h2 class="text-fg mb-2">your message</h2>
					<div class="h-px bg-border mb-6"></div>

					<textarea
						bind:value={secretMessage}
						placeholder="type your secret message..."
						class="w-full border border-border p-4 mb-6 bg-bg-card text-fg placeholder-fg-muted/30 font-mono text-sm resize-none h-32 focus:outline-none focus:border-aqua transition-colors duration-100"
					></textarea>

					<h2 class="text-fg mb-2 mt-8">cover image</h2>
					<div class="h-px bg-border mb-6"></div>

					<label class="block border border-dashed border-border p-8 text-center cursor-pointer hover:border-aqua transition-colors duration-100 mb-4">
						<input
							type="file"
							accept="image/png,image/jpeg"
							class="hidden"
							onchange={handleCoverImage}
						/>
						{#if coverImageUrl}
							<img src={coverImageUrl} alt="cover" class="max-h-48 mx-auto mb-2" />
							<span class="text-fg-muted/50 text-sm">click to change</span>
						{:else}
							<span class="text-fg-muted">drop image here<br /><span class="text-fg-muted/50">png or jpg</span></span>
						{/if}
					</label>

					{#if imageCapacity > 0}
						<p class="text-fg-muted/50 text-sm mb-6">
							capacity: {(imageCapacity / 1024).toFixed(1)} KB
							{#if dataSize > 0}
								&middot; required: ~{(dataSize / 1024).toFixed(1)} KB
								{#if dataSize <= imageCapacity}
									<span class="text-green">&check;</span>
								{:else}
									<span class="text-red">&cross; too large</span>
								{/if}
							{/if}
						</p>
					{/if}

					{#if sendError}
						<p class="mb-4 text-red text-sm">{sendError}</p>
					{/if}

					<button
						onclick={handleEncryptAndHide}
						disabled={!secretMessage || !coverImage || processing}
						class="px-6 py-2 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100 disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:border-border disabled:hover:text-fg-muted"
					>
						{#if processing}
							{processingStep}<span class="animate-pulse">|</span>
						{:else}
							encrypt & hide
						{/if}
					</button>
				</div>

			{:else if sendStep === 'result'}
				<div>
					<h2 class="text-fg mb-2">done</h2>
					<div class="h-px bg-border mb-6"></div>

					<p class="text-fg-muted/70 text-sm mb-6">
						message hidden. send this image to the recipient.
					</p>

					<div class="flex gap-4 items-center justify-center mb-6">
						{#if coverImageUrl}
							<div class="text-center">
								<img src={coverImageUrl} alt="original" class="max-h-32 border border-border" />
								<p class="text-fg-muted/50 text-xs mt-2">original</p>
							</div>
						{/if}
						<span class="text-aqua">&rarr;</span>
						{#if stegoImageUrl}
							<div class="text-center">
								<img src={stegoImageUrl} alt="with secret" class="max-h-32 border border-border" />
								<p class="text-fg-muted/50 text-xs mt-2">with secret</p>
							</div>
						{/if}
					</div>

					<div class="text-fg-muted/50 text-sm mb-8 font-mono">
						<p>&gt; encapsulated &nbsp;&nbsp; {stats.kemBytes} bytes</p>
						<p>&gt; encrypted &nbsp;&nbsp;&nbsp;&nbsp; {stats.encryptedBytes} bytes</p>
						<p>&gt; embedded &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {stats.totalBytes} bytes</p>
						<p>&gt; pixels changed &nbsp; {stats.pixelsChanged}%</p>
					</div>

					<button
						onclick={handleDownloadStego}
						class="w-full px-6 py-3 border border-border text-fg-muted hover:border-aqua hover:text-aqua transition-colors duration-100 mb-4"
					>
						download image
					</button>

					<button
						onclick={resetSender}
						class="text-fg-muted/50 hover:text-fg-muted transition-colors duration-100"
					>
						send another
					</button>
				</div>
			{/if}
		</div>
	{/if}
</main>

<style>
	.animate-in {
		animation: fadeIn 150ms ease-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(4px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
