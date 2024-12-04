from typing import Optional


class GroupNotFoundException(Exception):
    def __init__(self, group_uuid: Optional[str], custom_message: str = None):
        if custom_message:
            self.message = custom_message
        else:
            self.message = f"Group with the id {group_uuid} not found"
        super().__init__(self.message)
