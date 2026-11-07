<script setup lang="ts">
import AppHeader from '~/components/layout/AppHeader.vue'
import AppFooter from '~/components/layout/AppFooter.vue'
import AuthModal from '~/components/auth/AuthModal.vue'
import PopupAdModal from '~/components/home/PopupAdModal.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-studio-dark text-slate-100 font-sans">
    <AppHeader />
    
    <main class="flex-grow pt-24 sm:pt-28">
      <slot />
    </main>

    <AppFooter />
    
    <AuthModal />
    <PopupAdModal />
  </div>
</template>
