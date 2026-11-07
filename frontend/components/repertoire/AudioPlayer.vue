<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Play, Pause, Volume2, VolumeX, Download, FileText, Music } from 'lucide-vue-next'
import { useApi } from '~/composables/useApi'

const props = defineProps<{
  audioUrl: string
  title: string
  persianTitle: string
  composer: string
  slug: string
  sheetDownloadUrl?: string
  isFreeSheet?: boolean
}>()

const { apiFetch } = useApi()

const audio = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(0.85)
const isMuted = ref(false)

const formatTime = (secs: number) => {
  if (isNaN(secs)) return '00:00'
  const m = Math.floor(secs / 60)
  const s = Math.floor(secs % 60)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

const togglePlay = () => {
  if (!audio.value) return
  if (isPlaying.value) {
    audio.value.pause()
    isPlaying.value = false
  } else {
    audio.value.play().then(() => {
      isPlaying.value = true
      // Ping play count API
      apiFetch(`/repertoire/compositions/${props.slug}/play/`, { method: 'POST' }).catch(() => {})
    }).catch(err => {
      console.error('Audio play error', err)
    })
  }
}

const onTimeUpdate = () => {
  if (audio.value) {
    currentTime.value = audio.value.currentTime
  }
}

const onLoadedMetadata = () => {
  if (audio.value) {
    duration.value = audio.value.duration
  }
}

const onEnded = () => {
  isPlaying.value = false
  currentTime.value = 0
}

const seek = (event: Event) => {
  const target = event.target as HTMLInputElement
  const newTime = parseFloat(target.value)
  if (audio.value) {
    audio.value.currentTime = newTime
    currentTime.value = newTime
  }
}

const toggleMute = () => {
  if (!audio.value) return
  isMuted.value = !isMuted.value
  audio.value.muted = isMuted.value
}

const changeVolume = (event: Event) => {
  const target = event.target as HTMLInputElement
  const newVol = parseFloat(target.value)
  volume.value = newVol
  if (audio.value) {
    audio.value.volume = newVol
    isMuted.value = newVol === 0
  }
}

const handleDownloadSheet = () => {
  apiFetch(`/repertoire/compositions/${props.slug}/download-sheet/`, { method: 'POST' })
    .then((res) => {
      if (res?.download_url) {
        window.open(res.download_url, '_blank')
      }
    })
    .catch(() => {
      if (props.sheetDownloadUrl) {
        window.open(props.sheetDownloadUrl, '_blank')
      }
    })
}

onMounted(() => {
  audio.value = new Audio(props.audioUrl)
  audio.value.volume = volume.value
  audio.value.addEventListener('timeupdate', onTimeUpdate)
  audio.value.addEventListener('loadedmetadata', onLoadedMetadata)
  audio.value.addEventListener('ended', onEnded)
})

onUnmounted(() => {
  if (audio.value) {
    audio.value.pause()
    audio.value.removeEventListener('timeupdate', onTimeUpdate)
    audio.value.removeEventListener('loadedmetadata', onLoadedMetadata)
    audio.value.removeEventListener('ended', onEnded)
    audio.value = null
  }
})
</script>

<template>
  <div class="p-5 sm:p-6 rounded-2xl glass-panel border border-wood-800/80 shadow-2xl space-y-4">
    
    <!-- Track Info & Visualizer Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-wood-700 to-wood-950 flex items-center justify-center border border-amber-500/30 text-amber-400">
          <Music class="w-6 h-6 stroke-[2]" />
        </div>
        <div>
          <h4 class="text-base font-bold text-white">{{ persianTitle }}</h4>
          <p class="text-xs text-amber-300/80">{{ title }} • {{ composer }}</p>
        </div>
      </div>

      <!-- Animated Soundwave Equalizer -->
      <div class="flex items-end gap-1 h-6 px-2">
        <span
          v-for="bar in 8"
          :key="bar"
          class="w-1 bg-amber-400 rounded-full transition-all duration-300"
          :class="isPlaying ? `wave-bar-anim-${(bar % 5) + 1}` : 'h-1.5 opacity-40'"
        ></span>
      </div>
    </div>

    <!-- Progress Timeline Slider -->
    <div class="space-y-1">
      <input
        type="range"
        min="0"
        :max="duration || 100"
        step="0.1"
        :value="currentTime"
        @input="seek"
        class="w-full h-1.5 bg-wood-900 rounded-lg appearance-none cursor-pointer accent-amber-500"
      />
      <div class="flex justify-between text-[11px] font-mono text-slate-400">
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(duration) }}</span>
      </div>
    </div>

    <!-- Controls Toolbar -->
    <div class="flex flex-wrap items-center justify-between gap-4 pt-1">
      
      <!-- Play/Pause & Volume -->
      <div class="flex items-center gap-3">
        <button
          @click="togglePlay"
          class="w-11 h-11 rounded-full bg-amber-500 hover:bg-amber-400 text-black flex items-center justify-center shadow-lg shadow-amber-500/30 transition-transform active:scale-95"
          :title="isPlaying ? 'توقف موقت' : 'پخش قطعه'"
        >
          <Pause v-if="isPlaying" class="w-5 h-5 fill-black" />
          <Play v-else class="w-5 h-5 fill-black mr-0.5" />
        </button>

        <!-- Volume Controller -->
        <div class="flex items-center gap-1.5 text-slate-400">
          <button @click="toggleMute" class="hover:text-amber-400">
            <VolumeX v-if="isMuted || volume === 0" class="w-4 h-4 text-red-400" />
            <Volume2 v-else class="w-4 h-4" />
          </button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            :value="isMuted ? 0 : volume"
            @input="changeVolume"
            class="w-16 h-1 bg-wood-900 rounded-lg appearance-none cursor-pointer accent-amber-500"
          />
        </div>
      </div>

      <!-- Sheet Music PDF Download Button -->
      <button
        @click="handleDownloadSheet"
        class="px-4 py-2 rounded-xl bg-wood-900 hover:bg-wood-800 text-amber-300 text-xs font-semibold border border-amber-500/30 flex items-center gap-2 transition-all hover:scale-[1.02]"
      >
        <FileText class="w-4 h-4 text-amber-400" />
        <span>دانلود رایگان نت و تبلچر (PDF)</span>
        <Download class="w-3.5 h-3.5 opacity-70" />
      </button>

    </div>

  </div>
</template>
