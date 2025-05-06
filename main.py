# Directory: edd_system_app
# main.py
# edd_system_app start point

from app.actions.app_actions import AppAction

if __name__ == "__main__":
    print("EDD Technologies Repair System")
    app = AppAction()
    app.start()
