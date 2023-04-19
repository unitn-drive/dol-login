# UniTN Courses Scraper

Interactive scraper for your UniTN courses.

It allows you to get resources from the courses that you are taking and the courses you can enroll in; It stores and organizes them in a clean way.

## Getting started

- Install it with `pip install unitn-course-scraper`
- Create your own `.env` file (instructions are found in the `.env.example` file). Its path needs to be specified via command line arguments. When creating your `.env` file you should avoid using the **.studenti** sub-domain; It should look like this: **name.surname**@unitn.it
- Run it with `unitn-course-scraper -E .env`
- Use the "-h" argument to get further informations.

## What does it do

At this point of development, enrolled courses and available ones can be shown by `--list-enrolled` and `--list-available` arguments.
In future versions it will be possible to automatically enroll in courses and get all the educational content released by the lecturer (both slides and multimedia contents).