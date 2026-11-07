<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useApi } from '~/composables/useApi'
import { X, Phone, Lock, Mail, User as UserIcon, ArrowRight, CheckCircle2, AlertCircle } from 'lucide-vue-next'

const authStore = useAuthStore()
const { apiFetch } = useApi()

const mode = ref<'otp' | 'login' | 'register'>('otp')
const step = ref<'phone' | 'code'>('phone')

// Form inputs
const phoneNumber = ref('09121234567')
const otpCode = ref('')
const emailOrUsername = ref('')
const password = ref('')
const registerName = ref('')
const registerEmail = ref('')
const registerPhone = ref('')
const registerPassword = ref('')

const timer = ref(120)
let timerInterval: any = null
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const mockCodeHint = ref('')

watch(() => authStore.isAuthModalOpen, (isOpen) => {
  if (isOpen) {
    mode.value = authStore.authModalMode || 'otp'
    step.value = 'phone'
    errorMessage.value = ''
    successMessage.value = ''
  } else {
    clearInterval(timerInterval)
  }
})

const startTimer = () => {
  clearInterval(timerInterval)
  timer.value = 120
  timerInterval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--
    } else {
      clearInterval(timerInterval)
    }
  }, 1000)
}

// Request OTP
const handleRequestOtp = async () => {
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const res = await apiFetch('/accounts/otp/request/', {
      method: 'POST',
      body: { phone_number: phoneNumber.value },
    })
    step.value = 'code'
    startTimer()
    if (res.mock_code) {
      mockCodeHint.value = res.mock_code
      otpCode.value = res.mock_code // convenience in dev
    }
    successMessage.value = 'کد تایید ارسال شد.'
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || err?.data?.phone_number?.[0] || 'ارسال کد با خطا مواجه شد.'
  } finally {
    isLoading.value = false
  }
}

// Verify OTP
const handleVerifyOtp = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const res = await apiFetch('/accounts/otp/verify/', {
      method: 'POST',
      body: { phone_number: phoneNumber.value, code: otpCode.value },
    })
    authStore.setAuth(res.tokens, res.user)
    authStore.closeAuthModal()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'کد وارد شده معتبر نمی‌باشد.'
  } finally {
    isLoading.value = false
  }
}

// Email Login
const handleEmailLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const res = await apiFetch('/accounts/login/', {
      method: 'POST',
      body: { username_or_email: emailOrUsername.value, password: password.value },
    })
    authStore.setAuth(res.tokens, res.user)
    authStore.closeAuthModal()
  } catch (err: any) {
    errorMessage.value = err?.data?.non_field_errors?.[0] || 'نام کاربری یا رمز عبور نامعتبر است.'
  } finally {
    isLoading.value = false
  }
}

// Register
const handleRegister = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const res = await apiFetch('/accounts/register/', {
      method: 'POST',
      body: {
        username: registerPhone.value || registerEmail.value.split('@')[0],
        first_name: registerName.value,
        phone_number: registerPhone.value,
        email: registerEmail.value,
        password: registerPassword.value,
      },
    })
    authStore.setAuth(res.tokens, res.user)
    authStore.closeAuthModal()
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'ثبت‌نام انجام نشد. لطفاً اطلاعات را بررسی کنید.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div
    v-if="authStore.isAuthModalOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn"
    @click.self="authStore.closeAuthModal()"
  >
    <div class="relative w-full max-w-md rounded-2xl glass-panel p-6 sm:p-8 shadow-2xl border border-amber-500/20 text-slate-100">
      
      <!-- Close Button -->
      <button
        @click="authStore.closeAuthModal()"
        class="absolute top-4 left-4 p-2 rounded-xl text-slate-400 hover:text-white hover:bg-wood-900/60 transition-colors"
      >
        <X class="w-5 h-5" />
      </button>

      <!-- Modal Header -->
      <div class="text-center mb-6">
        <h3 class="text-xl font-bold text-white mb-1.5">
          ورود به پرتال هنرجویان و استودیو
        </h3>
        <p class="text-xs text-amber-200/70">
          دسترسی به دوره‌ها، تاریخ جلسات، نت‌های خریداری شده و رزرو وقت
        </p>
      </div>

      <!-- Mode Selector Tabs -->
      <div class="flex items-center gap-1 p-1 bg-studio-dark/80 rounded-xl mb-6 border border-wood-900">
        <button
          @click="mode = 'otp'; step = 'phone'"
          class="flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all"
          :class="mode === 'otp' ? 'bg-amber-500 text-black shadow-sm' : 'text-slate-400 hover:text-white'"
        >
          ورود با شماره موبایل (OTP)
        </button>
        <button
          @click="mode = 'login'"
          class="flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all"
          :class="mode === 'login' ? 'bg-amber-500 text-black shadow-sm' : 'text-slate-400 hover:text-white'"
        >
          ورود با رمز عبور
        </button>
        <button
          @click="mode = 'register'"
          class="flex-1 py-1.5 text-xs font-semibold rounded-lg transition-all"
          :class="mode === 'register' ? 'bg-amber-500 text-black shadow-sm' : 'text-slate-400 hover:text-white'"
        >
          ثبت‌نام جدید
        </button>
      </div>

      <!-- Feedback Alerts -->
      <div v-if="errorMessage" class="mb-4 p-3 rounded-xl bg-red-950/60 border border-red-500/30 flex items-center gap-2 text-xs text-red-300">
        <AlertCircle class="w-4 h-4 shrink-0 text-red-400" />
        <span>{{ errorMessage }}</span>
      </div>
      <div v-if="successMessage" class="mb-4 p-3 rounded-xl bg-emerald-950/60 border border-emerald-500/30 flex items-center gap-2 text-xs text-emerald-300">
        <CheckCircle2 class="w-4 h-4 shrink-0 text-emerald-400" />
        <span>{{ successMessage }}</span>
      </div>

      <!-- Mode 1: OTP Flow -->
      <div v-if="mode === 'otp'">
        <div v-if="step === 'phone'" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1.5">شماره موبایل</label>
            <div class="relative">
              <input
                v-model="phoneNumber"
                type="tel"
                placeholder="09121234567"
                dir="ltr"
                class="w-full px-4 py-2.5 rounded-xl bg-studio-dark border border-wood-800 text-white font-mono placeholder-slate-500 focus:outline-none focus:border-amber-500"
              />
              <Phone class="w-4 h-4 text-slate-500 absolute top-3.5 right-3" />
            </div>
            <p class="text-[11px] text-slate-400 mt-1">کد یکبار مصرف ۶ رقمی برای شما پیامک خواهد شد.</p>
          </div>

          <button
            @click="handleRequestOtp"
            :disabled="isLoading || !phoneNumber"
            class="w-full py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-lg shadow-amber-500/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2"
          >
            <span v-if="isLoading">در حال ارسال...</span>
            <span v-else>دریافت کد تایید</span>
          </button>
        </div>

        <div v-else class="space-y-4">
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="text-xs font-medium text-slate-300">کد ۶ رقمی پیامک شده</label>
              <button @click="step = 'phone'" class="text-[11px] text-amber-400 hover:underline">
                تغییر شماره ({{ phoneNumber }})
              </button>
            </div>
            <input
              v-model="otpCode"
              type="text"
              maxlength="6"
              placeholder="123456"
              dir="ltr"
              class="w-full text-center tracking-widest text-lg font-mono px-4 py-2.5 rounded-xl bg-studio-dark border border-wood-800 text-white focus:outline-none focus:border-amber-500"
            />
          </div>

          <div v-if="mockCodeHint" class="p-2.5 rounded-lg bg-wood-950/80 border border-amber-500/30 text-center">
            <span class="text-xs text-amber-300">کد آزمایشی برای تست: </span>
            <span class="font-mono font-bold text-white">{{ mockCodeHint }}</span>
          </div>

          <div class="flex items-center justify-between text-xs text-slate-400">
            <span>زمان باقی‌مانده: {{ Math.floor(timer / 60) }}:{{ String(timer % 60).padStart(2, '0') }}</span>
            <button
              v-if="timer === 0"
              @click="handleRequestOtp"
              class="text-amber-400 hover:underline font-medium"
            >
              ارسال مجدد کد
            </button>
          </div>

          <button
            @click="handleVerifyOtp"
            :disabled="isLoading || otpCode.length < 5"
            class="w-full py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-bold text-sm shadow-lg shadow-amber-500/20 disabled:opacity-50 transition-all"
          >
            <span v-if="isLoading">در حال بررسی...</span>
            <span v-else>ورود به سامانه</span>
          </button>
        </div>
      </div>

      <!-- Mode 2: Email + Password Login -->
      <div v-else-if="mode === 'login'" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">ایمیل، شماره یا نام کاربری</label>
          <div class="relative">
            <input
              v-model="emailOrUsername"
              type="text"
              placeholder="bahavar یا 0912... یا ایمیل"
              class="w-full px-4 py-2.5 rounded-xl bg-studio-dark border border-wood-800 text-white placeholder-slate-500 focus:outline-none focus:border-amber-500"
            />
            <UserIcon class="w-4 h-4 text-slate-500 absolute top-3.5 right-3" />
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1.5">رمز عبور</label>
          <div class="relative">
            <input
              v-model="password"
              type="password"
              placeholder="••••••••"
              class="w-full px-4 py-2.5 rounded-xl bg-studio-dark border border-wood-800 text-white placeholder-slate-500 focus:outline-none focus:border-amber-500"
            />
            <Lock class="w-4 h-4 text-slate-500 absolute top-3.5 right-3" />
          </div>
        </div>

        <button
          @click="handleEmailLogin"
          :disabled="isLoading || !emailOrUsername || !password"
          class="w-full py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-sm shadow-lg shadow-amber-500/20 disabled:opacity-50 transition-all"
        >
          <span v-if="isLoading">در حال بررسی اطلاعات...</span>
          <span v-else>ورود با حساب کاربری</span>
        </button>
      </div>

      <!-- Mode 3: Register -->
      <div v-else class="space-y-3">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">نام و نام خانوادگی</label>
          <input
            v-model="registerName"
            type="text"
            placeholder="مثال: علی احمدی"
            class="w-full px-3 py-2 rounded-xl bg-studio-dark border border-wood-800 text-white text-sm focus:outline-none focus:border-amber-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">شماره تماس (جهت هماهنگی کلاس‌ها)</label>
          <input
            v-model="registerPhone"
            type="tel"
            dir="ltr"
            placeholder="09121234567"
            class="w-full px-3 py-2 rounded-xl bg-studio-dark border border-wood-800 text-white text-sm font-mono focus:outline-none focus:border-amber-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">ایمیل (اختیاری)</label>
          <input
            v-model="registerEmail"
            type="email"
            dir="ltr"
            placeholder="student@example.com"
            class="w-full px-3 py-2 rounded-xl bg-studio-dark border border-wood-800 text-white text-sm focus:outline-none focus:border-amber-500"
          />
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">رمز عبور (حداقل ۶ کاراکتر)</label>
          <input
            v-model="registerPassword"
            type="password"
            placeholder="••••••••"
            class="w-full px-3 py-2 rounded-xl bg-studio-dark border border-wood-800 text-white text-sm focus:outline-none focus:border-amber-500"
          />
        </div>

        <button
          @click="handleRegister"
          :disabled="isLoading || !registerName || !registerPhone || !registerPassword"
          class="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-bold text-sm shadow-lg shadow-amber-500/20 disabled:opacity-50 transition-all mt-2"
        >
          <span v-if="isLoading">در حال ثبت‌نام...</span>
          <span v-else>تکمیل ثبت‌نام و ورود</span>
        </button>
      </div>

    </div>
  </div>
</template>
