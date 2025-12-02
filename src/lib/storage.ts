import { toBase64, fromBase64, type KeyPair } from './crypto';

const STORAGE_KEY = 'pq-stego-keypair';

export function saveKeyPair(keyPair: KeyPair): void {
	const data = {
		publicKey: toBase64(keyPair.publicKey),
		secretKey: toBase64(keyPair.secretKey)
	};
	localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function loadKeyPair(): KeyPair | null {
	const stored = localStorage.getItem(STORAGE_KEY);
	if (!stored) return null;

	try {
		const data = JSON.parse(stored);
		return {
			publicKey: fromBase64(data.publicKey),
			secretKey: fromBase64(data.secretKey)
		};
	} catch {
		return null;
	}
}

export function clearKeyPair(): void {
	localStorage.removeItem(STORAGE_KEY);
}

export function hasKeyPair(): boolean {
	return localStorage.getItem(STORAGE_KEY) !== null;
}
