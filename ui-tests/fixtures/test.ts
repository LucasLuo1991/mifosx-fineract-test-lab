import { test as base, expect } from '@playwright/test';
import { ApiClient } from '../api/client.js';
import { PageManager } from '../pages/page.manager.js';
import { addAuthSessionStorage } from '../support/auth.js';
import { buildUser } from './users.js';

type TestFixtures = {
  apiClient: ApiClient;
  buildUser: typeof buildUser;
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

  apiClient: async ({}, use) => {
    const apiClient = new ApiClient();

    try {
      await use(apiClient);
    } finally {
      await apiClient.dispose();
    }
  },

  buildUser: async ({}, use) => {
    await use(buildUser);
  },
});

export { expect };
