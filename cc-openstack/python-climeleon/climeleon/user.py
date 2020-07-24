from operator import attrgetter

from keystoneauth1.exceptions import NotFound

from climeleon.base import BaseCommand
from climeleon.util import column_align


class UserInspectCommand(BaseCommand):

    def register_args(self, parser):
        parser.add_argument("user", metavar="USER",
            help=("The user name or ID"))

    def run(self):
        user = self.args.user
        region_name = self.args.os_region_name
        keystone = self.keystone()

        query = {}
        try:
            ks_user = keystone.users.get(user)
            query['name'] = ks_user.name
        except NotFound:
            query['name'] = user

        # For some reason Keystone can return multiple copies of federated
        # users--this seems like an API bug. Use a map to require uniqueness.
        user_ids = set(user.id for user in keystone.users.list(**query))

        report_lines = [
            f'User: {user}',
            f'Found {len(user_ids)} user account(s).',
        ]

        for user_id in user_ids:
            user = keystone.users.get(user_id)
            is_federated = user.domain_id != 'default'
            projects = sorted(keystone.projects.list(user=user), key=attrgetter('name'))
            project_lines = [
                f' - {p.name or p.id}' for p in projects
            ] or [' (none)']
            report_lines.extend([
                '-'*60,
                f'ID: {user.id}',
                f'Name: {user.name}',
                f'Domain: {user.domain_id}',
                f'Federated: {is_federated}',
                'Projects:', '\n'.join(project_lines),
            ])

        print('\n'.join(report_lines))
