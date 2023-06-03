class State_manager:
    def __init__(self, game):
        self._game = game
        self._game_states = {
            0 : "TEST",
            1 : "MENU",
            2 : "INVENTORY",
            3 : "GAME"
        }
        
    def change_state(self, state: str or int):
        if isinstance(state, int):
            self._game.game_state = self._game_states[state]
        else:
            self._game.game_state = state