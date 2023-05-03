# Hinge Health Data Engineering Onsite Project

The US Softball League has entered into an agreement with Unity Golf Club to provide a common set of membership benefits to both organizations. But there are problems: the data is not entirely compatible. To help these two fine organizations, clean up the data and provide some simple statistics.

## Challenge Overview

Write a small Python or Go application to process and analyze the data provided in the included files.

**Be sure to set aside at least 15-30 minutes near the end of the session to ensure Part 3 gets completed.**

The objective is not necessarily to _finish_ the exercise, it's to observe how you proceed through the work required. Use the exercise as an opportunity to show what **quality production code** looks like.

> If using Python we recommend using the `pandas` package for this exercise, though it's not required.

## Guidelines

We expect to see the following in the final solution code:

- Unit tests _(as appropriate)_
- Integration and/or end-to-end tests _(as appropriate)_
- Dedependency management with [pipenv](https://pipenv.readthedocs.io/en/latest/) and a Pipfile or Go modules
- Code quality tooling _(linting, etc.)_

> If any of these concepts are unfamiliar to you, the Hinge Health engineer partnered with you will provide assistance.

Again, you are not expected to finish the entire exercise. We expect you to only spend a total of 2 hours to work on the assignment. Please incrementally commit your work into a branch. We like to follow your thinking through the git commits.

Once you have completed your submission, issue a Pull Request. Please do not push directly to master.

## Part 1: Data Munging

Given two data files, your first task is to standardize and combine them into a common file for further analysis.

Steps:
1. Transform us_softball_league.tsv to match unity_golf_club.csv in columns and format.
    - Standardize first and last name columns.
    - Convert dates into a common format.
    - All states should be in two character abbreviation.
2. Combine the two files into one master file.
    - Indicate the source file for each record in the combined file.
3. Use companies.csv to replace `company_id` with the company name.
4. Identify suspect records (hint: look for impossible chronological combinations).
    - Write bad records into a separate file.
    - Drop those records from the main file.

Samples:

`us_softball_league.tsv`:

| id |              name | date_of_birth | company_id | last_active | score | joined_league |     us_state |
|---:|------------------:|--------------:|-----------:|------------:|------:|--------------:|-------------:|
|  0 |   Mikayla Brennan |    11/02/1966 |          2 |  07/04/2018 |    84 |          1989 |     Illinois |
|  1 |     Thomas Holmes |    11/29/1962 |          1 |  05/15/2018 |    92 |          1972 |    Wisconsin |
|  2 |       Corey Jones |    12/20/1964 |          7 |  08/25/2018 |    47 |          2007 |   New Mexico |
|  3 |      Laura Howard |    04/26/1989 |          8 |  04/15/2018 |    76 |          1976 |   New Jersey |
|  4 | Daniel Mclaughlin |    06/19/1966 |         13 |  05/10/2018 |    56 |          1986 | Rhode Island |

`unity_golf_club.csv`:

| id |  first_name |  last_name |        dob | company_id | last_active | score | member_since | state |
|---:|------------:|-----------:|-----------:|-----------:|------------:|------:|-------------:|------:|
|  0 |      Robert | Mclaughlin | 1967/03/26 |          3 |  2018/08/25 |    57 |         2013 |    OR |
|  1 |    Brittany |     Norris | 1972/09/06 |         12 |  2018/03/29 |    73 |         1986 |    MD |
|  2 |      Sharon |    Nichols | 1971/04/19 |          7 |  2018/04/11 |    92 |         1985 |    WY |
|  3 | Christopher |       Ware | 1977/05/25 |         11 |  2018/07/20 |    74 |         2003 |    PA |
|  4 |       Kevin |      Scott | 1981/12/15 |          8 |  2018/11/20 |    42 |         1994 |    MN |

`companies.csv`:

| id |                       name |
|---:|---------------------------:|
|  0 |        Williams-Stephenson |
|  1 | Brown, Vasquez and Sanchez |
|  2 |               Keller Group |
|  3 |               Mcdonald Inc |
|  4 |                  Bruce Inc |


## Part 2: Ingestion System

Build a data model to support the data seen here and write software that will write this data to a database. For the purposes of this exercise use a SQLite3 or PostgreSQL database running locally.

> Proceed as if the dataset does not fit entirely into RAM.

## Part 3: Follow-up

Write a document (a simple TODO.txt or TODO.md is fine) outlining the next steps for this "project", taking into account all the progress to this point. Suggestions for further enhancement, improvement, and refactoring are encouraged.

If the entire exercise has not been completed, the TODO should also outline the work remaining to reach the end of the exercise.
