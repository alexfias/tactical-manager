from __future__ import annotations

from pathlib import Path

from tactical_manager.core.data import create_round_robin_fixtures, load_clubs_from_folder
from tactical_manager.core.season import Season
from tactical_manager.ui.cli import run_cli


def choose_user_club(clubs: dict) -> str:
    club_names = list(clubs.keys())

    print("Choose your club:")
    for i, name in enumerate(club_names, start=1):
        print(f"{i}. {name}")

    while True:
        choice = input("> ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(club_names):
                return club_names[idx]

        print("Invalid choice. Please enter a valid number.")
    print()
    print(render_club_overview(user_club))
    print()

def main() -> None:
    clubs = load_clubs_from_folder(Path("data/clubs"))
    print("Loaded clubs:", list(clubs.keys()))

    fixtures = create_round_robin_fixtures(list(clubs.keys()))
    user_club = choose_user_club(clubs)

    season = Season(
        clubs=clubs,
        fixtures=fixtures,
        user_club=user_club,
    )

    run_cli(season)


if __name__ == "__main__":
    main()