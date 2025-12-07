# Task Manager Project

A Django-based task management system built as an internship assignment.

## Tech Stack

- Python 3
- Django
- PostgreSQL
- Bootstrap 5
- Ajax (vanilla JS)
- Running on Ubuntu WSL with VS Code

## Features

- User authentication (login/logout)
- Task CRUD (create, read, update, delete)
- Delete confirmation page
- Search by title/description
- Filter by status (pending, in progress, completed)
- Pagination (10 tasks per page)
- Ajax toggle for task status (pending <-> completed)
- Permission: users can only see and manage their own tasks

## How to run locally

1. Create and activate a virtual environment
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
