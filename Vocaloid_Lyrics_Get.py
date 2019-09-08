# Get a random song from the Vocaloid wikis below:
# Hatsune Miku wiki (Japanese only):
# https://www5.atwiki.jp/hmiku/
# Vocaloid Lyrics Wiki (May have English translations):
# https://vocaloidlyrics.fandom.com/wiki/Vocaloid_Lyrics_Wiki

from bs4 import BeautifulSoup
import requests, codecs, random, sys, time


'''Gets a page with requests, handles for connection issues'''
def page_get(web_page):
    timeout_count = 0
    timeout_check = False
    while not(timeout_check):
        try:
            song_page = requests.get(web_page, timeout = 5)
            timeout_check = True
        except Exception:
            if (timeout_count >= 3):
                return None
            timeout_count += 1
            time.sleep(3)
    return song_page


'''Used for printing singers and producers in vlw_song_get'''
def print_a_text(tr_tag):
    if (tr_tag.a == None):
        print(tr_tag.text.strip())
        return
    
    a_tags = tr_tag.find_all("a")
    for index, item in enumerate(a_tags, start = 1):
        if (index == len(a_tags)):
            print(item.text)
        else:
            print(item.text, end = ", ")
    return


def vlw_song_get():
    ### vlw_ will be for "Vocaloid Lyrics Wiki" ###
    
    song_found = False
    while not (song_found):
        song_page = "https://vocaloidlyrics.fandom.com/wiki/Special:Random"
        vlw_song = page_get(song_page)
        
        if (vlw_song == None):
            return "Timeout limit reached, check for connection issues."

        vlw_soup = BeautifulSoup(vlw_song.text, "lxml")
        
        # Handle for if an individual song's page isn't selected
        if ("(disambiguation)" in vlw_soup.title.text):
            print("Disambiguation page found")
            print(vlw_soup.title.text)
            print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
            print("Trying again for a song page...")
            print()
            time.sleep(5)
        else:
            song_found = True
    try:
        title_format = vlw_soup.title.text.find("|")

        print("Title:", vlw_soup.title.text[:title_format].strip())

        print("Original Upload Date: ", end = "")
        print(vlw_soup.find("b", text = "Original Upload Date")
              .next_element.next_element.next_element.next_element.text.strip())

        print("Producers(s): ", end = "")
        print_a_text(vlw_soup.find("b", text = "Producer(s)").parent\
                     .parent.next_sibling.next_sibling)

        print("Singer(s): ", end = "")
        print_a_text(vlw_soup.find("b", text = "Singer").parent\
                     .parent.next_sibling.next_sibling)
        
        print("Link:",vlw_soup.find("link", rel="canonical").get("href"))
        print()
        
        try:
            for ruby in vlw_soup.find_all("ruby"):
                ruby.replace_with(ruby.text)
        except AttributeError:
            pass
        
        try:
            skip_line = ["Japanese", "Romaji", "English", "Official"]
            for lyric in vlw_soup.find("table", style = "width:100%").stripped_strings:
                if not(lyric in skip_line):
                    print(lyric)
        except AttributeError:
            '''For when there is only one language. No further formatting needed.'''
            print(vlw_soup.find("div", class_ = "poem").text)

        # Get translator if available
        for p_tag in vlw_soup.find_all("p"):
            if (p_tag.text.find("English") != -1):
                print()
                print(p_tag.text.strip())

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
            # Try to find a song page
            page_number = str(random.choice(range(14, 39800)))
            song_page = "https://w.atwiki.jp/hmiku/pages/" + page_number + ".html"
            mw_song = page_get(song_page)
        
            if (mw_song == None):
                return "Timeout limit reached, check for connection issues."
            
            mw_soup = BeautifulSoup(mw_song.text, "lxml")
            if (mw_soup.title.text == "エラー - 初音ミク Wiki - アットウィキ"):
                print("Song page not found, trying again...")
                time.sleep(5)
            elif (mw_soup.find("h3", text = "CD紹介") != None):
                # Skip pages for CDs
                print("CD page found, retrying for song page...")
                time.sleep(5)
            elif (mw_soup.find("h3", text = "特徴") != None):
                # Skip pages for Producers
                print("Producer page found, retrying for song page...")
                time.sleep(5)
            else:
                song_found = True
                print()
        title_format = mw_soup.title.text.find(" - 初音ミク Wiki")
        print("Link:", song_page)
        print("Title:", mw_soup.title.text[:title_format])

        # Remove any lyric source links before lyrics section
        try:
            mw_soup.find("a", target = "_blank", rel = "nofollow").parent.decompose()
        except AttributeError:
            pass
        
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
        
        skip_line = ["代表的なPV紹介", ")", "（動画より書き起こし）"]
        if (mw_soup.find("ruby") == None):
            for lyric in mw_strings[lyrics_start:lyrics_end]:
                if not(lyric in skip_line):
                    print(lyric)
        else:
            # Extra formatting for if ruby is used for furigana
            lyrics = [line for line in mw_strings[lyrics_start:lyrics_end]
                      if line not in skip_line]
            while("(" in lyrics):
                for index, lyric in enumerate(lyrics):
                    if lyric == "(":
                        lyrics[index - 2] = lyrics[index - 2] \
                                            + lyrics[index - 1] \
                                            + lyrics[index + 2]

                        lyrics.remove(lyrics[index + 2])
                        lyrics.remove(lyrics[index + 1])
                        lyrics.remove(lyrics[index])
                        lyrics.remove(lyrics[index - 1])
                        break

            for lyric in lyrics:
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
    

'''To do list'''
# Possible feature add: Collect all links from a session and save to file.
# mw: Get upload date if availabe (need to use nico ext link above song info)
# mw: Found page with extra lyrics section that enumerates lyric lines
# (https://w.atwiki.jp/hmiku/pages/23024.html)
# May try to add a way to ignore sections like this, it seems rare though.

# vlw: Format lyrics somehow? Seems too difficult to be worth it.

