<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Clock, Eye, User, Calendar, MessageSquare, Send, CheckCircle2 } from 'lucide-vue-next'
import { useSeoSchema } from '~/composables/useSeoSchema'

const route = useRoute()
const { injectArticleSchema } = useSeoSchema()

const post = ref({
  id: 1,
  title: 'رازهای دست‌یابی به راسگوادوی روان و قدرتمند در گیتار فلامنکو',
  slug: 'secrets-of-flamenco-rasgueado',
  category_name: 'تکنیک و نوازندگی',
  author_name: 'بهاور',
  reading_time_minutes: 7,
  excerpt: 'بررسی ارگونومی دست راست، نحوه رهاسازی انگشتان و تمرینات مرحله‌ای برای دستیابی به راسگوادوی متقارن و بدون کوفتگی عضله.',
  view_count: 840,
  published_at: '۱۴۰۳/۰۸/۱۵',
  content: `
### اهمیت ارگونومی دست راست در فلامنکو
تکنیک راسگوادو (Rasgueado) شناسه صوتی پرشور گیتار فلامنکو است. بسیاری از هنرجویان به اشتباه تصور می‌کنند که قدرت ضربات حاصل انقباض عضلات ساعد است، در حالی که نیروی واقعی از **رهاسازی ارتجاعی** انگشتان به دست می‌آید.

#### ۱. تثبیت موقعیت انگشت شست (Pulgar)
انگشت شست باید مانند یک تکیه‌گاه محکم روی سیم ششم (یا کلاف بالایی ساز) قرار گیرد. این کار باعث می‌شود تا محور چرخش مچ دست پایدار مانده و وزن دست به شکل یکنواخت به انگشتان e (کوچک)، a (حلقه)، m (میانی) و i (اشاره) منتقل شود.

#### ۲. راسگوادوی بادبزنی (Abanico)
در مدل ابانیکو، حرکت از چرخش ساعد و ضربه روی سیم‌ها آغاز می‌شود. ضربه رو به پایین شست، سپس پرتاب انگشتان و بازگشت با شست به بالا یک چرخه ریتمیک ۳ ضربه‌ای بی‌نقص ایجاد می‌کند.

#### ۳. تمرینات روزانه بدون ساز (Mental & Finger Independence)
- قرار دادن دست روی میز و باز کردن تک‌تک انگشتان بدون حرکت دادن مچ
- تمرین ریتم با مترونوم از تمپوی ۶۰ BPM و افزایش ۵ واحدی پس از هر ۳ دقیقه اجرای بی‌نقص.
`,
  comments: [
    {
      id: 1,
      user_name: 'حمید طاهری',
      comment: 'استاد عالی بود. نکته تکیه‌گاه شست روی سیم ششم واقعاً مشکلم در ضربات تند رو حل کرد.',
      created_at: '۱۴۰۳/۰۸/۱۶',
    },
  ],
})

// Inject Schema.org Article
injectArticleSchema({
  title: post.value.title,
  excerpt: post.value.excerpt,
  author_name: post.value.author_name,
  published_at: post.value.published_at,
  slug: post.value.slug,
})

const commentName = ref('')
const commentText = ref('')
const commentSent = ref(false)

const handleSendComment = () => {
  if (commentName.value && commentText.value) {
    post.value.comments.push({
      id: Date.now(),
      user_name: commentName.value,
      comment: commentText.value,
      created_at: 'هم‌اکنون',
    })
    commentSent.value = true
    commentName.value = ''
    commentText.value = ''
  }
}

useHead({
  title: `${post.value.title} | وبلاگ بهاور موزیک`,
})
</script>

<template>
  <article class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
    
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-xs text-slate-400">
      <NuxtLink to="/" class="hover:text-amber-400">خانه</NuxtLink>
      <span>/</span>
      <NuxtLink to="/blog" class="hover:text-amber-400">وبلاگ</NuxtLink>
      <span>/</span>
      <span class="text-amber-300 font-medium">{{ post.title }}</span>
    </nav>

    <!-- Header -->
    <header class="space-y-4 border-b border-wood-900 pb-8">
      <span class="px-3 py-1 rounded-full bg-wood-950 text-amber-400 text-xs font-semibold border border-amber-500/20 inline-block">
        {{ post.category_name }}
      </span>
      <h1 class="text-2xl sm:text-4xl font-extrabold text-white leading-tight">
        {{ post.title }}
      </h1>
      
      <div class="flex flex-wrap items-center gap-4 text-xs text-slate-400">
        <span class="flex items-center gap-1.5">
          <User class="w-4 h-4 text-amber-500" />
          <span>{{ post.author_name }}</span>
        </span>
        <span class="flex items-center gap-1.5">
          <Calendar class="w-4 h-4 text-amber-500" />
          <span>{{ post.published_at }}</span>
        </span>
        <span class="flex items-center gap-1.5">
          <Clock class="w-4 h-4 text-amber-500" />
          <span>{{ post.reading_time_minutes }} دقیقه مطالعه</span>
        </span>
        <span class="flex items-center gap-1.5">
          <Eye class="w-4 h-4 text-amber-500" />
          <span>{{ post.view_count }} بازدید</span>
        </span>
      </div>
    </header>

    <!-- Content Body -->
    <div class="p-6 sm:p-10 rounded-3xl glass-panel border border-wood-900/80 prose prose-invert prose-amber max-w-none text-slate-200 leading-loose text-sm sm:text-base whitespace-pre-line">
      {{ post.content }}
    </div>

    <!-- Author Bio Box -->
    <div class="p-6 rounded-2xl bg-wood-950/80 border border-amber-500/20 flex flex-col sm:flex-row items-center gap-4 text-center sm:text-right">
      <div class="w-16 h-16 rounded-full bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 font-bold text-xl shrink-0">
        بهاور
      </div>
      <div>
        <h4 class="text-base font-bold text-white mb-1">درباره نویسنده: بهاور</h4>
        <p class="text-xs text-slate-300 leading-relaxed">
          موزیسین، آهنگساز و مدرس ارشد گیتار با بیش از ۱۵ سال تجربه تدریس دانشگاهی، اجرای زنده و سرپرستی ضبط در استودیو آکوستیک.
        </p>
      </div>
    </div>

    <!-- Comments Section -->
    <div class="space-y-6 pt-6">
      <h3 class="text-lg font-bold text-white border-r-2 border-amber-500 pr-2.5">
        دیدگاه‌ها و پرسش‌های هنرجویان ({{ post.comments.length }})
      </h3>

      <!-- Existing Comments -->
      <div class="space-y-4">
        <div
          v-for="c in post.comments"
          :key="c.id"
          class="p-4 rounded-xl glass-panel border border-wood-900 space-y-1.5 text-xs text-slate-300"
        >
          <div class="flex items-center justify-between font-bold text-white">
            <span>{{ c.user_name }}</span>
            <span class="text-[10px] text-slate-500 font-mono">{{ c.created_at }}</span>
          </div>
          <p class="leading-relaxed">{{ c.comment }}</p>
        </div>
      </div>

      <!-- Add Comment Form -->
      <form @submit.prevent="handleSendComment" class="p-6 rounded-2xl glass-panel border border-wood-900 space-y-4">
        <h4 class="text-sm font-bold text-white">ارسال دیدگاه یا سوال فنی</h4>
        
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">نام شما</label>
          <input
            v-model="commentName"
            type="text"
            required
            placeholder="مثال: آرش کیانی"
            class="w-full px-4 py-2 text-xs rounded-xl bg-studio-dark border border-wood-800 text-white focus:outline-none focus:border-amber-500"
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">متن دیدگاه</label>
          <textarea
            v-model="commentText"
            required
            rows="3"
            placeholder="دیدگاه خود را پیرامون این مقاله بنویسید..."
            class="w-full p-3 text-xs rounded-xl bg-studio-dark border border-wood-800 text-white focus:outline-none focus:border-amber-500 leading-relaxed"
          ></textarea>
        </div>

        <button
          type="submit"
          class="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-xs flex items-center gap-2 transition-colors"
        >
          <Send class="w-3.5 h-3.5" />
          <span>ثبت دیدگاه</span>
        </button>

        <p v-if="commentSent" class="text-xs text-emerald-400">
          دیدگاه شما با موفقیت ثبت شد.
        </p>
      </form>

    </div>

  </article>
</template>
