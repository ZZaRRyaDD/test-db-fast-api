class User:
    """Model for each User instance for factory."""

    def __init__(
        self,
        name: str,
        surname: str,
        phone: str,
        email: str,
        passport_id: str,
        passport_series: str,
    ) -> None:
        """Constructor for User object."""
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.passport_id = passport_id
        self.passport_series = passport_series

    def __str__(self) -> str:
        """Represent object User."""
        return f"{self.name} {self.surname}"
