<script setup lang="ts">
import { Clock, Eye, ArrowLeft } from 'lucide-vue-next'

defineProps<{
  post: {
    id: number
    title: string
    slug: string
    category_name: string
    author_name: string
    excerpt: string
    reading_time_minutes: number
    view_count: number
    published_at: string
  }
}>()
</script>

<template>
  <article class="group relative rounded-2xl glass-panel border border-wood-900/80 hover:border-amber-500/40 p-5 transition-all duration-300 hover:shadow-2xl hover:shadow-amber-950/20 flex flex-col justify-between space-y-4">
    
    <div>
      <div class="flex items-center justify-between text-xs text-amber-400 font-semibold mb-2">
        <span>{{ post.category_name }}</span>
        <span class="flex items-center gap-1 text-slate-400 font-normal text-[11px]">
          <Clock class="w-3.5 h-3.5 text-amber-500" />
          {{ post.reading_time_minutes }} دقیقه مطالعه
        </span>
      </div>

      <NuxtLink :to="`/blog/${post.slug}`">
        <h3 class="text-base font-bold text-white group-hover:text-amber-400 transition-colors line-clamp-2 leading-relaxed mb-2">
          {{ post.title }}
        </h3>
      </NuxtLink>

      <p class="text-xs text-slate-300 line-clamp-3 leading-relaxed">
        {{ post.excerpt }}
      </p>
    </div>

    <div class="pt-3 border-t border-wood-900/60 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2 text-slate-400 text-[11px]">
        <span>نویسنده: {{ post.author_name }}</span>
        <span>•</span>
        <span class="flex items-center gap-1">
          <Eye class="w-3 h-3" />
          {{ post.view_count }}
        </span>
      </div>

      <NuxtLink
        :to="`/blog/${post.slug}`"
        class="text-amber-400 font-medium text-xs hover:underline flex items-center gap-1"
      >
        <span>ادامه مطلب</span>
        <ArrowLeft class="w-3.5 h-3.5" />
      </NuxtLink>
    </div>

  </article>
</template>
