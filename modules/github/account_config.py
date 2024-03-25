from injector import inject


class AccountConfig:
    @inject
    def __init__(self, account_data: dict):
        self.config = account_data

    def get_username(self) -> str:
        return self.config["username"]
