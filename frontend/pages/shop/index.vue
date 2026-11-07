<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, ShoppingBag, SlidersHorizontal, Check, Trash2, ArrowLeft } from 'lucide-vue-next'
import { useCartStore } from '~/stores/cart'
import ProductCard from '~/components/shop/ProductCard.vue'

const cartStore = useCartStore()

const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedType = ref('all')
const sortBy = ref('featured')

const categories = [
  { id: 'all', name: 'همه دسته‌ها' },
  { id: 'guitars', name: 'سازها و گیتارها' },
  { id: 'accessories', name: 'سیم و اکسسوری' },
  { id: 'courses', name: 'دوره‌های ویدیویی' },
  { id: 'sheet-music', name: 'کتاب‌های نت' },
]

const products = ref([
  {
    id: 1,
    title: 'گیتار فلامنکو دست‌ساز الحمبرا مدل 7FP Flamenco Negra',
    slug: 'alhambra-7fp-flamenco-negra',
    category_slug: 'guitars',
    category_name: 'ساز و گیتارهای دست‌ساز',
    product_type: 'physical',
    product_type_display: 'ساز و ابزار فیزیکی',
    price: 68500000,
    discount_price: 64000000,
    current_price: 64000000,
    discount_percent: 6,
    is_in_stock: true,
    short_description: 'صفحه رویی صنوبر ماسیو آلمانی، پشت و بغل رزوود هندی با پاسخ‌دهی صدایی رسا.',
  },
  {
    id: 2,
    title: 'سیم گیتار کلاسیک و فلامنکو ساوارز مدل 500ARJ Corum Alliance',
    slug: 'savarez-500arj-corum-alliance',
    category_slug: 'accessories',
    category_name: 'سیم و اکسسوری نوازندگی',
    product_type: 'accessory',
    product_type_display: 'اکسسوری و لوازم جانبی',
    price: 1850000,
    discount_price: 1650000,
    current_price: 1650000,
    discount_percent: 10,
    is_in_stock: true,
    short_description: 'ترکیب تریبل‌های آلیانس کربن با تنشن بالا و بیس‌های کروم نرم و منعطف.',
  },
  {
    id: 3,
    title: 'دوره جامع ویدئویی تکنیک‌های دست راست در گیتار فلامنکو و آکوستیک',
    slug: 'masterclass-right-hand-flamenco-acoustic',
    category_slug: 'courses',
    category_name: 'دوره‌ها و مسترکلاس‌های دیجیتال',
    product_type: 'digital_course',
    product_type_display: 'دوره ویدیویی / مسترکلاس',
    price: 1450000,
    discount_price: 980000,
    current_price: 980000,
    discount_percent: 32,
    is_in_stock: true,
    short_description: '۱۲ ساعت آموزش ویدیویی ۴ زاویه‌ای، بررسی آناتومی دست و سرعت‌بخشی به ضربات.',
  },
  {
    id: 4,
    title: 'کتاب پارتیتور و تبلچر آثار برگزیده موسیقی فلامنکو و اسپانیایی',
    slug: 'selected-flamenco-masterpieces-book',
    category_slug: 'sheet-music',
    category_name: 'کتاب‌های نت و متدهای تخصصی',
    product_type: 'sheet_music',
    product_type_display: 'کتاب نت و پارتیتور دیجیتال',
    price: 420000,
    discount_price: 350000,
    current_price: 350000,
    discount_percent: 16,
    is_in_stock: true,
    short_description: 'گردآوری و انگشت‌گذاری شده توسط بهاور همراه با توضیحات تحلیل هارمونی.',
  },
])

const isCartDrawerOpen = ref(false)

const filteredProducts = computed(() => {
  return products.value.filter((p) => {
    const matchesCat = selectedCategory.value === 'all' || p.category_slug === selectedCategory.value
    const matchesType = selectedType.value === 'all' || p.product_type === selectedType.value
    const matchesSearch = !searchQuery.value || p.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCat && matchesType && matchesSearch
  })
})

useHead({
  title: 'فروشگاه تخصصی گیتار، اکسسوری و دوره‌ها | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
    
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-wood-900 pb-8">
      <div>
        <h1 class="text-2xl sm:text-4xl font-extrabold text-white mb-2">فروشگاه تخصصی ادوات و دوره‌ها</h1>
        <p class="text-sm text-slate-400">سازهای دست‌چین شده، اکسسوری‌های استاندارد نوازندگی و مسترکلاس‌های دیجیتال</p>
      </div>

      <!-- Quick Cart Button -->
      <button
        @click="isCartDrawerOpen = true"
        class="relative px-5 py-3 rounded-2xl glass-panel border border-amber-500/30 text-amber-300 font-bold text-sm flex items-center gap-2 hover:bg-wood-900/60 transition-all self-start md:self-auto"
      >
        <ShoppingBag class="w-5 h-5 text-amber-400" />
        <span>سبد خرید شما</span>
        <span
          v-if="cartStore.totalCount > 0"
          class="px-2 py-0.5 rounded-full bg-amber-500 text-black text-xs font-bold"
        >
          {{ cartStore.totalCount }}
        </span>
      </button>
    </div>

    <!-- Filters & Search Toolbar -->
    <div class="space-y-4">
      <div class="flex flex-col sm:flex-row items-center gap-4">
        
        <!-- Search Input -->
        <div class="relative flex-1 w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="جستجوی عنوان ساز، کتاب، سیم یا دوره..."
            class="w-full px-4 py-3 pl-10 rounded-xl bg-studio-card border border-wood-800 text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 text-sm"
          />
          <Search class="w-4 h-4 text-slate-400 absolute top-3.5 left-3.5" />
        </div>

        <!-- Category Pills -->
        <div class="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            class="px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border"
            :class="selectedCategory === cat.id ? 'bg-amber-500 text-black border-amber-500 shadow-md shadow-amber-500/20' : 'bg-studio-card text-slate-300 border-wood-900 hover:border-amber-500/40'"
          >
            {{ cat.name }}
          </button>
        </div>

      </div>
    </div>

    <!-- Product Grid -->
    <div v-if="filteredProducts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
      />
    </div>

    <div v-else class="text-center py-20 rounded-3xl glass-panel p-8">
      <p class="text-slate-400 text-sm">هیچ محصولی با معیارهای جستجوی شما یافت نشد.</p>
    </div>

    <!-- Cart Drawer / Modal -->
    <div
      v-if="isCartDrawerOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md"
      @click.self="isCartDrawerOpen = false"
    >
      <div class="relative w-full max-w-lg rounded-3xl glass-panel p-6 sm:p-8 shadow-2xl border border-amber-500/30 text-right space-y-6">
        
        <div class="flex items-center justify-between border-b border-wood-900 pb-4">
          <div class="flex items-center gap-2">
            <ShoppingBag class="w-5 h-5 text-amber-400" />
            <h3 class="text-lg font-bold text-white">سبد خرید شما</h3>
          </div>
          <button @click="isCartDrawerOpen = false" class="text-slate-400 hover:text-white text-xs">
            بستن
          </button>
        </div>

        <div v-if="cartStore.items.length > 0" class="space-y-4 max-h-80 overflow-y-auto pr-1">
          <div
            v-for="item in cartStore.items"
            :key="item.productId"
            class="flex items-center justify-between gap-3 p-3 rounded-xl bg-studio-dark/80 border border-wood-900"
          >
            <div class="flex-1">
              <h4 class="text-xs font-bold text-white line-clamp-1">{{ item.title }}</h4>
              <span class="text-[11px] text-amber-400 font-mono">
                {{ item.price.toLocaleString('fa-IR') }} تومان
              </span>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="cartStore.updateQuantity(item.productId, item.quantity - 1)"
                class="w-6 h-6 rounded-md bg-wood-900 text-white flex items-center justify-center text-xs"
              >
                -
              </button>
              <span class="text-xs font-mono font-bold text-white w-4 text-center">{{ item.quantity }}</span>
              <button
                @click="cartStore.updateQuantity(item.productId, item.quantity + 1)"
                class="w-6 h-6 rounded-md bg-wood-900 text-white flex items-center justify-center text-xs"
              >
                +
              </button>
              <button
                @click="cartStore.removeItem(item.productId)"
                class="text-red-400 hover:text-red-300 p-1 mr-1"
                title="حذف"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-10 text-slate-400 text-sm">
          سبد خرید شما در حال حاضر خالی است.
        </div>

        <!-- Total & Checkout -->
        <div v-if="cartStore.items.length > 0" class="pt-4 border-t border-wood-900 space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm text-slate-300">مبلغ کل قابل پرداخت:</span>
            <div class="text-lg font-bold text-amber-400 font-mono">
              {{ cartStore.totalPrice.toLocaleString('fa-IR') }}
              <span class="text-xs text-slate-400 mr-1">تومان</span>
            </div>
          </div>

          <NuxtLink
            to="/shop/callback?demo_checkout=1"
            @click="isCartDrawerOpen = false; cartStore.clearCart()"
            class="w-full py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-xl shadow-amber-500/20 flex items-center justify-center gap-2 transition-transform hover:scale-105"
          >
            <span>اتصال به درگاه بانکی شاپرک و پرداخت</span>
            <ArrowLeft class="w-4 h-4" />
          </NuxtLink>
        </div>

      </div>
    </div>

  </div>
</template>
