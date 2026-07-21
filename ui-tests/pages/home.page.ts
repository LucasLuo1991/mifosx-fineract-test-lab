import { type Locator, type Page, expect } from '@playwright/test';
import { tenantId } from '../support/env.js';
import { routes } from '../support/routes.js';
import { BasePage } from './base.page.js';

export class HomePage extends BasePage {
    private readonly closeWarningButton: Locator;
    private readonly authWarning: Locator;
    private readonly sidebarToggleButton: Locator;
    private readonly signOutButton: Locator;

    constructor(page: Page) {
        super(page, routes.home);
        this.closeWarningButton = this.page.locator('mifosx-warning-dialog').getByRole('button', { name: 'Close' });
        this.authWarning = this.page.getByText('This system is for authorized use only.');
        this.sidebarToggleButton = this.page.getByRole('button', { description: 'Toggle Collapse', exact: true });
        this.signOutButton = this.page.getByRole('button', { description: 'Sign Out', exact: true });
    }

    private loginSuccessToast(username: string): Locator {
        return this.page.getByText(`${username} successfully logged in!`);
    }

    private welcomeMessage(username: string): Locator {
        return this.page.getByText(`Welcome ${username} to ${tenantId}`);
    }

    async expectAuthWarning() {
        await expect(this.authWarning).toBeVisible();
    }

    async dismissAuthWarning() {
        await this.expectAuthWarning();
        await this.closeWarningButton.click();
        await expect(this.authWarning).not.toBeVisible();
    }

    async signOut() {
        await this.sidebarToggleButton.click();
        await this.signOutButton.click();
    }

    async expectLoginSuccessToast(username: string) {
        const loginSuccessToast = this.loginSuccessToast(username);

        await expect(loginSuccessToast).toBeVisible();
        await expect(loginSuccessToast).not.toBeVisible();
    }

    async expectWelcomeMessage(username: string) {
        await expect(this.welcomeMessage(username)).toBeVisible();
    }
}
