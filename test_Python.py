from playwright.sync_api import Page, sync_playwright
import pytest



# parametrizovaná fixture pro různé browsery
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def page(request) -> Page:
    browser_type_name = request.param

    with sync_playwright() as p:
        browser_type = getattr(p, browser_type_name)
        browser = browser_type.launch(headless=False, slow_mo=5000)
        context = browser.new_context()
        page = context.new_page()        
        
        yield page

        # Cleanup
        browser.close()



def test_link_vyukovy_portal(page: Page):
    # přejít na tu stránku https://engeto.cz/
    page.goto("https://engeto.cz/")

    # najít a kliknout na odkaz
    link = page.locator("#main-header > div > div > a")
    link.click()

    # ověřit, že url je https://portal.engeto.com/lobby/sign-in
    assert page.url == "https://portal.engeto.com/lobby/sign-in"


@pytest.mark.parametrize("locator, popis", [
    ("#top-menu > li.area-kurzy.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.children-items-type-row > ul > li:nth-child(3) > span", "Krátkodobé kurzy na 1–3 dny"),
    ("#top-menu > li.area-kurzy.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.children-items-type-row > ul > li:nth-child(1) > span", "Akademie na 1,5–3 měsíce"),
    ("#top-menu > li.area-kurzy.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.children-items-type-row > ul > li:nth-child(2) > span", "Balíčky kurzů na 3–6 měsíců")
],            
ids=["Test: Krátkodobé kurzy na 1–3 dny", "Test: Akademie na 1,5–3 měsíce", "Test: Balíčky kurzů na 3–6 měsíců"]
)
def test_hover_kurzy(locator, popis, page: Page):
    # přejít na tu stránku https://engeto.cz/
    page.goto("https://engeto.cz/")

    # najet myší na ten obrázek
    img = page.locator("#top-menu > li.area-kurzy.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.children-items-type-row")
    img.wait_for(state="visible")
    img.hover()

    # najít a počkat na text
    text = page.locator(locator)
    text.wait_for(state="visible")

    # kontrola, že vnitřní text je text v proměnné "popis"
    assert text.inner_text().replace("\xa0", " ").strip() == popis


def test_login_odebirat(page):
    # přejít na tu stránku https://engeto.cz/
    page.goto("https://engeto.cz/")
    
    # vyplnění mailové adresy
    mail = "test@gmail.com"
    mail_input = page.locator("body > footer > div > div.block-footer-newsletter.flex.flex-mobile-column.gap-8.gap-mobile-24 > div.newsletter-form.flex.flex-mobile-column.gap-8.gap-mobile-16 > label > input.has-text-md-regular-font-size")
    mail_input.fill(mail)

    # kliknutí na tlačítko "Odebírat"
    button = page.locator("body > footer > div > div.block-footer-newsletter.flex.flex-mobile-column.gap-8.gap-mobile-24 > div.newsletter-form.flex.flex-mobile-column.gap-8.gap-mobile-16 > a")
    button.click()

    # objeví se text s potvrzením
    confirmation = page.locator("body > footer > div > div.block-footer-newsletter.flex.flex-mobile-column.gap-8.gap-mobile-24 > div.newsletter-form.flex.flex-mobile-column.gap-8.gap-mobile-16 > span")
    assert confirmation.is_visible()




