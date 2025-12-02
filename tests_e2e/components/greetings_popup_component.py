from playwright.sync_api import Locator, expect


class GreetingsPopupComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def greetings_popup_component(self) -> Locator:
        return self.element.locator("[data-test-id='greetings-popup']")

    @property
    def welcome_header(self) -> Locator:
        return self.element.locator('div.vc-dialog-header__title:has-text("Welcome")')

    @property
    def opus_logo(self) -> Locator:
        return self.element.locator('img[alt="Opus LOGO"]')

    @property
    def we_are_processing_text(self) -> Locator:
        return self.element.locator('h2.text-center.text-3xl.font-bold')

    @property
    def you_will_receive_an_email_text(self) -> Locator:
        return self.element.locator('span.px-8.text-sm')

    @property
    def in_the_mean_time_text(self) -> Locator:
        return self.element.locator('span.flex.text-base.font-bold')

    @property
    def first_point_mark(self) -> Locator:
        return self.element.locator('.mt-0\\.5 > .mt-1\\.5')

    @property
    def research_and_buy_text(self) -> Locator:
        return self.element.locator('div.text-sm:has-text("Research and buy from hundreds of suppliers")')

    @property
    def take_a_tour_button(self) -> Locator:
        return self.element.locator('button.vc-button.vc-button--size--xs.vc-button--color--primary.vc-button--solid--primary:has(a:has-text("Take a tour of OPUS"))')

    @property
    def start_exploring_button(self) -> Locator:
        return self.element.locator('button:has-text("Start exploring OPUS")')

    @property
    def second_point_mark(self) -> Locator:
        return self.element.locator('div.flex.size-5.items-center.justify-center.rounded-full.bg-primary.text-center.text-additional-50 span:has-text("2")')

    @property
    def explore_the_entire_omnia_text(self) -> Locator:
        return self.element.locator('span.text-sm:has-text("Explore the entire OMNIA Partners portfolio of contracts.")')

    @property
    def portfolio_link(self) -> Locator:
        return self.element.locator('a[href="https://www.omniapartners.com/solutions/contract-offerings"]')

    @property
    def close_button(self) -> Locator:
        return self.element.locator('button.vc-dialog-header__close')

    # Operations/Actions
    def get_welcome_header(self):
        expect(self.welcome_header).to_be_visible()
        expect(self.welcome_header).to_have_text('Welcome')

    def get_opus_logo(self):
        expect(self.opus_logo).to_be_visible()

    def get_we_are_processing_text(self):
        expect(self.we_are_processing_text).to_be_visible()
        expect(self.we_are_processing_text).to_have_text("We’re processing your registration")

    def get_you_will_receive_an_email_text(self):
        expect(self.you_will_receive_an_email_text).to_be_visible()
        expect(self.you_will_receive_an_email_text).to_have_text(
            "You'll receive an email once our team has confirmed your membership eligibility. In most instances this will be the same day, but it may take up to one business day."
        )

    def get_in_the_mean_time_text(self):
        expect(self.in_the_mean_time_text).to_be_visible()
        expect(self.in_the_mean_time_text).to_have_text(
            'In the meantime, you have access to explore the benefits of your OMNIA Partners membership:'
        )

    def get_first_point_mark(self):
        expect(self.first_point_mark).to_be_visible()
        expect(self.first_point_mark).to_have_text('1')

    def get_research_and_buy_text(self):
        expect(self.research_and_buy_text).to_be_visible()
        expect(self.research_and_buy_text).to_have_text(
            'Research and buy from hundreds of suppliers you know and trust using our ecommerce platform, OPUS. All in one place at zero cost to you.'
        )

    def get_take_a_tour_button(self):
        expect(self.take_a_tour_button).to_be_visible()
        expect(self.take_a_tour_button).to_have_text('Take a tour of OPUS')
        expect(self.take_a_tour_button).to_be_enabled()
        # Validate the anchor inside the button
        anchor = self.take_a_tour_button.locator('a')
        expect(anchor).to_have_attribute('href', 'https://info.omniapartners.com/opus-new-user-tour')

    def get_start_exploring_button(self):
        expect(self.start_exploring_button).to_be_visible()
        expect(self.start_exploring_button).to_have_text('Start exploring OPUS')

    def get_second_point_mark(self):
        expect(self.second_point_mark).to_be_visible()
        expect(self.second_point_mark).to_have_text('2')

    def get_explore_the_entire_omnia_text(self):
        expect(self.explore_the_entire_omnia_text).to_be_visible()
        expect(self.explore_the_entire_omnia_text).to_have_text(
            'Explore the entire OMNIA Partners portfolio of contracts.'
        )

    def get_portfolio_link(self):
        expect(self.portfolio_link).to_be_visible()
        expect(self.portfolio_link).to_have_attribute(
            'href', 'https://www.omniapartners.com/solutions/contract-offerings'
        )
        expect(self.portfolio_link).to_be_enabled()
        expect(self.portfolio_link).to_have_text('Open the contract portfolio in a new tab')

    def get_close_button(self):
        expect(self.close_button).to_be_visible()
        expect(self.close_button).to_be_enabled()
