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

    def team_id(self) -> int:
        return self.team_info.team_id

    def team_name(self) -> str:
        return self.team_info.team_name
