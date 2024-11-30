class GroupNotFoundException(Exception):
    def __init__(self, group_uuid: str):
        self.message = f"Group with the id {group_uuid} not found"
        super().__init__(self.message)
