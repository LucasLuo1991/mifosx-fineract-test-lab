import { expect, test as setup } from '../fixtures/test.js';
import {
  addAuthSessionStorage,
  authStorageStateFile,
  loginCredentials,
  saveAuthSessionStorage,
} from '../support/auth.js';

setup('create authenticated storage state', async ({ browser, page, pageManager }) => {
  const loginPage = pageManager.login;

  await setup.step('Login and save storage state', async () => {
    await loginPage.goto();
    await loginPage.login(loginCredentials.username, loginCredentials.password);
    await expect(page).toHaveURL('/#/home');
    await page.context().storageState({ path: authStorageStateFile });
    await saveAuthSessionStorage(page);
  });

  await setup.step('Verify storage state can be loaded', async () => {
    const testContext = await browser.newContext({storageState: authStorageStateFile });
    await addAuthSessionStorage(testContext);
    const testPage = await testContext.newPage();
    await testPage.goto('/#/home');
    await expect(testPage).not.toHaveURL('/#/login');
    await testContext.close();
  });
});
