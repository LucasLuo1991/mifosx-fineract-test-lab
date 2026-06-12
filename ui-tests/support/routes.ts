export const routes = {
    login: '/#/login',
    home: '/#/home',
    clients: {
        list: '/#/clients',
        create: '/#/clients/create',
        details: (clientId: number | string) => `/#/clients/${clientId}`,
        edit: (clientId: number | string) => `/#/clients/${clientId}/edit`,
    },
} as const;