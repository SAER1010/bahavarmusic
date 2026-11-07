<script setup lang="ts">
import { Music, Play, FileText, Video, Headphones } from 'lucide-vue-next'

defineProps<{
  piece: {
    id: number
    title: string
    persian_title: string
    slug: string
    composer: string
    arranger: string
    genre_display: string
    key_signature: string
    tempo_bpm: number
    duration_display: string
    is_free_sheet_music: boolean
    has_tutorial: boolean
    play_count: number
    download_count: number
  }
}>()
</script>

<template>
  <div class="group relative rounded-2xl glass-panel border border-wood-900/80 hover:border-amber-500/40 p-5 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-950/20 flex flex-col justify-between space-y-4">
    
    <!-- Top Header -->
    <div class="flex items-start justify-between gap-3">
      <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-600/30 to-wood-950 border border-amber-500/20 flex items-center justify-center text-amber-400 shrink-0 group-hover:scale-105 transition-transform">
        <Music class="w-6 h-6 stroke-[2]" />
      </div>

      <div class="flex flex-wrap items-center gap-1.5">
        <span class="px-2 py-0.5 rounded-md bg-wood-900/80 text-amber-300 text-[10px] font-medium border border-amber-500/20">
          {{ piece.genre_display }}
        </span>
        <span v-if="piece.has_tutorial" class="px-2 py-0.5 rounded-md bg-emerald-950/80 text-emerald-300 text-[10px] font-medium border border-emerald-500/30 flex items-center gap-1">
          <Video class="w-3 h-3" />
          <span>مسترکلاس ویدیویی</span>
        </span>
      </div>
    </div>

    <!-- Title & Specs -->
    <div>
      <NuxtLink :to="`/repertoire/${piece.slug}`">
        <h3 class="text-base font-bold text-white group-hover:text-amber-400 transition-colors mb-1">
          {{ piece.persian_title }}
        </h3>
      </NuxtLink>
      <p class="text-xs text-amber-200/70 mb-3">{{ piece.title }} • {{ piece.composer }}</p>

      <div class="flex items-center gap-4 text-[11px] text-slate-400 font-mono">
        <span>گام: {{ piece.key_signature }}</span>
        <span>تمپو: {{ piece.tempo_bpm }} BPM</span>
        <span>طول: {{ piece.duration_display }}</span>
      </div>
    </div>

    <!-- Actions & Stats -->
    <div class="pt-3 border-t border-wood-900/60 flex items-center justify-between text-xs">
      <div class="flex items-center gap-3 text-slate-400 text-[11px]">
        <span class="flex items-center gap-1">
          <Headphones class="w-3.5 h-3.5 text-amber-500" />
          {{ piece.play_count.toLocaleString('fa-IR') }}
        </span>
        <span class="flex items-center gap-1">
          <FileText class="w-3.5 h-3.5 text-amber-500" />
          {{ piece.download_count.toLocaleString('fa-IR') }} دانلود
        </span>
      </div>

      <NuxtLink
        :to="`/repertoire/${piece.slug}`"
        class="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs transition-colors"
      >
        <Play class="w-3.5 h-3.5 fill-black mr-0.5" />
        <span>شنیدن و نت</span>
      </NuxtLink>
    </div>

  </div>
</template>
