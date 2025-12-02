<script lang="ts">
	import { Eye } from 'lucide-svelte';
	import { onMount } from 'svelte';

	interface Props {
		onAnimationComplete?: () => void;
		onHover?: () => void;
		onLeave?: () => void;
	}

	let { onAnimationComplete, onHover, onLeave }: Props = $props();

	let showEye = $state(false);
	let showText = $state(false);
	let animationComplete = $state(false);

	onMount(() => {
		// Start animation automatically
		setTimeout(() => {
			showEye = true;
		}, 300);

		// Show text after eye appears
		setTimeout(() => {
			showText = true;
		}, 1300);

		// Mark animation complete
		setTimeout(() => {
			animationComplete = true;
			onAnimationComplete?.();
		}, 2500);
	});

	function handleMouseEnter() {
		if (animationComplete) {
			onHover?.();
		}
	}

	function handleMouseLeave() {
		if (animationComplete) {
			onLeave?.();
		}
	}
</script>

<div
	class="logo-container"
	onmouseenter={handleMouseEnter}
	onmouseleave={handleMouseLeave}
	role="img"
	aria-label="Plainsight logo"
>
	<div class="logo-text">
		<span class="text-part left" class:visible={showText}>pl</span>
		<span class="eye-letter" class:visible={showEye}>
			<Eye size={32} strokeWidth={1.5} />
		</span>
		<span class="text-part right" class:visible={showText}>insight</span>
	</div>
</div>

<style>
	.logo-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		cursor: pointer;
	}

	.logo-text {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 40px;
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

	@keyframes blink {
		0%, 85%, 100% {
			transform: scaleY(1);
		}
		90%, 95% {
			transform: scaleY(0.1);
		}
	}
</style>
