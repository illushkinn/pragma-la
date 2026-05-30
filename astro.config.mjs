import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'

export default defineConfig({
  site: 'https://pragma.med',
  output: 'static',
  integrations: [sitemap()],
  build: {
    format: 'file',
  },
})
