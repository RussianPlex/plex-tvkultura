PREFIX = "/video/tvkultura"
NAME = "TVKultura.Ru"
ICON = "tvkultura.png"
ART = "tvkultura.jpg"

BASE_URL = "https://tvkultura.ru/"
BRAND_URL = BASE_URL+"brand/"


# Channel initialization
def Start():
    ObjectContainer.title1 = NAME
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'


# Main menu
@handler(PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():
    oc = ObjectContainer(title1=NAME)
    brands = SharedCodeService.vgtrk.brand_menu(BRAND_URL)
    for brand in brands.list:
        oc.add(DirectoryObject(
            key=Callback(BrandMenu, url=brand.href),
            title=brand.title,
            summary=brand.about + ("\n\n[" + brand.schedule + "]" if brand.schedule else ''),
            thumb=Resource.ContentsOfURLWithFallback(url=brand.big_thumb, fallback=brand.small_thumb),
        ))
    return oc


@route(PREFIX+'/brand/')
def BrandMenu(url):
    pass
