export const useSeoSchema = () => {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl || 'https://bahavarmusic.com'

  const injectPersonSchema = () => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': ['Person', 'MusicGroup'],
            name: 'بهاور | Bahavar',
            alternateName: 'Bahavar Music',
            url: siteUrl,
            image: `${siteUrl}/images/bahavar-profile.jpg`,
            jobTitle: ['موزیسین', 'آهنگساز', 'مدرس ارشد گیتار', 'تولیدکننده موسیقی استودیو'],
            genre: ['Flamenco', 'Classical Guitar', 'Contemporary Acoustic', 'Persian Fusion'],
            description: 'بهاور، نوازنده، آهنگساز و مدرس گیتار کلاسیک و فلامنکو و مدیر استودیو آکوستیک ضبط صدا.',
            sameAs: [
              'https://instagram.com/bahavarmusic',
              'https://t.me/bahavarmusic',
              'https://youtube.com/@BahavarMusicOfficial',
              'https://soundcloud.com/bahavarmusic',
            ],
          }),
        },
      ],
    })
  }

  const injectProductSchema = (product: {
    title: string
    description: string
    price: number
    discount_price?: number
    is_in_stock: boolean
    cover_image?: string
    slug: string
  }) => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Product',
            name: product.title,
            description: product.description,
            image: product.cover_image || `${siteUrl}/images/placeholder-product.jpg`,
            offers: {
              '@type': 'Offer',
              price: product.discount_price || product.price,
              priceCurrency: 'IRR',
              availability: product.is_in_stock
                ? 'https://schema.org/InStock'
                : 'https://schema.org/OutOfStock',
              url: `${siteUrl}/shop/${product.slug}`,
            },
          }),
        },
      ],
    })
  }

  const injectCourseSchema = (course: {
    title: string
    description: string
    price: number
    slug: string
  }) => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Course',
            name: course.title,
            description: course.description,
            provider: {
              '@type': 'Person',
              name: 'بهاور',
              sameAs: siteUrl,
            },
            offers: {
              '@type': 'Offer',
              price: course.price,
              priceCurrency: 'IRR',
              category: 'Paid',
            },
          }),
        },
      ],
    })
  }

  const injectMusicCompositionSchema = (piece: {
    title: string
    persian_title: string
    composer: string
    genre: string
    audio_stream_url?: string
    slug: string
  }) => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'MusicComposition',
            name: piece.persian_title,
            alternateName: piece.title,
            composer: {
              '@type': 'Person',
              name: piece.composer,
            },
            genre: piece.genre,
            url: `${siteUrl}/repertoire/${piece.slug}`,
            recordedAs: piece.audio_stream_url
              ? {
                  '@type': 'MusicRecording',
                  name: piece.persian_title,
                  url: piece.audio_stream_url,
                }
              : undefined,
          }),
        },
      ],
    })
  }

  const injectArticleSchema = (article: {
    title: string
    excerpt: string
    author_name: string
    published_at: string
    featured_image?: string
    slug: string
  }) => {
    useHead({
      script: [
        {
          type: 'application/ld+json',
          children: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Article',
            headline: article.title,
            description: article.excerpt,
            author: {
              '@type': 'Person',
              name: article.author_name || 'بهاور',
            },
            datePublished: article.published_at,
            image: article.featured_image || `${siteUrl}/images/default-blog.jpg`,
            mainEntityOfPage: `${siteUrl}/blog/${article.slug}`,
          }),
        },
      ],
    })
  }

  return {
    injectPersonSchema,
    injectProductSchema,
    injectCourseSchema,
    injectMusicCompositionSchema,
    injectArticleSchema,
  }
}
