from pyramid.view import view_config
import webrepo.infrastructure.static_cache

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'My Web App'}


def extend_model(model_dict):
    model_dict['build_cache_id'] = webrepo.infrastructure.static_cache.build_cache_id()
    return model_dict
