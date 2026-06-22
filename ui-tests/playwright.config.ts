import { defineConfig, devices } from '@playwright/test';
import process from 'process';
import { fileURLToPath } from 'url';
import { authStorageStateFile } from './support/auth.js';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
import dotenv from 'dotenv';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

dotenv.config({ path: path.resolve(__dirname, '../.env'), quiet: true });

const isCI = !!process.env.CI;
const webAppBaseUrl = process.env.WEB_APP_URL || `http://localhost:${process.env.WEB_APP_PORT || '4200'}`;

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
