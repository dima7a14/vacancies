class VacancyExistsException(Exception):
    def __init__(self, data: dict) -> None:
        self.title = data.get("title")
        self.link = data.get("link")

    def __str__(self):
        if self.title is not None and self.link is not None:
            return f"Vacancy {self.title} [{self.link}] already exists"
        else:
            return "Vacancy already exists"
