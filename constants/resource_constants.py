resources = {
    # '*':                ['admin', 'secrets', 'admin_read'],
    # 'delete':           ['destructive'],
    # 'deletecollection': ['destructive'],
    # 'secrets':          ['secrets'],
    #
    'admin': ['*'],
    'admin_read': ['*'],
    'destructive': ['delete'],
    'destructive_': ['deletecollection'],
    'secrets': ['secrets'],
}
