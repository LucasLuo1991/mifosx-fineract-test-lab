import dotenv from 'dotenv';
import path from 'path';
import process from 'process';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

dotenv.config({ path: path.resolve(__dirname, '../../.env'), quiet: true });

const DEFAULT_API_PATH = '/fineract-provider/api';
const HEALTH_PATH = '/fineract-provider/actuator/health';

const fineractPort = process.env.FINERACT_PORT || '3000';
const webAppPort = process.env.WEB_APP_PORT || '4200';

export const isCI = !!process.env.CI;
export const webAppBaseUrl = process.env.WEB_APP_URL || `http://localhost:${webAppPort}`;
export const serverUrl = trimTrailingSlashes(process.env.SERVER_URL || `http://localhost:${fineractPort}`);
export const apiBaseUrl = buildApiBaseUrl();
export const fineractHealthUrl = `${serverUrl}${HEALTH_PATH}`;
export const tenantId = process.env.TENANT_ID || 'default';

export const apiCredentials = {
    username: process.env.API_USER || 'mifos',
    password: process.env.API_PASS || 'password',
};

export const loginCredentials = apiCredentials;

function buildApiBaseUrl(): string {
    const configuredApiBaseUrl = process.env.API_BASE_URL?.trim();

    if (configuredApiBaseUrl) {
        return `${configuredApiBaseUrl.replace(/\/+$/, '')}/`;
    }

    if (serverUrl.endsWith(DEFAULT_API_PATH)) {
        return `${serverUrl}/`;
    }

    return `${serverUrl}${DEFAULT_API_PATH}/`;
}

function trimTrailingSlashes(value: string): string {
    return value.replace(/\/+$/, '');
}
