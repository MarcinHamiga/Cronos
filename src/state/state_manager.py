from src.state.game_states import GameStates


class StateManager:

    def __init__(self, game):
        self._game = game
        self._current_state = GameStates.MENU

    @property
    def current_state(self):
        return self._current_state

    def change_state(self, state):
        if isinstance(state, GameStates):
            self._current_state = state
            return self._current_state

        if isinstance(state, str):
            try:
                self._current_state = GameStates[state.upper()]
                return self._current_state
            except KeyError as exc:
                raise ValueError(f"Unknown game state: {state}") from exc

        raise TypeError(f"Unsupported state type: {type(state).__name__}")
