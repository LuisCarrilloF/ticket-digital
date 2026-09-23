class Business:
    def __init__(
        self,
        name: str,
        description: str,
        logo: str,
        services: list[str] | None = None,
    ):
        self.name = name
        self.description = description
        self.logo = logo
        self.services = services or []