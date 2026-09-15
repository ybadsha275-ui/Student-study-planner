Student Study Planner

A desktop study-planning application built with Python and CustomTkinter. It combines task management, planning, focus sessions, analytics, reminders, gamification, reporting, and local data backup in one application.

Features

Dashboard with task statistics, overall progress, study streak, XP, level, daily goal, workload, focus time, and achievements

Task management with add, edit, delete, complete/undo, search, filtering, sorting, starred tasks, due dates, priority, subject, category, difficulty, estimated study time, descriptions, subtasks, and recurring tasks

Automatic task progress based on subtasks

Smart Daily Planner that ranks pending tasks using deadline, priority, difficulty, progress, and starred importance

Interactive study calendar with task dates and daily task details

Focus Mode with configurable Pomodoro focus/break durations and selected-task support

Focus-session tracking with study dates and total focus time

Analytics with workload statistics, status/priority charts, subject progress, and a 30-day study heatmap

Deadline reminders for overdue, today's, and tomorrow's tasks while the application is running

Gamification with XP, levels, and achievement badges

Study report with performance, study-time, consistency, subject, and gamification information

JSON backup export/import for tasks, study data, and gamification data

Dark/light appearance switching

Local data storage; no external database or cloud account is required

Technology Stack

Python

Tkinter

CustomTkinter

tkcalendar

Matplotlib

Pandas

JSON file storage

datetime / calendar / uuid / os / tkinter utilities

Project Structure

student study planner/
│
├── main.py
├── requirements.txt
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── task_manager.py
│   ├── gamification.py
│   └── backup_manager.py
│
├── gui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── tasks.py
│   ├── planner.py
│   ├── calendar.py
│   ├── focus.py
│   ├── analytics.py
│   ├── reminders.py
│   ├── achievements.py
│   └── reports.py
│
├── data/
│   ├── tasks.json
│   ├── study_data.json
│   └── gamification.json
│
└── assets/

Architecture

The project follows a simple layered structure:

GUI Layer
   ↓
Business Logic Layer
   ↓
Local Data Layer

Examples:

TasksView
   ↓
task_manager.py
   ↓
tasks.json

FocusView
   ↓
task_manager.py + gamification.py
   ↓
study_data.json + gamification.json

main.py acts as the application controller and connects the GUI pages.

Installation

Use Python 3.13 or another compatible Python 3.x installation.

Install dependencies:

python -m pip install -r requirements.txt

Run the Application

From the project root:

python main.py

Quick Demo

A strong demonstration sequence is:

Open Dashboard

Add a task with priority, due date, difficulty, estimated time, and subtasks

Complete subtasks and demonstrate automatic progress

Complete the task and demonstrate XP/achievement feedback

Open Smart Planner

Open Calendar and show the task deadline

Open Focus Mode and run a short test session

Open Analytics and show charts/heatmap

Open Study Report and export it

Open Settings and demonstrate backup export/import

Data and Backup

The application stores information locally in the data folder. The backup feature combines the application's task, study, and gamification data into a single JSON backup file.

Before importing a backup, the application asks for confirmation because the imported data replaces the current stored data.

GitHub

The project is maintained in Git using the main branch.

Typical update workflow:

git status
git add .
git commit -m "Update Student Study Planner"
git push

Current Scope

The current implementation is a single-user desktop application with local storage. Cloud synchronization, user accounts, and an AI assistant are not part of the current implemented version.

Academic Objective

The project demonstrates practical Python GUI development, modular programming, data persistence, event-driven programming, file handling, visualization, task scheduling logic, and basic software architecture through a useful student-focused application.