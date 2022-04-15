#!/usr/bin/env python3
# Copyright 2021-2022 NetCracker Technology Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from collections import OrderedDict

from kubemarine import admission
from kubemarine.core import flow

tasks = OrderedDict({
    "check_inventory": admission.check_inventory,
    "delete_default_pss": admission.delete_default_pss,
    "apply_default_pss": admission.apply_default_pss,
    "restart_pods": admission.restart_pods_task
})


def main(cli_arguments=None):

    cli_help = '''
    Script for managing pss on existing Kubernetes cluster.

    How to use:

    '''

    parser = flow.new_parser(cli_help)
    parser.add_argument('--tasks',
                        default='',
                        help='define comma-separated tasks to be executed')

    parser.add_argument('--exclude',
                        default='',
                        help='exclude comma-separated tasks from execution')

    parser.add_argument('procedure_config', metavar='procedure_config', type=str,
                        help='config file for add_node procedure')

    args = flow.parse_args(parser, cli_arguments)

    defined_tasks = []
    defined_excludes = []

    if args.tasks != '':
        defined_tasks = args.tasks.split(",")

    if args.exclude != '':
        defined_excludes = args.exclude.split(",")

    context = flow.create_context(args, procedure='manage_pss',
                                  included_tasks=defined_tasks, excluded_tasks=defined_excludes)
    context['inventory_regenerate_required'] = True

    flow.run(
        tasks,
        defined_tasks,
        defined_excludes,
        args.config,
        context,
        procedure_inventory_filepath=args.procedure_config,
    )


if __name__ == '__main__':
    main()