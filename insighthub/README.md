# InsightHub

InsightHub is a lightweight, topic-centred survey platform built with Django.

The idea behind InsightHub is simple: surveys become more useful when they are organised around subjects that people can explore and build on. Instead of treating every survey as an isolated questionnaire, InsightHub groups surveys into reusable **Topics** such as education, technology, wellbeing, research, or any other area of interest.

Users can browse existing Topics to discover how surveys are already organised, create a new Topic when an appropriate subject does not yet exist, and create Surveys within those Topics. This creates a growing catalogue in which related surveys can be discovered together rather than existing as disconnected forms.

InsightHub is intentionally lightweight at its current stage. The current version provides a fully functional foundation for creating and organising Topics, Surveys, Questions and reusable answer options through the application interface.

The longer-term vision is to develop this foundation into a richer, community-oriented survey platform where people can discover, create, participate in and engage with surveys around shared interests.

## Why Topics and Surveys are separate

InsightHub separates **Topics** from **Surveys** because they serve different purposes.

A **Topic** represents a broader subject or area of interest.

A **Survey** represents a specific questionnaire within that subject.

For example:

### Technology

- How do you use AI tools?
- Remote working technology
- Favourite productivity applications

### Education

- Online learning preferences
- Study habits
- Student experience with digital courses

This structure allows an existing Topic to be reused by multiple Surveys. Users do not need to create a new category every time they create a questionnaire, while people browsing the platform can discover related Surveys through subjects that interest them.

The result is closer to a small **survey community or survey hub** than a collection of unrelated forms.

## Current functionality

InsightHub currently provides functionality for managing the main building blocks of a survey.

### Topics

Users can:

- browse all Topics;
- view individual Topic details;
- create new Topics;
- edit existing Topics;
- delete Topics with confirmation.

Topic validation helps prevent invalid and duplicate Topic titles.

### Surveys

Users can:

- browse all Surveys;
- view individual Survey details;
- create Surveys under existing Topics;
- edit Surveys;
- delete Surveys with confirmation;
- define launch and expiration dates;
- filter Surveys by Topic;
- sort Surveys by newest, launch date or expiration date.

Survey validation helps ensure that scheduling information is logically valid.

### Questions

Surveys can contain Questions with:

- text responses;
- single-choice responses;
- multiple-choice responses;
- required or optional status;
- configurable display order.

Questions can be created, edited and deleted through the application interface.

### Reusable answer options

InsightHub also supports reusable answer options for choice-based Questions.

For example:

- Very satisfied
- Satisfied
- Neutral
- Dissatisfied
- Very dissatisfied

An answer option can be created once and associated with Questions where appropriate.

This provides a reusable many-to-many relationship between Questions and answer options and supports the questionnaire-building workflow.

## How InsightHub is structured

The current relationship between the main concepts is:

```text
Topic
  |
  | one-to-many
  v
Survey
  |
  | one-to-many
  v
Question
  |
  | many-to-many
  v
Choice
```

A **Topic** can contain multiple Surveys.

A **Survey** belongs to one Topic and can contain multiple Questions.

A **Question** belongs to one Survey and can use multiple reusable Choices.

A **Choice** can be associated with multiple Questions.

## Typical workflow

A typical content-creation workflow in InsightHub is:

1. Browse the existing Topics.
2. Select an appropriate Topic or create a new one.
3. Create a Survey and associate it with that Topic.
4. Add Questions to the Survey.
5. Create reusable answer options when required.
6. Associate answer options with single-choice or multiple-choice Questions.
7. Browse, filter and sort Surveys through the Survey catalogue.

The application's core objects can be created through the user interface, allowing InsightHub to be used without relying on pre-populated database content.

## Project structure

InsightHub is organised into three Django applications:

- `core` - site-wide functionality such as the homepage;
- `catalogue` - Topics and Topic management;
- `surveys` - Surveys, Questions and answer options.

This separation keeps general site functionality, catalogue functionality and survey functionality organised into distinct areas of responsibility.

## Technology

InsightHub is built with:

- Python
- Django
- Django Template Language
- HTML
- CSS
- SQLite
- Git
- GitHub

SQLite keeps the application lightweight and allows it to run locally without requiring a separate database server.

## Installation and local setup

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd insighthub
```

Create a virtual environment.

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script for the current terminal session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Django in the active virtual environment if it is not already available:

```bash
pip install django
```

Apply the database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the local address displayed by Django in your browser.

## Database

InsightHub uses SQLite.

The local database file is not required as part of the repository. Django migrations define the database structure and recreate it during project setup.

Run:

```bash
python manage.py migrate
```

to create the required database tables.

The application is designed so that its required content can then be created through the normal user interface.

## Running the tests

Run the complete automated test suite with:

```bash
python manage.py test
```

Django uses a separate temporary test database while running the test suite, so automated test data does not need to be stored in the development database.

## Design approach

InsightHub follows a reusable Django structure based on:

- template inheritance;
- a shared base template;
- reusable template components;
- named and namespaced URLs;
- class-based views;
- reusable ModelForms;
- user-friendly form validation;
- confirmation before destructive actions;
- relational database modelling;
- responsive CSS styling.

The project separates presentation, catalogue functionality and survey functionality so that the application can be expanded without redesigning its core domain structure.

## Project status

InsightHub is a **functional lightweight application and an extensible foundation**, rather than a finished large-scale survey service.

The current version focuses on the creation, organisation and management side of the platform. Topics, Surveys, Questions and reusable answer options can be created and managed through the user interface, while Surveys can also be browsed, filtered and sorted.

The current application therefore establishes the structure needed for a survey platform without attempting to implement every feature of a full production service.

## Future development

The current version provides a foundation that can be extended further.

Possible future enhancements include:

- participant-facing Survey completion;
- storing Survey responses;
- Survey results and analytics;
- user accounts and ownership;
- permissions for Survey and Topic management;
- search and improved Topic discovery;
- richer Survey status and participation views;
- community and sharing features;
- more advanced questionnaire controls.

These features represent future development opportunities and are not presented as functionality of the current version.

## Vision

The longer-term idea behind InsightHub is to move beyond isolated online questionnaires.

A traditional survey is usually created, distributed and completed as a standalone form. InsightHub explores a different model in which surveys belong to broader subjects that people can discover and revisit.

In that sense, InsightHub is intended to develop towards a **community-oriented hub for surveys**: a place where people can explore subjects that interest them, discover related questionnaires, create new Surveys, and eventually participate in and engage with the insights generated around those subjects.

The current version establishes the core data model and management workflow required to support that direction.

## Purpose of the project

InsightHub was developed as an individual Django project to demonstrate the design and implementation of a cohesive web application using Django fundamentals.

The project focuses on meaningful relationships between data rather than treating individual models as isolated technical requirements:

- Topics organise Surveys.
- Surveys contain Questions.
- Questions can use reusable answer options.

The current implementation therefore serves two purposes: it is a functional lightweight survey-management application today, and it provides a structured foundation for developing a more complete survey community platform in the future.
