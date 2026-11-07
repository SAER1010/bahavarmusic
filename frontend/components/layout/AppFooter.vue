<script setup lang="ts">
import { ref } from 'vue'
import { Music, MapPin, Phone, Mail, Instagram, Send, ShieldCheck, Heart } from 'lucide-vue-next'

const emailInput = ref('')
const isSubscribed = ref(false)

const handleNewsletter = () => {
  if (emailInput.value) {
    isSubscribed.value = true
    emailInput.value = ''
  }
}
</script>

<template>
  <footer class="relative bg-studio-dark pt-16 pb-12 border-t border-wood-900/60 overflow-hidden">
    
    <!-- Musical Stave / Waveform Visual Element -->
    <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-amber-500 to-transparent opacity-60"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12">
      <div class="w-full flex items-center justify-center gap-1 opacity-20 hover:opacity-40 transition-opacity my-4">
        <span v-for="i in 40" :key="i" class="w-1 bg-amber-400 rounded-full" :style="{ height: `${((i * 17) % 36) + 8}px` }"></span>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
        
        <!-- Column 1: Bahavar Bio & Brand -->
        <div class="space-y-4">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-amber-500 flex items-center justify-center text-black font-bold">
              <Music class="w-5 h-5 stroke-[2.5]" />
            </div>
            <span class="text-xl font-bold text-white">بهاور موزیک</span>
          </div>
          <p class="text-sm text-slate-400 leading-relaxed">
            پلتفرم رسمی بهاور؛ آهنگساز، نوازنده و مدرس گیتار. مرکزی برای ارتقای استانداردهای نوازندگی، ضبط استودیویی با تجهیزات بین‌المللی و انتشار پارتیتورهای اصیل موسیقی.
          </p>
          <div class="flex items-center gap-3 pt-2">
            <a
              href="https://instagram.com/bahavarmusic"
              target="_blank"
              class="w-9 h-9 rounded-lg bg-studio-card border border-wood-800/80 flex items-center justify-center text-slate-400 hover:text-amber-400 hover:border-amber-500/50 transition-colors"
              title="اینستاگرام"
            >
              <Instagram class="w-4 h-4" />
            </a>
            <a
              href="https://t.me/bahavarmusic"
              target="_blank"
              class="w-9 h-9 rounded-lg bg-studio-card border border-wood-800/80 flex items-center justify-center text-slate-400 hover:text-amber-400 hover:border-amber-500/50 transition-colors"
              title="تلگرام"
            >
              <Send class="w-4 h-4" />
            </a>
            <a
              href="https://youtube.com/@BahavarMusicOfficial"
              target="_blank"
              class="w-9 h-9 rounded-lg bg-studio-card border border-wood-800/80 flex items-center justify-center text-slate-400 hover:text-amber-400 hover:border-amber-500/50 transition-colors"
              title="یوتیوب"
            >
              <Music class="w-4 h-4" />
            </a>
          </div>
        </div>

        <!-- Column 2: Quick Links -->
        <div class="space-y-4">
          <h4 class="text-base font-semibold text-white border-r-2 border-amber-500 pr-2.5">
            دسترسی سریع
          </h4>
          <ul class="space-y-2.5 text-sm text-slate-400">
            <li>
              <NuxtLink to="/repertoire" class="hover:text-amber-400 transition-colors">آرشیو قطعات و دانلود نت‌های رایگان</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/booking" class="hover:text-amber-400 transition-colors">رزرو وقت مشاوره و آموزش خصوصی</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/shop" class="hover:text-amber-400 transition-colors">سازهای تست شده و مسترکلاس‌ها</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/blog" class="hover:text-amber-400 transition-colors">مقالات تکنیک نوازندگی و آکوستیک</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/dashboard" class="hover:text-amber-400 transition-colors">پرتال و میز کار هنرجویان</NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Column 3: Studio Location & Contact -->
        <div class="space-y-4">
          <h4 class="text-base font-semibold text-white border-r-2 border-amber-500 pr-2.5">
            استودیو بهاور
          </h4>
          <ul class="space-y-3 text-sm text-slate-400">
            <li class="flex items-start gap-2.5">
              <MapPin class="w-4 h-4 text-amber-500 shrink-0 mt-1" />
              <span>تهران، خیابان ولیعصر، نرسیده به ونک، برج نگار، طبقه ۶، استودیو موسیقی بهاور</span>
            </li>
            <li class="flex items-center gap-2.5">
              <Phone class="w-4 h-4 text-amber-500 shrink-0" />
              <span dir="ltr" class="font-mono text-left">021 - 8877 6655</span>
            </li>
            <li class="flex items-center gap-2.5">
              <Mail class="w-4 h-4 text-amber-500 shrink-0" />
              <span class="font-mono text-xs">contact@bahavarmusic.com</span>
            </li>
          </ul>
        </div>

        <!-- Column 4: Newsletter & e-Namad Trust Badge -->
        <div class="space-y-4">
          <h4 class="text-base font-semibold text-white border-r-2 border-amber-500 pr-2.5">
            خبرنامه و نمادهای اعتماد
          </h4>
          <p class="text-xs text-slate-400 leading-relaxed">
            جهت اطلاع از انتشار نت‌های جدید، تخفیف دوره‌ها و زمان‌بندی مسترکلاس‌ها عضو خبرنامه شوید.
          </p>

          <form @submit.prevent="handleNewsletter" class="space-y-2">
            <div class="flex items-center gap-2">
              <input
                v-model="emailInput"
                type="email"
                placeholder="ایمیل خود را بنویسید..."
                required
                class="w-full px-3 py-2 text-xs rounded-lg bg-studio-card border border-wood-800 text-white placeholder-slate-500 focus:outline-none focus:border-amber-500"
              />
              <button
                type="submit"
                class="px-3.5 py-2 text-xs font-semibold rounded-lg bg-amber-500 text-black hover:bg-amber-400 transition-colors shrink-0"
              >
                عضویت
              </button>
            </div>
            <p v-if="isSubscribed" class="text-[11px] text-emerald-400">
              با تشکر! عضویت شما در خبرنامه تایید شد.
            </p>
          </form>

          <!-- e-Namad & Samandehi Trust Badges Placeholder -->
          <div class="pt-2 flex items-center gap-3">
            <div class="p-2 rounded-xl bg-studio-card border border-wood-900 flex items-center gap-2 hover:border-amber-500/40 transition-colors">
              <ShieldCheck class="w-7 h-7 text-amber-400" />
              <div class="flex flex-col">
                <span class="text-[11px] font-bold text-slate-200">اینماد الکترونیکی</span>
                <span class="text-[9px] text-slate-400">مجوز پرداخت رسمی</span>
              </div>
            </div>
            <div class="p-2 rounded-xl bg-studio-card border border-wood-900 flex items-center gap-2 hover:border-amber-500/40 transition-colors">
              <ShieldCheck class="w-7 h-7 text-amber-500" />
              <div class="flex flex-col">
                <span class="text-[11px] font-bold text-slate-200">نشان ساماندهی</span>
                <span class="text-[9px] text-slate-400">وزارت فرهنگ و ارشاد</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Copyright -->
      <div class="mt-12 pt-6 border-t border-wood-900/60 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <p>© تمامی حقوق مادی و معنوی این پلتفرم متعلق به «بهاور» است.</p>
        <p class="flex items-center gap-1">
          طراحی و توسعه اختصاصی برای هنرمندان با
          <Heart class="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
        </p>
      </div>
    </div>
  </footer>
</template>
