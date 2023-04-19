# UniTN Courses Scraper

Interactive scraper for your UniTN courses.

It allows you to get resources from the courses that you are taking and the courses you can enroll in; It stores and organizes them in a clean way.

## Getting started

- Install a fresh version of Python 3.11 to your local machine (with your virtual environment management of choice)
- Install the requirements with `pip install -r requirements.txt`
- Add a copy of the `.env` file to the root of the project (instructions are found in the `.env.example` file). Env file can be specified via command line arguments. When creating your `.env` file you should avoid using the **.studenti** sub-domain; It should look like this: **name.surname**@unitn.it
- Add the "-h" argument to get further informations.

## What does it do

At this point of development, enrolled courses and available ones can be shown by `--list-enrolled` and `--list-available` arguments.
In future versions it will be possible to automatically enroll in courses and get all the educational content released by the lecturer (both slides and multimedia contents).