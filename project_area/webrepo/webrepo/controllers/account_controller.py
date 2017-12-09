import pyramid_handlers
from webrepo.controllers.base_controller import BaseController
from webrepo.viewmodels.register_viewmodel import RegisterViewModel


class AccountController(BaseController):
    @pyramid_handlers.action(renderer='templates/account/index.pt')
    def index(self):
        return {}

    @pyramid_handlers.action(renderer='templates/account/signin.pt')
    def signin(self):
        return {}

    # GET /account/register
    @pyramid_handlers.action(renderer='templates/account/register.pt', request_method='GET', name='register')
    def register_get(self):
        print('Calling register via GET...')
        vm = RegisterViewModel()
        return vm.to_dict()

    # POST /account/register
    @pyramid_handlers.action(renderer='templates/account/register.pt', request_method='POST', name='register')
    def register_post(self):
        vm = RegisterViewModel()
        vm.from_dict(self.request.POST)

        vm.validate()
        if vm.error:
            return vm.to_dict()

        # validate no account exists, password match
        # create account in DB
        # send welcome email

        # redirect
        print("Redirecting to account index page...")
        self.redirect('/account')

