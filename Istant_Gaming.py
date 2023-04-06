from cloudscraper import create_scraper
from selectolax.parser import HTMLParser
import sqlite3
from datetime import datetime
import sys
from os import system


def scraping():
    
    scraper = create_scraper()
    # Change the link of your countries if you're not italian.
    link_whishlist = 'https://www.instant-gaming.com/it/wishlist/'


    # Puoi sostituire o aggiornare qui il tuo user agent
    # You can replace or update here your user agent
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    # Aggiungi il valore del cookie "auto". Lo puoi trovare su Chrome, nella console degli sviluppatori -> Application -> Cookies. Non condividerlo con nessuno.
    # Add here value of cookie "auto". You can find it in the developer console -> Application -> Cookies. Don't share it.
    cookies = {'auto' : 'set_here_your_value'}
    
    request = scraper.get(link_whishlist, cookies=cookies, headers=headers)
    request.encoding = 'utf-8'
    soup = HTMLParser(request.text)


    cursor = sqlite3.connect(f'{sys.path[0]}/Prezzi_giochi.db')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Prezzi (
    Nome VARCHAR (255),
    Data datetime,
    Prezzo float,
    PRIMARY KEY(Nome, Data, Prezzo))''')
    cursor.commit()
    
    data = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    op_sys = sys.platform.lower()

    for gioco in soup.css('div.item'):

        try:
            nome = gioco.css_first('div.text').text(strip=True)
            prezzo = float(gioco.css_first('div.price').text().strip('€'))
        except:
            continue

        if op_sys == 'linux' and not len(cursor.execute(f'SELECT * FROM Prezzi WHERE Nome="{nome}" AND Prezzo < "{prezzo}"').fetchall()):
            system(f'notify-send -t 5000 "{nome}" "Minimo storico per {nome} a {prezzo}€"')
                   

        cursor.execute(f"INSERT OR REPLACE INTO Prezzi VALUES (?, ?, ?)", (nome, data, prezzo))
    
    cursor.commit()




if __name__ == '__main__':
        scraping()