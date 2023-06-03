import curses
import pickle

# Initialize curses
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)

# Initialize the maps and dimensions
width = 30
height = 30
layer1 = [[0] * width for _ in range(height)]
layer2 = [[0] * width for _ in range(height)]
layer3 = [[0] * width for _ in range(height)]

# Function to draw the maps
def draw_maps(stdscr, active_layer, cursor_pos):
    stdscr.clear()

    # Determine the active layer color
    if active_layer == 1:
        active_color = curses.color_pair(1)
    elif active_layer == 2:
        active_color = curses.color_pair(2)
    elif active_layer == 3:
        active_color = curses.color_pair(3)
    else:
        active_color = curses.color_pair(0)

    # Draw the maps
    for row in range(height):
        for col in range(width):
            tile1 = str(layer1[row][col])
            tile2 = str(layer2[row][col])
            tile3 = str(layer3[row][col])

            if active_layer == 1:
                stdscr.addstr(row, col * 4, tile1, active_color)
            elif active_layer == 2:
                stdscr.addstr(row, col * 4, tile2, active_color)
            elif active_layer == 3:
                stdscr.addstr(row, col * 4, tile3, active_color)
            else:
                stdscr.addstr(row, col * 4, tile1)
                stdscr.addstr(row, col * 4 + 1, tile2)
                stdscr.addstr(row, col * 4 + 2, tile3)

    # Draw the cursor
    stdscr.move(cursor_pos[0], cursor_pos[1] * 4)

    stdscr.refresh()
# Function to save the maps to a file
def save_maps(file_name):
    maps = {
        'layer1': {
            'data': layer1,
            'width': width,
            'height': height
        },
        'layer2': {
            'data': layer2,
            'width': width,
            'height': height
        },
        'layer3': {
            'data': layer3,
            'width': width,
            'height': height
        }
    }

    with open(file_name, 'wb') as file:
        pickle.dump(maps, file)

# Main program loop
def main(stdscr):
    active_layer = 1
    cursor_pos = [0, 0]

    while True:
        # Draw the maps
        draw_maps(stdscr, active_layer, cursor_pos)

        # Get user input
        key = stdscr.getch()

        if key == ord('1'):
            active_layer = 1
        elif key == ord('2'):
            active_layer = 2
        elif key == ord('3'):
            active_layer = 3
        elif key == ord('+'):
            if active_layer == 1:
                layer1[cursor_pos[0]][cursor_pos[1]] += 1
            elif active_layer == 2:
                layer2[cursor_pos[0]][cursor_pos[1]] += 1
            elif active_layer == 3:
                layer3[cursor_pos[0]][cursor_pos[1]] += 1
        elif key == ord('-'):
            if active_layer == 1:
                layer1[cursor_pos[0]][cursor_pos[1]] -= 1
            elif active_layer == 2:
                layer2[cursor_pos[0]][cursor_pos[1]] -= 1
            elif active_layer == 3:
                layer3[cursor_pos[0]][cursor_pos[1]] -= 1
        elif key == curses.KEY_UP:
            cursor_pos[0] -= 1
            if cursor_pos[0] < 0:
                cursor_pos[0] = 0
        elif key == curses.KEY_DOWN:
            cursor_pos[0] += 1
            if cursor_pos[0] >= height:
                cursor_pos[0] = height - 1
        elif key == curses.KEY_LEFT:
            cursor_pos[1] -= 1
            if cursor_pos[1] < 0:
                cursor_pos[1] = 0
        elif key == curses.KEY_RIGHT:
            cursor_pos[1] += 1
            if cursor_pos[1] >= width:
                cursor_pos[1] = width - 1
        elif key == ord('s'):
            # Prompt the user for a file name
            stdscr.addstr(height + 2, 0, "Enter file name: ")
            file_name = stdscr.getstr().decode('utf-8')
            save_maps(file_name)
# Run the program
curses.wrapper(main)