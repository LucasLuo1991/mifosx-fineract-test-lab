import { test as base, expect } from '@playwright/test';
import { PageManager } from '../pages/page.manager.js';
import { addAuthSessionStorage } from '../support/auth.js';

type TestFixtures = {
  pageManager: PageManager;
};

export const test = base.extend<TestFixtures>({
  context: async ({ browser, contextOptions }, use, testInfo) => {
    const context = await browser.newContext(contextOptions);

    if (testInfo.project.name !== 'auth-setup') {
      await addAuthSessionStorage(context);
    }

    await use(context);
    await context.close();
  },

  pageManager: async ({ page }, use) => {
    await use(new PageManager(page));
  },
});

export { expect };
