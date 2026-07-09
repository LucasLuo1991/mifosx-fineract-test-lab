import type { APIRequestContext, APIResponse } from '@playwright/test';
import { BaseEndpoint } from './base-endpoint.js';

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

export class UsersEndpoint extends BaseEndpoint {
    constructor(getRequestContext: () => Promise<APIRequestContext>) {
        super(getRequestContext);
    }

    async create(user: CreateUserRequest): Promise<APIResponse> {
        return this.post('v1/users', user);
    }
}
