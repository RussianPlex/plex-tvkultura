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
    brands = SharedCodeService.vgtrk.brand_menu(BRAND_URL)
    oc = ObjectContainer(title1=NAME)
    for brand in brands.list:
        oc.add(DirectoryObject(
            key=Callback(BrandMenu, url=brand.href),
            title=brand.title,
            summary=brand.about + ("\n\n[" + brand.schedule + "]" if brand.schedule else ''),
            thumb=Resource.ContentsOfURLWithFallback(url=brand.big_thumb, fallback=brand.small_thumb),
        ))
    return oc


@route(PREFIX+'/brand')
def BrandMenu(url):
    brand = SharedCodeService.vgtrk.brand_detail(url)
    if brand.video_href:
        return VideoViewTypePictureMenu(brand.video_href)


@route(PREFIX+'/video/viewtype-picture')
def VideoViewTypePictureMenu(url):
    page = SharedCodeService.vgtrk.video_menu(url)
    videos = page.view_type('picture')
    oc = ObjectContainer(title1=page.title)
    for video in videos.list:
        callback = Callback(MetadataObjectForURL, href=video.href, thumb=video.thumb, title=video.title)
        oc.add(EpisodeObject(
            key=callback,
            rating_key=video.href,
            title=video.title,
            thumb=video.thumb,
            items=MediaObjectsForURL(callback)
        ))
    return oc


def MetadataObjectForURL(href, title, thumb, **kwargs):
    # This is a sort-of replacement for the similar method from the URL Services, just different parameters list.
    video_clip_object = VideoClipObject(
        key=Callback(MetadataObjectForURL, url=href, title=title, thumb=thumb, **kwargs),
        rating_key=href,
        title=title,
        thumb=thumb,
        items=MediaObjectsForURL(
            Callback(RedirectToActualVideoUrl, href=href)
        ),
        **kwargs
    )
    return ObjectContainer(
        no_cache=True,
        objects=[video_clip_object]
    )


def MediaObjectsForURL(callback):
    # This is a sort-of replacement for the similar method from the URL Services, just different parameters list.
    return [
        MediaObject(
            container=Container.MP4,
            video_codec=VideoCodec.H264,
            audio_codec=AudioCodec.AAC,
            parts=[
                PartObject(key=callback)
            ]
        )
    ]


@indirect
def RedirectToActualVideoUrl(href):
    pass
