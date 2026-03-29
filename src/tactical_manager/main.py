from __future__ import annotations

from pathlib import Path
from tactical_manager.core.data import create_demo_teams, create_round_robin_fixtures, load_teams_from_folder
from tactical_manager.core.season import Season
from tactical_manager.ui.cli import run_cli


def choose_user_team(teams: dict) -> str:
    team_names = list(teams.keys())

    print("Choose your team:")
    for i, name in enumerate(team_names, start=1):
        print(f"{i}. {name}")

    while True:
        choice = input("> ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(team_names):
                return team_names[idx]

        print("Invalid choice. Please enter a valid number.")


def main() -> None:
    #teams = create_demo_teams()
    teams = load_teams_from_folder(Path("data/teams"))
    print("Loaded teams:", list(teams.keys()))

    fixtures = create_round_robin_fixtures(list(teams.keys()))

    user_team = choose_user_team(teams)

    season = Season(
        teams=teams,
        fixtures=fixtures,
        user_team=user_team,
    )

    run_cli(season)


if __name__ == "__main__":
    main()