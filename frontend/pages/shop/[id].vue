<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { ShoppingBag, Star, Check, ShieldCheck, Truck, RefreshCw, ChevronLeft, ArrowRight } from 'lucide-vue-next'
import { useCartStore } from '~/stores/cart'
import { useSeoSchema } from '~/composables/useSeoSchema'

const route = useRoute()
const cartStore = useCartStore()
const { injectProductSchema } = useSeoSchema()

// Demo product details
const product = ref({
  id: 1,
  title: 'گیتار فلامنکو دست‌ساز الحمبرا مدل 7FP Flamenco Negra',
  slug: 'alhambra-7fp-flamenco-negra',
  category_name: 'ساز و گیتارهای دست‌ساز',
  product_type: 'physical',
  product_type_display: 'ساز و ابزار فیزیکی',
  price: 68500000,
  discount_price: 64000000,
  current_price: 64000000,
  discount_percent: 6,
  stock_quantity: 3,
  is_in_stock: true,
  short_description: 'صفحه رویی صنوبر ماسیو آلمانی، پشت و بغل رزوود هندی با پاسخ‌دهی صدایی رسا و کوبنده.',
  description: `این ساز یکی از شاهکارهای کارگاه الحمبرا در کشور اسپانیاست که توسط استاد بهاور به صورت حضوری تست فنی و ساند-چک شده است.
  
طنین صدای این گیتار به دلیل استفاده از چوب‌های کهنه کاری شده درجه یک، در فرکانس‌های میدرنج و بیس بسیار شفاف بوده و اجرای ضربات گلپ (Golpe) و راسگوادو بدون کوچک‌ترین افت رزونانس انجام می‌پذیرد.
  
اکشن سیم‌ها در فرت دوازدهم ۲.۸ میلی‌متر تنظیم شده تا سرعت اجرای تکنیک‌های پیکادو به حداکثر ممکن برسد.`,
  features: [
    'صفحه تاپ: سالید اسپروس آلمانی (Solid German Spruce)',
    'صفحه بک و ساید: رزوود هندی با رگه‌های طبیعی متقارن',
    'فینگربرد و بریج: چوب آبنوس آفریقایی (African Ebony)',
    'گوشی‌های کوک: طلایی لوکس با آبکاری ضد زنگ و نسبت دقیق',
    'همراه با هاردکیس اورجینال اسپانیایی و رطوبت‌سنج',
  ],
  reviews: [
    {
      id: 1,
      user_name: 'امیرحسین رضایی (هنرجوی دوره فلامنکو)',
      rating: 5,
      comment: 'ساز بعد از تست در استودیو به دستم رسید. کوک فوق‌العاده پایدار و اکشن بسیار راحتی داره. ممنون از استاد بهاور عزیز.',
      created_at: '۱۴۰۳/۰۷/۲۰',
    },
    {
      id: 2,
      user_name: 'کیوان مقدم',
      rating: 5,
      comment: 'صدای سدر و رزونانس بیس این گیتار بینظیره. برای اجرای بولریاس و تارانتا بهترین گزینه ممکنه.',
      created_at: '۱۴۰۳/۰۸/۰۲',
    },
  ],
})

// Inject Structured Data for SEO
injectProductSchema({
  title: product.value.title,
  description: product.value.short_description,
  price: product.value.price,
  discount_price: product.value.discount_price,
  is_in_stock: product.value.is_in_stock,
  slug: product.value.slug,
})

const isAdded = ref(false)

const handleAddToCart = () => {
  cartStore.addItem({
    id: product.value.id,
    title: product.value.title,
    price: product.value.current_price,
    product_type: product.value.product_type,
    slug: product.value.slug,
  })
  isAdded.value = true
  setTimeout(() => {
    isAdded.value = false
  }, 2000)
}

useHead({
  title: `${product.value.title} | فروشگاه بهاور موزیک`,
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
    
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-xs text-slate-400">
      <NuxtLink to="/" class="hover:text-amber-400">خانه</NuxtLink>
      <span>/</span>
      <NuxtLink to="/shop" class="hover:text-amber-400">فروشگاه</NuxtLink>
      <span>/</span>
      <span class="text-amber-300 font-medium">{{ product.title }}</span>
    </nav>

    <!-- Product Showcase Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
      
      <!-- Visual Showcase -->
      <div class="space-y-4">
        <div class="aspect-square rounded-3xl glass-panel border border-amber-500/20 overflow-hidden bg-studio-dark/80 flex items-center justify-center p-8 text-center">
          <div class="w-full h-full rounded-2xl bg-gradient-to-br from-wood-950 via-studio-card to-black flex flex-col items-center justify-center p-6 text-amber-500/60 border border-wood-900">
            <span class="text-lg font-bold text-amber-400 mb-2">تست شده در استودیو بهاور</span>
            <span class="text-xs text-slate-400 max-w-xs">کلیه سازها و تجهیزات پیش از ارسال رگلاژ و کنترل کیفی می‌شوند.</span>
          </div>
        </div>
      </div>

      <!-- Details & Purchase Actions -->
      <div class="space-y-6">
        
        <div>
          <span class="text-xs font-semibold text-amber-400 block mb-2">
            {{ product.category_name }}
          </span>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-white leading-tight mb-3">
            {{ product.title }}
          </h1>
          <p class="text-sm text-slate-300 leading-relaxed">
            {{ product.short_description }}
          </p>
        </div>

        <!-- Price Card -->
        <div class="p-6 rounded-2xl glass-panel border border-wood-900 space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-400">قیمت نهایی با احتساب رگلاژ تخصصی:</span>
            <div class="text-left font-mono">
              <span v-if="product.discount_price" class="text-xs text-slate-500 line-through block">
                {{ product.price.toLocaleString('fa-IR') }} تومان
              </span>
              <div class="text-2xl font-black text-amber-400">
                {{ product.current_price.toLocaleString('fa-IR') }}
                <span class="text-xs font-normal text-slate-300 mr-1">تومان</span>
              </div>
            </div>
          </div>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row items-center gap-3 pt-2">
            <button
              @click="handleAddToCart"
              class="w-full sm:flex-1 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-xl shadow-amber-500/20 flex items-center justify-center gap-2 transition-transform active:scale-95"
            >
              <Check v-if="isAdded" class="w-5 h-5 text-black" />
              <ShoppingBag v-else class="w-5 h-5" />
              <span>{{ isAdded ? 'به سبد خرید اضافه شد!' : 'افزودن به سبد خرید' }}</span>
            </button>

            <NuxtLink
              to="/shop/callback?instant=1"
              class="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-wood-900 hover:bg-wood-800 text-amber-300 border border-amber-500/30 text-sm font-semibold flex items-center justify-center transition-colors"
            >
              خرید آنی
            </NuxtLink>
          </div>
        </div>

        <!-- Guarantee Features -->
        <div class="grid grid-cols-3 gap-3 text-center">
          <div class="p-3 rounded-xl bg-studio-card/80 border border-wood-900/80">
            <ShieldCheck class="w-5 h-5 text-amber-400 mx-auto mb-1" />
            <span class="text-[11px] text-slate-300 block">ضمانت اصالت و سلامت</span>
          </div>
          <div class="p-3 rounded-xl bg-studio-card/80 border border-wood-900/80">
            <Truck class="w-5 h-5 text-amber-400 mx-auto mb-1" />
            <span class="text-[11px] text-slate-300 block">ارسال ایمن در هاردکیس</span>
          </div>
          <div class="p-3 rounded-xl bg-studio-card/80 border border-wood-900/80">
            <RefreshCw class="w-5 h-5 text-amber-400 mx-auto mb-1" />
            <span class="text-[11px] text-slate-300 block">مهلت تست ۷ روزه</span>
          </div>
        </div>

        <!-- Specifications -->
        <div class="space-y-3">
          <h4 class="text-sm font-bold text-white border-r-2 border-amber-500 pr-2">ویژگی‌های فنی برجسته:</h4>
          <ul class="space-y-2 text-xs text-slate-300">
            <li v-for="(feat, idx) in product.features" :key="idx" class="flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
              <span>{{ feat }}</span>
            </li>
          </ul>
        </div>

      </div>

    </div>

    <!-- Description & Customer Reviews -->
    <div class="space-y-8 pt-8 border-t border-wood-900">
      
      <!-- Full Description -->
      <div class="p-6 sm:p-8 rounded-3xl glass-panel border border-wood-900/80 space-y-4">
        <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">نقد و بررسی تخصصی بهاور:</h3>
        <div class="text-sm text-slate-300 leading-relaxed whitespace-pre-line">
          {{ product.description }}
        </div>
      </div>

      <!-- Reviews -->
      <div class="space-y-6">
        <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">
          دیدگاه‌های تایید شده هنرجویان و خریداران
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="rev in product.reviews"
            :key="rev.id"
            class="p-5 rounded-2xl glass-panel border border-wood-900 space-y-2"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white">{{ rev.user_name }}</span>
              <div class="flex items-center text-amber-400">
                <Star v-for="s in rev.rating" :key="s" class="w-3.5 h-3.5 fill-amber-400" />
              </div>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">{{ rev.comment }}</p>
            <span class="text-[10px] text-slate-500 font-mono block">{{ rev.created_at }}</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>
