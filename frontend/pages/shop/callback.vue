<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle2, AlertCircle, ShoppingBag, ArrowLeft, Download } from 'lucide-vue-next'

const route = useRoute()

const isSuccess = ref(true)
const refId = ref(`REF-${Math.random().toString(36).substring(2, 9).toUpperCase()}`)
const orderNumber = ref(`BHV-${Math.floor(100000 + Math.random() * 900000)}`)

useHead({
  title: 'نتیجه تراکنش بانکی | بهاور موزیک',
})
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-16 text-center space-y-8">
    <div class="p-8 sm:p-12 rounded-3xl glass-panel border border-emerald-500/30 shadow-2xl space-y-6">
      
      <!-- Status Icon -->
      <div class="w-20 h-20 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center mx-auto text-emerald-400">
        <CheckCircle2 class="w-10 h-10" />
      </div>

      <!-- Heading -->
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white mb-2">پرداخت با موفقیت انجام شد</h1>
        <p class="text-xs sm:text-sm text-slate-300">
          سفارش شما در سیستم ثبت شد و فاکتور رسمی به شماره موبایل شما پیامک گردید.
        </p>
      </div>

      <!-- Transaction Details -->
      <div class="p-4 rounded-2xl bg-studio-dark/80 border border-wood-900 space-y-3 text-xs sm:text-sm text-slate-300">
        <div class="flex items-center justify-between">
          <span class="text-slate-400">شماره پیگیری سفارش:</span>
          <span class="font-mono font-bold text-white">{{ orderNumber }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-slate-400">شماره ارجاع بانکی (RefID):</span>
          <span class="font-mono font-bold text-amber-400">{{ refId }}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-slate-400">وضعیت دسترسی دوره‌ها / نت‌ها:</span>
          <span class="text-emerald-400 font-bold">آنی فعال شد</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
        <NuxtLink
          to="/dashboard"
          class="w-full sm:w-auto px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-sm shadow-lg shadow-amber-500/20 flex items-center justify-center gap-2"
        >
          <span>مشاهده در پرتال هنرجو</span>
          <ArrowLeft class="w-4 h-4" />
        </NuxtLink>

        <NuxtLink
          to="/shop"
          class="w-full sm:w-auto px-6 py-3 rounded-xl bg-wood-900 hover:bg-wood-800 text-slate-300 text-sm font-semibold"
        >
          بازگشت به فروشگاه
        </NuxtLink>
      </div>

    </div>
  </div>
</template>
