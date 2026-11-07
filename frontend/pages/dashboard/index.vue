<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  User, 
  Calendar, 
  ShoppingBag, 
  Video, 
  FileText, 
  LogOut, 
  Clock, 
  CheckCircle2, 
  Download, 
  Play, 
  ShieldCheck,
  Award
} from 'lucide-vue-next'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const activeTab = ref<'bookings' | 'courses' | 'orders' | 'sheets' | 'profile'>('bookings')

// Demo data for student
const userBookings = ref([
  {
    id: 1,
    booking_code: 'BK-7A9F21',
    service_title: 'کلاس خصوصی گیتار کلاسیک و فلامنکو',
    date: '۱۴۰۳/۰۸/۲۲',
    time: '۱۶:۰۰ تا ۱۷:۰۰',
    status: 'confirmed',
    status_display: 'تایید شده و قطعی',
    location: 'استودیو نگار، اتاق آکوستیک ۲',
  },
  {
    id: 2,
    booking_code: 'BK-3B109C',
    service_title: 'ضبط آکوستیک استودیو (وکال و ساز)',
    date: '۱۴۰۳/۰۸/۳۰',
    time: '۱۸:۰۰ تا ۲۰:۰۰',
    status: 'pending',
    status_display: 'در انتظار پرداخت بیعانه',
    location: 'استودیو اصلی',
  },
])

const purchasedCourses = ref([
  {
    id: 1,
    title: 'مسترکلاس ویدیویی گام‌به‌گام اجرای قطعه آستوریاس',
    duration: '۵۵ دقیقه',
    progress: '۸۰٪ تکمیل شده',
    slug: 'asturias-leyenda-bahavar-arrangement',
    download_link: 'https://dl.bahavarmusic.com/tutorials/asturias-masterclass-1080p.zip',
  },
  {
    id: 2,
    title: 'دوره جامع ویدئویی تکنیک‌های دست راست در گیتار فلامنکو',
    duration: '۱۲ ساعت',
    progress: '۳۵٪ تکمیل شده',
    slug: 'masterclass-right-hand-flamenco-acoustic',
    download_link: 'https://dl.bahavarmusic.com/tutorials/right-hand-technique-hd.zip',
  },
])

const userOrders = ref([
  {
    id: 1,
    order_number: 'BHV-984210',
    total_amount: 1650000,
    status_display: 'ارسال شده با پست پیشتاز',
    tracking_code: '28491028391823901239',
    date: '۱۴۰۳/۰۸/۰۵',
    items: ['سیم گیتار ساوارز مدل 500ARJ Corum Alliance'],
  },
])

const savedSheets = ref([
  {
    id: 1,
    title: 'پارتیتور و تبلچر آستوریاس (تنظیم بهاور)',
    file_type: 'PDF - ۱۲ صفحه',
    download_url: 'https://bahavarmusic.com/sheets/asturias-bahavar-tab.pdf',
  },
  {
    id: 2,
    title: 'نت و آکوردهای قطعه رومانس گمنام (عشق اسپانیایی)',
    file_type: 'PDF - ۴ صفحه',
    download_url: 'https://bahavarmusic.com/sheets/romance-anonimo-tab.pdf',
  },
])

onMounted(() => {
  authStore.initAuth()
})

useHead({
  title: 'پرتال هنرجویان و میز کار کاربری | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    
    <!-- User Header Card -->
    <div class="p-6 sm:p-8 rounded-3xl glass-panel border border-amber-500/20 flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center text-black font-extrabold text-2xl shadow-xl shadow-amber-900/40">
          {{ authStore.user?.first_name ? authStore.user.first_name[0] : 'هـ' }}
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl sm:text-2xl font-extrabold text-white">
              {{ authStore.user?.full_name || 'هنرجوی آکادمی بهاور' }}
            </h1>
            <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold border border-emerald-500/30">
              هنرجوی فعال
            </span>
          </div>
          <p class="text-xs text-slate-400 font-mono mt-1">
            شماره موبایل: {{ authStore.user?.phone_number || '09121234567' }}
          </p>
        </div>
      </div>

      <!-- Quick Action / Logout -->
      <div class="flex items-center gap-3">
        <NuxtLink
          to="/booking"
          class="px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs shadow-md shadow-amber-500/20 transition-all"
        >
          رزرو جلسه جدید
        </NuxtLink>
        <button
          @click="authStore.logout()"
          class="p-2.5 rounded-xl bg-studio-dark text-slate-400 hover:text-red-400 border border-wood-900 hover:border-red-500/30 transition-colors"
          title="خروج از حساب"
        >
          <LogOut class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2 border-b border-wood-900">
      <button
        @click="activeTab = 'bookings'"
        class="px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2"
        :class="activeTab === 'bookings' ? 'bg-amber-500 text-black shadow-md' : 'text-slate-400 hover:text-white'"
      >
        <Calendar class="w-4 h-4" />
        <span>نوبت‌های رزرو شده ({{ userBookings.length }})</span>
      </button>

      <button
        @click="activeTab = 'courses'"
        class="px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2"
        :class="activeTab === 'courses' ? 'bg-amber-500 text-black shadow-md' : 'text-slate-400 hover:text-white'"
      >
        <Video class="w-4 h-4" />
        <span>دوره‌ها و مسترکلاس‌ها ({{ purchasedCourses.length }})</span>
      </button>

      <button
        @click="activeTab = 'orders'"
        class="px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2"
        :class="activeTab === 'orders' ? 'bg-amber-500 text-black shadow-md' : 'text-slate-400 hover:text-white'"
      >
        <ShoppingBag class="w-4 h-4" />
        <span>سفارشات خرید ({{ userOrders.length }})</span>
      </button>

      <button
        @click="activeTab = 'sheets'"
        class="px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2"
        :class="activeTab === 'sheets' ? 'bg-amber-500 text-black shadow-md' : 'text-slate-400 hover:text-white'"
      >
        <FileText class="w-4 h-4" />
        <span>نت‌های من ({{ savedSheets.length }})</span>
      </button>

      <button
        @click="activeTab = 'profile'"
        class="px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-2"
        :class="activeTab === 'profile' ? 'bg-amber-500 text-black shadow-md' : 'text-slate-400 hover:text-white'"
      >
        <User class="w-4 h-4" />
        <span>پروفایل و سطح نوازندگی</span>
      </button>
    </div>

    <!-- Tab 1: Bookings -->
    <div v-if="activeTab === 'bookings'" class="space-y-4">
      <div
        v-for="b in userBookings"
        :key="b.id"
        class="p-5 sm:p-6 rounded-2xl glass-panel border border-wood-900/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div class="space-y-1">
          <div class="flex items-center gap-2">
            <span class="text-xs font-mono font-bold text-amber-400">{{ b.booking_code }}</span>
            <span
              class="px-2 py-0.5 rounded-md text-[10px] font-bold"
              :class="b.status === 'confirmed' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'"
            >
              {{ b.status_display }}
            </span>
          </div>
          <h4 class="text-base font-bold text-white">{{ b.service_title }}</h4>
          <p class="text-xs text-slate-400">{{ b.location }}</p>
        </div>

        <div class="text-left sm:text-right font-mono text-xs text-slate-300">
          <div>تاریخ: {{ b.date }}</div>
          <div class="text-amber-400 font-bold">{{ b.time }}</div>
        </div>
      </div>
    </div>

    <!-- Tab 2: Courses -->
    <div v-else-if="activeTab === 'courses'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="c in purchasedCourses"
        :key="c.id"
        class="p-5 rounded-2xl glass-panel border border-wood-900/80 space-y-4"
      >
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-emerald-400">دسترسی مادام‌العمر</span>
          <span class="text-xs text-slate-400 font-mono">{{ c.duration }}</span>
        </div>
        <h4 class="text-sm font-bold text-white">{{ c.title }}</h4>

        <div class="pt-3 border-t border-wood-900 flex items-center justify-between gap-3">
          <NuxtLink
            :to="`/repertoire/${c.slug}`"
            class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black text-xs font-bold flex items-center gap-1.5"
          >
            <Play class="w-3.5 h-3.5 fill-black" />
            <span>مشاهده و پخش آنلاین</span>
          </NuxtLink>

          <a
            :href="c.download_link"
            class="p-2 rounded-xl bg-wood-900 text-amber-300 hover:text-white"
            title="دانلود فایل ویدیو"
          >
            <Download class="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>

    <!-- Tab 3: Orders -->
    <div v-else-if="activeTab === 'orders'" class="space-y-4">
      <div
        v-for="o in userOrders"
        :key="o.id"
        class="p-5 rounded-2xl glass-panel border border-wood-900/80 space-y-3"
      >
        <div class="flex items-center justify-between text-xs">
          <span class="font-mono font-bold text-amber-400">{{ o.order_number }}</span>
          <span class="text-emerald-400 font-medium">{{ o.status_display }}</span>
        </div>
        <div class="text-sm font-bold text-white">{{ o.items.join('، ') }}</div>
        <div class="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-wood-900">
          <span>کد رهگیری پست: <span class="font-mono text-slate-200">{{ o.tracking_code }}</span></span>
          <span class="font-mono text-amber-400 font-bold">{{ o.total_amount.toLocaleString('fa-IR') }} تومان</span>
        </div>
      </div>
    </div>

    <!-- Tab 4: Sheets -->
    <div v-else-if="activeTab === 'sheets'" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div
        v-for="s in savedSheets"
        :key="s.id"
        class="p-4 rounded-2xl glass-panel border border-wood-900/80 flex items-center justify-between"
      >
        <div>
          <h4 class="text-xs font-bold text-white mb-1">{{ s.title }}</h4>
          <span class="text-[11px] text-slate-400 font-mono">{{ s.file_type }}</span>
        </div>
        <a
          :href="s.download_url"
          target="_blank"
          class="p-2.5 rounded-xl bg-wood-900 hover:bg-wood-800 text-amber-400 hover:text-amber-300"
          title="دانلود مجدد نت"
        >
          <Download class="w-4 h-4" />
        </a>
      </div>
    </div>

    <!-- Tab 5: Profile & Instrument Level -->
    <div v-else-if="activeTab === 'profile'" class="max-w-xl p-6 rounded-3xl glass-panel border border-wood-900 space-y-4">
      <h3 class="text-base font-bold text-white border-r-2 border-amber-500 pr-2">شناسنامه هنرجویی در آکادمی</h3>
      
      <div class="space-y-3 text-xs text-slate-300">
        <div class="flex justify-between py-2 border-b border-wood-900">
          <span class="text-slate-400">ساز تخصصی:</span>
          <span class="font-bold text-white">گیتار فلامنکو و کلاسیک</span>
        </div>
        <div class="flex justify-between py-2 border-b border-wood-900">
          <span class="text-slate-400">سطح نوازندگی فعلی:</span>
          <span class="text-amber-400 font-bold">پیشرفته (بداهه‌نوازی و کمپاس‌شناسی)</span>
        </div>
        <div class="flex justify-between py-2 border-b border-wood-900">
          <span class="text-slate-400">تعداد جلسات گذرانده شده با بهاور:</span>
          <span class="font-mono text-white font-bold">۱۴ جلسه</span>
        </div>
      </div>
    </div>

  </div>
</template>
