<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, BookOpen } from 'lucide-vue-next'
import BlogCard from '~/components/blog/BlogCard.vue'

const searchQuery = ref('')
const selectedCategory = ref('all')

const categories = [
  { id: 'all', name: 'همه مقالات' },
  { id: 'technique', name: 'تکنیک و نوازندگی' },
  { id: 'gear', name: 'سازشناسی و آکوستیک' },
  { id: 'theory', name: 'تئوری و هارمونی' },
]

const posts = ref([
  {
    id: 1,
    title: 'رازهای دست‌یابی به راسگوادوی روان و قدرتمند در گیتار فلامنکو',
    slug: 'secrets-of-flamenco-rasgueado',
    category_slug: 'technique',
    category_name: 'تکنیک و نوازندگی',
    author_name: 'بهاور',
    reading_time_minutes: 7,
    excerpt: 'بررسی ارگونومی دست راست، نحوه رهاسازی انگشتان و تمرینات مرحله‌ای برای دستیابی به راسگوادوی متقارن و بدون کوفتگی عضله.',
    view_count: 840,
    published_at: '۱۴۰۳/۰۸/۱۵',
  },
  {
    id: 2,
    title: 'راهنمای جامع تفاوت چوب صنوبر (Spruce) و سرو (Cedar) در صفحه رویی گیتار',
    slug: 'spruce-vs-cedar-soundboard-guide',
    category_slug: 'gear',
    category_name: 'تجهیزات، سازشناسی و آکوستیک',
    author_name: 'بهاور',
    reading_time_minutes: 6,
    excerpt: 'کدام تاپ‌وود برای سبک نوازندگی شما مناسب‌تر است؟ تحلیل رزونانس، رنگ صوتی و سرعت باز شدن صدای ساز در گذر زمان.',
    view_count: 620,
    published_at: '۱۴۰۳/۰۸/۱۰',
  },
])

const filteredPosts = computed(() => {
  return posts.value.filter((p) => {
    const matchesCat = selectedCategory.value === 'all' || p.category_slug === selectedCategory.value
    const matchesSearch = !searchQuery.value || p.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCat && matchesSearch
  })
})

useHead({
  title: 'وبلاگ و مقالات تخصصی آموزش گیتار و موسیقی | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
    
    <!-- Header -->
    <div class="border-b border-wood-900 pb-8 space-y-2">
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white">وبلاگ، مقالات و آموزش‌های تخصصی</h1>
      <p class="text-sm text-slate-400">راهنماهای نوازندگی، ارگونومی دست، تحلیل سازهای موسیقی و ترفندهای استودیو</p>
    </div>

    <!-- Search & Filter -->
    <div class="flex flex-col sm:flex-row items-center gap-4">
      <div class="relative flex-1 w-full">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="جستجو در مقالات و راهنماهای آموزشی..."
          class="w-full px-4 py-3 pl-10 rounded-xl bg-studio-card border border-wood-800 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-amber-500"
        />
        <Search class="w-4 h-4 text-slate-400 absolute top-3.5 left-3.5" />
      </div>

      <div class="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="selectedCategory = cat.id"
          class="px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border"
          :class="selectedCategory === cat.id ? 'bg-amber-500 text-black border-amber-500 shadow-md shadow-amber-500/20' : 'bg-studio-card text-slate-300 border-wood-900 hover:border-amber-500/40'"
        >
          {{ cat.name }}
        </button>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="filteredPosts.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <BlogCard
        v-for="post in filteredPosts"
        :key="post.id"
        :post="post"
      />
    </div>

    <div v-else class="text-center py-20 rounded-3xl glass-panel p-8">
      <p class="text-slate-400 text-sm">مقاله‌ای با این مشخصات یافت نشد.</p>
    </div>

  </div>
</template>
