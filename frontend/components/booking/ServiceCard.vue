<script setup lang="ts">
import { Calendar, Clock, ArrowLeft, Mic, Guitar, Sliders, MessageCircle } from 'lucide-vue-next'

const props = defineProps<{
  service: {
    id: number
    title: string
    slug: string
    service_type: string
    service_type_display: string
    duration_minutes: number
    price: number
    description: string
    icon: string
  }
}>()

const getIconComponent = (icon: string) => {
  switch (icon) {
    case 'Mic': return Mic
    case 'Sliders': return Sliders
    case 'MessageCircle': return MessageCircle
    default: return Guitar
  }
}
</script>

<template>
  <div class="group relative rounded-2xl glass-panel border border-wood-900/80 hover:border-amber-500/40 p-6 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-950/20 flex flex-col justify-between space-y-4">
    
    <div>
      <div class="flex items-center justify-between mb-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500/20 to-wood-950 border border-amber-500/30 flex items-center justify-center text-amber-400 group-hover:scale-105 transition-transform">
          <component :is="getIconComponent(service.icon)" class="w-6 h-6" />
        </div>
        <div class="flex items-center gap-1 text-xs text-slate-400 font-mono">
          <Clock class="w-3.5 h-3.5 text-amber-500" />
          <span>{{ service.duration_minutes }} دقیقه</span>
        </div>
      </div>

      <h3 class="text-base font-bold text-white group-hover:text-amber-400 transition-colors mb-2">
        {{ service.title }}
      </h3>

      <p class="text-xs text-slate-300 line-clamp-3 leading-relaxed">
        {{ service.description }}
      </p>
    </div>

    <div class="pt-4 border-t border-wood-900/60 flex items-center justify-between">
      <div>
        <span class="text-[10px] text-slate-400 block">هزینه جلسه:</span>
        <div class="text-sm font-bold text-amber-400 font-mono">
          {{ service.price.toLocaleString('fa-IR') }}
          <span class="text-[10px] font-normal text-slate-400 mr-1">تومان</span>
        </div>
      </div>

      <NuxtLink
        :to="`/booking?service=${service.id}`"
        class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs shadow-md shadow-amber-500/20 transition-all hover:scale-105"
      >
        <Calendar class="w-3.5 h-3.5" />
        <span>رزرو آنلاین سانس</span>
      </NuxtLink>
    </div>

  </div>
</template>
