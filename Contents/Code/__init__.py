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
def VideoViewTypePictureMenu(url, page=1, referer=None, page_title=None, next_title=None):
    videos = SharedCodeService.vgtrk.video_menu(url, page=page, referer=referer, page_title=page_title, next_title=next_title)
    video_items = videos.view_type('picture')
    oc = ObjectContainer(title1=videos.title)
    for video in video_items.list:
        callback = Callback(MetadataObjectForURL, href=video.href, thumb=video.thumb, title=video.title)
        oc.add(EpisodeObject(
            key=callback,
            rating_key=video.href,
            title=video.title,
            thumb=video.thumb,
            items=MediaObjectsForURL(callback),
        ))
    next_page = video_items.next_page
    if next_page is not None:
        oc.add(NextPageObject(
            key=Callback(
                VideoViewTypePictureMenu,
                url=next_page.href,
                page=int(page) + 1,
                referer=url if referer is None else referer,
                page_title=videos.title,
                next_title=next_page.title
            ),
            title=next_page.title,
        ))
    return oc


def MetadataObjectForURL(href, thumb, title, **kwargs):
    # This is a sort-of replacement for the similar method from the URL Services, just different parameters list.
    page = SharedCodeService.vgtrk.video_page(href)
    video_clip_object = VideoClipObject(
        key=Callback(MetadataObjectForURL, href=href, thumb=thumb, title=title, **kwargs),
        rating_key=href,
        title=title,
        thumb=thumb,
        summary=page.full_text,
        items=MediaObjectsForURL(
            Callback(PlayVideo, href=href)
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
def PlayVideo(href):
    page = SharedCodeService.vgtrk.video_page(href)
    json = JSON.ObjectFromURL(page.datavideo_href, headers={'Referer': page.video_iframe_href})
    medialist = json['data']['playlist']['medialist']
    if len(medialist) > 1:
        raise RuntimeWarning('More than one media found, each should have been set as a PartObject!')
    quality = str(json['data']['playlist']['priority_quality'])
    transport = 'http'
    if 'sources' not in medialist[0] and medialist[0]['errors']:
        raise Ex.PlexNonCriticalError(2005, medialist[0]['errors'])
    video_url = medialist[0]['sources'][transport][quality]
    Log('Redirecting to video URL: %s' % video_url)
    return IndirectResponse(
        VideoClipObject,
        key=video_url,
        http_headers={'Referer': page.video_iframe_href},
        metadata_kwargs={'summary': page.full_text}
    )
