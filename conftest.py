import pytest


def pytest_addoption(parser):
    parser.addoption("--amurl", action="store")
    parser.addoption("--basic", action="store")
    parser.addoption("--cert", action="store")


@pytest.fixture(scope="session")
def acct_mgt_url(request):
    amurl_value = request.config.option.amurl
    if amurl_value is None:
        pytest.skip()
    return amurl_value


@pytest.fixture(scope="session")
def basic_auth(request):
    user_passwd = request.config.option.basic
    return user_passwd


@pytest.fixture(scope="session")
def cert(request):
    cert_value = request.config.option.cert
    return cert_value


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.amurl
    if "amurl" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("acct_mgt_url", [option_value])
    auth_str = metafunc.config.option.basic
    # metafunc.parametrize("basic_auth", [option_value])
    #   -- gets translated to:
    # metafunc.parametrize("cert", [option_value])
    #   --> get translated to the following:
    #   auth_ops = ["-E","./client_cert/acct-mgt-2.crt", "-key", "./client_cert/acct-mgt-2.key"]
    #   auth_ops = ["-cert", r"acct-mgt-2",]    metafunc.parametrize("auth_opts", [[]])
    if auth_str is not None:
        metafunc.parametrize("auth_opts", [["-u", auth_str]])
    else:
        metafunc.parametrize("auth_opts", [[]])
