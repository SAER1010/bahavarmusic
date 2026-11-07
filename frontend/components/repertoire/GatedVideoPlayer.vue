<script setup lang="ts">
import { ref } from 'vue'
import { Lock, Unlock, Play, Download, CheckCircle, Video, ShieldAlert } from 'lucide-vue-next'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'

const props = defineProps<{
  tutorial: {
    id: number
    title: string
    description: string
    preview_video_url: string
    duration_minutes: number
    price: number
    has_access: boolean
    accessible_stream_url?: string
    accessible_download_url?: string
  }
}>()

const emit = defineEmits(['unlocked'])

const authStore = useAuthStore()
const { apiFetch } = useApi()

const isUnlocking = ref(false)
const unlockSuccess = ref(false)

const handleUnlock = async () => {
  if (!authStore.isAuthenticated) {
    authStore.openAuthModal('otp')
    return
  }

  isUnlocking.value = true
  try {
    const res = await apiFetch(`/repertoire/tutorials/${props.tutorial.id}/unlock/`, {
      method: 'POST',
    })
    unlockSuccess.value = true
    emit('unlocked', res.tutorial)
  } catch (err) {
    console.error('Failed to unlock tutorial', err)
  } finally {
    isUnlocking.value = false
  }
}
</script>

<template>
  <div class="rounded-3xl glass-panel p-6 sm:p-8 border border-amber-500/30 overflow-hidden shadow-2xl space-y-6">
    
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-wood-900 pb-5">
      <div>
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold mb-2"
          :class="tutorial.has_access || unlockSuccess ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'"
        >
          <Unlock v-if="tutorial.has_access || unlockSuccess" class="w-3.5 h-3.5 text-emerald-400" />
          <Lock v-else class="w-3.5 h-3.5 text-amber-400" />
          <span>{{ tutorial.has_access || unlockSuccess ? 'دسترسی فعال است (دانشجوی مسترکلاس)' : 'محتوای آموزشی اختصاصی (Gated Masterclass)' }}</span>
        </div>
        <h3 class="text-xl sm:text-2xl font-bold text-white">{{ tutorial.title }}</h3>
      </div>

      <div class="text-left sm:text-right font-mono text-sm text-slate-400">
        مدت آموزش: {{ tutorial.duration_minutes }} دقیقه
      </div>
    </div>

    <!-- State 1: Authorized Video Player -->
    <div v-if="tutorial.has_access || unlockSuccess" class="space-y-4">
      <div class="relative aspect-video rounded-2xl overflow-hidden bg-black border border-emerald-500/40 shadow-2xl">
        <video
          controls
          controlslist="nodownload"
          class="w-full h-full object-cover"
          poster="/images/video-poster.jpg"
        >
          <source :src="tutorial.accessible_stream_url || tutorial.preview_video_url" type="video/mp4" />
          مرورگر شما از پخش مستقیم ویدیو پشتیبانی نمی‌کند.
        </video>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-wood-950/80 border border-emerald-500/30">
        <div class="flex items-center gap-2 text-emerald-300 text-sm">
          <CheckCircle class="w-5 h-5 text-emerald-400" />
          <span>دسترسی شما نامحدود است. می‌توانید ویدیو را مستقیماً دانلود فرمایید.</span>
        </div>

        <a
          v-if="tutorial.accessible_download_url"
          :href="tutorial.accessible_download_url"
          target="_blank"
          download
          class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-emerald-900/30 transition-transform hover:scale-105"
        >
          <Download class="w-4 h-4" />
          <span>دانلود فایل ویدیویی 1080p Full HD</span>
        </a>
      </div>
    </div>

    <!-- State 2: Locked / Gated State -->
    <div v-else class="space-y-6">
      <div class="relative aspect-video rounded-2xl overflow-hidden bg-studio-dark border border-wood-800 flex flex-col items-center justify-center p-6 text-center group">
        <!-- Background Mock Player Backdrop -->
        <div class="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-transparent"></div>
        <div class="relative z-10 space-y-4 max-w-md">
          <div class="w-16 h-16 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center mx-auto text-amber-400 shadow-xl">
            <Lock class="w-8 h-8" />
          </div>
          <h4 class="text-lg font-bold text-white">این مسترکلاس نیازمند دسترسی هنرجویی است</h4>
          <p class="text-xs text-slate-300 leading-relaxed">
            جهت مشاهده ویدیوهای تفصیلی میزان‌به‌میزان، تکنیک‌های سرعتی و آرشیو تمرینات عملی بهاور، دسترسی خود را فعال کنید.
          </p>
          <div class="text-amber-400 font-bold text-lg">
            هزینه دوره: {{ tutorial.price.toLocaleString('fa-IR') }} تومان
          </div>
          <button
            @click="handleUnlock"
            :disabled="isUnlocking"
            class="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-xl shadow-amber-500/30 transition-transform hover:scale-105 flex items-center justify-center gap-2 mx-auto"
          >
            <Unlock class="w-4 h-4" />
            <span v-if="isUnlocking">در حال اتصال به درگاه و فعال‌سازی...</span>
            <span v-else>خرید آنلاین و دسترسی فوری</span>
          </button>
        </div>
      </div>

      <!-- Syllabus / Description -->
      <div class="p-4 rounded-xl bg-wood-950/40 border border-wood-900 text-sm text-slate-300 leading-relaxed">
        <h5 class="font-bold text-amber-300 mb-2">سرفصل‌های این مسترکلاس:</h5>
        <p>{{ tutorial.description }}</p>
      </div>
    </div>

  </div>
</template>
