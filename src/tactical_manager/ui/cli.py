from __future__ import annotations

from tactical_manager.core.season import Season
from tactical_manager.ui.render import render_match, render_table


def ask_match_plan() -> str:
    print()
    print("Choose your match approach:")
    print("1. Defensive")
    print("2. Balanced")
    print("3. Attacking")
    choice = input("> ").strip()

    if choice == "1":
        return "defensive"
    if choice == "3":
        return "attacking"
    return "balanced"


def run_cli(season: Season) -> None:
    print("=== Tactical Manager ===")
    print()

    while True:
        print("Choose an option:")
        print("1. Play next fixture")
        print("2. Show table")
        print("3. Show history")
        print("4. Quit")
        choice = input("> ").strip()

        if choice == "1":
            plan = ask_match_plan()
            fixture = season.play_next_fixture(user_plan=plan)

            if fixture is None:
                print("Season finished.")
                print(render_table(season.table()))
                break

            print()
            print(render_match(fixture.result))
            print()

        elif choice == "2":
            print()
            print(render_table(season.table()))
            print()

        elif choice == "3":
            print()
            if season.history:
                for line in season.history:
                    print(line)
            else:
                print("No matches played yet.")
            print()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")
            print()