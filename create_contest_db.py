#!/usr/bin/env python3

"""
This spits out a coffeescript representation of the entire problem set, which when used in
conjunction with https://github.com/MAPSuio/deploy-ladder can be used to effectively deploy
a competition with minimal manual intervention.

The script traverses the directory structure and spits out a series of database insertion statements
on the following form:

    Problems.insert
      title: "Hello World"
      solution: "Hello World"
      answers: []
      draft: false
      activeFrom: new Date
      description: "Write `Hello World` into the answer box"

The script assumes that the problem description resided in a README.md while the answer is stored in an
answer.md. The script will crash immediately if these files are not present for a given problem.

Don't hesitate to contact Carl Martin Rosenberg (cmr@simula.no) if you are having problems.

Example invocation:

./create_contest_db.py --directory ../spring-challenge17/

"""

from os import path
from os import walk, path

import argparse

argparser = argparse.ArgumentParser(description="Create a database insertion script for a Programming Ladder competition.")
argparser.add_argument("-d", "--directory", help="Explicitly set project directory")

args = vars(argparser.parse_args())

#TODO: Make this a passable parameter

#JavaScript uses weird month notation, so March is 2
CONTEST_START = "new Date(2017, 2, 9, 17)"

def create_entry(root, files):

    answer_fd = open(path.join(root, 'answer.md'), 'r')
    answer = answer_fd.readlines()[0].strip()
    answer_fd.close()

    description_fd = open(path.join(root, 'README.md'), 'r')
    description = description_fd.readlines()
    description_fd.close()

    title = description[0].split("#")[1].strip()

    print("    Problems.insert")
    print("      title: " + "\"" + title + "\"")
    print("      solution: " + "\"" + answer + "\"")
    print("      answers: []")
    print("      draft: false")
    print("      activeFrom: " + CONTEST_START)
    print("      description:" + "\"\"\"" + "".join(description[1:]) + "\"\"\"")


print("Meteor.startup ->")
print("  if Problems.find().count() is 0")

if args["directory"]:
    starting_path = path.abspath(args["directory"])
else:
    starting_path = "."

for root, _, files in walk(starting_path):

    if root == starting_path or ".git" in root:
        continue

    create_entry(root, files)

print("if Meteor.users.find().count() is 1\n Meteor.users.update {}, {$set: {isAdmin: true}}")
