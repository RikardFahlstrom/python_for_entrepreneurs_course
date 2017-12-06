#  BaseController handles common layout, features, initialization

import webrepo.infrastructure.static_cache as static_cache
from webrepo.infrastructure.supressor import suppress
import pyramid.renderers


class BaseController:
    def __init__(self, request):
        self.request = request
        self.build_cache_id = static_cache.build_cache_id

        layout_render = pyramid.renderers.get_renderer('webrepo:templates/shared/_layout.pt')
        impl = layout_render.implementation()
        self.layout = impl.macros['layout']

    @property
    def is_logged_in(self):
        return True

    @suppress
    def dont_expose_as_web_action_base(self):
        print("Called dont_expose_as_web_action on base, what happened?")
