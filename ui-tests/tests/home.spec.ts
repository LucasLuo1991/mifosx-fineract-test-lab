import { test } from '../fixtures/test.js';

test('should show auth warning', async ({ pageManager }) => {
    const homePage = pageManager.home;
    await homePage.goto();
    await homePage.expectAuthWarning();
    await homePage.dismissAuthWarning();
});

test('should log out', async ({ pageManager }) => {
    const homePage = pageManager.home;
    const loginPage = pageManager.login;
    await homePage.goto();
    await homePage.dismissAuthWarning();
    await homePage.signOut();
    await loginPage.expectUrl();
});