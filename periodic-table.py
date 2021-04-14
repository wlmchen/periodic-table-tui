from curses import wrapper
from data import table, elements, logo, box
import curses

position = [3, 3]

def get_element(y, x):
    for element in elements:
        if element[1] == (y, x):
            return element
    return None

def find_element(name):
    for element in elements:
        for n in element[2]:
            if n.lower() == name.lower():
                return element
    return None


def navigate(stdscr):
    text = ""
    while True:
        key = stdscr.getch()
        c = chr(key)
        if key == 259: # up arrow
            if get_element(position[0] - 3, position[1]) is not None:
                position[0] = position[0] - 3
        if key == 258: # down arrow
            if get_element(position[0] + 3, position[1]) is not None:
                position[0] = position[0] + 3
        if key == 261: # right arrow
            if get_element(position[0], position[1] + 4) is not None:
                position[1] = position[1] + 4
        if key == 260:
            if get_element(position[0], position[1] - 4) is not None:
                position[1] = position[1] - 4
        if ("A" <= c <= "z") or c == " ":
            if len(text) <= 16:
                text += c
        if key == curses.KEY_ENTER or key in [10, 13]:
            print(find_element(text))
            text = ''


        draw_table(stdscr, 0, 0, elements)
        stdscr.addstr(21, 9, text)
        draw_highlighted_box(stdscr, position[0], position[1])
        draw_details_box(stdscr, get_element(position[0], position[1]))

def draw_logo(stdscr):
    stdscr.addstr(0,0, logo)

def draw_table(stdscr, y, x, elements):
    for line in range(0, len(table)):
        stdscr.addstr(line+y+1, x, table[line])

    for item in elements:
        stdscr.addstr(item[1][0], item[1][1]-1, item[0])

def draw_highlighted_box(stdscr, y, x):
    y = y-1
    stdscr.addstr(y-1, x-3, '╦═══╦', curses.color_pair(2))
    stdscr.addstr(y, x-3, '║', curses.color_pair(2))
    stdscr.addstr(y, x+1, '║', curses.color_pair(2))
    stdscr.addstr(y+1, x-3, '║', curses.color_pair(2))
    stdscr.addstr(y+1, x+1, '║', curses.color_pair(2))
    stdscr.addstr(y+2, x-3, '╩═══╩', curses.color_pair(2))

def draw_details_box(stdscr, element):
    stdscr.addstr(3, 80, element[2][0])
    for line in range(0, len(box)):
        stdscr.addstr(line, 80, box[line])


def curses_init(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
    stdscr.erase()



def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses_init(stdscr)
    #draw_logo(stdscr)
    draw_table(stdscr, 0, 0, elements)
    navigate(stdscr)


    stdscr.refresh()
    stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)

