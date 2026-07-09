import { request, type APIResponse } from '@playwright/test';
import { fineractHealthUrl } from '../support/env.js';

type HealthResponse = {
    status?: unknown;
};

export async function waitForHealthCheck(
    healthUrl = fineractHealthUrl,
    maxAttempts = 10,
    delaySeconds = 30,
    timeoutSeconds = 5,
): Promise<void> {
    const requestContext = await request.newContext();

    try {
        for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
            try {
                const response = await requestContext.fetch(healthUrl, {
                    timeout: timeoutSeconds * 1000,
                });

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
    } finally {
        await requestContext.dispose();
    }

    throw new Error(`Service did not become healthy at ${healthUrl}.`);
}

async function isHealthyResponse(response: APIResponse): Promise<boolean> {
    if (response.status() !== 200) {
        return false;
    }

    try {
        const body: unknown = await response.json();
        return isHealthResponse(body) && body.status === 'UP';
    } catch {
        return false;
    }
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
