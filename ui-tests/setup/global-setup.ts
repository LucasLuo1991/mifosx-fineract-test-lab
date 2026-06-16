import dotenv from 'dotenv';
import path from 'path';
import process from 'process';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

dotenv.config({ path: path.resolve(__dirname, '../../.env'), quiet: true });

const HEALTH_PATH = '/fineract-provider/actuator/health';

type HealthResponse = {
    status?: unknown;
};

export async function waitForHealthCheck(
    healthUrl = buildFineractHealthUrl(),
    maxAttempts = 10,
    delaySeconds = 30,
    timeoutSeconds = 5,
): Promise<void> {
    for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
        try {
            const response = await fetchWithTimeout(healthUrl, timeoutSeconds);
            if (await isHealthyResponse(response)) {
                return;
            }
        } catch {
            // Retry until the health check budget expires.
        }

        if (attempt < maxAttempts - 1) {
            await sleep(delaySeconds * 1000);
        }
    }

    throw new Error(`Service did not become healthy at ${healthUrl}.`);
}

function buildFineractHealthUrl(): string {
    const serverUrl = process.env.SERVER_URL || `http://localhost:${process.env.FINERACT_PORT || '3000'}`;
    return `${serverUrl.replace(/\/+$/, '')}${HEALTH_PATH}`;
}

async function fetchWithTimeout(url: string, timeoutSeconds: number): Promise<Response> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutSeconds * 1000);

    try {
        return await fetch(url, { signal: controller.signal });
    } finally {
        clearTimeout(timeout);
    }
}

async function isHealthyResponse(response: Response): Promise<boolean> {
    if (response.status !== 200) {
        return false;
    }

    const body: unknown = await response.json();
    return isHealthResponse(body) && body.status === 'UP';
}

function isHealthResponse(body: unknown): body is HealthResponse {
    return typeof body === 'object' && body !== null && !Array.isArray(body);
}

function sleep(milliseconds: number): Promise<void> {
    return new Promise((resolve) => {
        setTimeout(resolve, milliseconds);
    });
}

export default async function globalSetup(): Promise<void> {
    await waitForHealthCheck();
}
