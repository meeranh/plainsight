<script lang="ts">
	import { onMount } from 'svelte';
	import mermaid from 'mermaid';

	interface Props {
		chart: string;
	}

	let { chart }: Props = $props();
	let container: HTMLDivElement;
	let rendered = $state(false);

	onMount(async () => {
		mermaid.initialize({
			startOnLoad: false,
			theme: 'base',
			themeVariables: {
				// Background
				background: 'transparent',

				// Primary (nodes) - Gruvbox aqua tint
				primaryColor: '#3c3836',
				primaryBorderColor: '#8ec07c',
				primaryTextColor: '#ebdbb2',

				// Secondary - Gruvbox yellow tint
				secondaryColor: '#3c3836',
				secondaryBorderColor: '#fabd2f',
				secondaryTextColor: '#ebdbb2',

				// Tertiary - Gruvbox purple tint
				tertiaryColor: '#3c3836',
				tertiaryBorderColor: '#d3869b',
				tertiaryTextColor: '#ebdbb2',

				// Lines and text
				lineColor: '#fabd2f',
				textColor: '#ebdbb2',

				// Font
				fontFamily: 'Iosevka, monospace',
				fontSize: '32px',

				// Flowchart specific
				nodeBorder: '#8ec07c',
				mainBkg: '#3c3836',
				nodeTextColor: '#ebdbb2',

				// Edges
				edgeLabelBackground: '#1d2021',
			},
			flowchart: {
				htmlLabels: true,
				curve: 'basis',
				padding: 30,
				nodeSpacing: 80,
				rankSpacing: 80,
			},
			sequence: {
				actorMargin: 100,
				boxMargin: 20,
				boxTextMargin: 10,
				noteMargin: 20,
				messageMargin: 50,
				mirrorActors: true,
				width: 200,
				height: 80,
			},
		});

		try {
			const { svg } = await mermaid.render(`mermaid-${Math.random().toString(36).slice(2)}`, chart);
			container.innerHTML = svg;
			rendered = true;
		} catch (e) {
			console.error('Mermaid error:', e);
			container.textContent = 'Diagram error';
		}
	});
</script>

<div class="flex justify-center my-16 py-8">
	<div bind:this={container} class="mermaid-container">
		{#if !rendered}
			<span class="text-fg-muted text-sm">loading...</span>
		{/if}
	</div>
</div>

<style>
	.mermaid-container :global(svg) {
		width: 100%;
		height: auto;
		transform: scale(2.2);
		transform-origin: center;
	}

	.mermaid-container :global(svg text),
	.mermaid-container :global(svg tspan) {
		font-size: 28px !important;
		font-family: 'Iosevka', monospace !important;
	}

	.mermaid-container :global(.messageText),
	.mermaid-container :global(.sequenceNumber),
	.mermaid-container :global(.labelText) {
		font-size: 24px !important;
	}

	.mermaid-container :global(.actor),
	.mermaid-container :global(.actor-box text),
	.mermaid-container :global(text.actor) {
		font-size: 28px !important;
	}

	.mermaid-container :global(.loopText),
	.mermaid-container :global(.noteText) {
		font-size: 22px !important;
	}
</style>
