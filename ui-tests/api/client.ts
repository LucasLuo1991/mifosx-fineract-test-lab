import { request, type APIRequestContext, type APIResponse } from '@playwright/test';
import { fileURLToPath } from 'url';
import { apiBaseUrl, apiCredentials, tenantId } from '../support/env.js';

export type CreateUserRequest = {
    email: string;
    firstname: string;
    isLoginRetriesEnabled: boolean;
    isPasswordResetAllowed: boolean;
    lastname: string;
    officeId: number;
    password: string;
    passwordNeverExpires: boolean;
    repeatPassword: string;
    roles: number[];
    sendPasswordToEmail: boolean;
    username: string;
};

export class ApiClient {
    private request?: APIRequestContext;

    async init(): Promise<void> {
        if (this.request) {
            return;
        }

        this.request = await request.newContext({
            baseURL: apiBaseUrl,
            extraHTTPHeaders: {
                'Authorization': `Basic ${Buffer.from(`${apiCredentials.username}:${apiCredentials.password}`).toString('base64')}`,
                'fineract-platform-tenantid': tenantId,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        });
    }

    async createUser(user: CreateUserRequest): Promise<APIResponse> {
        const request = await this.ensureRequest();

        const response = await request.post('v1/users', {
            data: user,
        });
        return response;
    }

    async dispose(): Promise<void> {
        await this.request?.dispose();
        this.request = undefined;
    }

    private async ensureRequest(): Promise<APIRequestContext> {
        await this.init();
        return this.request!;
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

function buildExampleUser(): CreateUserRequest {
    const userSuffix = Date.now();
    const password = 'MifosUser123!';

    return {
        email: `newuser.${userSuffix}@mifos.org`,
        firstname: 'Test',
        isLoginRetriesEnabled: true,
        isPasswordResetAllowed: true,
        lastname: 'User',
        officeId: 1,
        password,
        passwordNeverExpires: true,
        repeatPassword: password,
        roles: [1],
        sendPasswordToEmail: false,
        username: `newuser${userSuffix}`,
    };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    const client = new ApiClient();
    try {
        const response = await client.createUser(buildExampleUser());
        const responseBody = await parseJsonResponse(response);
        console.log('User created:', responseBody);
    } finally {
        await client.dispose();
    }
}
