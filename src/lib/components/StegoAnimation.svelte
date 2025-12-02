<script lang="ts">
	import { Image, Eye } from 'lucide-svelte';

	interface Props {
		onEyesComplete?: () => void;
		onEyesFading?: () => void;
	}

	let { onEyesComplete, onEyesFading }: Props = $props();

	let showEye = $state(false);
	let showText = $state(false);
	let fading = $state(false);
	let timeouts: ReturnType<typeof setTimeout>[] = [];

	function clearAllTimeouts() {
		timeouts.forEach(t => clearTimeout(t));
		timeouts = [];
	}

	function handleMouseEnter() {
		clearAllTimeouts();
		fading = false;
		showEye = true;

		// After eye appears and starts blinking, show the text
		timeouts.push(setTimeout(() => {
			showText = true;
		}, 1000));

		// Trigger callback after text appears
		timeouts.push(setTimeout(() => {
			onEyesComplete?.();
		}, 2500));
	}

	function handleMouseLeave() {
		clearAllTimeouts();
		onEyesFading?.();
		fading = true;

		// Wait 1s, then fade out
		timeouts.push(setTimeout(() => {
			showText = false;
		}, 1000));

		timeouts.push(setTimeout(() => {
			showEye = false;
			fading = false;
		}, 1400));
	}
</script>

<div
	class="stego-container"
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	role="img"
	aria-label="Plainsight animation"
>
	<!-- The logo text with eye -->
	<div class="logo-text" class:visible={showEye} class:fading>
		<span class="text-part left" class:visible={showText} class:fading>pl</span>
		<span class="eye-letter" class:visible={showEye} class:fading>
			<Eye size={32} strokeWidth={1.5} />
		</span>
		<span class="text-part right" class:visible={showText} class:fading>insight</span>
	</div>

	<!-- Image icon trigger -->
	<div class="image-icon">
		<Image size={48} strokeWidth={1.5} class="text-fg-muted" />
	</div>
</div>

<style>
	.stego-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
	}

	.image-icon {
		padding: 8px;
	}

	.logo-text {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 40px;
		margin-bottom: 8px;
		font-size: 1.5rem;
		font-weight: 400;
		letter-spacing: 0.05em;
	}

	.text-part {
		color: var(--color-fg);
		opacity: 0;
		transition: opacity 0.8s ease-out, transform 0.8s ease-out;
	}

	.text-part.left {
		transform: translateX(10px);
	}

	.text-part.right {
		transform: translateX(-10px);
	}

	.text-part.visible {
		opacity: 1;
		transform: translateX(0);
	}

	.text-part.fading {
		opacity: 0;
		transition: opacity 0.3s ease-out;
	}

	.eye-letter {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		color: var(--color-red);
		opacity: 0;
		transform: scale(0.3);
		transition: opacity 0.4s ease-out, transform 0.4s ease-out;
		margin: 0 -2px;
	}

	.eye-letter.visible {
		opacity: 1;
		transform: scale(1);
		animation: blink 3s ease-in-out infinite;
	}

	.eye-letter.fading {
		opacity: 0;
		transform: scale(0.3);
		transition: opacity 0.3s ease-out, transform 0.3s ease-out;
		animation: none;
	}

	@keyframes blink {
		0%, 85%, 100% {
			transform: scaleY(1);
		}
		90%, 95% {
			transform: scaleY(0.1);
		}
	}
</style>
