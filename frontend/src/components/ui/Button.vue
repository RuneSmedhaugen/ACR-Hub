<template>
	<button
		:class="buttonClass"
		v-bind="$attrs"
		@click="$emit('click', $event)"
	>
		<slot />
	</button>
</template>

<script setup>
const props = defineProps({
	variant: { type: String, default: 'primary' }
})

const buttonClass = computed(() => {
	const base = 'px-4 py-2 rounded-lg font-medium'
	if (props.variant === 'secondary') return `${base} bg-neutral-800 border border-neutral-600 text-white`
	return `${base} bg-indigo-600 text-white hover:bg-indigo-500`
})
</script>

