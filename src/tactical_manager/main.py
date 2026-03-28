from __future__ import annotations

from pathlib import Path
from tactical_manager.core.season import Season, create_double_round_robin
from tactical_manager.ui.loaders import load_teams_from_json
from tactical_manager.ui.cli import run_cli


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    data_file = root / "data" / "teams" / "fictional_league.json"

    teams = load_teams_from_json(data_file)
    fixtures = create_double_round_robin(list(teams.keys()))
    season = Season(teams=teams, fixtures=fixtures)

    run_cli(season)


if __name__ == "__main__":
    main()
