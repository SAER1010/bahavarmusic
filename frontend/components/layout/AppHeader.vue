<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useCartStore } from '~/stores/cart'
import { 
  Music, 
  ShoppingBag, 
  Calendar, 
  BookOpen, 
  FileText, 
  User as UserIcon, 
  Sun, 
  Moon, 
  Menu, 
  X,
  Volume2
} from 'lucide-vue-next'

const authStore = useAuthStore()
const cartStore = useCartStore()
const colorMode = useColorMode()

const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)

const toggleColorMode = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
}

onMounted(() => {
  authStore.initAuth()
  cartStore.initCart()

  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 30
  })
})
</script>

<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-300"
    :class="[
      isScrolled 
        ? 'py-3 bg-studio-dark/90 backdrop-blur-md border-b border-wood-800/40 shadow-xl shadow-black/40' 
        : 'py-5 bg-gradient-to-b from-studio-dark/95 via-studio-dark/70 to-transparent'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        
        <!-- Brand & Audio Visualizer Accent -->
        <NuxtLink to="/" class="flex items-center gap-3 group">
          <div class="relative w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center shadow-lg shadow-amber-900/30 ring-1 ring-amber-400/40 group-hover:scale-105 transition-transform">
            <Music class="w-5 h-5 text-black stroke-[2.5]" />
          </div>
          <div class="flex flex-col">
            <div class="flex items-center gap-2">
              <span class="text-xl font-bold tracking-tight text-white group-hover:text-amber-400 transition-colors">
                بهاور موزیک
              </span>
              <!-- Equalizer Accent -->
              <div class="hidden sm:flex items-end gap-[2px] h-4 w-5 px-0.5">
                <span class="w-[3px] bg-amber-400 rounded-full wave-bar-anim-1"></span>
                <span class="w-[3px] bg-amber-500 rounded-full wave-bar-anim-2"></span>
                <span class="w-[3px] bg-amber-300 rounded-full wave-bar-anim-3"></span>
                <span class="w-[3px] bg-amber-600 rounded-full wave-bar-anim-4"></span>
              </div>
            </div>
            <span class="text-[10px] text-amber-200/60 font-medium tracking-wide">
              BAHAVAR • STUDIO & ACADEMY
            </span>
          </div>
        </NuxtLink>

        <!-- Desktop Navigation Mega-Menu -->
        <nav class="hidden md:flex items-center gap-1 lg:gap-2 px-3 py-1.5 rounded-full bg-studio-card/80 border border-wood-900/60 shadow-inner">
          <NuxtLink
            to="/repertoire"
            class="px-3.5 py-1.5 rounded-full text-sm font-medium text-slate-300 hover:text-amber-400 hover:bg-wood-950/60 transition-all flex items-center gap-1.5"
            active-class="!text-amber-400 !bg-wood-900/80 shadow-sm"
          >
            <Music class="w-4 h-4 text-amber-500" />
            <span>رپرتوار و نت‌ها</span>
          </NuxtLink>

          <NuxtLink
            to="/booking"
            class="px-3.5 py-1.5 rounded-full text-sm font-medium text-slate-300 hover:text-amber-400 hover:bg-wood-950/60 transition-all flex items-center gap-1.5"
            active-class="!text-amber-400 !bg-wood-900/80 shadow-sm"
          >
            <Calendar class="w-4 h-4 text-amber-500" />
            <span>رزرو استودیو و کلاس</span>
          </NuxtLink>

          <NuxtLink
            to="/shop"
            class="px-3.5 py-1.5 rounded-full text-sm font-medium text-slate-300 hover:text-amber-400 hover:bg-wood-950/60 transition-all flex items-center gap-1.5"
            active-class="!text-amber-400 !bg-wood-900/80 shadow-sm"
          >
            <ShoppingBag class="w-4 h-4 text-amber-500" />
            <span>فروشگاه ساز</span>
          </NuxtLink>

          <NuxtLink
            to="/blog"
            class="px-3.5 py-1.5 rounded-full text-sm font-medium text-slate-300 hover:text-amber-400 hover:bg-wood-950/60 transition-all flex items-center gap-1.5"
            active-class="!text-amber-400 !bg-wood-900/80 shadow-sm"
          >
            <BookOpen class="w-4 h-4 text-amber-500" />
            <span>وبلاگ و آموزش</span>
          </NuxtLink>
        </nav>

        <!-- Header Actions: Cart, Theme, Student Portal -->
        <div class="flex items-center gap-2 sm:gap-3">
          
          <!-- Cart Icon -->
          <NuxtLink
            to="/shop"
            class="relative p-2.5 rounded-xl bg-studio-card/80 border border-wood-900/60 text-slate-300 hover:text-amber-400 hover:border-amber-500/40 transition-all"
            title="سبد خرید"
          >
            <ShoppingBag class="w-5 h-5" />
            <span
              v-if="cartStore.totalCount > 0"
              class="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-amber-500 text-black text-xs font-bold flex items-center justify-center ring-2 ring-studio-dark animate-pulse"
            >
              {{ cartStore.totalCount }}
            </span>
          </NuxtLink>

          <!-- Color Mode Toggle -->
          <button
            @click="toggleColorMode"
            class="p-2.5 rounded-xl bg-studio-card/80 border border-wood-900/60 text-slate-300 hover:text-amber-400 transition-colors"
            :title="colorMode.value === 'dark' ? 'حالت روشن' : 'حالت تاریک'"
          >
            <Sun v-if="colorMode.value === 'dark'" class="w-5 h-5 text-amber-400" />
            <Moon v-else class="w-5 h-5 text-slate-400" />
          </button>

          <!-- Student Portal CTA -->
          <template v-if="authStore.isAuthenticated">
            <NuxtLink
              to="/dashboard"
              class="hidden sm:flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white font-medium text-sm shadow-lg shadow-amber-900/30 transition-all hover:scale-[1.02]"
            >
              <UserIcon class="w-4 h-4" />
              <span>پرتال هنرجو</span>
            </NuxtLink>
          </template>
          <template v-else>
            <button
              @click="authStore.openAuthModal('otp')"
              class="hidden sm:flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-semibold text-sm shadow-lg shadow-amber-500/20 transition-all hover:scale-[1.02]"
            >
              <UserIcon class="w-4 h-4" />
              <span>ورود هنرجویان</span>
            </button>
          </template>

          <!-- Mobile Menu Button -->
          <button
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="md:hidden p-2.5 rounded-xl bg-studio-card border border-wood-900/60 text-slate-300"
          >
            <X v-if="isMobileMenuOpen" class="w-5 h-5 text-amber-400" />
            <Menu v-else class="w-5 h-5" />
          </button>
        </div>

      </div>

      <!-- Mobile Dropdown Menu -->
      <div
        v-if="isMobileMenuOpen"
        class="md:hidden mt-4 p-4 rounded-2xl glass-panel space-y-3 shadow-2xl animate-fadeIn"
      >
        <NuxtLink
          to="/repertoire"
          @click="isMobileMenuOpen = false"
          class="flex items-center gap-3 p-2.5 rounded-xl text-slate-200 hover:bg-wood-900/50"
        >
          <Music class="w-5 h-5 text-amber-400" />
          <span>رپرتوار و نت‌ها</span>
        </NuxtLink>

        <NuxtLink
          to="/booking"
          @click="isMobileMenuOpen = false"
          class="flex items-center gap-3 p-2.5 rounded-xl text-slate-200 hover:bg-wood-900/50"
        >
          <Calendar class="w-5 h-5 text-amber-400" />
          <span>رزرو استودیو و کلاس‌ها</span>
        </NuxtLink>

        <NuxtLink
          to="/shop"
          @click="isMobileMenuOpen = false"
          class="flex items-center gap-3 p-2.5 rounded-xl text-slate-200 hover:bg-wood-900/50"
        >
          <ShoppingBag class="w-5 h-5 text-amber-400" />
          <span>فروشگاه تخصصی گیتار</span>
        </NuxtLink>

        <NuxtLink
          to="/blog"
          @click="isMobileMenuOpen = false"
          class="flex items-center gap-3 p-2.5 rounded-xl text-slate-200 hover:bg-wood-900/50"
        >
          <BookOpen class="w-5 h-5 text-amber-400" />
          <span>وبلاگ و مقالات آموزشی</span>
        </NuxtLink>

        <div class="pt-3 border-t border-wood-900/60">
          <button
            v-if="!authStore.isAuthenticated"
            @click="authStore.openAuthModal('otp'); isMobileMenuOpen = false"
            class="w-full py-2.5 rounded-xl bg-amber-500 text-black font-semibold flex items-center justify-center gap-2"
          >
            <UserIcon class="w-4 h-4" />
            <span>ورود / عضویت هنرجویان</span>
          </button>
          <NuxtLink
            v-else
            to="/dashboard"
            @click="isMobileMenuOpen = false"
            class="w-full py-2.5 rounded-xl bg-amber-600 text-white font-semibold flex items-center justify-center gap-2"
          >
            <UserIcon class="w-4 h-4" />
            <span>میز کار و پرتال هنرجو</span>
          </NuxtLink>
        </div>
      </div>

    </div>
  </header>
</template>
