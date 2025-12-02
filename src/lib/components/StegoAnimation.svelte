<script lang="ts">
	import { Image, Eye } from 'lucide-svelte';

	interface Props {
		onEyesComplete?: () => void;
		onEyesFading?: () => void;
	}

	let { onEyesComplete, onEyesFading }: Props = $props();

	const NUM_EYES = 12;
	const RADIUS = 280; // pixels from center

	let showEyes = $state(false);
	let eyeStates = $state<number[]>(Array(NUM_EYES).fill(0)); // 0=hidden, 1=visible, 2=fading
	let timeouts: ReturnType<typeof setTimeout>[] = [];

	// Random blink durations for each eye (1.5s to 3.5s)
	const blinkDurations = Array(NUM_EYES).fill(0).map(() => 1.5 + Math.random() * 2);

	// Calculate positions in a circle (starting from top, going clockwise)
	const eyePositions = Array(NUM_EYES).fill(0).map((_, i) => {
		const angle = (i / NUM_EYES) * 2 * Math.PI - Math.PI / 2; // Start from top
		return {
			x: Math.cos(angle) * RADIUS,
			y: Math.sin(angle) * RADIUS
		};
	});

	function clearAllTimeouts() {
		timeouts.forEach(t => clearTimeout(t));
		timeouts = [];
	}

	function handleMouseEnter() {
		clearAllTimeouts();
		showEyes = true;

		// Appear in circular fashion (one by one)
		for (let i = 0; i < NUM_EYES; i++) {
			timeouts.push(setTimeout(() => {
				eyeStates[i] = 1;
				eyeStates = [...eyeStates];
			}, i * 80)); // 80ms between each eye
		}

		// After all eyes formed + 1 second, trigger callback
		timeouts.push(setTimeout(() => {
			onEyesComplete?.();
		}, NUM_EYES * 80 + 1000));
	}

	function handleMouseLeave() {
		clearAllTimeouts();
		onEyesFading?.();

		// Wait 1s, then disappear in circular fashion
		for (let i = 0; i < NUM_EYES; i++) {
			timeouts.push(setTimeout(() => {
				eyeStates[i] = 2;
				eyeStates = [...eyeStates];
			}, 1000 + i * 150)); // 150ms between each fade
		}

		timeouts.push(setTimeout(() => {
			showEyes = false;
			eyeStates = Array(NUM_EYES).fill(0);
		}, 1000 + NUM_EYES * 150 + 500));
	}
</script>

<div
	class="stego-trigger"
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	role="img"
	aria-label="Steganography animation"
>
	<Image size={48} strokeWidth={1.5} class="text-fg-muted" />
</div>

<!-- Eyes in a circle around center -->
{#if showEyes}
	{#each eyePositions as pos, i}
		<div
			class="eye"
			class:visible={eyeStates[i] === 1}
			class:fade-out={eyeStates[i] === 2}
			style="
				--blink-duration: {blinkDurations[i]}s;
				--x: {pos.x}px;
				--y: {pos.y}px;
			"
		>
			<Eye size={24} strokeWidth={1.5} />
		</div>
	{/each}
{/if}

<style>
	.stego-trigger {
		cursor: pointer;
		padding: 8px;
	}

	.eye {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y)));
		color: var(--color-red);
		opacity: 0;
		z-index: 50;
		pointer-events: none;
	}

	.eye.visible {
		animation:
			fadeIn 400ms ease-out forwards,
			blink var(--blink-duration) ease-in-out 600ms infinite;
	}

	.eye.fade-out {
		opacity: 1;
		animation: fadeOut 400ms ease-out forwards;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(0.3);
		}
		to {
			opacity: 1;
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(1);
		}
	}

	@keyframes fadeOut {
		from {
			opacity: 1;
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(1);
		}
		to {
			opacity: 0;
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scale(0.3);
		}
	}

	@keyframes blink {
		0%, 85%, 100% {
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scaleY(1);
		}
		92% {
			transform: translate(calc(-50% + var(--x)), calc(-50% + var(--y))) scaleY(0.1);
		}
	}
</style>
