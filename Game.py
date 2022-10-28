class Game:
    class State:
        MAIN_MENU = 0
        SETTINGS_MENU = 1
        SELECT_LEVEL_MENU = 2
        CREDITS_MENU = 3

    settings = {}
    
    current_state = State.MAIN_MENU
