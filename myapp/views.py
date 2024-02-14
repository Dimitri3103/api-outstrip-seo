from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import urllib.error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from Screenshot import Screenshot
import pathlib
from webdriver_manager.chrome import ChromeDriverManager

# Create your views here.


def data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def title(soup):
    message = "No Title Found"
    text = soup.find("title").getText()
    if len(text) is not None:
        message = text
    else:
        message
    return message


def title_lenth(soup):
    title_text = soup.find("title").getText()
    title_length = len(title_text)
    return title_length


def meta_description(soup):
    message = "No Meta Description Found"

    content1 = soup.find("meta", {"name": "description"})
    content2 = soup.find("meta", {"property": "og:description"})
    if content2 is not None:
        message = content2.get("content")
    elif content1 is not None:
        message = content1.get("content")
    else:
        message
    return message


def meta_description_length(soup):
    length = 0
    content1 = soup.find("meta", {"name": "description"})
    content2 = soup.find("meta", {"property": "og:description"})
    if content2 is not None:
        length = len(content2.get("content"))
    elif content1 is not None:
        length = len(content1.get("content"))
    else:
        length = 0
    return length


def h1(soup):
    h1 = []
    head1 = soup.find_all("h1")
    for i in head1:
        h1.append(i.getText())
    return h1


def h2(soup):
    h2 = []
    head2 = soup.find_all("h2")
    for j in head2:
        h2.append(j.getText())
    return h2


def site(url):
    sitemaps_list = []
    page = f"{url}/sitemap.xml"
    site = requests.get(page)
    sitemap_index = BeautifulSoup(site.content, "html.parser")
    map = sitemap_index.find_all("loc")
    for i in map:
        sitemaps_list.append(i.getText())
    return sitemaps_list


def robottxt_check(url):
    site_robot_url = f"{url}/robots.txt"
    try:
        response = requests.get(site_robot_url)
        result = response.text
    except:
        pass
    return result


def error_check(url):
    try:
        urllib.request.urlopen(url)
        motif = "No Error"
    except urllib.error.URLError as e:
        motif = f"{e.code}: {e.reason}"
    return motif


def check_ssl(url):
    try:
        requests.get(url, verify=True)
        message = "VALID SSL certificate!"
    except requests.exceptions.SSLError:
        message = "INVALID SSL certificate!"
    return message


def alt_check(soup):
    notFound = []
    alt = soup.find_all("img", alt=True)
    for img in alt:
        if len(img["alt"]) == 0:
            notFound.append(img.get("src"))
        else:
            pass
    return notFound


def css_not_minify_check(soup):
    mini = []
    notMini = []
    link = soup.find_all("link", {"rel": "stylesheet"})
    # style = soup.find_all('style', {'type': 'text/css'})
    # checking CSS minification
    for i in link:
        link = i["href"]
        if "min" in i["href"].split("."):
            mini.append(link)
        elif "/*" in i.text:
            notMini.append(link)
        else:
            notMini.append(link)
    return notMini


def css_minify_check(soup):
    mini = []
    notMini = []
    link = soup.find_all("link", {"rel": "stylesheet"})
    # style = soup.find_all('style', {'type': 'text/css'})
    # checking CSS minification
    for i in link:
        link = i["href"]
        if "min" in i["href"].split("."):
            mini.append(link)
        elif "/*" in i.text:
            notMini.append(link)
        else:
            notMini.append(link)
    return mini


def JS_minify_check(soup):
    mini = []
    notMini = []
    script = soup.find_all("script")
    for i in script:
        l = str(i.get("src"))
        if "min" not in l.split("."):
            notMini.append(l)
        elif "\n" in i.getText():
            notMini.append(l)
        else:
            mini.append(l)
    return mini


def JS_not_minify_check(soup):
    mini = []
    notMini = []
    script = soup.find_all("script")
    for i in script:
        l = str(i.get("src"))
        if "min" not in l.split("."):
            notMini.append(l)
        elif "\n" in i.getText():
            notMini.append(l)
        else:
            mini.append(l)
    return notMini


def url_canonicaction_check(url):
    i = str(url.split())
    if "_" in i:
        message = "YES"
    else:
        message = "NO"
    return message


def old_tag_check(soup):
    old_tags = ["applet", "font", "center", "s", "strike", "u"]
    for i in old_tags:
        tags = soup.find_all(i)
        if i in tags:
            message = {i}
        else:
            message = "no issues"
    return message


def get_favicon(soup, url):
    """Scrape favicon."""
    if soup.find("link", attrs={"rel": "icon"}):
        favicon = soup.find("link", attrs={"rel": "icon"}).get("href")
    elif soup.find("link", attrs={"rel": "shortcut icon"}):
        favicon = soup.find("link", attrs={"rel": "shortcut icon"}).get("href")
    elif soup.find("meta", attrs={"itemprop": "image"}):
        favicon = soup.find("meta", attrs={"itemprop": "image"}).get("content")
    else:
        favicon = ""
    return favicon


def google_analytics_check(soup):
    script_list = []
    message = ""
    scrips = soup.find_all("script")
    for i in scrips:
        script_list.append(str(i.get("src")))
    for i in script_list:
        if i.startswith("https://www.googletagmanager"):
            message = i
            break
    else:
        message = "Not connected to Google Analytics"
    return message


def page_load_time(url):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # driver = webdriver.Chrome()

    driver.get(url)
    # navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script(
        "return window.performance.timing.responseStart"
    )
    domComplete = driver.execute_script("return window.performance.timing.domComplete")

    # backendPerformance_calc = responseStart - navigationStart
    load_time = round((domComplete - responseStart) / 1000, 2)
    driver.quit()
    return load_time


def screenshot(url):

    ob = Screenshot.Screenshot()
    # driver = webdriver.Chrome()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(url)
    img_url = ob.full_screenshot(
        driver,
        save_path="./media",
        image_name="screenshot.png",
        is_load_at_runtime=True,
        load_wait_time=3,
    )
    print(img_url)
    driver.close()
    driver.quit()

    return img_url


def cdn_delivered(soup):
    found = []
    notFound = []
    images = soup.find_all("img")
    link = soup.find_all("link", {"rel": "stylesheet"})
    script = soup.find_all("script")
    for img in images:
        I = str(img.get("src"))
        if I.startswith("https://cdn"):
            found.append(I)
        else:
            notFound.append(I)
    for i in link:
        J = i["href"]
        if J.startswith("https://cdn"):
            found.append(J)
        else:
            notFound.append(J)
    for i in script:
        l = str(i.get("src"))
        if l.startswith("https://cdn"):
            found.append(i.get("src"))
        else:
            notFound.append(i.get("src"))
    return found


def cdn_not_delivered(soup):
    found = []
    notFound = []
    images = soup.find_all("img")
    link = soup.find_all("link", {"rel": "stylesheet"})
    script = soup.find_all("script")
    for img in images:
        I = str(img.get("src"))
        if I.startswith("https://cdn"):
            found.append(I)
        else:
            notFound.append(I)
    for i in link:
        J = i["href"]
        if J.startswith("https://cdn"):
            found.append(J)
        else:
            notFound.append(J)
    for i in script:
        l = str(i.get("src"))
        if l.startswith("https://cdn"):
            found.append(i.get("src"))
        else:
            notFound.append(i.get("src"))
    return notFound


def responsive_image(soup):
    src = []
    images = soup.find_all("img")
    for img in images:
        i = str(img)
        try:
            if "srcset" in i:
                src.append(img.get("src"))
            elif "sizes=" in i:
                src.append(img.get("src"))
        except:
            pass
    return src


def non_responsive_image(soup):
    notFound = []
    images = soup.find_all("img")
    for img in images:
        i = str(img)
        try:
            if "srcset" not in i:
                notFound.append(img.get("src"))
            elif 'srcset=""' in i:
                notFound.append(img.get("src"))
        except:
            pass
    return notFound


def score(soup, url):
    counter = 100
    title_content = title(soup)
    if title_content == "No Title Found":
        counter -= 5
    else:
        pass
    title_lenth_content = title_lenth(soup)
    if 0 < title_lenth_content <= 60:
        pass
    else:
        counter -= 5
    mt_des_content = meta_description(soup)
    if mt_des_content == "No Meta Description Found":
        counter -= 5
    else:
        pass
    mt_length_content = meta_description_length(soup)
    if 0 < mt_length_content <= 160:
        pass
    else:
        counter -= 5
    H1 = h1(soup)
    if len(H1) == 0:
        counter -= 5
    else:
        pass
    H2 = h2(soup)
    if len(H2) == 0:
        counter -= 5
    else:
        pass
    sitemap = site(url)
    if len(sitemap) == 0:
        counter -= 5
    else:
        pass
    robot = robottxt_check(url)
    if len(robot) == 0:
        counter -= 5
    else:
        pass
    error = error_check(url)
    if error != "No Error":
        counter -= 5
    else:
        pass
    ssl = check_ssl(url)
    if ssl == "INVALID SSL certificate!":
        counter -= 5
    else:
        pass
    alt = alt_check(soup)
    if len(alt) != 0:
        counter -= 5
    else:
        pass
    css_minify = css_not_minify_check(soup)
    if len(css_minify) != 0:
        counter -= 5
    else:
        pass
    JS_minify = JS_not_minify_check(soup)
    if len(JS_minify) != 0:
        counter -= 5
    else:
        pass
    url_canonicaction = url_canonicaction_check(url)
    if url_canonicaction != "NO":
        counter -= 5
    else:
        pass
    old_tag = old_tag_check(soup)
    if old_tag != "no issues":
        counter -= 5
    else:
        pass
    favicon = get_favicon(soup, url)
    if len(favicon) == 0:
        counter -= 5
    else:
        pass
    google_analytics = google_analytics_check(soup)
    if google_analytics != "Not connected to Google Analytics":
        counter -= 5
    else:
        pass
    load_time = page_load_time(url)
    if load_time > 7:
        counter -= 5
    else:
        pass
    cdn = cdn_not_delivered(soup)
    if len(cdn) != 0:
        counter -= 5
    else:
        pass
    responsive_image_check = non_responsive_image(soup)
    if len(responsive_image_check) != 0:
        counter -= 5
    else:
        pass
    return counter


def index(request):
    return render(request, "index.html")


def is_seo_friendly(url):

    # Remove protocol and www prefix from the URL
    url = re.sub(r"^https?://(www\.)?", "", url)

    # Match against common SEO-friendly URL patterns
    patterns = [
        r"^[a-z0-9-]+$",  # Only lowercase letters, numbers, and hyphens
        r"^[a-z0-9-]+-[a-z0-9-]+$",  # Two or more words separated by hyphens
        r"^[a-z0-9-]+/[a-z0-9-]+$",  # Two or more words separated by a slash
    ]

    for pattern in patterns:
        if re.match(pattern, url):
            return True
        else:
            return False


def check_social_networks(url):
    # Fetch the HTML content of the web page
    response = requests.get(url)
    html_content = response.text

    # Define a list of popular social networks
    social_networks = ["facebook", "twitter", "instagram", "linkedin"]

    # Check if the web page is connected to any of the social networks
    connected_networks = []
    for network in social_networks:
        # Search for the social media URLs in the HTML content
        pattern = r"(?:https?:\/\/)?(?:www\.)?{0}\.com".format(network)
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            connected_networks.append(network)

    return connected_networks


# # Example usage
# url1 = 'https://www.example.com/seo-friendly-url'
# url2 = 'https://www.example.com/seo_friendly_url'
# url3 = 'https://www.example.com/not-seo-friendly-url'

# print(is_seo_friendly(url1))  # Output: True
# print(is_seo_friendly(url2))  # Output: True
# print(is_seo_friendly(url3))  # Output: False
