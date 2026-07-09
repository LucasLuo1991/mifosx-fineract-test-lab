import type { BrowserContext, Page } from '@playwright/test';
import { mkdir, readFile, writeFile } from 'fs/promises';
import path from 'path';

export const authStorageStateFile = 'playwright/.auth/user.json';
export const authSessionStorageStateFile = 'playwright/.auth/session.json';

export async function saveAuthSessionStorage(page: Page) {
    const sessionStorage = await page.evaluate(() => JSON.stringify(window.sessionStorage));

    await mkdir(path.dirname(authSessionStorageStateFile), { recursive: true });
    await writeFile(authSessionStorageStateFile, sessionStorage, 'utf-8');
}

export async function addAuthSessionStorage(context: BrowserContext) {
    const sessionStorage = await readFile(authSessionStorageStateFile, 'utf-8')
        .then((value) => JSON.parse(value) as Record<string, string>)
        .catch(() => undefined);

    if (!sessionStorage) {
        return;
    }

    await context.addInitScript((storage) => {
        for (const [key, value] of Object.entries(storage)) {
            window.sessionStorage.setItem(key, value);
        }
    }, sessionStorage);
}
