# -*- coding: utf-8 -*-
from base import VGTRKTestcase


class VideoTest(VGTRKTestcase):

    def test_all_view_types(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('AllViewTypes.htm'), '//tvkultura.ru')
        view_types = actual.view_types
        self.assertEquals(1, len(view_types))  # Still only one view type is implemented
        self.assertEquals(['picture'], list(view_types))

    def test_single_view_types(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('SingleViewType.htm'), '//tvkultura.ru')
        view_types = actual.view_types
        self.assertEquals(1, len(view_types))
        self.assertEquals(['picture'], list(view_types))

    def test_invalid_view_type(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('SingleViewType.htm'), '//tvkultura.ru')
        self.assertRaises(ValueError, actual.view_type, 'bad')

    def test_picture_view_type(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('SingleViewType.htm'), 'https://tvkultura.ru')
        self.assertEquals(u'Щелкунчик. XVII Международный телевизионный конкурс юных музыкантов', actual.title)
        videos = actual.view_type('picture')
        self.assertEquals('ViewTypePictureContainer', videos.__class__.__name__)
        self.assertTrue(videos.is_available)
        self.assertEquals(None, videos.next_page)
        videos_list = videos.list
        self.assertEquals(27, len(videos_list))
        self.assertEquals(u'Торжественное закрытие. Прямая трансляция', videos_list[0].title)
        self.assertEquals(u'Приглашение к участию', videos_list[26].title)
        self.assertEquals(False, videos_list[26].has_children)
        self.assertEquals('https://cdn-st3.rtr-vesti.ru/vh/pictures/md/105/205/4.jpg', videos_list[26].thumb)
        self.assertEquals('https://tvkultura.ru/video/show/brand_id/60346/episode_id/1334953/video_id/1522871/viewtype/picture/', videos_list[26].href)
        self.assertEquals('https://tvkultura.ru/video/jsonvideo/episode_id/1334953/video_id/1552053/', videos_list[26].ajaxurl)

    def test_picture_view_type_has_children(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('HasChildren.htm'), 'https://tvkultura.ru')
        self.assertEquals(u'Шедевры старого кино', actual.title)
        videos = actual.view_type('picture')
        self.assertEquals('ViewTypePictureContainer', videos.__class__.__name__)
        videos_list = videos.list
        self.assertEquals(48, len(videos_list))
        self.assertEquals(u'Поручик Киже', videos_list[23].title)
        self.assertEquals(True, videos_list[23].has_children)

    def test_picture_view_type_pagination(self):
        actual = self.vgtrk_service.video.VideoListPage(self.load_html('AllViewTypes.htm'), 'http://tvkultura.ru')
        self.assertEquals('ACADEMIA', actual.title)
        videos = actual.view_type('picture')
        self.assertEquals('ViewTypePictureContainer', videos.__class__.__name__)
        self.assertEquals('NextPageElement', videos.next_page.__class__.__name__)
        self.assertEquals(u'Показать еще', videos.next_page.title)
        self.assertEquals('http://tvkultura.ru/video/jsonseries/brand_id/20898/episode_id/154405/sort_by/date/page/', videos.next_page.href)
        self.assertEquals(48, len(videos.list))

    def test_video_menu_full(self):
        self.networking.http_response_body = self.get_file_contents('AllViewTypes.htm')
        actual = self.shared_code.video_menu('https://tvkultura.ru/video/show/')
        self.assertEquals('VideoListPage', actual.__class__.__name__)

    def test_video_menu_json(self):
        self.networking.http_response_body = self.get_file_contents('PaginatedResponse.json')
        actual = self.shared_code.video_menu(
            'https://tvkultura.ru/video/jsonseries/',
            page=2,
            page_title=u'Культурная революция',
            next_title=u'Показать еще',
            referer='https://tvkultura.ru/video/show/'
        )
        self.assertEquals('VideoListPaginated', actual.__class__.__name__)
        self.assertEquals(u'Культурная революция', actual.title)
        videos = actual.view_type('picture')
        self.assertEquals('ViewTypePictureContainer', videos.__class__.__name__)
        self.assertEquals('NextPageElement', videos.next_page.__class__.__name__)
        self.assertEquals(u'Показать еще', videos.next_page.title)
        self.assertEquals('https://tvkultura.ru/video/jsonseries/', videos.next_page.href)
        self.assertEquals(48, len(videos.list))

    def test_video_menu_json_last_page(self):
        self.networking.http_response_body = self.get_file_contents('LastPageResponse.json')
        actual = self.shared_code.video_menu(
            'https://tvkultura.ru/video/jsonseries/',
            page=3,
            page_title=u'Культурная революция',
            next_title=u'Показать еще',
            referer='https://tvkultura.ru/video/show/'
        )
        videos = actual.view_type('picture')
        self.assertEquals(None, videos.next_page)

    def test_video_page(self):
        actual = self.vgtrk_service.video.VideoPage(self.load_html('SingleViewType.htm'), 'https://tvkultura.ru')
        self.assertEquals(u'Щелкунчик. XVII Международный телевизионный конкурс юных музыкантов', actual.title)
        self.assertEquals(u'Трансляция из Концертного зала', actual.full_text[0:30])
        self.assertEquals(u'Финал и торжественное закрытие', actual.short_text[0:30])
        self.assertEquals('https://player.vgtrk.com/iframe/video/id/1604511/start_zoom/true/showZoomBtn/false/sid/kultura/?acc_video_id=episode_id/1438111/video_id/1552053/brand_id/60346', actual.video_iframe_href)
        self.assertEquals('1604511', actual.video_id)
        self.assertEquals('https://player.vgtrk.com/iframe/datavideo/id/1604511/sid/vh', actual.datavideo_href)
