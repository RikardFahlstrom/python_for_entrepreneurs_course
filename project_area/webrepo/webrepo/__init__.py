from pyramid.config import Configurator
import os
import webrepo
import webrepo.controllers.home_controller as home
import webrepo.controllers.albums_controller as albums
import webrepo.controllers.account_controller as account
from webrepo.data.dbsession import DbSessionFactory


def init_db(config):
    top_folder = os.path.dirname(webrepo.__file__)  # __file__ refers to current file, dirname gives path
    rel_folder = os.path.join('db', 'webrepo.sqlite')  # .join is a "smart" path creator

    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    init_includes(config)
    init_routing(config)
    init_db(config)

    return config.make_wsgi_app()


def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')
    add_controller_routes(config, albums.AlbumsController, 'albums')
    add_controller_routes(config, account.AccountController, 'account')

    config.scan()

def add_controller_routes(config, ctrl, prefix):
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{id}', handler=ctrl)

def init_includes(config):
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')
