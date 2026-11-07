<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  } else {
    authStore.openAuthModal('otp')
  }
})

useHead({
  title: 'ورود به پرتال هنرجویان | بهاور موزیک',
})
</script>

<template>
  <div class="min-h-[60vh] flex items-center justify-center p-4">
    <div class="text-center space-y-4">
      <div class="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center mx-auto animate-bounce">
        ♪
      </div>
      <h2 class="text-lg font-bold text-white">در حال بازگشایی فرم ورود...</h2>
      <p class="text-xs text-slate-400">اگر پنجره باز نشد، روی دکمه زیر کلیک نمایید.</p>
      <button
        @click="authStore.openAuthModal('otp')"
        class="px-5 py-2.5 rounded-xl bg-amber-500 text-black font-bold text-xs"
      >
        ورود با شماره موبایل یا رمز
      </button>
    </div>
  </div>
</template>
