import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './visual-tests',

  timeout: 30000,

  reporter: 'list',

  use: {
    baseURL: 'http://127.0.0.1:8000',
    viewport: {
      width: 1365,
      height: 900,
    },
    headless: true,
  },

  projects: [
    {
      name: 'chromium',
      use: {
        browserName: 'chromium',
      },
    },
  ],

  webServer: {
    command: 'python -m uvicorn main:app --host 127.0.0.1 --port 8000',
    url: 'http://127.0.0.1:8000',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});