import { defineConfig } from '@playwright/test'
import { existsSync } from 'node:fs'

export default defineConfig({
  testDir: './tests',
  timeout: 40000,
  workers: 2,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4175',
    headless: true,
    launchOptions: {
      ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : existsSync('/usr/bin/chromium') ? { executablePath: '/usr/bin/chromium' } : {}),
      args: ['--no-sandbox'],
    },
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run preview',
    url: 'http://127.0.0.1:4175',
    reuseExistingServer: !process.env.CI,
  },
})
