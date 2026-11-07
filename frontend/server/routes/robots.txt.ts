export default defineEventHandler((event) => {
  const config = useRuntimeConfig()
  const siteUrl = config.public.siteUrl || 'https://bahavarmusic.com'

  const robots = `User-agent: *
Allow: /
Disallow: /dashboard/
Disallow: /auth/
Disallow: /api/

Sitemap: ${siteUrl}/sitemap.xml
`

  setHeader(event, 'content-type', 'text/plain; charset=utf-8')
  return robots
})
