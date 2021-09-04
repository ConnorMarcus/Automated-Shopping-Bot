from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from requests_html import HTMLSession, AsyncHTMLSession
import time
import AdidasPaths
import sys


class AdidasCA_ShoeBot():
    """
    Designed for Adidas CA website for shoes
    """
    
    def __init__(self, product_page:str) -> None:
        """
        Initialize class with the product page of the shoe you want to buy
        """
        self._wd = webdriver.Chrome(executable_path="./chromedriver")
        self._wd.maximize_window()
        self._wd.get(product_page)
        time.sleep(5) #Wait For Page to Load
        self._wd.find_element_by_css_selector(AdidasPaths.accept_cookies).click() #Must Accept Cookies on Adidas CA
        
    def addToCart(self, size:int) -> None:        
        #Adidas CA has two different types of size buttons depending on the shoe
        try:
            buttons = self._wd.find_element_by_css_selector(AdidasPaths.size_selector)
            size_button = buttons.find_element_by_xpath(f'//*[@data-di-id="size_M{size}/W{size+1}"]')
        except NoSuchElementException:
            buttons = self._wd.find_element_by_css_selector(AdidasPaths.size_selector2)
            size_button = buttons.find_element_by_xpath(f'//*[@data-di-id="size_{size}"]')
        except:
            print("Page Timeout!")
            sys.exit()
        
        try:
            size_button.click()
            self._wd.find_element_by_css_selector(AdidasPaths.add_to_bag).click()        
            
        except:
            print("Size out of stock or unavailable!")
            sys.exit()
        
        try:
            checkout_button = WebDriverWait(self._wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, AdidasPaths.checkout)))
            checkout_button.click()
        except:
            print("Error While Adding Item to Bag!")
            sys.exit()            
            
    def checkout(self, info:list) -> None:
        """
        The info list should be in the form [FirstName, LastName, Address, City, 
        Province, PostalCode, Email, PhoneNumber]
        """        
        try:
            firstname_input = WebDriverWait(self._wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, AdidasPaths.first_name)))
            firstname_input.send_keys(info[0])            
        except:
            print("Page Timeout on Checkout Page!")
            sys.exit()             
            
        self._wd.find_element_by_css_selector(AdidasPaths.last_name).send_keys(info[1])
        self._wd.find_element_by_css_selector(AdidasPaths.address).send_keys(info[2])
        self._wd.find_element_by_css_selector(AdidasPaths.city).send_keys(info[3])
        
        self._wd.find_element_by_css_selector(AdidasPaths.province_button).click()
        try:
            provinces = WebDriverWait(self._wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, AdidasPaths.province_options)))
            provinces.find_elements_by_xpath(f"//*[text()='{info[4].capitalize()}']")[0].click()
        except:
            print("Invalid Province or Province Could not be Selected!")
            sys.exit()            
            
        self._wd.find_element_by_css_selector(AdidasPaths.postal_code).send_keys(info[5])
        self._wd.find_element_by_css_selector(AdidasPaths.email).send_keys(info[6])
        self._wd.find_element_by_css_selector(AdidasPaths.phone).send_keys(info[7])
        self._wd.find_element_by_css_selector(AdidasPaths.checkbox).click()
        self._wd.find_element_by_css_selector(AdidasPaths.checkbox2).click()
        self._wd.find_element_by_css_selector(AdidasPaths.pay_button).click()
                    
    def makePayment(self, paymentDetails:list) -> None:
        """
        Currently the payment inputs seem to be dynamically loaded in by a script
        so the HTML is not able to be accessed by the WebDriver.
        """
        pass



def main() -> None:
    #Testing
    url = 'https://www.adidas.ca/en/stan-smith-shoes/FX5501.html'
    url2 = 'https://www.adidas.ca/en/ultraboost-5.0-dna-slip-ons/GZ3155.html'
    url3 = 'https://www.adidas.ca/en/ultraboost-5.0-dna-primeblue-shoes/GX2562.html' #kids sizes
    url4 = 'https://www.adidas.ca/en/nmd_r1-shoes/GZ7945.html'
    
    bot = AdidasCA_ShoeBot(url)
    bot.addToCart(10)
    bot.checkout(["Connor", "Marcus", "4313 Totem Drive", "Ottawa", "Ontario", "K1V1L6", "connormarcus@bell.net", "6132619494"]) 
    #bot.makePayment([])

    
if __name__ == "__main__":
    main()
    