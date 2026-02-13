# Cronos - Agent Guidelines

## Project Overview

Cronos is a 2D creature-collecting RPG game built with Python and pygame. The game features exploration, turn-based combat, NPCs with dialogue systems, and an inventory/shop system.

## Build/Run Commands

```bash
# Run the game
python launch.py

# Create executable (if PyInstaller is installed)
pyinstaller --onefile --windowed launch.py
```

## Dependencies

- Python 3.11+
- pygame
- pytmx (for Tiled map support)
- PyInstaller (optional, for packaging)

Install dependencies:
```bash
pip install pygame pytmx
```

## Testing

No formal test suite exists. Manual testing by running the game:
```bash
python launch.py
```

## Code Style Guidelines

### Imports

Organize imports in three groups, separated by blank lines:
1. Standard library imports (e.g., `random`, `pathlib`, `time`)
2. Third-party imports (e.g., `pygame`, `pytmx`)
3. Local module imports

Example:
```python
import random
from pathlib import Path
from time import time

import pygame
import pytmx

import map
import person
from menu import Menu
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `Game`, `Player`, `Creature`, `FightScreen`)
- **Functions/Methods**: snake_case (e.g., `attack_target`, `check_collision`, `get_dialogue`)
- **Private Methods**: Prefix with underscore (e.g., `_handle_events`, `_set_rectangle`)
- **Constants/Configuration Attributes**: UPPERCASE (e.g., `ASSETS`, `SCREEN`, `CLOCK`)
- **Instance Variables**: snake_case (e.g., `current_time`, `game_state`)

### Classes and Inheritance

- Base classes should define the interface; subclasses implement specific behavior
- Use `super().__init__()` when inheriting
- Common base classes: `Creature`, `Person`, `Item`, `Skill`, `Status`, `Event`

Example:
```python
class Flametorch(Creature):
    def __init__(self, level, image, name=""):
        super().__init__(level, 100, 35, 24, 10, [], name, "Fire")
        self.skills = []
        self.set_image(image)
```

### Control Flow

- Use `match`/`case` statements for multi-way branching (Python 3.10+)
- Use `if`/`elif`/`else` for simple conditions

Example:
```python
match self.game_state:
    case "MENU":
        self.menu_state()
    case "MAP":
        self.map_state()
    case "FIGHT":
        self.fight_state()
    case _:
        self.map_state()
```

### String Formatting

- Use f-strings for all string interpolation
- Use `__str__` method for class string representation

Example:
```python
def __str__(self):
    return f"{self.__class__.__name__}"

name_text = f"Name: {str(self.creature)}"
```

### Error Handling

- Use `try`/`except` blocks sparingly, mainly for expected errors
- `IndexError` is commonly caught for list operations
- `pygame.error` may be caught for display-related issues

Example:
```python
try:
    for x in range(3):
        card_surface = self.item_cards[x + self.offset * 3].draw_card(True)
except IndexError:
    pass
```

### Type Hints

- Type hints are optional but encouraged for function signatures
- Use built-in types: `str`, `int`, `bool`, `list`, `tuple`, `dict`
- Use `Optional` from typing when needed

Example:
```python
def __init__(self, coords: tuple, img=None):
def set_max_health(self, amount: int):
def check_for_item(self, name: str):
```

### Documentation

- Use docstrings for public methods (comments in Polish or English are acceptable)
- Keep docstrings concise and describe purpose, not implementation

Example:
```python
def get_action(self, action, reaction, creature, uses_item=False):
    """Collects information about actions performed by player and enemy"""

def teleport(self, game):
    """Teleports the player to specified coordinates on the specified map"""
```

### Game Architecture Patterns

#### Game State Management
- Use `State_manager` class for state transitions
- Valid states: `"MENU"`, `"MAP"`, `"INVENTORY"`, `"FIGHT"`, `"SETTINGS"`, `"SHOP"`

#### Drawing Pattern
- Each screen/UI element has `draw()` method
- Use pygame Surfaces and Rects for rendering
- Call `pygame.display.flip()` once per frame

#### Update Pattern
- Each screen/UI element has `update(keys)` method for input handling
- Use cooldown timers to prevent input spam

Example:
```python
def update(self, keys):
    cur_time = time()
    if keys[pygame.K_UP] and cur_time - self.last_click > self.cooldown:
        self.current_item += 1
        self.last_click = cur_time
```

### File Organization

```
Cronos/
├── launch.py          # Entry point
├── game.py            # Main game class and loop
├── creature.py        # Creature classes
├── person.py          # Player and NPC classes
├── fight.py           # Combat system
├── inventory.py       # Inventory UI
├── items.py           # Item classes
├── skills.py          # Skill classes
├── statuses.py        # Status effect classes
├── dialogue.py        # Dialogue system
├── menu.py            # Menu screens
├── shop.py            # Shop interface
├── map.py             # Map handling and events
├── statemanager.py    # Game state management
├── assets/            # Game assets (images)
├── fonts/             # Font files
└── maps/              # Tiled map files (.tmx)
```

### Common Color Scheme

- Background: `(0, 0, 0)` (black) or `(200, 200, 200)` (light gray)
- Primary UI: `(128, 0, 35)` (dark red/burgundy)
- Active/Selected: `(255, 255, 255)` (white)
- Text: `(255, 255, 255)` on dark, `(0, 0, 0)` on light

### Key Input Handling

- Movement: Arrow keys or WASD
- Confirm: `pygame.K_RETURN` or `pygame.K_SPACE`
- Cancel/Back: `pygame.K_c` or `pygame.K_ESCAPE`
- Sprint: `pygame.K_LSHIFT` or `pygame.K_RSHIFT`
- Inventory toggle: `pygame.K_i`
