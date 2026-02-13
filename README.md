# Cronos

A 2D RPG game built with Python and pygame featuring exploration, NPCs with dialogue systems, and an inventory/shop system.

## Requirements

- Python 3.10 - 3.14
- Poetry (for dependency management)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cronos.git
cd cronos

# Install dependencies with Poetry
poetry install

# Run the game
poetry run python launch.py
```

Alternatively, without Poetry:

```bash
pip install pygame pytmx
python launch.py
```

## Controls

| Action | Keys |
|--------|------|
| Movement | Arrow keys or WASD |
| Sprint | Hold Shift |
| Interact | E or Space |
| Inventory | I |
| Pause/Menu | Escape |
| Confirm | Enter or Space |
| Cancel/Back | C or Backspace |

## Project Structure

```
Cronos/
├── launch.py           # Entry point
├── src/
│   ├── core/           # Game loop, state management
│   ├── entities/       # Player, NPCs
│   ├── systems/        # Inventory, shop
│   ├── world/          # Maps, events
│   ├── ui/             # Menus, HUD
│   └── data/           # Items, dialogue
├── assets/             # Game sprites and images
├── maps/               # Tiled map files (.tmx)
└── fonts/              # Font files
```

## Features

- **Exploration**: Navigate through tile-based maps with collision detection
- **NPCs**: Interact with various characters with branching dialogue
- **Inventory System**: Manage items with a dynamic UI
- **Shop System**: Buy and sell items with merchants
- **Map Events**: Teleporters, dialogue triggers, and more

## Creating Maps

Maps are created using [Tiled Map Editor](https://www.mapeditor.org/). Place `.tmx` files in the `maps/` directory.

Custom tile properties:
- `impassable`: Boolean - prevents player movement
- `danger_zone`: Boolean - (reserved for future use)

## License

Apache 2.0 - see [LICENSE](LICENSE) for details.
