<script setup lang="ts">
import { ref } from 'vue'
import { 
  Music, 
  Guitar, 
  Calendar, 
  ShoppingBag, 
  BookOpen, 
  Sparkles, 
  ArrowLeft, 
  Play, 
  Users, 
  Mic, 
  Award,
  ChevronLeft
} from 'lucide-vue-next'
import { useSeoSchema } from '~/composables/useSeoSchema'
import ProductCard from '~/components/shop/ProductCard.vue'
import CompositionCard from '~/components/repertoire/CompositionCard.vue'
import ServiceCard from '~/components/booking/ServiceCard.vue'
import BlogCard from '~/components/blog/BlogCard.vue'

const { injectPersonSchema } = useSeoSchema()
injectPersonSchema()

// Mock data (SSR safe fallback)
const featuredProducts = ref([
  {
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
    is_in_stock: true,
    short_description: 'صفحه رویی صنوبر ماسیو آلمانی، پشت و بغل رزوود هندی با پاسخ‌دهی صدایی رسا.',
  },
  {
    id: 2,
    title: 'سیم گیتار کلاسیک و فلامنکو ساوارز مدل 500ARJ Corum Alliance',
    slug: 'savarez-500arj-corum-alliance',
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

const recentPieces = ref([
  {
    id: 1,
    title: 'Asturias (Leyenda)',
    persian_title: 'آستوریاس (افسانه) - تنظیم اختصاصی بهاور',
    slug: 'asturias-leyenda-bahavar-arrangement',
    composer: 'Isaac Albéniz',
    arranger: 'بهاور',
    genre_display: 'فلامنکو (سولئا، بولریاس، تارانتا)',
    key_signature: 'G minor / D Phrygian',
    tempo_bpm: 132,
    duration_display: '06:15',
    is_free_sheet_music: true,
    has_tutorial: true,
    play_count: 1420,
    download_count: 560,
  },
  {
    id: 2,
    title: 'Romance Anónimo',
    persian_title: 'رومانس گمنام (عشق اسپانیایی)',
    slug: 'romance-anonimo-spanish-romance',
    composer: 'Spanish Traditional',
    arranger: 'بهاور',
    genre_display: 'کلاسیک و رنسانس',
    key_signature: 'E minor / E major',
    tempo_bpm: 92,
    duration_display: '03:40',
    is_free_sheet_music: true,
    has_tutorial: false,
    play_count: 2890,
    download_count: 1120,
  },
  {
    id: 3,
    title: 'Caravan Melodies',
    persian_title: 'نوای کاروان (تنظیم آکوستیک بهاور)',
    slug: 'navaye-karevan-acoustic-arrangement',
    composer: 'مرتضی محجوبی / تنظیم بهاور',
    arranger: 'بهاور',
    genre_display: 'نواها و تنظیم‌های محلی و اصیل ایرانی',
    key_signature: 'شور / دشتی',
    tempo_bpm: 88,
    duration_display: '04:55',
    is_free_sheet_music: true,
    has_tutorial: false,
    play_count: 1950,
    download_count: 830,
  },
])

const services = ref([
  {
    id: 1,
    title: 'کلاس خصوصی گیتار کلاسیک و فلامنکو',
    slug: 'private-guitar-lesson',
    service_type: 'guitar_class',
    service_type_display: 'آموزش تخصصی گیتار',
    duration_minutes: 60,
    price: 750000,
    icon: 'Guitar',
    description: 'آموزش تک‌نفره حضوری در استودیو یا آنلاین با تمرکز بر سونوریته، ریتم‌شناسی، تکنیک‌های پیشرفته و رپرتوار جهانی.',
  },
  {
    id: 2,
    title: 'ضبط آکوستیک استودیو (وکال و سازهای زهی)',
    slug: 'studio-acoustic-recording',
    service_type: 'studio_recording',
    service_type_display: 'ضبط استودیو',
    duration_minutes: 120,
    price: 1800000,
    icon: 'Mic',
    description: 'رکورد در اتاق آکوستیک استاندارد استودیو بهاور مجهز به میکروفون‌های لامپی نویمن و پری‌امپ‌های یونیورسال آئودیو.',
  },
  {
    id: 3,
    title: 'میکس و مسترینگ تک‌آهنگ یا آلبوم',
    slug: 'mixing-mastering-services',
    service_type: 'mix_master',
    service_type_display: 'میکس و مسترینگ',
    duration_minutes: 90,
    price: 3500000,
    icon: 'Sliders',
    description: 'پالایش فرکانسی، داینامیک، استریو ایمیجینگ و مسترینگ مطابق استانداردهای روز اسپاتیفای و اپل‌موزیک.',
  },
  {
    id: 4,
    title: 'مشاوره تخصصی، استعدادیابی و خرید ساز',
    slug: 'consultation-and-assessment',
    service_type: 'consultation',
    service_type_display: 'مشاوره و تعیین سطح',
    duration_minutes: 45,
    price: 300000,
    icon: 'MessageCircle',
    description: 'جلسه تحلیل سطح نوازندگی هنرجو، ارزیابی نقاط قوت و ضعف، برنامه‌ریزی آموزشی و تست ساز پیش از خرید.',
  },
])

const latestPosts = ref([
  {
    id: 1,
    title: 'رازهای دست‌یابی به راسگوادوی روان و قدرتمند در گیتار فلامنکو',
    slug: 'secrets-of-flamenco-rasgueado',
    category_name: 'تکنیک و نوازندگی',
    author_name: 'بهاور',
    reading_time_minutes: 7,
    excerpt: 'بررسی ارگونومی دست راست، نحوه رهاسازی انگشتان و تمرینات مرحله‌ای برای دستیابی به راسگوادوی متقارن و بدون کوفتگی عضله.',
    view_count: 840,
    published_at: '۱۴۰۳/۰۸/۱۵',
  },
  {
    id: 2,
    title: 'راهنمای جامع تفاوت چوب صنوبر (Spruce) و سرو (Cedar) در صفحه رویی گیتار',
    slug: 'spruce-vs-cedar-soundboard-guide',
    category_name: 'تجهیزات، سازشناسی و آکوستیک',
    author_name: 'بهاور',
    reading_time_minutes: 6,
    excerpt: 'کدام تاپ‌وود برای سبک نوازندگی شما مناسب‌تر است؟ تحلیل رزونانس، رنگ صوتی و سرعت باز شدن صدای ساز در گذر زمان.',
    view_count: 620,
    published_at: '۱۴۰۳/۰۸/۱۰',
  },
])

useHead({
  title: 'بهاور موزیک | آکادمی گیتار، استودیو ضبط و پلتفرم تخصصی موسیقی',
})
</script>

<template>
  <div class="space-y-24 sm:space-y-32 pb-24">
    
    <!-- Hero Section -->
    <section class="relative min-h-[85vh] flex items-center justify-center overflow-hidden">
      <!-- Ambient Lighting Backdrops -->
      <div class="absolute top-1/4 -right-20 w-96 h-96 bg-amber-600/15 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute bottom-10 -left-20 w-96 h-96 bg-wood-700/20 rounded-full blur-3xl pointer-events-none"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 py-12 text-center">
        
        <!-- Persona Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-panel border border-amber-500/30 text-amber-300 text-xs sm:text-sm font-semibold mb-8 animate-fadeIn">
          <Sparkles class="w-4 h-4 text-amber-400" />
          <span>پلتفرم رسمی بهاور | آهنگساز، مدرس ارشد گیتار و مدیر استودیو</span>
        </div>

        <!-- Hero Headline -->
        <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-[1.3] max-w-4xl mx-auto mb-6">
          طنین اصالت، تکنیک و نوآوری در
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-300 to-amber-500">
            گیتار و تولید موسیقی
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="text-sm sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed mb-10">
          از فراگیری آکادمیک گیتار کلاسیک و فلامنکو تا ضبط در استودیوی مجهز آکوستیک، دسترسی رایگان به گنجینه پارتیتورها و مسترکلاس‌های تخصصی.
        </p>

        <!-- High Converting Hero CTAs -->
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
          <NuxtLink
            to="/booking"
            class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm sm:text-base shadow-xl shadow-amber-500/25 transition-all hover:scale-105 flex items-center justify-center gap-2"
          >
            <Calendar class="w-5 h-5" />
            <span>رزرو نوبت مشاوره / شروع آموزش</span>
          </NuxtLink>

          <NuxtLink
            to="/repertoire"
            class="w-full sm:w-auto px-8 py-4 rounded-2xl glass-panel hover:bg-wood-950/80 text-white font-semibold text-sm sm:text-base border border-wood-800 hover:border-amber-500/40 transition-all flex items-center justify-center gap-2"
          >
            <Play class="w-4 h-4 text-amber-400 fill-amber-400" />
            <span>شنیدن آثار و دانلود نت‌ها</span>
          </NuxtLink>
        </div>

        <!-- Quick Highlight Tags -->
        <div class="mt-12 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-400">
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            آموزش تک‌نفره و آنلاین بین‌المللی
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            ضبط با میکروفون‌های لامپی نویمن
          </span>
          <span class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
            پارتیتور و نت‌های رایگان PDF
          </span>
        </div>

      </div>
    </section>

    <!-- Studio Metrics & Counter Bar -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        
        <div class="p-6 rounded-2xl glass-panel border border-wood-900/80 flex flex-col items-center text-center space-y-2">
          <Users class="w-8 h-8 text-amber-400" />
          <div class="text-2xl sm:text-3xl font-extrabold text-white font-mono">۶۸۰+</div>
          <div class="text-xs text-slate-400">هنرجوی فارغ‌التحصیل</div>
        </div>

        <div class="p-6 rounded-2xl glass-panel border border-wood-900/80 flex flex-col items-center text-center space-y-2">
          <Mic class="w-8 h-8 text-amber-400" />
          <div class="text-2xl sm:text-3xl font-extrabold text-white font-mono">۳,۴۰۰</div>
          <div class="text-xs text-slate-400">ساعت رکورد در استودیو</div>
        </div>

        <div class="p-6 rounded-2xl glass-panel border border-wood-900/80 flex flex-col items-center text-center space-y-2">
          <Music class="w-8 h-8 text-amber-400" />
          <div class="text-2xl sm:text-3xl font-extrabold text-white font-mono">۱۲۰+</div>
          <div class="text-xs text-slate-400">قطعه و پارت نت منتشر شده</div>
        </div>

        <div class="p-6 rounded-2xl glass-panel border border-wood-900/80 flex flex-col items-center text-center space-y-2">
          <Award class="w-8 h-8 text-amber-400" />
          <div class="text-2xl sm:text-3xl font-extrabold text-white font-mono">۹۹٪</div>
          <div class="text-xs text-slate-400">رضایت هنرجویان و مراجعین</div>
        </div>

      </div>
    </section>

    <!-- Section: Repertoire & Free Sheet Music -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
        <div>
          <div class="text-xs font-semibold text-amber-400 mb-1">گنجینه قطعات و پارتیتورها</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-white">آثار، نت‌ها و تبلچرهای رسمی</h2>
        </div>
        <NuxtLink to="/repertoire" class="inline-flex items-center gap-1 text-sm font-semibold text-amber-400 hover:underline">
          <span>مشاهده تمام رپرتوار</span>
          <ChevronLeft class="w-4 h-4" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CompositionCard
          v-for="piece in recentPieces"
          :key="piece.id"
          :piece="piece"
        />
      </div>
    </section>

    <!-- Section: Studio & Booking Services -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
        <div>
          <div class="text-xs font-semibold text-amber-400 mb-1">سیستم نوبت‌دهی آنلاین</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-white">خدمات آکوستیک استودیو و کلاس‌ها</h2>
        </div>
        <NuxtLink to="/booking" class="inline-flex items-center gap-1 text-sm font-semibold text-amber-400 hover:underline">
          <span>انتخاب زمان و رزرو نوبت</span>
          <ChevronLeft class="w-4 h-4" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <ServiceCard
          v-for="service in services"
          :key="service.id"
          :service="service"
        />
      </div>
    </section>

    <!-- Section: Shop & Courses Showcase -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
        <div>
          <div class="text-xs font-semibold text-amber-400 mb-1">فروشگاه تخصصی موسیقی</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-white">سازها، اکسسوری و دوره‌های ویدئویی</h2>
        </div>
        <NuxtLink to="/shop" class="inline-flex items-center gap-1 text-sm font-semibold text-amber-400 hover:underline">
          <span>ورود به فروشگاه کامل</span>
          <ChevronLeft class="w-4 h-4" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <ProductCard
          v-for="product in featuredProducts"
          :key="product.id"
          :product="product"
        />
      </div>
    </section>

    <!-- Section: Latest Articles & Educational Blog -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
        <div>
          <div class="text-xs font-semibold text-amber-400 mb-1">آموزش و آگاهی</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-white">تازه‌ترین مقالات تکنیک و سازشناسی</h2>
        </div>
        <NuxtLink to="/blog" class="inline-flex items-center gap-1 text-sm font-semibold text-amber-400 hover:underline">
          <span>مطالعه وبلاگ</span>
          <ChevronLeft class="w-4 h-4" />
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BlogCard
          v-for="post in latestPosts"
          :key="post.id"
          :post="post"
        />
      </div>
    </section>

  </div>
</template>
