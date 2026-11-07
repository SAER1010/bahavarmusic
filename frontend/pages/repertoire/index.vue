<script setup lang="ts">
import { ref, computed } from 'vue'
import { Music, Search, Filter } from 'lucide-vue-next'
import CompositionCard from '~/components/repertoire/CompositionCard.vue'

const searchQuery = ref('')
const selectedGenre = ref('all')

const genres = [
  { id: 'all', name: 'همه سبک‌ها' },
  { id: 'flamenco', name: 'فلامنکو' },
  { id: 'classical', name: 'کلاسیک' },
  { id: 'folk_persian', name: 'نواهای اصیل ایرانی' },
  { id: 'acoustic_fusion', name: 'فیوژن و آکوستیک' },
]

const pieces = ref([
  {
    id: 1,
    title: 'Asturias (Leyenda)',
    persian_title: 'آستوریاس (افسانه) - تنظیم اختصاصی بهاور',
    slug: 'asturias-leyenda-bahavar-arrangement',
    genre_key: 'flamenco',
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
    genre_key: 'classical',
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
    genre_key: 'folk_persian',
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

const filteredPieces = computed(() => {
  return pieces.value.filter((p) => {
    const matchesGenre = selectedGenre.value === 'all' || p.genre_key === selectedGenre.value
    const matchesSearch = !searchQuery.value || 
      p.persian_title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      p.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesGenre && matchesSearch
  })
})

useHead({
  title: 'آرشیو آثار، قطعات و نت‌های رایگان گیتار | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
    
    <!-- Header -->
    <div class="border-b border-wood-900 pb-8 space-y-2">
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white">رپرتوار، قطعات و دانلود رایگان نت‌ها</h1>
      <p class="text-sm text-slate-400">آثار اجرایی و تنظیمی بهاور همراه با پخش صوتی، پارتیتور PDF، تبلچر استاندارد و مسترکلاس‌های ویدیویی</p>
    </div>

    <!-- Toolbar -->
    <div class="flex flex-col sm:flex-row items-center gap-4">
      <div class="relative flex-1 w-full">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجوی قطعه، آهنگساز یا دستگاه..."
          class="w-full px-4 py-3 pl-10 rounded-xl bg-studio-card border border-wood-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500"
        />
        <Search class="w-4 h-4 text-slate-400 absolute top-3.5 left-3.5" />
      </div>

      <div class="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
        <button
          v-for="g in genres"
          :key="g.id"
          @click="selectedGenre = g.id"
          class="px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border"
          :class="selectedGenre === g.id ? 'bg-amber-500 text-black border-amber-500 shadow-md shadow-amber-500/20' : 'bg-studio-card text-slate-300 border-wood-900 hover:border-amber-500/40'"
        >
          {{ g.name }}
        </button>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="filteredPieces.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CompositionCard
        v-for="piece in filteredPieces"
        :key="piece.id"
        :piece="piece"
      />
    </div>

    <div v-else class="text-center py-20 rounded-3xl glass-panel p-8">
      <p class="text-slate-400 text-sm">قطعه‌ای با مشخصات مورد نظر شما یافت نشد.</p>
    </div>

  </div>
</template>
