import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

SELENIUM_GRID = "http://localhost:4444/wd/hub"


class Browsers:
    CHROME: str = "chrome"
    EDGE: str = "edge"
    FIREFOX: str = "firefox"


def pytest_addoption(parser):
    parser.addoption(
        "--select-browser",
        action="store",
        default=Browsers.CHROME,
        help="Choose which browser to run tests, defaults to 'chrome'",
        choices=(Browsers.CHROME, Browsers.EDGE, Browsers.FIREFOX),
    )


def select_driver(browser):
    match browser:
        case Browsers.CHROME:
            return webdriver.Remote(command_executor=SELENIUM_GRID, options=ChromeOptions())
        case Browsers.EDGE:
            return webdriver.Remote(command_executor=SELENIUM_GRID, options=EdgeOptions())
        case Browsers.FIREFOX:
            return webdriver.Remote(command_executor=SELENIUM_GRID, options=FirefoxOptions())
        case _:
            return webdriver.Remote(command_executor=SELENIUM_GRID, options=ChromeOptions())


@pytest.fixture(scope="function")
def driver(request):
    """Create a webdriver instance per test function, so it doesn't use the same browser session
    for more than one test.
    """

    browser = request.config.getoption("--select-browser")
    custom_driver = select_driver(browser)

    custom_driver.maximize_window()
    custom_driver.set_script_timeout(30)
    custom_driver.set_page_load_timeout(30)
    custom_driver.implicitly_wait(0)

    yield custom_driver

    custom_driver.quit()
