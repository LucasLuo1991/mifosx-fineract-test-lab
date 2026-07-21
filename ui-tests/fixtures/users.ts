import { randomUUID } from 'crypto';
import type { CreateUserRequest } from '../api/users-endpoint.js';

export const users = {
    'default-user': {
        email: 'newuser.{unique}@mifos.org',
        firstname: 'Test',
        isLoginRetriesEnabled: true,
        isPasswordResetAllowed: true,
        lastname: 'User',
        officeId: 1,
        password: 'MifosUser123!',
        passwordNeverExpires: true,
        repeatPassword: 'MifosUser123!',
        roles: [1],
        sendPasswordToEmail: false,
        username: 'newuser{unique}',
    },
} satisfies Record<string, CreateUserRequest>;

type UserFixtureKey = keyof typeof users;

export function buildUser(key: UserFixtureKey = 'default-user', overrides: Partial<CreateUserRequest> = {}): CreateUserRequest {
    const fixture = users[key];

    if (!fixture) {
        throw new Error(`User fixture "${key}" was not found.`);
    }

    return applyUniqueToken({ ...fixture, ...overrides });
}

function applyUniqueToken(user: CreateUserRequest): CreateUserRequest {
    const unique = `${Date.now()}${randomUUID().replaceAll('-', '').slice(0, 3)}`;

    return {
        ...user,
        email: user.email.replaceAll('{unique}', unique),
        firstname: user.firstname.replaceAll('{unique}', unique),
        lastname: user.lastname.replaceAll('{unique}', unique),
        password: user.password.replaceAll('{unique}', unique),
        repeatPassword: user.repeatPassword.replaceAll('{unique}', unique),
        roles: [...user.roles],
        username: user.username.replaceAll('{unique}', unique),
    };
}
