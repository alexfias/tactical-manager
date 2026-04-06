# Tactical Manager

A football management game focused on **meaningful decisions**,  
**tactical trade-offs**, and **long-term club development**.

---

## 🎮 Current State

Tactical Manager is an **early-stage but playable game prototype**  
with both CLI and a growing PySide6 (Qt) GUI.

You can currently:

- Simulate full seasons
- Play matches via a match engine
- View league tables and match results
- Navigate through multiple GUI pages (team, season, club, settings)
- Manage your club at a basic level

---

## 🧠 Vision

The goal is to build a football manager where:

- Decisions have **long-term consequences**
- Systems are **deep but transparent**
- Trade-offs matter (short-term vs long-term success)

Core mechanics will include:

- Player development & aging
- Tactical identity
- Financial constraints
- Squad planning over multiple seasons

---

## 🚀 Features (Current)

- Match simulation engine
- League system with standings
- Multi-page GUI (PySide6)
- Basic club and team structure
- CLI interface (stable)

---

## 🖥️ Run

### CLI

```bash
python scripts/run_cli.py
```

### GUI

```bash
python scripts/run_gui.py
```

---

## 🧱 Project Structure

```
src/tactical_manager/
├── core/                 # Core game logic (season, match engine, models)
├── ui/
│   ├── cli/              # CLI interface
│   └── gui/
│       ├── pages/        # Main UI pages (team, club, season, etc.)
│       ├── widgets/      # Reusable UI components
│       ├── navigation/   # Navigation system (bottom bar, routing)
│       └── app.py        # GUI entry point
```

---

## 🔧 Tech Stack

- Python
- PySide6 (Qt GUI)

---

## 📍 Roadmap

### Short Term (v0.2.x)

- Financial system (revenue, costs, balance sheet)
- Improved navigation & UI structure
- Team management (lineups, roles, substitutions)
- Match setup (tactics, mentality)

### Mid Term

- Player development system
- Transfers & contracts
- Scouting & recruitment

### Long Term

- Advanced match simulation (spatial/2D engine)
- AI managers & league dynamics
- Multi-season progression with deep systems

---

## ⚠️ Status

This is an **actively developed early-stage project**.  
Expect frequent updates and breaking changes.

---

## 📦 Version

### v0.1.0 — First Playable Version

- CLI + GUI
- Match simulation
- League system

### Next (v0.2.0 goal)

- Full season simulation with finances
- Functional team & club management UI

---

## 💡 Philosophy

This project explores a key idea:

> A great management game is not about options —  
> it’s about **meaningful consequences**.
