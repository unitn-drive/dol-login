import argparse
from login.login import login, login_dol
from login.login import input
from login.login import get_attended_courses
from login.login import get_available_courses
from utils.utils import saveJSON
from login.subscribe import subscribe, unsubscribe


def parse_args():
    parser = argparse.ArgumentParser(prog='unitn-course-scraper',
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
    coursegroup.add_argument('--course-name', '--name', '-n', action='store', metavar='COURSE_NAME',
                             type=str, help='Show course info, selecting by name')

    # Download course resources (top level parser)
    parser.add_argument('--download', type=str, default='all', const='all', nargs='?',
                        help='download option (default = download all files)', metavar='CONTENT_TYPE')
    subparsers = parser.add_subparsers(
        help='choose what to download (default = all): video, pdf, all')

    # create the parser for the "download" command
    parser_download = subparsers.add_parser('--download')
    parser_download.add_argument('video', nargs=1, action='store',
                                 help='download video', metavar='CONTENT_TYPE')
    parser_download.add_argument('pdf', nargs=1, action='store',
                                 help='download pdf', metavar='CONTENT_TYPE')

    # MANIPULATE ARGS
    args = parser.parse_args()
    if args.env == None:
        parser.print_help()
        exit(1)

    if args.list_enrolled == None and args.list_available == None:
        args.list_enrolled = True
        args.list_available = True

    # LOG IN
    username, password = input(
        env=args.env
    )
    session, Bearer_auth, tokenRelayState, tokenSAMLResponse, data = login(
        username, password)

    print(args)
    # WHAT TO DO

    # if args.list_enrolled:
    #     print("ATTENDED COURSES")
    #     saveJSON('attended_courses', get_attended_courses(session, Bearer_auth))

    # if args.list_available:
    #     print("AVAILABLE COURSES")
    #     saveJSON('avaiable_courses', get_available_courses(session, Bearer_auth))

    sampleCourse = 'https://webapps.unitn.it/geco/#/public/redirectcorso/2022|91290|1|N0|75022'
    url = subscribe(session, Bearer_auth, sampleCourse)
    print(url)
    login_dol(session)
    unsubscribe(session, url)
