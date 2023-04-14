import argparse
parser = argparse.ArgumentParser(
    description='A python program to scrape unitn courses and store resources in a local folder')

parser.add_argument('username', nargs=1, type=str,
                    help='Insert your mail or username, no format required (e.g. name.surname@unitn.it, name.surname)')

parser.add_argument('password', nargs=1, type=str,
                    help='Insert your password')
# Show courses list
parser.add_argument('--list-enrolled', '--list-registered', '-le', dest='list-enrolled',  action=argparse.BooleanOptionalAction,
                    help='Show list of courses you are enrolled in')
parser.add_argument('--list-available', '--list-av', '-la', dest='list-available',
                    action=argparse.BooleanOptionalAction, help='Show list of available courses')
parser.add_argument('--list-all', '--all', '-a', dest='list-all',  action=argparse.BooleanOptionalAction,
                    help='Show list of all courses')


# Show course info
parser.add_argument('--code', '--course-code', '-c', dest='code',
                    type=int, help='Show course info, selecting by code')
parser.add_argument('--name', '--course-name', '-n', dest='c-name',
                    type=str, help='Show course info, selecting by name')

args = parser.parse_args()
print(args)
