<script setup lang="ts">
import { ShoppingBag, Star, Check } from 'lucide-vue-next'
import { useCartStore } from '~/stores/cart'

const props = defineProps<{
  product: {
    id: number
    title: string
    slug: string
    category_name: string
    product_type: string
    product_type_display: string
    price: number
    discount_price?: number
    current_price: number
    discount_percent: number
    is_in_stock: boolean
    cover_image?: string
    short_description: string
  }
}>()

const cartStore = useCartStore()

const handleAddToCart = () => {
  cartStore.addItem({
    id: props.product.id,
    title: props.product.title,
    price: props.product.current_price,
    cover_image: props.product.cover_image,
    product_type: props.product.product_type,
    slug: props.product.slug,
  })
}
</script>

<template>
  <div class="group relative rounded-2xl glass-panel border border-wood-900/80 hover:border-amber-500/40 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-950/20 flex flex-col overflow-hidden">
    
    <!-- Discount Badge -->
    <div
      v-if="product.discount_percent > 0"
      class="absolute top-3 right-3 z-10 px-2.5 py-1 rounded-lg bg-red-600 text-white text-[11px] font-bold shadow-md"
    >
      {{ product.discount_percent }}٪ تخفیف
    </div>

    <!-- Product Image Preview / Icon Placeholder -->
    <NuxtLink :to="`/shop/${product.slug}`" class="relative aspect-square w-full bg-studio-dark/80 overflow-hidden flex items-center justify-center">
      <img
        v-if="product.cover_image"
        :src="product.cover_image"
        :alt="product.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div v-else class="w-full h-full bg-gradient-to-br from-wood-950 to-studio-card flex items-center justify-center p-6 text-center text-amber-500/50">
        <span class="text-xs font-medium">{{ product.product_type_display }}</span>
      </div>
    </NuxtLink>

    <!-- Details -->
    <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
      <div>
        <span class="text-[11px] font-semibold text-amber-400 block mb-1">
          {{ product.category_name || product.product_type_display }}
        </span>
        <NuxtLink :to="`/shop/${product.slug}`">
          <h3 class="text-sm font-bold text-white group-hover:text-amber-400 transition-colors line-clamp-2 leading-relaxed">
            {{ product.title }}
          </h3>
        </NuxtLink>
        <p class="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
          {{ product.short_description }}
        </p>
      </div>

      <!-- Price & Add to Cart -->
      <div class="pt-3 border-t border-wood-900/60 flex items-center justify-between">
        <div>
          <span v-if="product.discount_price" class="text-[11px] text-slate-500 line-through block font-mono">
            {{ product.price.toLocaleString('fa-IR') }}
          </span>
          <div class="text-base font-bold text-amber-400 font-mono">
            {{ product.current_price.toLocaleString('fa-IR') }}
            <span class="text-[11px] font-normal text-slate-400 mr-1">تومان</span>
          </div>
        </div>

        <button
          @click="handleAddToCart"
          class="p-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black shadow-md shadow-amber-500/20 active:scale-95 transition-all"
          title="افزودن به سبد خرید"
        >
          <ShoppingBag class="w-4 h-4" />
        </button>
      </div>

    </div>

  </div>
</template>
