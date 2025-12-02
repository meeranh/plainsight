// LSB Steganography implementation

// Calculate maximum bytes that can be hidden in an image
export function getCapacity(width: number, height: number): number {
	// Each pixel has RGB channels (3 bytes), we use 1 bit per channel
	// So 3 bits per pixel = 3/8 bytes per pixel
	// Reserve 4 bytes for length header
	return Math.floor((width * height * 3) / 8) - 4;
}

// Hide data in image using LSB steganography
export function hideData(imageData: ImageData, data: Uint8Array): ImageData {
	const pixels = imageData.data;
	const capacity = getCapacity(imageData.width, imageData.height);

	if (data.length > capacity) {
		throw new Error(`Data too large: ${data.length} bytes, capacity: ${capacity} bytes`);
	}

	// Create length header (4 bytes, big-endian)
	const lengthBuffer = new ArrayBuffer(4);
	new DataView(lengthBuffer).setUint32(0, data.length, false);
	const lengthBytes = new Uint8Array(lengthBuffer);

	// Combine length header and data
	const fullData = new Uint8Array(4 + data.length);
	fullData.set(lengthBytes, 0);
	fullData.set(data, 4);

	// Convert to bits
	const bits: number[] = [];
	for (const byte of fullData) {
		for (let i = 7; i >= 0; i--) {
			bits.push((byte >> i) & 1);
		}
	}

	// Embed bits into image
	let bitIndex = 0;
	for (let i = 0; i < pixels.length && bitIndex < bits.length; i++) {
		// Skip alpha channel (every 4th byte)
		if ((i + 1) % 4 === 0) continue;

		// Set LSB of pixel to bit
		pixels[i] = (pixels[i] & 0xfe) | bits[bitIndex];
		bitIndex++;
	}

	return imageData;
}

// Extract hidden data from image
export function extractData(imageData: ImageData): Uint8Array {
	const pixels = imageData.data;

	// Extract bits from image
	const bits: number[] = [];
	for (let i = 0; i < pixels.length; i++) {
		// Skip alpha channel
		if ((i + 1) % 4 === 0) continue;
		bits.push(pixels[i] & 1);
	}

	// Convert first 32 bits to length
	let length = 0;
	for (let i = 0; i < 32; i++) {
		length = (length << 1) | bits[i];
	}

	// Validate length
	const maxLength = Math.floor(bits.length / 8) - 4;
	if (length <= 0 || length > maxLength) {
		throw new Error('No hidden data found or data corrupted');
	}

	// Extract data bytes
	const data = new Uint8Array(length);
	for (let i = 0; i < length; i++) {
		let byte = 0;
		for (let j = 0; j < 8; j++) {
			byte = (byte << 1) | bits[32 + i * 8 + j];
		}
		data[i] = byte;
	}

	return data;
}

// Load image from file and return ImageData
export function loadImage(file: File): Promise<{ imageData: ImageData; width: number; height: number }> {
	return new Promise((resolve, reject) => {
		const img = new Image();
		const url = URL.createObjectURL(file);

		img.onload = () => {
			URL.revokeObjectURL(url);

			const canvas = document.createElement('canvas');
			canvas.width = img.width;
			canvas.height = img.height;

			const ctx = canvas.getContext('2d');
			if (!ctx) {
				reject(new Error('Could not get canvas context'));
				return;
			}

			ctx.drawImage(img, 0, 0);
			const imageData = ctx.getImageData(0, 0, img.width, img.height);

			resolve({
				imageData,
				width: img.width,
				height: img.height
			});
		};

		img.onerror = () => {
			URL.revokeObjectURL(url);
			reject(new Error('Failed to load image'));
		};

		img.src = url;
	});
}

// Convert ImageData to PNG blob
export function imageDataToBlob(imageData: ImageData): Promise<Blob> {
	return new Promise((resolve, reject) => {
		const canvas = document.createElement('canvas');
		canvas.width = imageData.width;
		canvas.height = imageData.height;

		const ctx = canvas.getContext('2d');
		if (!ctx) {
			reject(new Error('Could not get canvas context'));
			return;
		}

		ctx.putImageData(imageData, 0, 0);

		canvas.toBlob(
			(blob) => {
				if (blob) {
					resolve(blob);
				} else {
					reject(new Error('Failed to create blob'));
				}
			},
			'image/png',
			1.0
		);
	});
}

// Create download URL for blob
export function createDownloadUrl(blob: Blob): string {
	return URL.createObjectURL(blob);
}

// Trigger download of a blob
export function downloadBlob(blob: Blob, filename: string): void {
	const url = createDownloadUrl(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
}
