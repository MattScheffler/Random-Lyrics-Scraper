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

from bs4 import BeautifulSoup
import requests, codecs, random, sys, time

def vlw_song_get():
    ### vlw_ will be for "Vocaloid Lyrics Wiki" ###
    '''Song with Japanese, Romaji, and English'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/ゴキブリの味_(Gokiburi_no_Aji)").text
    '''Song with Japanese and Romaji only'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/闇屋の娘は眼で殺す_(Yamiya_no_Musume_wa_Me_de_Korosu)").text
    '''Song with only one language'''
    #vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/I%27m_Breathless").text
    '''Random song, will be the final choice used when finished'''
    vlw_song = requests.get("https://vocaloidlyrics.fandom.com/wiki/Special:Random").text
    
    vlw_soup = BeautifulSoup(vlw_song, "lxml")
    # First handle if an individual song's page isn't selected
    if ("(disambiguation)" in vlw_soup.title.text):
        print("Disambiguation page found")
        print(vlw_soup.title.text)
        print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
    else:
        try:
            title_format = vlw_soup.title.text.find("|")
 
            print("Title:", vlw_soup.title.text[:title_format].strip())
            
            print(vlw_soup.find("b", text = "Producer(s)").text + ":")
            print(vlw_soup.find("b", text = "Producer(s)")
                  .next_element.next_element.next_element.next_element.text.strip())

            print(vlw_soup.find("b", text = "Singer").text + "(s):")
            print(vlw_soup.find("b", text = "Singer")
                  .next_element.next_element.next_element.next_element.text.strip())

            print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
            print()
            try:
                #print(vlw_soup.find("table", style = "width:100%").text)
                skip_line = ["Japanese", "Romaji", "English"]
                for lyric in vlw_soup.find("table", style = "width:100%").stripped_strings:
                    if (lyric in skip_line):
                        pass
                    else:
                        print(lyric)
            except AttributeError:
                '''For when there is only one language. No further formatting needed.'''
                print(vlw_soup.find("div", class_ = "poem").text)
        except Exception as e:
            print(e)

    '''Save lyrics to file for testing, may leave the option in the finished program.'''
    ##with codecs.open("Lyrics_Test_File_Stripped.txt","w", encoding = "utf-8") as f:
    ##    for lyric in vlw_soup.find("table", style = "width:100%").stripped_strings:
    ##        f.write(lyric)

def mw_song_get():
    ### mw will be for "Miku Wiki" ###
    ''' Pages have address of "https://w.atwiki.jp/hmiku/pages/NUMBER.html"
        There seems to be ~39,800 pages
        Songs start at page 14
    '''
    try:
        song_found = False
        while not (song_found):
            '''Test page for a producer'''
            #song_page = "view-source:https://w.atwiki.jp/hmiku/pages/11860.html"
            '''Test page for a CD page'''
            #song_page = "https://w.atwiki.jp/hmiku/pages/9146.html"
            '''Test page with furigana in lyrics'''
            #song_page = "view-source:https://w.atwiki.jp/hmiku/pages/39235.html"

            # Try to find a song page
            page_number = str(random.choice(range(14, 39800)))
            song_page = "https://w.atwiki.jp/hmiku/pages/" + page_number + ".html"
            mw_song = requests.get(song_page).text
            mw_soup = BeautifulSoup(mw_song, "lxml")
            if (mw_soup.title.text == "エラー - 初音ミク Wiki - アットウィキ"):
                print("Song page not found, trying again...")
                time.sleep(5)
            elif (mw_soup.find("h3", text = "CD紹介") != None):
                # Skip pages for CDs
                print("CD page found, retrying for song page...")
                time.sleep(5)
            else:
                song_found = True
        title_format = mw_soup.title.text.find(" - 初音ミク Wiki")
        print("Link:", song_page)
        print("Title:", mw_soup.title.text[:title_format])
        
        # get lyrics, composition, arrangement, and singer(s)
        song_info_start = mw_soup.text.find("作詞：")
        song_info_end = mw_soup.text.find("曲紹介")
        # change endpoint when there is no song introduction
        if (song_info_end == -1):
            song_info_end = mw_soup.text.find("歌詞")
        print(mw_soup.text[song_info_start:song_info_end].strip())
        print()

        # Optional song introduction info
        song_intro_start = mw_soup.text.find("曲紹介")
        if not (song_intro_start == -1):
            song_intro_end = mw_soup.text.find("歌詞")
            print(mw_soup.text[song_intro_start:song_intro_end].strip())
            print()
        
        # Get section with lyrics
        mw_strings = [s for s in mw_soup.stripped_strings]
        for s in mw_strings:
            if s == "歌詞":
                lyrics_start = mw_strings.index(s)
            elif s == "コメント":
                lyrics_end = mw_strings.index(s)
            else:
                pass
        for lyric in mw_strings[lyrics_start:lyrics_end]:
            if (lyric == "代表的なPV紹介"):
                pass
            else:
                print(lyric)
                
    except Exception as e:
        print(e)

def main_menu():
    print("Enter 'vlw' to get a random song from the Vocaloid Lyrics Wiki.")
    print("Enter 'mw' to get a random song from the Hatsune Miku Wiki.")
    print("Enter 'quit' to quit the program.")
    
def main(site_choice):
    if (str(site_choice) == "vlw"):
        vlw_song_get()
    elif (str(site_choice) == "mw"):
        mw_song_get()
    elif (str(site_choice) == 'quit'):
        pass
    else:
        print("Use 'vlw' or 'mw'")

if (__name__ == "__main__"):
    # Will need special fonts for displaying Japanese in cmd
    #main(sys.argv[1])
    site_select = str()
    while (site_select != "quit"):
        main_menu()
        site_select = input("Selection: ")
        print()
        main(site_select)
        print()
    print("Ending program")
    end = input("Press 'Enter' key to exit...")
    

#vlw_song_get()
#mw_song_get()


