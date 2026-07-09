import { defineConfig, devices } from '@playwright/test';
import { authStorageStateFile } from './support/auth.js';
import { isCI, webAppBaseUrl } from './support/env.js';

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  globalSetup: './setup/global-setup.ts',
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: isCI,
  /* Retry on CI only */
  retries: isCI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: isCI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: isCI
    ? [
        ['junit', { outputFile: 'test-results/playwright-results.xml' }],
        ['html', { outputFolder: 'playwright-report', open: 'never' }],
      ]
    : 'html',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
  },
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('')`. */
    baseURL: webAppBaseUrl,

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'retain-on-failure',
    screenshot: 'on',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'auth-setup',
      testDir: './setup',
      testMatch: /.*\.setup\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'authenticated-tests',
      dependencies: ['auth-setup'],
      use: {
        ...devices['Desktop Chrome'],
        storageState: authStorageStateFile,
      },
    },
  ],
});
