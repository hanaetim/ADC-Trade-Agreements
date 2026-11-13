import { defineConfig } from '@playwright/test';

/**
 * Playwright configuration for E2E tests
 * Uses E2E_BACKEND_PORT and E2E_FRONTEND_PORT from environment
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: 'html',
  timeout: Number(process.env.E2E_TEST_TIMEOUT ?? 30_000),
  
  use: {
    baseURL: `http://127.0.0.1:${process.env.E2E_FRONTEND_PORT ?? '5173'}`,
    trace: 'on-first-retry',
    actionTimeout: Number(process.env.E2E_ACTION_TIMEOUT ?? 10_000),
    navigationTimeout: Number(process.env.E2E_NAVIGATION_TIMEOUT ?? 15_000),
  },

  webServer: [
    // Backend server
    {
      command: `${process.env.E2E_PYTHON ?? 'python'} -m alembic upgrade head && ${process.env.E2E_PYTHON ?? 'python'} -m app.seed && ${process.env.E2E_PYTHON ?? 'python'} -m uvicorn app.main:app --host 127.0.0.1 --port ${process.env.E2E_BACKEND_PORT ?? '9000'}`,
      cwd: '../backend',
      url: `http://127.0.0.1:${process.env.E2E_BACKEND_PORT ?? '9000'}/api/v1/health`,
      reuseExistingServer: false,
      timeout: 180_000,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        DATABASE_URL: process.env.E2E_DATABASE_URL ?? 'sqlite:///./e2e.db',
        RATE_LIMIT_ENABLED: 'false',
      },
    },
    // Frontend dev server
    {
      command: `npm run dev -- --host 127.0.0.1 --port ${process.env.E2E_FRONTEND_PORT ?? '5173'} --strictPort`,
      url: `http://127.0.0.1:${process.env.E2E_FRONTEND_PORT ?? '5173'}`,
      reuseExistingServer: false,
      timeout: 180_000,
      stdout: 'pipe',
      stderr: 'pipe',
      env: {
        BACKEND_PORT: process.env.E2E_BACKEND_PORT ?? '9000',
      },
    },
  ],
});
