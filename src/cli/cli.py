import argparse
from src.login.login import login
from src.login.login import input
from src.login.login import get_attended_courses
from src.login.login import get_available_courses


def parse_args():
    parser = argparse.ArgumentParser(
        description='A python program to scrape unitn courses and store resources in a local folder')

    parser.add_argument(
        '-E', '--env', help="Position of the env file that contains username and password",         required=True)

    # Show courses list
    listgroup = parser.add_mutually_exclusive_group()
    listgroup.add_argument('--list-enrolled', '--list-registered', action=argparse.BooleanOptionalAction,
                           help='Show list of courses you are enrolled in')
    listgroup.add_argument('--list-available', '--list-av',
                           action=argparse.BooleanOptionalAction, help='Show list of available courses')
    listgroup.add_argument('--list-all', '--all', action=argparse.BooleanOptionalAction,
                           help='Show list of all courses')

    # Show course info
    coursegroup = parser.add_mutually_exclusive_group()
    coursegroup.add_argument('--code', '--course-code', '-c', action='store', metavar='COURSE_CODE',
                             type=int, help='Show course info, selecting by code')
    coursegroup.add_argument('--course-name', '--name', '-n', action='store', metavar='COURSE_CODE',
                             type=str, help='Show course info, selecting by name')

    # # Download course resources (top level parser)
    # # parser.add_argument()
    # download_subparser = parser.add_subparsers(
    #     title='Download Subcommand', help='download otion (default = download all files)', prog='download')

    # parser_a = download_subparser.add_parser(
    #     'download', help='a help')
    # parser_a.add_argument('bar', type=int, help='bar help')

    args = parser.parse_args()
    if args.env == None:
        parser.print_help()
        exit(1)

    if args.list_enrolled == None and args.list_available == None:
        args.list_enrolled = True
        args.list_available = True

    username, password = input(
        env=args.env
    )
    session, Bearer_auth, tokenRelayState, tokenSAMLResponse, data = login(
        username, password)

    print("ATTENDED COURSES")

    print(get_attended_courses(session, Bearer_auth))

    print("AVAILABLE COURSES")

    print(get_available_courses(session, Bearer_auth))
