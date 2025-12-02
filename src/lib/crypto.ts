import { ml_kem768 } from '@noble/post-quantum/ml-kem.js';

export interface KeyPair {
	publicKey: Uint8Array;
	secretKey: Uint8Array;
}

export interface EncapsulationResult {
	cipherText: Uint8Array;
	sharedSecret: Uint8Array;
}

export interface EncryptedPayload {
	kemCiphertext: Uint8Array;
	iv: Uint8Array;
	ciphertext: Uint8Array;
}

// Generate ML-KEM-768 key pair
export function generateKeyPair(): KeyPair {
	const { publicKey, secretKey } = ml_kem768.keygen();
	return { publicKey, secretKey };
}

// Encapsulate using recipient's public key
export function encapsulate(publicKey: Uint8Array): EncapsulationResult {
	const { cipherText, sharedSecret } = ml_kem768.encapsulate(publicKey);
	return { cipherText, sharedSecret };
}

// Decapsulate using own secret key
export function decapsulate(cipherText: Uint8Array, secretKey: Uint8Array): Uint8Array {
	return ml_kem768.decapsulate(cipherText, secretKey);
}

// Helper to get ArrayBuffer from Uint8Array
function toArrayBuffer(arr: Uint8Array): ArrayBuffer {
	return arr.buffer.slice(arr.byteOffset, arr.byteOffset + arr.byteLength) as ArrayBuffer;
}

// Derive AES-256 key from shared secret using HKDF
async function deriveAESKey(sharedSecret: Uint8Array): Promise<CryptoKey> {
	const keyMaterial = await crypto.subtle.importKey(
		'raw',
		toArrayBuffer(sharedSecret),
		'HKDF',
		false,
		['deriveKey']
	);

	return crypto.subtle.deriveKey(
		{
			name: 'HKDF',
			hash: 'SHA-256',
			salt: new Uint8Array(32),
			info: new TextEncoder().encode('plainsight-aes-key')
		},
		keyMaterial,
		{ name: 'AES-GCM', length: 256 },
		false,
		['encrypt', 'decrypt']
	);
}

// Encrypt message with AES-256-GCM
export async function encryptMessage(
	message: string,
	recipientPublicKey: Uint8Array
): Promise<EncryptedPayload> {
	// Encapsulate to get shared secret
	const { cipherText: kemCiphertext, sharedSecret } = encapsulate(recipientPublicKey);

	// Derive AES key
	const aesKey = await deriveAESKey(sharedSecret);

	// Generate IV
	const iv = crypto.getRandomValues(new Uint8Array(12));

	// Encrypt
	const encoded = new TextEncoder().encode(message);
	const ciphertext = new Uint8Array(
		await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, aesKey, encoded)
	);

	return { kemCiphertext, iv, ciphertext };
}

// Decrypt message with AES-256-GCM
export async function decryptMessage(
	payload: EncryptedPayload,
	secretKey: Uint8Array
): Promise<string> {
	// Decapsulate to get shared secret
	const sharedSecret = decapsulate(payload.kemCiphertext, secretKey);

	// Derive AES key
	const aesKey = await deriveAESKey(sharedSecret);

	// Decrypt
	const decrypted = await crypto.subtle.decrypt(
		{ name: 'AES-GCM', iv: toArrayBuffer(payload.iv) },
		aesKey,
		toArrayBuffer(payload.ciphertext)
	);

	return new TextDecoder().decode(decrypted);
}

// Serialize payload to bytes
export function serializePayload(payload: EncryptedPayload): Uint8Array {
	// Format: [kemCiphertext (1088 bytes)] [iv (12 bytes)] [ciphertext length (4 bytes)] [ciphertext]
	const ciphertextLength = payload.ciphertext.length;
	const totalLength = 1088 + 12 + 4 + ciphertextLength;
	const result = new Uint8Array(totalLength);

	let offset = 0;

	// KEM ciphertext (fixed 1088 bytes for ML-KEM-768)
	result.set(payload.kemCiphertext, offset);
	offset += 1088;

	// IV (12 bytes)
	result.set(payload.iv, offset);
	offset += 12;

	// Ciphertext length (4 bytes, big-endian)
	const lengthBytes = new DataView(new ArrayBuffer(4));
	lengthBytes.setUint32(0, ciphertextLength, false);
	result.set(new Uint8Array(lengthBytes.buffer), offset);
	offset += 4;

	// Ciphertext
	result.set(payload.ciphertext, offset);

	return result;
}

// Deserialize bytes to payload
export function deserializePayload(data: Uint8Array): EncryptedPayload {
	let offset = 0;

	// KEM ciphertext
	const kemCiphertext = data.slice(offset, offset + 1088);
	offset += 1088;

	// IV
	const iv = data.slice(offset, offset + 12);
	offset += 12;

	// Ciphertext length
	const lengthView = new DataView(data.buffer, data.byteOffset + offset, 4);
	const ciphertextLength = lengthView.getUint32(0, false);
	offset += 4;

	// Ciphertext
	const ciphertext = data.slice(offset, offset + ciphertextLength);

	return { kemCiphertext, iv, ciphertext };
}

// Encode bytes to base64
export function toBase64(data: Uint8Array): string {
	return btoa(String.fromCharCode(...data));
}

// Decode base64 to bytes
export function fromBase64(str: string): Uint8Array {
	return Uint8Array.from(atob(str), (c) => c.charCodeAt(0));
}
