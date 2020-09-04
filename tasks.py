def admin(role_name, cluster=False):
    print(f"{role_name} is {'a cluster' if cluster else 'an '}admin role")


def admin_read(role_name, cluster=False):
    print(f"{role_name} is {'a cluster' if cluster else 'an '}admin read role")


def destructive(role_name, cluster=False):
    print(f"{role_name} is a Destructive {'cluster ' if cluster else ''} role")


def secrets(role_name, cluster=False):
    print(f"{role_name} {'cluster' if cluster else ''}role can play with secrets")


def admin_binding(role_name, kind, namespace, cluster=False):
    print(f"{kind} {role_name} has Admin Privileges in namespace {namespace if namespace else 'Cluster' if cluster else ''}")


def admin_read_binding(role_name, kind, namespace, cluster=False):
    print(f"{kind} {role_name} has Read Admin Privileges in namespace {namespace if namespace else 'Cluster' if cluster else ''}")


def destructive_binding(role_name, kind, namespace, verbs, cluster=False):
    print(f"{kind} {role_name} has privileges to {','.join(verbs)} secrets in namespace {namespace if namespace else 'Cluster' if cluster else ''}")


def secrets_binding(role_name, kind, namespace, verbs, cluster=False):
    print(f"{kind} {role_name} has privileges to {','.join(verbs)} secrets in namespace {namespace if namespace else 'Cluster' if cluster else ''}")


def impersonate(role_name, cluster=False):
    pass

# Mapping for roles: (verb, resource)
# Mapping for bindings: (verb, resource, binding)

FUNCTION_MAPPING = {
    ('admin', 'admin'):                 admin,
    ('admin_read', 'admin'):            admin_read,
    ('destructive', 'destructive'):     destructive,
    ('secrets', 'secrets'):             secrets,
    ('admin', 'admin', 'binding'):      admin_binding,
    ('admin_read', 'admin', 'binding'): admin_binding,
    ('secrets', 'secrets', 'binding'):  secrets_binding,
}
