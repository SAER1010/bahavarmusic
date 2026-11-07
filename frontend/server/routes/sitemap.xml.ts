export default defineEventHandler((event) => {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl || 'https://bahavarmusic.com'
  const currentDate = new Date().toISOString().split('T')[0]

  const staticRoutes = [
    { loc: '/', priority: '1.0', changefreq: 'daily' },
    { loc: '/repertoire', priority: '0.9', changefreq: 'weekly' },
    { loc: '/booking', priority: '0.9', changefreq: 'weekly' },
    { loc: '/shop', priority: '0.9', changefreq: 'daily' },
    { loc: '/blog', priority: '0.8', changefreq: 'weekly' },
  ]

  const initialSlugs = [
    { loc: '/repertoire/asturias-leyenda-bahavar-arrangement', priority: '0.8' },
    { loc: '/repertoire/romance-anonimo-spanish-romance', priority: '0.8' },
    { loc: '/repertoire/navaye-karevan-acoustic-arrangement', priority: '0.8' },
    { loc: '/shop/alhambra-7fp-flamenco-negra', priority: '0.8' },
    { loc: '/shop/masterclass-right-hand-flamenco-acoustic', priority: '0.9' },
    { loc: '/blog/secrets-of-flamenco-rasgueado', priority: '0.7' },
    { loc: '/blog/spruce-vs-cedar-soundboard-guide', priority: '0.7' },
  ]

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticRoutes
  .map(
    (route) => `  <url>
    <loc>${siteUrl}${route.loc}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>${route.changefreq}</changefreq>
    <priority>${route.priority}</priority>
  </url>`
  )
  .join('\n')}
${initialSlugs
  .map(
    (route) => `  <url>
    <loc>${siteUrl}${route.loc}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>${route.priority}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`

  setHeader(event, 'content-type', 'application/xml; charset=utf-8')
  return sitemapXml
})
