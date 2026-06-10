import type { Page } from '@playwright/test';

export class LoginPage {
  constructor(private readonly page: Page) { }

  async goto() {
    await this.page.goto('/#/login');
  }

  async login(username: string, password: string) {
    await this.page.getByLabel('Username').fill(username);
    await this.page.getByLabel('Password').fill(password);
    await this.page.locator('.m3-button-container--full-width').click();
  }
}
