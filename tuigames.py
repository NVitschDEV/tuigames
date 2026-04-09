import curses
from curses.textpad import rectangle

# --- ASCII ART DEFINITIONS ---
ART_SNAKE = ["  ____   ", " /  __\  ", " |  \/|  ", " \____/  ", "  SNAKE  "]

ART_SETTINGS = ["   ___   ", "  / _ \  ", " | (_) | ", "  \___/  ", " SETTINGS"]

ART_QUIT = ["  ____   ", " |  _ \  ", " | | | | ", " |_| |_| ", "  QUIT   "]

CUSTOM_ART = {0: ART_SNAKE, 1: ART_SETTINGS, 2: ART_QUIT}


def main(stdscr):
    # Setup
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.use_default_colors()

    # Pair 1: Box & Art | Pair 2: Selection Highlight
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)

    # Grid Dimensions (1 Row, 3 Columns)
    rows, cols = 1, 3
    box_h, box_w = 8, 22
    gap_x = 4

    # Calculate total width/height for centering
    total_w = (cols * box_w) + ((cols - 1) * gap_x)
    total_h = box_h

    current_selection = 0

    while True:
        stdscr.erase()
        sh, sw = stdscr.getmaxyx()

        # Calculate centering coordinates
        start_y = (sh - total_h) // 2
        start_x = (sw - total_w) // 2

        # Draw the 3 Boxes
        for i in range(3):
            # Calculate position for each box in the row
            x1 = start_x + (i * (box_w + gap_x))
            y1 = start_y
            x2, y2 = x1 + box_w, y1 + box_h

            # 1. Draw the box border
            stdscr.attron(curses.color_pair(1))
            rectangle(stdscr, y1, x1, y2, x2)

            # 2. Draw the unique ASCII Art for this index
            art = CUSTOM_ART.get(i, ["No Art"])
            art_start_y = y1 + (box_h - len(art)) // 2

            for line_idx, line in enumerate(art):
                print_x = x1 + (box_w - len(line)) // 2
                stdscr.addstr(art_start_y + line_idx, print_x, line)
            stdscr.attroff(curses.color_pair(1))

            # 3. Draw the Underline + Pointer IF selected
            if i == current_selection:
                underline_char = "═"
                underline_str = underline_char * (box_w + 1)

                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                # Place underline exactly 1 line below the box
                stdscr.addstr(y2 + 1, x1, underline_str)
                # Centered pointer
                stdscr.addstr(y2 + 1, x1 + (box_w // 2), "▲")
                stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        # Instructions Footer
        instr = "ARROWS to Move | ENTER to Select | 'q' to Quit"
        stdscr.addstr(sh - 1, (sw - len(instr)) // 2, instr)

        # Input Handling
        key = stdscr.getch()

        if key in [curses.KEY_LEFT, ord("a"), ord("A")]:
            if current_selection > 0:
                current_selection -= 1
        elif key in [curses.KEY_RIGHT, ord("d"), ord("D")]:
            if current_selection < 2:
                current_selection += 1
        elif key in [ord("\n"), curses.KEY_ENTER]:
            # Action based on selection
            if current_selection == 2:  # Quit option
                break
        elif key in [ord("q"), ord("Q")]:
            break


if __name__ == "__main__":
    curses.wrapper(main)
