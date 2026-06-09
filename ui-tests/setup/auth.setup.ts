import { test as setup, expect } from '@playwright/test';
import { authStorageStateFile } from '../support/auth.js';

setup('create authenticated storage state', async ({ page }) => {
  await page.goto('/#/login');
  await page.getByLabel('Username').fill('mifos');
  await page.getByLabel('Password').fill('password');
  await page.locator('.m3-button-container--full-width').click();
  await expect(page).toHaveURL('/#/home');
  await page.context().storageState({ path: authStorageStateFile });
});
