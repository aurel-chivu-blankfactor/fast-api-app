class UserNotFoundException(Exception):
    def __init__(self, user_uuid: str):
        self.message = f"User {user_uuid} not found"
        super().__init__(self.message)
