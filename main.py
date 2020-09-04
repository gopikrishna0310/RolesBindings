import argparse

from classes import BindingCheck, ResultNames, RoleCheck


def args_parser():
    parser = argparse.ArgumentParser(description="Pass files to verify roles and their bindings in cluster and standalone")
    parser.add_argument('--cluster_role', '-cr', type=str, required=False, help='Cluster roles JSON', )
    parser.add_argument('--role', '-r', type=str, required=False, help='Roles JSON')
    parser.add_argument('--role_bindings', '-rb', type=str, required=False, help='Role Bindings JSON')
    parser.add_argument('--cluster_role_bindings', '-crb', type=str, required=False, help='Cluster Role Bindings JSON')
    return parser.parse_args()


if __name__ == '__main__':
    args = args_parser()
    result_names = ResultNames()

    if args.role:
        print("Starting ROLES")
        RoleCheck(file_path=args.role, result_names=result_names, cluster=False)
    if args.cluster_role:
        print("Starting CLUSTER ROLES")
        RoleCheck(file_path=args.cluster_role, result_names=result_names, cluster=True)
    if args.role_bindings:
        print("Starting ROLES BINDINGS")
        BindingCheck(file_path=args.role_bindings, result_names=result_names, cluster=False)
    if args.cluster_role_bindings:
        print("Starting CLUSTER ROLES BINDINGS")
        BindingCheck(file_path=args.cluster_role_bindings, result_names=result_names, cluster=True)
    print(result_names.name_set)
