import type { APIRequestContext, APIResponse } from '@playwright/test';

type RequestOptions = NonNullable<Parameters<APIRequestContext['fetch']>[1]>;
type RequestContextProvider = () => Promise<APIRequestContext>;

export class BaseEndpoint {
    constructor(private readonly getRequestContext: RequestContextProvider) {
    }

    protected async get(endpoint: string, expectedStatus = 200, options: RequestOptions = {}): Promise<APIResponse> {
        return this.sendRequest('GET', endpoint, expectedStatus, options);
    }

    protected async post(
        endpoint: string,
        data: unknown,
        expectedStatus = 200,
        options: RequestOptions = {},
    ): Promise<APIResponse> {
        return this.sendRequest('POST', endpoint, expectedStatus, { ...options, data });
    }

    protected async put(
        endpoint: string,
        data: unknown,
        expectedStatus = 200,
        options: RequestOptions = {},
    ): Promise<APIResponse> {
        return this.sendRequest('PUT', endpoint, expectedStatus, { ...options, data });
    }

    private async sendRequest(
        method: string,
        endpoint: string,
        expectedStatus: number,
        options: RequestOptions,
    ): Promise<APIResponse> {
        const requestContext = await this.getRequestContext();
        const normalizedEndpoint = endpoint.replace(/^\/+/, '');
        const response = await requestContext.fetch(normalizedEndpoint, {
            ...options,
            method,
        });

        if (response.status() !== expectedStatus) {
            const body = await response.text();
            throw new Error(
                `Expected status ${expectedStatus} but got ${response.status()} for ${method} ${normalizedEndpoint}: ${body}`,
            );
        }

        return response;
    }
}

export async function parseJsonResponse<T = unknown>(response: APIResponse): Promise<T | null> {
    const body = await response.text();

    if (!response.ok()) {
        throw new Error(`Fineract API request failed: ${response.status()} ${response.statusText()}\n${body}`);
    }

    const contentType = response.headers()['content-type'] || '';

    if (!contentType.includes('application/json')) {
        throw new Error(`Expected JSON response but received "${contentType || 'unknown'}"\n${body}`);
    }

    return body ? JSON.parse(body) as T : null;
}
