import random
import requests
from bs4 import BeautifulSoup
import clipboard
import textwrap
try:
    import curses
except ImportError:
    curses = None

url = 'http://www.9sep.org/free-xunlei-vip'


def get_source(debug_func=lambda x: None):
    # with open('cache.json', 'r', encoding='utf-8') as f:
    #     result = json.load(f)
    # return result
    debug_func('get content from %s ...' % url)
    req = requests.get(url)
    debug_func('DONE')
    debug_func('analyze...')
    soup = BeautifulSoup(req.text, 'html5lib')
    debug_func('DONE')
    debug_func('find section...')
    articles = soup.find_all('article')
    debug_func('DONE')
    collect = []

    debug_func('find user name and password...')
    for each in articles:
        user_and_password = each.find_all(id='cp')
        for user, pwd in zip(user_and_password[::2], user_and_password[1::2]):
            collect.append((user.text, pwd.text))
    debug_func('DONE')
    return collect

if curses is not None:

    class Screen(object):

        def __init__(self):
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.keypad(1)

            self.stdscr = stdscr
            self.history = []

        def close(self):
            curses.nocbreak()
            self.stdscr.keypad(0)
            curses.echo()
            curses.endwin()

        __del__ = close

        @property
        def height(self):
            return self.stdscr.getmaxyx()[0]

        @property
        def width(self):
            return self.stdscr.getmaxyx()[1]

        def write(self, line, refresh=False):
            self.history.append(line)
            if refresh:
                self.refresh()

        def erase_with(self, line, index=-1, refresh=False):
            self.history[index] = line
            if refresh:
                self.refresh()

        def erase(self, refresh=False):
            self.history.pop(-1)
            if refresh:
                self.refresh()

        def refresh(self):
            addch = self.stdscr.addch
            proper_lines = []
            accept_width = self.width
            for each_line in self.history:
                if len(each_line) < accept_width:
                    proper_lines.append(
                            self._fill_str(each_line, accept_width))
                else:
                    text = textwrap.fill(each_line, accept_width)
                    proper_lines.extend(self._fill_str(x, accept_width)
                                        for x in text.splitlines())

            accept_height = self.height
            now_height = len(proper_lines)
            if now_height >= accept_height:
                proper_lines = proper_lines[now_height - accept_height + 1:]

            for x, line in enumerate(proper_lines):
                for y, each_word in enumerate(line):
                    addch(x, y, each_word)
            self.stdscr.refresh()

        def _fill_str(self, string, width):
            lack = width - len(string)
            return string + ' ' * lack

        def clear(self):
            del self.history[:]
            self.stdscr.clear()

        def getch(self):
            return self.stdscr.getch()

        def check_input(self, key):
            return self.getch() == ord(key)

else:

    try:
        input = raw_input
    except NameError:
        pass

    class Screen(object):

        def __init__(self):
            self._input = None

        def write(self, text, refresh=False):
            print(text)

        def clear(self):
            pass

        def refresh(self):
            self._input = input()

        def check_input(self, i):
            return self._input == i

        erase_with = write

        def erase(self):
            pass

        def getch(self):
            pass


def main():
    screen = Screen()
    screen.write('source: %s' % url, True)
    collect = get_source(lambda x: screen.write(x, True))
    random.shuffle(collect)
    screen.clear()
    screen.write('       username | password')
    screen.write('================|=========')
    for index, (user, pwd) in enumerate(collect):
        line = '%15s | %s' % (user, pwd)
        screen.write(line)
        clipboard.copy(user)
        screen.write('user copied, enter to copy password')
        screen.refresh()
        if screen.check_input('q'):
            return

        clipboard.copy(pwd)
        screen.erase_with('password copied, enter for next')
        screen.refresh()
        if screen.check_input('q'):
            return

        screen.erase()

    screen.write('no more. Any key to exit')
    screen.getch()


if __name__ == '__main__':
    main()
