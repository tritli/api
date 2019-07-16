from config import API_USER, API_PASS


def check_api_user(user_name: str, password: str):
    if user_name == API_USER and password == API_PASS:
        return True
    return False
