#!/usr/bin/python

import i3ipc     # Required for interactions with i3 and its IPC interface
import sys       # Required for exiting
import math      # Required for rounding
import argparse  # Required for easy arguments to command

VERSION = (1, 0)

i3 = i3ipc.Connection()


def go_to_workspace(workspace_number):
    if workspace_number <= 0:
        workspace_number = 1
    i3_command = 'workspace number %s' % (workspace_number)
    print('i3 Command: %s' % i3_command)
    i3.command(i3_command)


def move_to_workspace(workspace_number):
    if workspace_number <= 0:
        print('Not doing anything to a negative workspace')
        return 1
    i3_command = 'move container to workspace number %s' % (workspace_number)
    print('i3 Command: %s' % i3_command)
    i3.command(i3_command)


def rename_workspace(workspace_name):
    i3_command = 'rename workspace to "%s"' % (workspace_name)
    print('i3 Command: %s' % i3_command)
    i3.command(i3_command)


def get_workspace_number_and_name(workspace_name):
    try:
        if ': ' in workspace_name:
            workspace_number, workspace_name = workspace_name.split(': ')
        else:
            workspace_number = workspace_name
        workspace_number = int(workspace_number)
    except ValueError:
        print("Unable to parse Workspace's number and name")
        return (1, workspace_name)
    return (workspace_number, workspace_name)


def make_workspace_name(workspace_number, workspace_name):
    return ': '.join([str(workspace_number), workspace_name])


def get_workspace_block(workspace_number):
    return int(math.floor((workspace_number-1)/10))*10


def shift_workspace_number(workspace_number, direction, number, exact):
    if direction is not None:
        if direction == 'up':
            workspace_number += 10
        elif direction == 'down':
            workspace_number -= 10
        elif direction == 'next':
            workspace_number += 1
        elif direction == 'prev':
            workspace_number -= 1
    elif number is not None:
        if exact is True:
            workspace_number = number
        else:
            workspace_block = get_workspace_block(workspace_number)
            workspace_number_in_block = number
            workspace_number = workspace_block + workspace_number_in_block
    return workspace_number


def action_go(workspace_number, workspace_name, args):
    workspace_number = shift_workspace_number(workspace_number, args.direction, args.number, args.exact)
    go_to_workspace(workspace_number)


def action_move(workspace_number, workspace_name, args):
    workspace_number = shift_workspace_number(workspace_number, args.direction, args.number, args.exact)
    return move_to_workspace(workspace_number)


def action_rename(workspace_number, workspace_name, args):
    if args.number is not None:
        workspace_number = args.number
    if args.name is not None:
        workspace_name = args.name
    rename_workspace(make_workspace_name(workspace_number, workspace_name))


def parse_args():
    parser = argparse.ArgumentParser(description='simplifying large amounts of i3 workspaces')
    parser.set_defaults(action=None)
    parser.add_argument('--version', action='version', version="%(prog)s {}.{}".format(*VERSION))

    subparsers = parser.add_subparsers(help='check help for each command for required arguments')

    parser_go = subparsers.add_parser('go', help="like the 'workspace number' command")
    parser_go.set_defaults(action=action_go)
    parser_go.add_argument('--exact', action='store_true',
                           help="number arguments will be the actual workspace number instead of the index in the current block")
    group_go = parser_go.add_mutually_exclusive_group(required=True)
    group_go.add_argument('-d', '--direction', choices=['up', 'down', 'next', 'prev'],
                          help='operate relative to the current workspace; up/down = +/- 10')
    group_go.add_argument('-n', '--number', type=int,
                          help='specify workspace number')

    parser_move = subparsers.add_parser('move', help="like the 'move container to workspace number' command")
    parser_move.set_defaults(action=action_move)
    parser_move.add_argument('--exact', action='store_true',
                             help="number arguments will be the actual workspace number instead of the index in the current block")
    group_move = parser_move.add_mutually_exclusive_group(required=True)
    group_move.add_argument('-d', '--direction', choices=['up', 'down', 'next', 'prev'],
                            help='operate relative to the current workspace; up/down = +/- 10')
    group_move.add_argument('-n', '--number', type=int,
                            help='specify workspace number')

    parser_rename = subparsers.add_parser('rename', help="like the 'rename workspace to' command")
    parser_rename.set_defaults(action=action_rename)
    parser_rename.add_argument('-na', '--name',
                               help='change the name of the current workspace')
    parser_rename.add_argument('-nu', '--number', type=int,
                               help='change the number of the current workspace')

    args = parser.parse_args()

    if args.action is None:
        parser.print_help()
        return

    return args


def main():
    args = parse_args()

    workspace_name = i3.get_tree().find_focused().workspace().name
    workspace_number, workspace_name = get_workspace_number_and_name(workspace_name)

    sys.exit(args.action(workspace_number, workspace_name, args))


if __name__ == '__main__':
    main()
