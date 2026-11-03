import { existsSync } from 'node:fs';
import { defineConfig, devices } from '@playwright/test';

const API_PORT = 8010;
const WEB_PORT = 5180;
const venvPython = '../../.venv/bin/python';
const python = process.env.E2E_PYTHON || (existsSync(venvPython) ? venvPython : 'python');

export default defineConfig({
  testDir: './e2e',
  // One shared backend with an in-memory DB, so specs run in order.
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  use: {
    baseURL: `http://127.0.0.1:${WEB_PORT}`,
    headless: true,
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      // LLM_PROVIDER=fake is TEST-ONLY: scripted fixture responses, no API calls.
      command: `${python} -m uvicorn backend.main:get_app --factory --port ${API_PORT}`,
      cwd: '..',
      url: `http://127.0.0.1:${API_PORT}/health`,
      env: {
        LLM_PROVIDER: 'fake',
        DB_PATH: ':memory:',
        WEB_ORIGINS: `http://127.0.0.1:${WEB_PORT}`,
      },
      reuseExistingServer: false,
      timeout: 60_000,
    },
    {
      command: `npx vite --port ${WEB_PORT} --strictPort --host 127.0.0.1`,
      url: `http://127.0.0.1:${WEB_PORT}`,
      env: { VITE_API_TARGET: `http://127.0.0.1:${API_PORT}` },
      reuseExistingServer: false,
      timeout: 60_000,
    },
  ],
});
