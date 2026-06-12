import { type Page, expect } from '@playwright/test';

export abstract class BasePage {
    protected constructor(protected readonly page: Page,
        protected readonly route: string) { }

    async goto() {
        await this.page.goto(this.route);
    }

    async expectUrl() {
        await expect(this.page).toHaveURL(this.route);
    }
}