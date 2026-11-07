<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  Calendar, 
  Clock, 
  CheckCircle2, 
  ArrowLeft, 
  ArrowRight, 
  Guitar, 
  Mic, 
  Sliders, 
  MessageCircle, 
  User, 
  Phone, 
  Mail, 
  FileText 
} from 'lucide-vue-next'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const route = useRoute()
const authStore = useAuthStore()
const { apiFetch } = useApi()

const step = ref(1)

const services = [
  {
    id: 1,
    title: 'کلاس خصوصی گیتار کلاسیک و فلامنکو',
    slug: 'private-guitar-lesson',
    service_type_display: 'آموزش تخصصی تک‌نفره',
    duration_minutes: 60,
    price: 750000,
    icon: 'Guitar',
    description: 'آموزش تک‌نفره حضوری در استودیو یا آنلاین با تمرکز بر سونوریته، ریتم‌شناسی، تکنیک‌های پیشرفته و رپرتوار جهانی.',
  },
  {
    id: 2,
    title: 'ضبط آکوستیک استودیو (وکال و سازهای زهی)',
    slug: 'studio-acoustic-recording',
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
    service_type_display: 'مشاوره و تعیین سطح',
    duration_minutes: 45,
    price: 300000,
    icon: 'MessageCircle',
    description: 'جلسه تحلیل سطح نوازندگی هنرجو، ارزیابی نقاط قوت و ضعف، برنامه‌ریزی آموزشی و تست ساز پیش از خرید.',
  },
]

// State
const selectedServiceId = ref(1)
const selectedDate = ref('')
const selectedSlot = ref('')
const clientName = ref('')
const clientPhone = ref('')
const clientEmail = ref('')
const notes = ref('')

const isSubmitting = ref(false)
const bookingResult = ref<any>(null)

// Generated next 5 days
const availableDates = computed(() => {
  const dates = []
  const today = new Date()
  for (let i = 1; i <= 6; i++) {
    const d = new Date()
    d.setDate(today.getDate() + i)
    const yyyy = d.getFullYear()
    const mm = String(d.getMonth() + 1).padStart(2, '0')
    const dd = String(d.getDate()).padStart(2, '0')
    const iso = `${yyyy}-${mm}-${dd}`
    const label = d.toLocaleDateString('fa-IR', { weekday: 'long', day: 'numeric', month: 'long' })
    dates.push({ iso, label })
  }
  return dates
})

const availableSlots = [
  '14:00 تا 15:00',
  '16:00 تا 17:00',
  '18:00 تا 19:00',
  '20:00 تا 21:00',
]

const selectedService = computed(() => {
  return services.find(s => s.id === selectedServiceId.value) || services[0]
})

onMounted(() => {
  if (route.query.service) {
    selectedServiceId.value = parseInt(route.query.service as string)
    step.value = 2
  }
  if (availableDates.value.length > 0) {
    selectedDate.value = availableDates.value[0].iso
  }
  if (authStore.user) {
    clientName.value = authStore.user.full_name || authStore.user.first_name || ''
    clientPhone.value = authStore.user.phone_number || ''
    clientEmail.value = authStore.user.email || ''
  }
})

const handleCompleteBooking = async () => {
  isSubmitting.value = true
  const bookingCode = `BK-${Math.random().toString(36).substring(2, 8).toUpperCase()}`
  
  // Simulated booking creation
  setTimeout(() => {
    bookingResult.value = {
      booking_code: bookingCode,
      service_title: selectedService.value.title,
      date: selectedDate.value,
      slot: selectedSlot.value || '16:00 تا 17:00',
      client_name: clientName.value,
      client_phone: clientPhone.value,
      total_fee: selectedService.value.price,
    }
    isSubmitting.value = false
    step.value = 5 // confirmation step
  }, 800)
}

useHead({
  title: 'سیستم رزرواسیون نوبت و استودیو | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
    
    <!-- Title & Multi-step Indicator -->
    <div class="text-center space-y-3">
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white">سیستم رزرواسیون آنلاین نوبت و استودیو</h1>
      <p class="text-xs sm:text-sm text-slate-400">کلاس‌های آموزشی خصوصی، رکورد استودیویی، میکس و مسترینگ و جلسات مشاوره</p>
      
      <!-- Stepper Indicator -->
      <div class="pt-6 flex items-center justify-center gap-2 sm:gap-4 max-w-xl mx-auto">
        <div
          v-for="s in 4"
          :key="s"
          class="flex items-center gap-2"
        >
          <div
            class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all"
            :class="[
              step === s ? 'bg-amber-500 text-black ring-4 ring-amber-500/20' : 
              step > s ? 'bg-emerald-600 text-white' : 'bg-wood-950 text-slate-500 border border-wood-800'
            ]"
          >
            <CheckCircle2 v-if="step > s" class="w-4 h-4" />
            <span v-else>{{ s }}</span>
          </div>
          <div v-if="s < 4" class="w-6 sm:w-12 h-0.5 bg-wood-900" :class="{ '!bg-emerald-500': step > s }"></div>
        </div>
      </div>
    </div>

    <!-- Step 1: Service Selection -->
    <div v-if="step === 1" class="space-y-6">
      <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">گام ۱: انتخاب خدمت یا کلاس</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="s in services"
          :key="s.id"
          @click="selectedServiceId = s.id; step = 2"
          class="p-5 rounded-2xl glass-panel border cursor-pointer transition-all duration-200 hover:scale-[1.01]"
          :class="selectedServiceId === s.id ? 'border-amber-500 bg-amber-500/10 shadow-lg shadow-amber-500/10' : 'border-wood-900 hover:border-amber-500/40'"
        >
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-bold text-amber-400">{{ s.service_type_display }}</span>
            <span class="text-xs text-slate-400 font-mono">{{ s.duration_minutes }} دقیقه</span>
          </div>
          <h4 class="text-base font-bold text-white mb-2">{{ s.title }}</h4>
          <p class="text-xs text-slate-300 leading-relaxed mb-4">{{ s.description }}</p>
          <div class="flex items-center justify-between pt-3 border-t border-wood-900/60">
            <span class="text-xs text-slate-400">هزینه هر جلسه:</span>
            <span class="text-sm font-bold text-amber-400 font-mono">{{ s.price.toLocaleString('fa-IR') }} تومان</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 2: Date & Slot Selection -->
    <div v-else-if="step === 2" class="space-y-6">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">گام ۲: تاریخ و سانس زمانی</h3>
        <button @click="step = 1" class="text-xs text-amber-400 hover:underline">تغییر خدمت ({{ selectedService.title }})</button>
      </div>

      <!-- Dates -->
      <div>
        <label class="block text-xs font-medium text-slate-300 mb-2">روزهای در دسترس:</label>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <button
            v-for="d in availableDates"
            :key="d.iso"
            @click="selectedDate = d.iso"
            class="p-3 rounded-xl border text-xs font-medium transition-all"
            :class="selectedDate === d.iso ? 'bg-amber-500 text-black font-bold border-amber-500 shadow-md' : 'bg-studio-card text-slate-300 border-wood-900 hover:border-amber-500/40'"
          >
            {{ d.label }}
          </button>
        </div>
      </div>

      <!-- Slots -->
      <div>
        <label class="block text-xs font-medium text-slate-300 mb-2">سانس‌های خالی در استودیو:</label>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button
            v-for="slot in availableSlots"
            :key="slot"
            @click="selectedSlot = slot"
            class="p-3 rounded-xl border text-xs font-mono transition-all"
            :class="selectedSlot === slot ? 'bg-amber-500 text-black font-bold border-amber-500 shadow-md' : 'bg-studio-card text-slate-300 border-wood-900 hover:border-amber-500/40'"
          >
            {{ slot }}
          </button>
        </div>
      </div>

      <div class="flex items-center justify-between pt-6">
        <button @click="step = 1" class="px-5 py-2.5 rounded-xl text-slate-400 hover:text-white text-xs">
          مرحله قبل
        </button>
        <button
          @click="step = 3"
          :disabled="!selectedDate || !selectedSlot"
          class="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs disabled:opacity-50 transition-all"
        >
          ادامه و ثبت توضیحات
        </button>
      </div>
    </div>

    <!-- Step 3: Project Notes -->
    <div v-else-if="step === 3" class="space-y-6">
      <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">گام ۳: اهداف جلسه و نیازمندی‌ها</h3>
      
      <div>
        <label class="block text-xs font-medium text-slate-300 mb-2">توضیحات و نیازمندی‌های پروژه یا کلاس (اختیاری):</label>
        <textarea
          v-model="notes"
          rows="5"
          placeholder="مثال: قطعه مورد نظر برای ضبط، سبک نوازندگی، سطح فعلی در گیتار یا تمپوی آهنگ..."
          class="w-full p-4 rounded-xl bg-studio-card border border-wood-800 text-white placeholder-slate-500 text-xs focus:outline-none focus:border-amber-500 leading-relaxed"
        ></textarea>
      </div>

      <div class="flex items-center justify-between pt-4">
        <button @click="step = 2" class="px-5 py-2.5 rounded-xl text-slate-400 hover:text-white text-xs">
          مرحله قبل
        </button>
        <button
          @click="step = 4"
          class="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs transition-all"
        >
          مرحله بعد (مشخصات متقاضی)
        </button>
      </div>
    </div>

    <!-- Step 4: Contact & Confirmation -->
    <div v-else-if="step === 4" class="space-y-6">
      <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">گام ۴: اطلاعات تماس و نهایی‌سازی رزرو</h3>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">نام و نام خانوادگی</label>
          <input
            v-model="clientName"
            type="text"
            placeholder="مثال: سهراب حسینی"
            class="w-full px-4 py-2.5 rounded-xl bg-studio-card border border-wood-800 text-white text-xs focus:outline-none focus:border-amber-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">شماره موبایل جهت ارسال پیامک تایید</label>
          <input
            v-model="clientPhone"
            type="tel"
            dir="ltr"
            placeholder="09121234567"
            class="w-full px-4 py-2.5 rounded-xl bg-studio-card border border-wood-800 text-white font-mono text-xs focus:outline-none focus:border-amber-500"
          />
        </div>
      </div>

      <!-- Booking Summary Box -->
      <div class="p-5 rounded-2xl bg-wood-950/80 border border-amber-500/30 space-y-3 text-xs text-slate-300">
        <h4 class="font-bold text-amber-300 text-sm">خلاصه رزرو نوبت شما:</h4>
        <div class="flex justify-between">
          <span>سرویس:</span>
          <span class="font-bold text-white">{{ selectedService.title }}</span>
        </div>
        <div class="flex justify-between">
          <span>تاریخ و زمان:</span>
          <span class="font-mono text-amber-400">{{ selectedDate }} ({{ selectedSlot }})</span>
        </div>
        <div class="flex justify-between">
          <span>هزینه نهایی:</span>
          <span class="font-mono font-bold text-amber-400">{{ selectedService.price.toLocaleString('fa-IR') }} تومان</span>
        </div>
      </div>

      <div class="flex items-center justify-between pt-4">
        <button @click="step = 3" class="px-5 py-2.5 rounded-xl text-slate-400 hover:text-white text-xs">
          مرحله قبل
        </button>
        <button
          @click="handleCompleteBooking"
          :disabled="isSubmitting || !clientName || !clientPhone"
          class="px-8 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-xs shadow-xl shadow-amber-500/20 disabled:opacity-50 transition-all flex items-center gap-2"
        >
          <span v-if="isSubmitting">در حال ثبت نوبت در تقویم استودیو...</span>
          <span v-else>ثبت قطعی نوبت و تایید</span>
        </button>
      </div>
    </div>

    <!-- Step 5: Success Confirmation -->
    <div v-else-if="step === 5" class="p-8 sm:p-12 rounded-3xl glass-panel border border-emerald-500/40 text-center space-y-6 shadow-2xl">
      <div class="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center mx-auto text-emerald-400">
        <CheckCircle2 class="w-8 h-8" />
      </div>

      <div>
        <h2 class="text-2xl font-extrabold text-white mb-2">نوبت شما با موفقیت رزرو گردید</h2>
        <p class="text-xs sm:text-sm text-slate-300">
          پیامک تایید حاوی لوکیشن دقیق استودیو و کد نوبت به شماره شما ارسال شد.
        </p>
      </div>

      <div class="max-w-md mx-auto p-4 rounded-2xl bg-studio-dark border border-wood-900 text-xs space-y-2 text-slate-300">
        <div class="flex justify-between">
          <span>کد رهگیری نوبت:</span>
          <span class="font-mono font-bold text-amber-400">{{ bookingResult?.booking_code }}</span>
        </div>
        <div class="flex justify-between">
          <span>خدمت رزرو شده:</span>
          <span class="text-white">{{ bookingResult?.service_title }}</span>
        </div>
        <div class="flex justify-between">
          <span>زمان برگزاری:</span>
          <span class="font-mono text-white">{{ bookingResult?.date }} - {{ bookingResult?.slot }}</span>
        </div>
      </div>

      <div class="flex justify-center gap-3 pt-2">
        <NuxtLink
          to="/dashboard"
          class="px-6 py-2.5 rounded-xl bg-amber-500 text-black font-bold text-xs shadow-lg shadow-amber-500/20"
        >
          مشاهده در پرتال من
        </NuxtLink>
        <NuxtLink
          to="/"
          class="px-6 py-2.5 rounded-xl bg-wood-900 text-slate-300 text-xs font-semibold"
        >
          بازگشت به صفحه اصلی
        </NuxtLink>
      </div>
    </div>

  </div>
</template>
