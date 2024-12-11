from dataclasses import dataclass


@dataclass
class TeamInfo:
    team_id: int
    team_name: str


@dataclass
class AppInfo:
    team_info: TeamInfo
    title: str

    def __init__(self, team_id: int, team_name: str, title: str) -> None:
        self.team_info = TeamInfo(team_id, team_name)
        self.title = title
