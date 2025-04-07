from utils.commonLocators.dialog_modal_locators import DialogModalLocators

class DialogModalActions:
    def __init__(self, page):
        self.page = page
        self.locators = DialogModalLocators

    def close_dialog_modal(self):
        self.page.click(self.locators.CLOSE_DIALOG_MODAL)   
   
    
    def check_dialog_modal_is_open(self):
        self.page.locator(self.locators.DIALOG_MODAL).is_visible()
    
    def check_dialog_modal_is_closed(self):
        self.page.locator(self.locators.DIALOG_MODAL).is_hidden()

    def click_create_button(self):
        self.page.click(self.locators.CREATE_BUTTON)   


    def get_dialog_modal_title(self):
        self.page.locator(self.locators.DIALOG_MODAL_TITLE).is_visible()
    
    def check_dialog_modal_title(self, title: str):
        self.page.locator(self.locators.DIALOG_MODAL_TITLE).text_content().contains(title)

    def get_dialog_modal_content(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_CONTENT)
    
    def get_dialog_modal_footer(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_FOOTER)

    def check_create_button(self):
        self.page.locator(self.locators.CREATE_BUTTON).is_visible()
        self.page.locator(self.locators.CREATE_BUTTON).is_enabled()    
        
    def get_dialog_modal_button_close(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CLOSE)
    
    def get_dialog_modal_button_confirm(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CONFIRM)
    
    def get_dialog_modal_button_cancel(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CANCEL)
    
    def get_dialog_modal_button_confirm(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CONFIRM)
    
    def get_dialog_modal_button_cancel(self):
        return self.page.text_content(self.locators.DIALOG_MODAL_BUTTON_CANCEL)
    
    


