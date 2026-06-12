import type { Page } from '@playwright/test';
import { routes } from '../support/routes.js';
import { BasePage } from './base.page.js';


export class HomePage extends BasePage {
    constructor(page: Page) {
        super(page, routes.home);
    }
}
