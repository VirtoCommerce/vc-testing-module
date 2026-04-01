from page_objects.layouts.main import MainLayout


class HomePage(MainLayout):

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/"

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
