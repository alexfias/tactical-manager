from __future__ import annotations

from tactical_manager.core.season import Season
from tactical_manager.ui.render import render_match, render_table
from tactical_manager.core.models import Tactic
from tactical_manager.ui.render import render_squad

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

def choose_tactic() -> Tactic:
    print("Choose mentality:")
    print("1. Defensive")
    print("2. Balanced")
    print("3. Attacking")
    m = input("> ").strip()

    mentality_map = {"1": 35.0, "2": 50.0, "3": 70.0}
    mentality = mentality_map.get(m, 50.0)

    return Tactic(
        formation="4-4-2",
        mentality=mentality,
        pressing=50.0,
        tempo=50.0,
        width=50.0,
        directness=50.0,
        defensive_line=50.0,
    )

def run_cli(season: Season) -> None:
    print("=== Tactical Manager ===")
    print()

    while True:
        print("Choose an option:")
        print("1. Play next fixture")
        print("2. Show table")
        print("3. Show history")
        print("4. Team management")
        print("5. Quit")
        choice = input("> ").strip()

        if choice == "1":
            plan = ask_match_plan()
            tactic = choose_tactic()
            fixture = season.play_next_fixture(user_plan=plan, user_tactic=tactic)

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
            run_team_management(season)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")
            print()


def run_team_management(season: Season) -> None:
    while True:
        print()
        print(f"=== Team Management: {season.user_team} ===")
        print("1. View full squad")
        print("2. Back")
        subchoice = input("> ").strip()

        team = season.teams[season.user_team]

        if subchoice == "1":
            print()
            print(render_squad(team.squad))

        elif subchoice == "2":
            print()
            break

        else:
            print("Invalid choice.")