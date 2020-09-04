import json

from constants import resource_constants, verb_constants
from tasks import FUNCTION_MAPPING

VERBS = verb_constants.verbs
RESOURCES = resource_constants.resources


def file_loader(file_path):
    with open(file_path, 'r') as file_buffer:
        return json.load(file_buffer)


class ResultNames:
    def __init__(self):
        self.name_set = []

    def add_name(self, name, func, verbs, resources, verb_str, resource_str, cluster=False):
        self.name_set.append({
            'name': name,
            'cluster': cluster,
            'func': func.__name__,
            'verbs': verbs,
            'resources': resources,
            'verb_str': verb_str,
            'resource_str': resource_str
        })

    def get_names(self):
        """
        Return enumerated list of index, name pairs
        """
        return [(num, _['name']) for num, _ in enumerate(self.name_set)]

    def get_name_by_index(self, index):
        return self.name_set[index]


class RoleCheck:
    def __init__(self, file_path, result_names, cluster=False):
        """
        :param file_path: Can be changed to a string in future for making it REST compatible
        :param result_names: ResultNames
        """
        self.cluster = cluster
        self.roles = file_loader(file_path=file_path)
        self.result_names = result_names
        self.roles_checker()

    @staticmethod
    def _helper(collection, item):
        """
        Helper to handle the process of iterating the collections
        :param collection:  Verb dict collection or Resource dict collection
        :param item: the verb/resource in question
        """
        value = ''
        for k, v in collection.items():
            if set(v) == set(item):
                value = k
                break
        return value

    def roles_checker(self):
        """
        Method which iterates over the file/streams items and further handles the checking
        """
        for role_item in self.roles['items']:
            role_name = role_item['metadata']['name']
            for roles_rule in role_item['rules']:
                if all(map(lambda x: x in roles_rule.keys(), ('verbs', 'resources'))):
                    role_verbs = roles_rule['verbs']
                    role_resources = roles_rule['resources']
                    self.role_check(verbs=role_verbs, resources=role_resources, role_name=role_name)

    def role_check(self, verbs, resources, role_name):
        """
        Method to filter the method into the theoretical funcs(admin, admin_read, etc) based on verbs and resources in
        Roles and ClusterRoles 'items'
        :type verbs: list
        """
        # if tuple(verbs) in VERBS.keys():
        #     verb_str = VERBS[verbs]
        # if resources != "" and tuple(resources) in RESOURCES.keys():
        #     resource_str = RESOURCES[resources]

        verb_str, resource_str = [self._helper(*args) for args in ((VERBS, verbs), (RESOURCES, resources))]
        if verb_str and resource_str:
            function_ = FUNCTION_MAPPING.get((verb_str, resource_str), lambda x, y: print('Invalid', x, y, verb_str, resource_str))
            function_(role_name, self.cluster)
            self.result_names.add_name(name=role_name, func=function_, verbs=verbs,
                                       resources=resources, verb_str=verb_str, resource_str=resource_str,
                                       cluster=self.cluster)


class BindingCheck:
    def __init__(self, file_path, result_names, cluster=False):
        self.cluster = cluster
        self.bindings = file_loader(file_path=file_path)
        self.result_names = result_names
        self.verify_bindings()

    def verify_bindings(self):
        """
        Verifies for each binding if a role_name or cluster_role_name parsed earlier is found
        """
        role_names = self.result_names.get_names()
        for binding in self.bindings['items']:
            if any(map(lambda x: x in binding.keys(), ('subjects',))):
                binding_name = binding["roleRef"]["name"]  # Actually the role name bound to
                binding_kind = binding["roleRef"]['kind']
                for subject in binding["subjects"]:
                    if "namespace" in subject.keys():
                        binding_namespace = subject["namespace"]  # Should be metadata.namespace but (?)

                        matched_role_names = [i for i in role_names if i[1] == binding_name]
                        map(lambda x:
                            FUNCTION_MAPPING.get((x['verb_str'], x['resource_str']))
                                (binding_name, binding_kind, binding_namespace, x['verbs'], self.cluster),
                            [self.result_names.name_set[index] for index, _ in matched_role_names]
                            )
