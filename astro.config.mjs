import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'
import vercel from '@astrojs/vercel'

export default defineConfig({
  site: 'https://pragma.med',
  output: 'static',
  adapter: vercel({ webAnalytics: { enabled: false } }),
  integrations: [sitemap()],
  server: { port: 4322 },
})
