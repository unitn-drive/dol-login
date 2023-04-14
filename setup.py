from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='unitn-courses-scraper',
    version='0.0.1',
    description='Interactive scraper for your unitn courses',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['unitn', 'courses', 'scraper', '@unitn.it',
              'moodle', 'dol', 'gestionecorsi', 'didatticaonline'],
    author='Toniolo Marco',
    author_email='marcotoniolomail@gmail.com',
    py_modules=['unitn_courses_scraper'],
    package_dir={'': 'src'},
    license='GPLv3',
    classifiers=["Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Operating System :: OS Independent",
                 ],
    install_requires=[
        'dotenv >= 0.21.0', 'requests >= 2.28.2', 'grequests >= 0.6.0', 'bs4 >= 0.0.1', 'json >= 2.0.9'],
)
