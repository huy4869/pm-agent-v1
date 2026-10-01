from dataclasses import dataclass, field


@dataclass
class ResourceProfile:
    name: str
    role: str | None = None
    skills: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
