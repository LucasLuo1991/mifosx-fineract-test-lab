import { request, type APIRequestContext } from '@playwright/test';
import { apiBaseUrl, apiCredentials, tenantId } from '../support/env.js';
import { UsersEndpoint } from './users-endpoint.js';

export { parseJsonResponse } from './base-endpoint.js';
export { UsersEndpoint, type CreateUserRequest } from './users-endpoint.js';

export class ApiClient {
    readonly users: UsersEndpoint;
    private requestContext?: APIRequestContext;

    constructor() {
        this.users = new UsersEndpoint(() => this.ensureRequest());
    }

    async dispose(): Promise<void> {
        await this.requestContext?.dispose();
        this.requestContext = undefined;
    }

    private async ensureRequest(): Promise<APIRequestContext> {
        if (!this.requestContext) {
            this.requestContext = await request.newContext({
                baseURL: apiBaseUrl,
                extraHTTPHeaders: {
                    'Authorization': `Basic ${Buffer.from(`${apiCredentials.username}:${apiCredentials.password}`).toString('base64')}`,
                    'fineract-platform-tenantid': tenantId,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            });
        }

        return this.requestContext;
    }
}
