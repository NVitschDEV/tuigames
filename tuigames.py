import curses
from curses.textpad import rectangle


def main(stdscr):
    # Initial setup
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.use_default_colors()

    # Define our colors
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Grid component dimensions
    rows, cols = 2, 3
    box_h = 6
    box_w = 20
    gap_y = 2
    gap_x = 4

    # Calculate the total physical size of the grid
    total_w = (cols * box_w) + ((cols - 1) * gap_x)
    total_h = (rows * box_h) + ((rows - 1) * gap_y)

    current_selection = 0

    while True:
        stdscr.erase()
        sh, sw = stdscr.getmaxyx()

        # 1. Safety Check: Ensure terminal can fit the grid + some padding
        if sh < total_h + 4 or sw < total_w + 4:
            warning1 = "TERMINAL TOO SMALL!"
            warning2 = (
                f"Current: {sw}x{sh}. Need at least: {total_w + 4}x{total_h + 4}."
            )

            stdscr.addstr(1, (sw - len(warning1)) // 2, warning1, curses.color_pair(2))
            stdscr.addstr(2, (sw - len(warning2)) // 2, warning2)
            stdscr.getch()
            continue

        # 2. Centering Math: Find the top-left starting coordinate for the whole grid
        start_y = (sh - total_h) // 2
        start_x = (sw - total_w) // 2

        # 3. Centered Instructions
        instructions = "Linux Mode: Use WASD or Arrows to navigate. Press 'q' to quit."
        # Place instructions dynamically above the grid
        stdscr.addstr(max(0, start_y - 2), (sw - len(instructions)) // 2, instructions)

        # 4. Draw the Grid
        for i in range(6):
            r = i // cols
            c = i % cols

            # Calculate coordinates relative to our centered starting point
            y1 = start_y + (r * (box_h + gap_y))
            x1 = start_x + (c * (box_w + gap_x))
            y2 = y1 + box_h
            x2 = x1 + box_w

            # Draw the box outline
            rectangle(stdscr, y1, x1, y2, x2)

            # Calculate center of the individual box for text
            center_y = y1 + (box_h // 2)
            label = f" Window {i + 1} "

            # Apply highlight if selected
            if i == current_selection:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(center_y, x1 + 1, label.center(box_w - 1))
                stdscr.addstr(center_y + 1, x1 + 1, " Selected ".center(box_w - 1))
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(center_y, x1 + 1, label.center(box_w - 1))

        # 5. Input Handling
        key = stdscr.getch()

        if key in [curses.KEY_UP, ord("w"), ord("W")]:
            if current_selection >= cols:
                current_selection -= cols
        elif key in [curses.KEY_DOWN, ord("s"), ord("S")]:
            if current_selection < (rows - 1) * cols:
                current_selection += cols
        elif key in [curses.KEY_LEFT, ord("a"), ord("A")]:
            if current_selection % cols != 0:
                current_selection -= 1
        elif key in [curses.KEY_RIGHT, ord("d"), ord("D")]:
            if current_selection % cols != cols - 1:
                current_selection += 1
        elif key in [ord("q"), ord("Q")]:
            break


if __name__ == "__main__":
    curses.wrapper(main)
