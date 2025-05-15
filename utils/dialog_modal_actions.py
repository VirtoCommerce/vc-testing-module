from utils.commonLocators.dialog_modal_locators import DialogModalLocators
from playwright.sync_api import expect

class DialogModalActions:
    def __init__(self, page):
        self.page = page
        self.locators = DialogModalLocators
        self.dialog_modal_title = None



    def close_dialog_modal(self):
        self.page.click(self.locators.CLOSE_DIALOG_MODAL)   
   
    
    def check_dialog_modal_is_open(self):
        expect(self.page.locator(self.locators.DIALOG_MODAL)).to_be_visible()
    
    def check_dialog_modal_is_closed(self):
        expect(self.page.locator(self.locators.DIALOG_MODAL)).to_be_hidden()

    def click_create_button(self):
        self.page.click(self.locators.CREATE_BUTTON)   


    def get_dialog_modal_title(self):
        self.page.locator(self.locators.DIALOG_MODAL_TITLE).is_visible()
    
    def check_dialog_modal_title(self, title: str):
        """Check if the dialog modal title contains the expected title text"""
        title_text = self.page.locator(self.locators.DIALOG_MODAL_TITLE).text_content()
        return title in title_text

    def check_create_button(self):
        self.page.locator(self.locators.CREATE_BUTTON).is_visible()
        self.page.locator(self.locators.CREATE_BUTTON).is_enabled()    
        
    def get_dialog_modal_button_close(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CLOSE)
    
    def get_dialog_modal_button_confirm(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CONFIRM)
    
    def get_dialog_modal_button_cancel(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CANCEL)
    
    def click_dialog_modal_button_OK(self):
        self.page.locator(self.locators.DIALOG_MODAL_BUTTON_OK).is_visible()
        self.page.locator(self.locators.DIALOG_MODAL_BUTTON_OK).is_enabled()
        self.page.click(self.locators.DIALOG_MODAL_BUTTON_OK)
    
    def click_dialog_modal_button_cancel(self):
        self.page.locator(self.locators.DIALOG_MODAL_BUTTON_CANCEL).is_visible()
        self.page.locator(self.locators.DIALOG_MODAL_BUTTON_CANCEL).is_enabled()
        self.page.click(self.locators.DIALOG_MODAL_BUTTON_CANCEL)
    
    


