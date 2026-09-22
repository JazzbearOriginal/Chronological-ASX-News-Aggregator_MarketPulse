######Jazzbear
#####Version#: 105414092026
######Data layout for each site: ("URL": str,"Title": str,"Summary": str | None,"Date": str,"DateTime": datetime)

###imports
from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from nicegui import ui

#############################################################################################Livewiremarket###DONE
###specifies the website and the browser to impersonate
response = requests.get("https://www.livewiremarkets.com/feeds/latest", impersonate="chrome")

###shuts down the code if the website rejects the scraper
if response.status_code != 200:
    raise SystemExit(f"blocked: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

###
lwArticles = []
###
cards = soup.find_all("a", class_="group block sm:flex hover:no-underline visited:text-darkestgray text-body")
times = soup.find_all("time",class_="hidden sm:block sm:flex-none order-1 w-36 uppercase pre-header-sm lg:pre-header-md text-darkgray")

for card, time_tag in zip(cards, times):
    href = card.get("href")
    if not isinstance(href, str):
        continue

    title_tag = card.find("h2")
    summary_tag = card.find("div",class_="paragraph-sm text-darkestgray break-word mt-2 sm:paragraph-xs lg:paragraph-lg")

    ####datetime
    date_string = time_tag.get_text(strip=True)
    date_time = datetime.strptime(date_string,"%B %d, %Y %H:%M")
    lwURL = (f"https://www.livewiremarkets.com{href}")

    lwArticles.append({
        "URL": lwURL,
        "Title": title_tag.get_text(strip=True) if title_tag else None,
        "Summary": summary_tag.get_text(strip=True) if summary_tag else None,
        "Date": date_string,
        "DateTime": date_time
    })

################################################################################################Market Index###DONE
resp = requests.get("https://www.marketindex.com.au/news/category/all?src=kma", impersonate="chrome")

###shuts down the code if the website rejects the scraper
if resp.status_code != 200:
    raise SystemExit(f"blocked: {resp.status_code}")

sou = BeautifulSoup(resp.text, "html.parser")

###declare dicts
seen = set()
miArticles = []
###final dict of stored information

###specifies a section of the site to sort through into the variable
section = sou.find_all("article")
###current time of running
scrape_time = datetime.now()

for sec in section:
    title_tag = sec.find("a", class_ = "text-black hover:underline visited:text-neutral-content-label")
    if not title_tag:
        continue
    href = title_tag.get("href")
    if not isinstance(href, str):
        continue
    if href in seen:
        continue

    seen.add(href)

    date_tag = sec.find("div", class_="time-container smaller-font")
    date = (date_tag.get_text(strip=True)if date_tag else None)
    ###convert to datetime
    tempDate = date
    if "UPDATED" in tempDate:
        tempDate = tempDate.replace("UPDATED", "").strip()
    if "min" in tempDate:
        numb = int(tempDate.split()[0])
        date_obj = scrape_time - timedelta(minutes=numb)

    elif "hour" in tempDate:
        numb = int(tempDate.split()[0])
        date_obj = scrape_time - timedelta(hours=numb)

    else:
        date_obj = datetime.strptime(f"{tempDate} {scrape_time.year}","%d %B %Y")

    miURL = (f"https://www.marketindex.com.au{href}")
    article_data = {
        "URL": miURL,
        "Title": title_tag.get_text(strip=True),
        "Summary": "",
        "Date": date,
        "DateTime": date_obj
    }
    miArticles.append(article_data)

#######################################################################################AFR#####DONE
onse = requests.get("https://www.afr.com/markets", impersonate="chrome")

if onse.status_code != 200:
    raise SystemExit(f"blocked: {response.status_code}")

oup = BeautifulSoup(onse.text, "html.parser")

###declare dicts
seen = set()
frArticles = []
###
bars = oup.find_all("div", attrs={"data-testid": "StoryTileBase"})


for bar in bars:
    headline = bar.find(attrs={"data-testid": "StoryTileHeadline-h3"})

    if not headline:
        continue

    title_link = headline.find("a")

    if not title_link:
        continue

    href = title_link.get("href")



    if not isinstance(href, str):
        continue

    date_tag = bar.find("time")
    if not date_tag:
        continue

    date_string = date_tag.get("datetime")
    if not isinstance(date_string, str):
        continue

    key = (href, date_string)

    if key in seen:
        continue

    seen.add(key)

    summary_tag = bar.find("p", attrs={"data-pb-type": "ab"})

    ###convert to datetime for chrono
    clean_date = (date_string.replace(" – ", " ").replace(".", ":").upper())
    date_time = datetime.strptime(clean_date,"%b %d, %Y %I:%M%p")
    frURL = (f"https://www.afr.com{href}")

    frArticles.append({
        "URL": frURL,
        "Title": title_link.get_text(strip=True),
        "Summary": (summary_tag.get_text(strip=True) if summary_tag else None),
        "Date": date_string,
        "DateTime": date_time
    })
###############################################################all together #######################################
allArticles = (frArticles + miArticles + lwArticles)
allArticles.sort(key=lambda article: article["DateTime"],reverse=True)
############################################################################################################FRONT END############
ui.add_css('''
    .nicegui-link, .nicegui-link:link, .nicegui-link:visited {
        text-decoration: none !important;
        color: inherit !important;
    }
''')
###Header/title
ui.html('<h1 class="title">▼ Market Pulse ▲</h1><style>.title{text-align:center;font-size:4.2rem;font-family:Georgia, serif;font-weight:normal;letter-spacing:1px;background:linear-gradient(90deg,#dc2626,#84cc16);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}</style>')
ui.separator()
with ui.tabs().classes("w-full") as tabs:
    All = ui.tab("All")
    lwTab = ui.tab("LiveWire Markets")
    miTab = ui.tab("Market Index")
    afrTab = ui.tab("Aus Financial Review")
with ui.tab_panels(tabs,value=All).classes("w-full"):
    with ui.tab_panel(All):
        with ui.timeline(side='right', color='green'):
            for article in allArticles:
                with ui.card():
                    with ui.link(target=(article["URL"])):
                        ui.timeline_entry((article["Summary"]), title=article["Title"], subtitle=article["Date"]).style('font-size: 125%')

    with ui.tab_panel(lwTab):
        with ui.timeline(side='right', color='yellow'):
            for article in lwArticles:
                with ui.card():
                    with ui.link(target=(article["URL"])):
                        ui.timeline_entry((article["Summary"]), title=article["Title"], subtitle=article["Date"]).style('font-size: 125%')

    with ui.tab_panel(miTab):
        with ui.timeline(side='right', color='blue'):
            for article in miArticles:
                with ui.card():
                    with ui.link(target=(article["URL"])):
                        ui.timeline_entry((article["Summary"]), title=article["Title"], subtitle=article["Date"]).style('font-size: 125%')

    with ui.tab_panel(afrTab):
        with ui.timeline(side='right', color='black'):
            for article in frArticles:
                with ui.card():
                    with ui.link(target=(article["URL"])):
                        ui.timeline_entry((article["Summary"]), title=article["Title"], subtitle=article["Date"]).style('font-size: 125%')

ui.run()
