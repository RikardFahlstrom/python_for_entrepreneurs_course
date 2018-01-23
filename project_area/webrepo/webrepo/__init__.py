from pyramid.config import Configurator
import os
import webrepo
import webrepo.controllers.home_controller as home
import webrepo.controllers.albums_controller as albums
import webrepo.controllers.account_controller as account
import webrepo.controllers.admin_controller as admin
import webrepo.controllers.newsletter_controller as news
from webrepo.data.dbsession import DbSessionFactory
from webrepo.email.template_parser import EmailTemplateParser
from webrepo.services.email_service import EmailService
from webrepo.services.mailinglist_service import MailingListService

dev_mode = False


def init_db(_):
    top_folder = os.path.dirname(webrepo.__file__)  # __file__ refers to current file, dirname gives path
    rel_folder = os.path.join('db', 'webrepo.sqlite')  # .join is a "smart" path creator

    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


def init_email_templates(_):
    EmailTemplateParser.global_init()


def main(_, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    init_mode(config)
    init_includes(config)
    init_email_templates(config)
    init_routing(config)
    init_db(config)
    init_mailing_list(config)
    init_smtp_mail(config)

    return config.make_wsgi_app()


def init_smtp_mail(config):
    global dev_mode
    unset = 'YOUR VALUE'

    settings = config.get_settings()
    smtp_username = settings.get('smtp_username')
    smtp_password = settings.get('smtp_password')
    smtp_server = settings.get('smtp_server')
    smtp_port = settings.get('smtp_port')

    if smtp_username == unset:
        print("WARNING: SMTP server values not set in config file. Outbound email will not work.")

    EmailService.global_init(smtp_username, smtp_password, smtp_server, smtp_port, dev_mode)


def init_mailing_list(config):
    unset = 'ADD_YOUR_API_KEY'

    settings = config.get_settings()
    mailchimp_api = settings.get('mailchimp_api')
    mailchimp_list_id = settings.get('mailchimp_list_id')

    if mailchimp_api == unset:
        print("WARNING: Mailchimp API values not set in config file. Mailing list subscriptions will not work.")

    MailingListService.global_init(mailchimp_api, mailchimp_list_id)


def init_mode(config):
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
    print("Running in {} mode.".format('dev' if dev_mode else 'prod'))


def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')
    add_controller_routes(config, albums.AlbumsController, 'albums')
    add_controller_routes(config, account.AccountController, 'account')
    add_controller_routes(config, admin.AdminController, 'admin')
    add_controller_routes(config, news.NewsLetterController, 'newsletter')

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
