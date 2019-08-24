# Project Idea:
# Go to a random song page on the Miku wiki (https://www5.atwiki.jp/hmiku/tag/曲)
# Or go to a page on the Vocaloid Lyrics Wiki
# Get the song name, lyrics, producer, singer, and page link
# Display the data in a window
# Have the ability to repeat as much as you want

'''Miku wiki'''
# Song lyrics start at .find("h3", text = "歌詞")
# and end right before .find("h3", text = コメント")
# Song pages will be like: https://www5.atwiki.jp/hmiku/pages/NUMBER.html
# The NUMBER doesn't start at 1, need to find min/max values

'''Vocaloid Lyrics wiki'''
# Song lyrics stored in a <table>
# Can get all lyrics with .find("table", style = "width:100%")
# Random song page: "https://vocaloidlyrics.fandom.com/wiki/Special:Random"

'''
    Use beautifulsoup for scraping,
    requests for getting website data,
    and lxml for parsing the HTML
'''
from bs4 import BeautifulSoup
import requests
# Test with AstroPage
'''
web_data = requests.get("https://astropage.neocities.org").text
web_soup = BeautifulSoup(web_data, "lxml")

print(web_soup.prettify())
'''
### vlw_ will be for "Vocaloid Lyrics Wiki" ###
vlw_random_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/May_I_Know_U").text
#vlw_random_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/Special:Random").text
vlw_soup = BeautifulSoup(vlw_random_song, "lxml")
if ("(disambiguation)" in vlw_soup.title.text):
    print("Disambiguation page found")
    print(vlw_soup.title.text)
    print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
else:
    try:
        title_format = vlw_soup.title.text.find("|")
        singers = []
        for singer in vlw_soup.find_all("a", class_ = "mw-redirect"):
            singers.append(singer.text)
        
        print("Title:", vlw_soup.title.text[:title_format].strip())
        print("Singer(s): ", end = "")
        for singer in range(0,len(singers)-1):
            if (singer == len(singers)-2):
                print(singers[singer])
            else:
                print(singers[singer], end = ", ")
        print(f"Producer: {singers[len(singers)-1]}")
        print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
        try:
##            lyrics_table = vlw_soup.find("table", style = "width:100%")
##            for lyric in lyrics_table.find_all("td").stripped_strings:
##                print(lyric.text)
##            print(vlw_soup.find("table", style = "width:100%").text)
            for lyric in vlw_soup.find("table", style = "width:100%").strings:
                print(lyric)
        except AttributeError:
            print(vlw_soup.find("div", class_ = "poem").text)
    except:
        print("Page error, try again.")

