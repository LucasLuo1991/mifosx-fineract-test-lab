import { test } from '../fixtures/test.js';
import { PageManager } from '../pages/page.manager.js';

test('should log in as a newly created user', async ({ browser, apiClient, buildUser }) => {
    // Use a fresh context so the test starts unauthenticated.
    const context = await browser.newContext();

    try {
        const page = await context.newPage();
        const pageManager = new PageManager(page);
        const loginPage = pageManager.login;
        const homePage = pageManager.home;
        const newUser = buildUser();

        await apiClient.users.create(newUser);
        await loginPage.goto();
        await loginPage.expectUrl();
        await loginPage.login(newUser.username, newUser.password);
        await homePage.expectUrl();
        await homePage.dismissAuthWarning();
        await homePage.expectWelcomeMessage(newUser.username);
    } finally {
        await context.close();
    }
});

test('should not log in with invalid credentials', async ({ browser }) => {
    // Use a fresh context so the test starts unauthenticated.
    const context = await browser.newContext();

    try {
        const page = await context.newPage();
        const pageManager = new PageManager(page);
        const loginPage = pageManager.login;

        await loginPage.goto();
        await loginPage.expectUrl();
        await loginPage.login('invalid-username', 'invalid-password');
        await loginPage.expectLoginFailedToast();
        await loginPage.expectLoginFormCleared();
        await loginPage.expectUrl();
    } finally {
        await context.close();
    }
});