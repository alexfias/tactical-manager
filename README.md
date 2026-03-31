# Tactical Manager

A football management game prototype focused on meaningful decisions,
tactical trade-offs, and long-term squad dynamics.

## 🎮 Current State

Tactical Manager is now a **playable prototype** with both CLI and Qt
GUI interfaces.

You can: - Play through a season - Simulate matches - View league
tables - Track match history - Interact via command line or graphical
interface

## 🧠 Core Idea

Every decision affects the future state of the club through: - fatigue -
morale - tactical choices - squad structure

The goal is to build a system where **decisions have long-term
consequences**, not just short-term outcomes.

## 🚀 Features

-   Match simulation engine
-   League system with standings
-   Team and squad structure
-   CLI interface (stable)
-   Qt GUI (early version with splash screen)

## 🖥️ Run

### CLI

python scripts/run_cli.py

### GUI (Qt)

python scripts/run_gui.py

## 🧱 Project Structure

src/tactical_manager/ ├── core/ \# Game logic (season, teams, match
engine) ├── ui/ │ ├── cli.py \# Command line interface │ └── gui_qt.py
\# Qt GUI

## 🔧 Tech Stack

-   Python
-   PySide6 (Qt for GUI)

## 📍 Roadmap

Next steps: - GUI match setup (tactics & mentality) - Improved
navigation (dashboard, views) - Team management (lineups,
substitutions) - Player development & long-term dynamics - Financial
system

## ⚠️ Status

This is an **early-stage prototype** under active development. Expect
frequent changes and breaking updates.

------------------------------------------------------------------------

Built as an experiment in designing a football manager where **decisions
truly matter**.


## v0.1.0 — First Playable Version

- GUI and CLI interface
- Match simulation engine
- Tactical decisions influence outcomes
- League table and match history tracking

Next:
- Improved UI layout
- Squad management
- Match visualization