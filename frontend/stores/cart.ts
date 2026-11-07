import { defineStore } from 'pinia'

export interface CartItem {
  id: number
  productId: number
  title: string
  price: number
  quantity: number
  coverImage?: string
  productType: string
  slug: string
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),

  getters: {
    totalCount: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),
    totalPrice: (state) => state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
  },

  actions: {
    initCart() {
      if (process.client) {
        const saved = localStorage.getItem('bahavar_cart')
        if (saved) {
          try {
            this.items = JSON.parse(saved)
          } catch (e) {
            console.error('Failed to parse cart', e)
          }
        }
      }
    },

    saveCart() {
      if (process.client) {
        localStorage.setItem('bahavar_cart', JSON.stringify(this.items))
      }
    },

    addItem(product: { id: number; title: string; price: number; cover_image?: string; product_type: string; slug: string }) {
      const existing = this.items.find((item) => item.productId === product.id)
      if (existing) {
        if (product.product_type === 'digital_course' || product.product_type === 'sheet_music') {
          // Digital products only need 1 quantity
          return
        }
        existing.quantity += 1
      } else {
        this.items.push({
          id: Date.now(),
          productId: product.id,
          title: product.title,
          price: product.price,
          quantity: 1,
          coverImage: product.cover_image,
          productType: product.product_type,
          slug: product.slug,
        })
      }
      this.saveCart()
    },

    removeItem(productId: number) {
      this.items = this.items.filter((item) => item.productId !== productId)
      this.saveCart()
    },

    updateQuantity(productId: number, quantity: number) {
      const item = this.items.find((i) => i.productId === productId)
      if (item) {
        if (quantity <= 0) {
          this.removeItem(productId)
        } else {
          item.quantity = quantity
          this.saveCart()
        }
      }
    },

    clearCart() {
      this.items = []
      this.saveCart()
    },
  },
})
