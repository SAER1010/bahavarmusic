<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Music, FileText, ArrowRight, Video, Download, ShieldCheck, Heart, Share2 } from 'lucide-vue-next'
import { useSeoSchema } from '~/composables/useSeoSchema'
import AudioPlayer from '~/components/repertoire/AudioPlayer.vue'
import GatedVideoPlayer from '~/components/repertoire/GatedVideoPlayer.vue'

const route = useRoute()
const { injectMusicCompositionSchema } = useSeoSchema()

// Demo composition details
const piece = ref({
  id: 1,
  title: 'Asturias (Leyenda)',
  persian_title: 'آستوریاس (افسانه) - تنظیم اختصاصی بهاور',
  slug: 'asturias-leyenda-bahavar-arrangement',
  composer: 'Isaac Albéniz',
  arranger: 'بهاور',
  genre: 'Flamenco / Classical',
  genre_display: 'فلامنکو (سولئا، بولریاس، تارانتا)',
  key_signature: 'G minor / D Phrygian',
  tempo_bpm: 132,
  duration_display: '06:15',
  audio_url: 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3',
  sheet_download_url: 'https://bahavarmusic.com/sheets/asturias-bahavar-tab.pdf',
  is_free_sheet_music: true,
  description: `قطعه ماندگار «آستوریاس (افسانه)» در اصل پنجمین موومان از سوئیت اسپانیایی اثر ایساک آلبنیس برای پیانو بوده که در این نسخه با تنظیم و ارکستراسیون اختصاصی بهاور برای تک‌نوازی گیتار نایلون بازآفرینی شده است.
  
در این نسخه، بخش آغازین با استفاده از ضربات شست قدرتمند و پدال نت ر ریتم‌پردازی شده و در بخش میانی (Copla) از تکنیک‌های آوازین فلامنکو و کشش‌های داینامیک بهره گرفته شده است.`,
  technical_notes: [
    'تکنیک‌های کلیدی: آلزاپوا (Alzapúa)، راسگوادوی ۳ ضربه‌ای، ترملوی کلاسیک و فلامنکو',
    'کوک ساز: استاندارد (E-A-D-G-B-E) یا Drop D برای پایداری بم در پدا‌ل‌های بیس',
    'پیش‌نیاز نوازندگی: تسلط بر پوزیسیون‌های اول تا هفتم و استقلال انگشت شست (P)',
  ],
  gated_tutorial: {
    id: 1,
    title: 'مسترکلاس ویدیویی گام‌به‌گام اجرای قطعه آستوریاس',
    description: 'تحلیل دقیق انگشت‌گذاری دست چپ و راست میزان به میزان، عبور از افت سرعت در تمپوی بالا، تنظیم داینامیک و بیان آگوگیک.',
    preview_video_url: 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3',
    accessible_stream_url: 'https://stream.bahavarmusic.com/tutorials/asturias-masterclass-full.mp4',
    accessible_download_url: 'https://dl.bahavarmusic.com/tutorials/asturias-masterclass-1080p.zip',
    duration_minutes: 55,
    price: 240000,
    has_access: false,
  },
})

// Inject Schema.org
injectMusicCompositionSchema({
  title: piece.value.title,
  persian_title: piece.value.persian_title,
  composer: piece.value.composer,
  genre: piece.value.genre_display,
  audio_stream_url: piece.value.audio_url,
  slug: piece.value.slug,
})

const onTutorialUnlocked = (updatedTutorial: any) => {
  piece.value.gated_tutorial.has_access = true
}

useHead({
  title: `${piece.value.persian_title} | نت و آموزش | بهاور موزیک`,
})
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
    
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-xs text-slate-400">
      <NuxtLink to="/" class="hover:text-amber-400">خانه</NuxtLink>
      <span>/</span>
      <NuxtLink to="/repertoire" class="hover:text-amber-400">رپرتوار</NuxtLink>
      <span>/</span>
      <span class="text-amber-300 font-medium">{{ piece.persian_title }}</span>
    </nav>

    <!-- Composition Header & Embedded Audio Player -->
    <div class="space-y-6">
      <div class="space-y-2">
        <span class="px-3 py-1 rounded-full bg-wood-950 text-amber-400 text-xs font-semibold border border-amber-500/20 inline-block">
          {{ piece.genre_display }}
        </span>
        <h1 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">
          {{ piece.persian_title }}
        </h1>
        <p class="text-sm text-slate-300">
          آهنگساز اصلی: {{ piece.composer }} • تنظیم برای گیتار و نوازنده: {{ piece.arranger }}
        </p>
      </div>

      <!-- Live Embedded Audio Player Component -->
      <AudioPlayer
        :audio-url="piece.audio_url"
        :title="piece.title"
        :persian-title="piece.persian_title"
        :composer="piece.composer"
        :slug="piece.slug"
        :sheet-download-url="piece.sheet_download_url"
        :is-free-sheet="piece.is_free_sheet_music"
      />
    </div>

    <!-- Piece Story & Technical Breakdown -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Story -->
      <div class="md:col-span-2 p-6 rounded-3xl glass-panel border border-wood-900 space-y-4">
        <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">تحلیل ساختاری و داستان قطعه</h3>
        <p class="text-xs sm:text-sm text-slate-300 leading-relaxed whitespace-pre-line">
          {{ piece.description }}
        </p>
      </div>

      <!-- Specs Sidebar -->
      <div class="p-6 rounded-3xl glass-panel border border-wood-900 space-y-4">
        <h3 class="text-base font-bold text-amber-300 border-r-2 border-amber-500 pr-2">نکات تکنیکی و اجرایی</h3>
        <ul class="space-y-2 text-xs text-slate-300">
          <li v-for="(note, idx) in piece.technical_notes" :key="idx" class="flex items-start gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0"></span>
            <span class="leading-relaxed">{{ note }}</span>
          </li>
        </ul>
      </div>

    </div>

    <!-- Gated Masterclass Video Section -->
    <div class="space-y-4">
      <div class="flex items-center gap-2">
        <Video class="w-5 h-5 text-amber-400" />
        <h2 class="text-xl sm:text-2xl font-bold text-white">مسترکلاس ویدیویی آموزشی این اثر</h2>
      </div>

      <!-- Custom Gated Video Player -->
      <GatedVideoPlayer
        :tutorial="piece.gated_tutorial"
        @unlocked="onTutorialUnlocked"
      />
    </div>

  </div>
</template>
