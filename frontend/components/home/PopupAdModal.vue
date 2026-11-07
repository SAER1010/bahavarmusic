<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { X, Sparkles, ArrowLeft } from 'lucide-vue-next'

const isOpen = ref(false)
const popupData = ref({
  title: 'ثبت‌نام ترم جدید مسترکلاس فلامنکو و آکوستیک',
  badge_text: 'ظرفیت محدود - ۳۰٪ تخفیف',
  subtitle: 'دوره جامع تکنیک‌های دست راست با استاد بهاور',
  description: 'با ثبت‌نام در این ترم، پکیج اختصاصی نت‌ها و تبلچرهای رسمی قطعات رپرتوار را نیز رایگان دریافت نمایید.',
  cta_text: 'مشاهده سرفصل‌ها و رزرو صندلی',
  cta_link: '/booking',
  cookie_dismiss_hours: 24,
  show_delay_seconds: 3,
})

const closePopup = () => {
  isOpen.value = false
  if (process.client) {
    const expireTime = Date.now() + popupData.value.cookie_dismiss_hours * 60 * 60 * 1000
    localStorage.setItem('bahavar_popup_dismissed_until', expireTime.toString())
  }
}

onMounted(() => {
  if (process.client) {
    const dismissedUntil = localStorage.getItem('bahavar_popup_dismissed_until')
    if (dismissedUntil && Date.now() < parseInt(dismissedUntil)) {
      return
    }

    setTimeout(() => {
      isOpen.value = true
    }, popupData.value.show_delay_seconds * 1000)
  }
})
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn"
    @click.self="closePopup"
  >
    <div class="relative w-full max-w-lg rounded-3xl glass-panel p-6 sm:p-8 shadow-2xl border border-amber-500/30 overflow-hidden text-right">
      
      <!-- Top Decorative Accent -->
      <div class="absolute -top-12 -right-12 w-32 h-32 bg-amber-500/20 rounded-full blur-2xl pointer-events-none"></div>

      <!-- Close Button -->
      <button
        @click="closePopup"
        class="absolute top-4 left-4 p-2 rounded-xl text-slate-400 hover:text-white hover:bg-wood-900/60 transition-colors"
      >
        <X class="w-5 h-5" />
      </button>

      <!-- Badge -->
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/30 mb-4">
        <Sparkles class="w-3.5 h-3.5 text-amber-400" />
        <span>{{ popupData.badge_text }}</span>
      </div>

      <!-- Title & Subtitle -->
      <h3 class="text-xl sm:text-2xl font-bold text-white mb-2 leading-tight">
        {{ popupData.title }}
      </h3>
      <p class="text-sm font-medium text-amber-400/90 mb-3">
        {{ popupData.subtitle }}
      </p>

      <!-- Description -->
      <p class="text-xs sm:text-sm text-slate-300 leading-relaxed mb-6">
        {{ popupData.description }}
      </p>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row items-center gap-3">
        <NuxtLink
          :to="popupData.cta_link"
          @click="closePopup"
          class="w-full sm:flex-1 py-3 px-6 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-xl shadow-amber-500/20 flex items-center justify-center gap-2 transition-transform hover:scale-[1.02]"
        >
          <span>{{ popupData.cta_text }}</span>
          <ArrowLeft class="w-4 h-4" />
        </NuxtLink>

        <button
          @click="closePopup"
          class="w-full sm:w-auto py-3 px-4 text-xs font-medium text-slate-400 hover:text-white"
        >
          بعداً یادآوری کن
        </button>
      </div>

    </div>
  </div>
</template>
