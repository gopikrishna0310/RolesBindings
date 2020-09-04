verbs = {
    # '*':                ['admin', 'secrets'],
    # 'get':              ['admin_read', 'secrets'],
    # 'list':             ['admin_read', 'secrets'],
    # 'create':           ['secrets'],
    # 'update':           ['secrets'],
    # 'delete':           ['destructive'],
    # 'deletecollection': ['destructive']

    'admin': ['*'],
    'admin_read': ['get', 'list'],
    'destructive': ['delete'],
    'destructive_': ['deletecollection'],
    'secrets': ['*', 'get', 'list', 'update', 'create'],
}
