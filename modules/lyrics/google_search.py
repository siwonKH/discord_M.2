import config
from modules.request.async_request import get_request
from modules.request.async_bs4 import do_beautiful_soup


async def google_lyrics(search):
    parse_len = config.parse_len

    try:
        url = "https://www.google.com/search?q=" + search + " lyrics"
        res = await get_request(url)
        soup = await do_beautiful_soup(res.text)
        title = soup.select_one('.kno-ecr-pt > span').text
        artist = soup.select_one('.wwUB2c').text
        lyrics_element = soup.select('.bbVIQb')[1]

        lyrics = ""
        for paragraph in lyrics_element.select('div'):
            for sentence in paragraph.select('span'):
                lyrics += sentence.text + "\n"
            lyrics += "\n"
        lyrics_len = len(lyrics)
    except:
        return None, None, None, None

    parse_pos = [0]

    pos = parse_len
    while lyrics_len > pos:
        while lyrics[pos] != "\n":
            pos -= 1
        parse_pos.append(pos)
        pos += parse_len
    parse_pos.append(lyrics_len)
    return lyrics, title, artist, parse_pos