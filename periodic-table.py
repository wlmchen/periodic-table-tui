#!/usr/bin/env python3
import time
import math
import json
import os.path
import curses

position = [3, 3]

box = [
"---------------",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"|",
"---------------"]

table = []

# For generating the periodic table

def generate_table():
    line = "═║"
    corner = "╔╗╝╚"
    junction = "╠╦╣╩╬"

    table_width = 18
    table_format = [
         1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,
         3,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  6,  7,  8,  9, 10,
        11, 12,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
        55, 56, -1, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
        87, 88, -2,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,
         0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
         0,  0, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,  0,
         0,  0, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,100,101,102,103,  0
    ]
    table_column_numbers = [
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,18,
        0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,13,14,15,16,17, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 3, 4, 5, 6, 7, 8, 9,10,11,12, 0, 0, 0, 0, 0, 0
    ]
    table_height = len(table_format) // table_width

    table = [(" "*4*table_width + " ") for i in range(3*table_height+2)]

    for z,i in enumerate(table_column_numbers):
        if i==0:
            continue

        x = (z % table_width) * 4 + 1
        y = (z // table_width) * 3

        table[y] = table[y][:x] + str(i).rjust(2,' ') + table[y][x+2:]

    for z,i in enumerate(table_format):
        if i==0:
            continue
        if i>118:
            continue

        element = elements[i-1]
        x = (z % table_width) * 4
        y = (z // table_width) * 3 + 1
        if y//3 >= 7:
            x += 1
            y -= 1

        if i==-1:
            table[y+1] = table[y+1][:x+1] + "57-" + table[y+1][x+4:]
            table[y+2] = table[y+2][:x+1] + " 71" + table[y+2][x+4:]
            continue
        if i==-2:
            table[y+1] = table[y+1][:x+1] + "89-" + table[y+1][x+4:]
            table[y+2] = table[y+2][:x+1] + "103" + table[y+2][x+4:]
            continue

        b = get_surrounding_elements(table_format, table_width, z)

        tl = get_corner_piece(b,0,corner,junction)
        tr = get_corner_piece(b,1,corner,junction)
        br = get_corner_piece(b,2,corner,junction)
        bl = get_corner_piece(b,3,corner,junction)

        element["corners"] = [tl,tr,br,bl]

        for j in range(4):
            a=table[y+j]
            if j==0:
                table[y] = a[:x] + tl + line[0]*3 + tr + a[x+5:]
            elif j==1:
                table[y+1] = a[:x] + line[1] + str(i).ljust(3) + line[1] + a[x+5:]
            elif j==2:
                table[y+2] = a[:x] + line[1] + " "*3 + line[1] + a[x+5:]
            elif j==3:
                table[y+3] = a[:x] + bl + line[0]*3 + br + a[x+5:]

    return table

def get_corner_piece(detected_elements, i, corner, junction):
    a = 2*i
    l = len(detected_elements)

    less = detected_elements[(a+l-1)%l]
    middle = detected_elements[a]
    more = detected_elements[(a+1)%l]
    s = less+middle+more

    if s==3:
        return junction[4]
    elif s==2:
        return junction[4]
    elif s==1:
        if less:
            return junction[(i+1)%4]
        elif more:
            return junction[(i)%4]
    elif s==0:
        return corner[i]

def get_surrounding_elements(table_format, table_width, i):
    # Start the detect with all values checkable
    r = [1,1,1,1,1,1,1,1]
    m = i % table_width
    l = len(table_format)

    # Detect edges of the table
    q1 = i < table_width
    q2 = m == table_width -1
    q3 = i >= l - table_width
    q4 = m == 0

    # There is no elements to the side where the edge of the board is
    if q1:
        r[1] = 0
    if q2:
        r[3] = 0
    if q3:
        r[5] = 0
    if q4:
        r[7] = 0

    # There is no elements to the diagonal if it is at one of those edges
    if q1 or q2:
        r[2] = 0
    if q2 or q3:
        r[4] = 0
    if q3 or q4:
        r[6] = 0
    if q4 or q1:
        r[0] = 0

    # Detect if there are surrounding elements on the checkable sides
    for z,j in enumerate(r):
        if j:
            r[z] = detect_surrounding_borders(table_format, table_width, z, i)

    return r

def detect_surrounding_borders(table_format, table_width, z, i):
    # Detect if an element next to the current one exists
    p = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)][z]
    if table_format[i+p[0]+p[1]*table_width] <= 0:
        return 0
    return 1



# For navigating the periodic table

def get_element(y, x):
    for element in elements:
        if element['coordinates'] == [y, x]:
            return element
    return None

def find_element(name):
    for element in elements:
        for n in element['names']:
            if n.lower() == name.lower():
                return element
        if element['symbol'].lower() == name.lower():
            return element
    return None

def navigate(stdscr, min_h, min_w):
    text = ""
    not_found = False
    draw_table(stdscr, 0, 0, elements)
    stdscr.addstr(35, 1, "Search: ")
    element = get_element(position[0], position[1])
    draw_highlighted_box(stdscr, element, position[0], position[1])
    draw_details_box(stdscr, element, 2, 76)
    while True:
        check_term_minsize(stdscr, min_h, min_w)
        try:
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
                if text.lower() == 'quit':
                    return
                element = find_element(text)
                if element is None:
                    not_found = True
                if element is not None:
                    position[0], position[1] = element['coordinates'][0], element['coordinates'][1]
                text = ''
            if key == curses.KEY_BACKSPACE:
                text = text[:-1]


            stdscr.erase()
            if not_found is True:
                stdscr.addstr(36, 1, "NOT FOUND", curses.color_pair(6))
                not_found = False
            draw_table(stdscr, 0, 0, elements)
            stdscr.addstr(35, 1, "Search: ")
            stdscr.addstr(35, 9, text)
            element = get_element(position[0], position[1])
            draw_highlighted_box(stdscr, element, position[0], position[1])
            draw_details_box(stdscr, element, 2, 76)
        except KeyboardInterrupt:
            stdscr.refresh
            return
        except:
            check_term_minsize(stdscr, min_h, min_w)

def draw_table(stdscr, y, x, elements):
    for line in range(0, len(table)):
        stdscr.addstr(line+y+1, x, table[line], curses.color_pair(7))

    for item in elements:
        stdscr.addstr(item['coordinates'][0]+1, item['coordinates'][1]-1, item['symbol'])

def draw_highlighted_box(stdscr, element, y, x):
    corners = element["corners"]
    stdscr.addstr(y-1, x-3, corners[0]+'═══'+corners[1], curses.color_pair(2))
    stdscr.addstr(y, x-3, '║', curses.color_pair(2))
    stdscr.addstr(y, x+1, '║', curses.color_pair(2))
    stdscr.addstr(y+1, x-3, '║', curses.color_pair(2))
    stdscr.addstr(y+1, x+1, '║', curses.color_pair(2))
    stdscr.addstr(y+2, x-3, corners[3]+'═══'+corners[2], curses.color_pair(2))

def draw_details_box(stdscr, element, y, x):
    if element['state'] == 'gas':
        emoji = '💨'
    if element['state'] == 'liq':
        emoji = '💧'
    if element['state'] == 'solid':
        emoji = '🧊'
    if element['state'] == 'artificial':
        emoji = '🧪'
    stdscr.addstr(y, x, element['names'][0], curses.color_pair(5))
    stdscr.addstr(y+1, x, 'Valence Electrons: ' + element['valence'])
    stdscr.addstr(y+2, x, 'Neutrons: ' + str(element['neutrons']))
    stdscr.addstr(y+3, x, 'Protons: ' + str(element['protons']))
    stdscr.addstr(y+4, x, 'Electrons: ' + str(element['electrons']))
    stdscr.addstr(y+5, x, 'State: ' + element['state'] + ' ' + emoji)
    stdscr.addstr(y+6, x, 'Atomic Radius: ' + element['radius'] + ('' if element['radius']=='' else 'pm'))
    try:
        stdscr.addstr(y+7, x, 'Density: ' + str(float(element['density'])))
    except:
        pass
    stdscr.addstr(y+8, x, 'Electronegativity: ' + element['electronegativity'])
    stdscr.addstr(y+9, x, 'Melting Point: ' + element['melting'])
    stdscr.addstr(y+10, x, 'Boiling Point: ' + element['boiling'])
    stdscr.addstr(y+11, x, 'Specific Heat: ' + element['specific_heat'])
    stdscr.addstr(y+12, x, 'Year of Discovery: ' + element['year'])
    for line in range(0, len(box)):
        stdscr.addstr(line, 74, box[line], curses.color_pair(5))


def curses_init(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.erase()

def check_term_minsize(stdscr, min_h, min_w):
    while True:
        h, w = stdscr.getmaxyx()
        if (h < min_h) or (w < min_w):
            stdscr.erase()
            if h < min_h:
                red_h_bar = str("V" * (w-1))
                stdscr.addstr(h-1, 0, red_h_bar, curses.color_pair(6))
            if w < min_w:
                for l in range(0, h):
                    stdscr.addstr(l, w-2, ">", curses.color_pair(6))
            res = "Terminal too small!"
            stdscr.addstr(h//2, w//2-len(res)//2, res)
        stdscr.refresh()
        if (h >= min_h) and (w >= min_w):
            break
        time.sleep(.10)


def main(stdscr):
    stdscr.clear()
    curses_init(stdscr)
    min_h, min_w = 35, 95
    check_term_minsize(stdscr, min_h, min_w)

    navigate(stdscr, min_h, min_w)

if __name__ == "__main__":
    if os.path.exists('elements.json'):
        with open('elements.json','r') as f:
            elements = json.loads(f.read())
        table = generate_table()
        curses.wrapper(main)
    else:
        print("Unable to load elements")
