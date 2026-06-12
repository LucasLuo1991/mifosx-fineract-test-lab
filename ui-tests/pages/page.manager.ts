import type { Page } from '@playwright/test';
import { HomePage } from './home.page.js';
import { LoginPage } from './login.page.js';

export class PageManager {
  private readonly pages = new Map<string, unknown>();

  constructor(private readonly page: Page) { }

  get login(): LoginPage {
    return this.get('login', () => new LoginPage(this.page));
  }

  get home(): HomePage {
    return this.get('home', () => new HomePage(this.page));
  }

  private get<T>(name: string, createPage: () => T): T {
    if (!this.pages.has(name)) {
      this.pages.set(name, createPage());
    }

    return this.pages.get(name) as T;
  }
}
