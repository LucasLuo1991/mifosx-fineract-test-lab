import { type Locator, type Page, expect } from '@playwright/test';
import { routes } from '../support/routes.js';
import { BasePage } from './base.page.js';

export class LoginPage extends BasePage {
  private readonly usernameInput: Locator;
  private readonly passwordInput: Locator;
  private readonly loginButton: Locator;
  private readonly loginFailedToast: Locator;
  private readonly userNameRequiredError: Locator;
  private readonly passwordRequiredError: Locator;

  constructor(page: Page) {
    super(page, routes.login);
    this.usernameInput = this.page.getByLabel('Username');
    this.passwordInput = this.page.getByLabel('Password');
    this.loginButton = this.page.getByRole('button', { name: 'Login' });
    this.loginFailedToast = this.page.getByText(' Your session has expired or the credentials are invalid.');
    this.userNameRequiredError = this.page.getByText('Username is required');
    this.passwordRequiredError = this.page.getByText('Password is required (min length 8)');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectLoginFailedToast() {
    await expect(this.loginFailedToast).toBeVisible();
    await expect(this.loginFailedToast).not.toBeVisible();
  }

  async expectLoginFormCleared() {
    await expect(this.usernameInput).toBeEmpty();
    await expect(this.passwordInput).toBeEmpty();
    await expect(this.userNameRequiredError).toBeVisible();
    await expect(this.passwordRequiredError).toBeVisible();
  }
}