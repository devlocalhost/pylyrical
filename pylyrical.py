from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from rich.traceback import install

from platform import system as sysname
from requests import get
from time import sleep
from bs4 import BeautifulSoup
from os import system

install()

API_URL = 'https://api.genius.com/search/'
TKN = 'S3CR3T0K3N' # get it on https://genius.com/api-clients by creating a client and clicking Generate Access Token
# SRCH = 'killshot eminem' # Your search term
CLEARCMD = None # must be a string. if your OS does not use clear or cls to clear the terminal
# then replace None with the command which your OS uses to clear the screen

cust_theme = Theme({'greensty': 'bold #43b581', 'redsty': 'bold #f04947', 'blurplesty': 'bold #7289DA', 'yellowsty': 'bold #fdcc4b', 'light': 'bold #bfbdbd'})
console = Console(theme=cust_theme)

def clearscr(CLEARCMD=None):
    """
    Windows 🤮 (and other OS) support to clean the terminal screen
    """
    if CLEARCMD == None:
        if sysname() == 'Windows':
            system('cls')

        elif sysname() == 'Linux':
            system('clear')

        else:
            console.print(f'Define clear command for "{sysname()}" please!', style='redsty')

    elif CLEARCMD != None:
        clearscr(CLEARCMD)

def scrape(link):
    lyricsform = []
        
    for lyricsdata in BeautifulSoup(get(link).text, 'html.parser').select('div[class*=Lyrics__Container]'):
        dat = lyricsdata.get_text('\n')
        lyricsform.append(f"{dat}\n")

    clearscr()

    console.print(str(''.join(lyricsform)).replace('[', '\n['), style='light')

def search(query_term):
    data = {"q": query_term}
    headers = {"Authorization": f"Bearer {TKN}"}

    result = get(API_URL, params=data, headers=headers).json()

    urls_list = []
    search_results = []

    for song in result['response']['hits']:
        artist = song['result']['artist_names']
        title = song['result']['title']
        genius_url = song['result']['url']

        # thumbnail = song['result']['header_image_url']

        urls_list.append(genius_url)
        search_results.append(f'{title} by {artist}')

    clearscr()

    for name in search_results:
        console.print(f'[blurplesty]{search_results.index(name)}. {name}[/blurplesty]')

    link_num = console.input('[yellowsty]Enter the number of the song you want lyrics for, or type b to go back\n -> [/yellowsty]')

    if link_num.lower() == 'b':
        main()

    else:
        clearscr()

        console.print(f'[greensty]Choosed: {search_results[int(link_num)]}[/greensty]')
        console.print('[yellowsty]Scraping lyrics...[/yellowsty]')

        scrape(urls_list[int(link_num)])

def main():
    clearscr()

    search_term = console.input('[yellowsty]I want to search for...\n -> [/yellowsty]')
    console.print(f'[greensty]Searching for {search_term}[/greensty]')

    search(search_term)

main()
