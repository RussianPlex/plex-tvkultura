# -*- coding: utf-8 -*-
from plex_test_case import PlexTestCase


class VGTRKServiceTest(PlexTestCase):

    def test_brand_list(self):
        actual = self.vgtrk_service.brands.BrandsListPage(self.load_html('BrandList.htm'), '//tvkultura.ru')
        self.assertEquals(u'Передачи текущего сезона', actual.title)
        brands = actual.list
        self.assertEquals(86, len(brands))
        self.assertEquals(u'Взаимоотношения власти и культуры, религии и государства', brands[39].about[0:56])
        self.assertEquals('//tvkultura.ru/brand/show/brand_id/20862/', brands[39].href)
        self.assertEquals(None, brands[0].schedule)
        self.assertEquals(u'Пн, Вт, Ср, Чт', brands[23].schedule)
        self.assertEquals(u'Чт', brands[39].schedule)
        self.assertEquals('https://cdn-st3.rtr-vesti.ru/vh/pictures/b/186/591.jpg', brands[39].big_thumb)
        self.assertEquals('https://cdn-st3.rtr-vesti.ru/vh/pictures/r/186/591.jpg', brands[39].small_thumb)
        self.assertEquals(u'Культурная революция', brands[39].title)

    def test_brand_menu(self):
        self.networking.http_response_body = self.load_html('BrandList.htm')
        actual = self.shared_code.brand_menu('https://tvkultura.ru/brand/')
        self.assertEquals('BrandsListPage', actual.__class__.__name__)

    def load_html(self, filename):
        html = self.get_file_contents(filename)
        return self.environment['HTML'].ElementFromString(html)

    @property
    def shared_code(self):
        return self.shared_code_environment['vgtrk']

    @property
    def vgtrk_service(self):
        return self.shared_code.vgtrk_service