import curses

# --- ASCII ART DEFINITIONS ---
ART_SNAKE = ["  SNAKE  ", "  (o o)  ", "  --v--  "]
ART_SETTINGS = [" SETTINGS", "   [X]   ", "   / \   "]
ART_QUIT = ["   QUIT  ", "   [Q]   ", "   / \   "]

CUSTOM_ART = {0: ART_SNAKE, 1: ART_SETTINGS, 2: ART_QUIT}


def draw_custom_box(stdscr, y1, x1, y2, x2, is_selected):
    """Draws a single-line box for normal, double-line for selected."""
    if is_selected:
        # Double-line border characters
        chars = {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "v": "║", "h": "═"}
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
    else:
        # Single-line border characters
        chars = {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "v": "│", "h": "─"}
        stdscr.attron(curses.color_pair(1))

    # Draw Corners
    stdscr.addch(y1, x1, chars["tl"])
    stdscr.addch(y1, x2, chars["tr"])
    stdscr.addch(y2, x1, chars["bl"])
    stdscr.addch(y2, x2, chars["br"])

    # Draw Horizontal lines
    for x in range(x1 + 1, x2):
        stdscr.addch(y1, x, chars["h"])
        stdscr.addch(y2, x, chars["h"])

    # Draw Vertical lines
    for y in range(y1 + 1, y2):
        stdscr.addch(y, x1, chars["v"])
        stdscr.addch(y, x2, chars["v"])

    stdscr.attroff(curses.color_pair(1))
    stdscr.attroff(curses.color_pair(2))


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.use_default_colors()

    # Pair 1: Normal Gray/White | Pair 2: Teal/Cyan Highlight
    curses.init_pair(1, 250, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)

    cols = 3
    # Selection box is slightly larger than others
    box_h, box_w = 10, 26
    gap_x = 4
    total_w = (cols * box_w) + ((cols - 1) * gap_x)
    current_selection = 0

    while True:
        stdscr.erase()
        sh, sw = stdscr.getmaxyx()
        start_y = (sh - box_h) // 2
        start_x = (sw - total_w) // 2

        for i in range(3):
            is_sel = i == current_selection

            # Layout logic
            x1 = start_x + (i * (box_w + gap_x))
            y1 = start_y - 2 if is_sel else start_y  # Selected box pops up slightly
            x2, y2 = x1 + box_w, y1 + box_h

            # 1. Draw the stylized box
            draw_custom_box(stdscr, y1, x1, y2, x2, is_sel)

            # 2. Draw ASCII Art
            art = CUSTOM_ART.get(i, [])
            art_y = y1 + (box_h - len(art)) // 2
            for idx, line in enumerate(art):
                stdscr.addstr(art_y + idx, x1 + (box_w - len(line)) // 2, line)

            # 3. Draw the stylized pointer (The Teal double-line + Triangle)
            if is_sel:
                pointer_y = y2 + 2
                pointer_line = "═══"
                # Centering the custom selector: ═══ ▲ ═══
                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                center_x = x1 + (box_w // 2)
                stdscr.addstr(pointer_y, center_x - 4, pointer_line)
                stdscr.addstr(pointer_y, center_x, "▲")
                stdscr.addstr(pointer_y, center_x + 2, pointer_line)
                stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()
        key = stdscr.getch()

        if key in [curses.KEY_LEFT, ord("a")]:
            current_selection = max(0, current_selection - 1)
        elif key in [curses.KEY_RIGHT, ord("d")]:
            current_selection = min(2, current_selection + 1)
        elif key in [ord("q"), 27]:  # q or ESC
            break


if __name__ == "__main__":
    curses.wrapper(main)
