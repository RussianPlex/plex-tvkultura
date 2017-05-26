# -*- coding: utf-8 -*-
from plex_test_case import PlexTestCase


class VGTRKTestcase(PlexTestCase):

    def load_html(self, filename):
        html = self.get_file_contents(filename)
        return self.environment['HTML'].ElementFromString(html)

    @property
    def shared_code(self):
        return self.shared_code_environment['vgtrk']

    @property
    def vgtrk_service(self):
        return self.shared_code.vgtrk_service
