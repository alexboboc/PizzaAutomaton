from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time, datetime, sys, re, os, json

DELIVERY_ADDRESS = os.environ["DELIVERY_ADDRESS"].strip()
DELIVERY_FLOOR = os.environ["DELIVERY_FLOOR"].strip()
DELIVERY_DOOR = os.environ["DELIVERY_DOOR"].strip()
WAITING_TIME = 2

with open("paths.json") as paths_file:
    PATHS = json.load(paths_file)

with open("pizzas.json") as pizzas_file:
    PIZZAS = json.load(pizzas_file)

# --------------------------------------------------
#   Initialize ChromeDriver
# --------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
driver.maximize_window()

# --------------------------------------------------
#   Load initial page
# --------------------------------------------------
driver.get("https://maipizza.es/#/delivery")
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   App download is offered; cancel
# --------------------------------------------------
continue_button = driver.find_element_by_css_selector(PATHS["location_screen"]["application_modal"])
continue_button.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   If browser tries to get location, cancel
# --------------------------------------------------
try:
    location_alert = driver.switch_to.alert
    location_alert.dismiss()
except:
    pass

# --------------------------------------------------
#   If browser displays location error, dismiss
# --------------------------------------------------
try:
    close_altert_button = driver.find_element_by_class_name(PATHS["location_screen"]["location_error_modal"])
    close_altert_button.click()
    time.sleep(WAITING_TIME)
except:
    pass

# --------------------------------------------------
#   Input address
# --------------------------------------------------
address_field = driver.find_element_by_css_selector(PATHS["location_screen"]["address_field"])
address_field.clear()
address_field.send_keys(DELIVERY_ADDRESS)
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Accept suggested location
# --------------------------------------------------
location_suggestion_dropdown = driver.find_element_by_css_selector(PATHS["location_screen"]["location_suggestion"])
location_suggestion_dropdown.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Submit location
# --------------------------------------------------
check_address_button = driver.find_element_by_css_selector(PATHS["location_screen"]["check_address_button"])
check_address_button.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Input floor level and door number
# --------------------------------------------------
level_field = driver.find_element_by_css_selector(PATHS["location_screen"]["level_field"])
level_field.send_keys(DELIVERY_FLOOR)
door_field = driver.find_element_by_css_selector(PATHS["location_screen"]["door_field"])
door_field.send_keys(DELIVERY_DOOR)

# --------------------------------------------------
#   Start order
# --------------------------------------------------
start_order_button = driver.find_element_by_css_selector(PATHS["location_screen"]["submit_address_button"])
start_order_button.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Accept cookies (message occludes buttons)
# --------------------------------------------------
cookie_accept_button = driver.find_element_by_css_selector(PATHS["menu_screen"]["cookie_accept_button"])
cookie_accept_button.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   On Mon-Thu, there's 3x1 deal on mediums, on
#   other days it's 2x1 on familiars
# --------------------------------------------------
weekday = datetime.datetime.today().weekday()
familiars = False
if weekday in range(4):
    pizzas_idxs = [PIZZAS["bbq_inferno"], PIZZAS["fondue"], PIZZAS["chicken_grill"]]
else:
    pizzas_idxs = [PIZZAS["bbq_inferno"], PIZZAS["chicken_grill"]]
    familiars = True

# --------------------------------------------------
#   Add pizzas to the cart
# --------------------------------------------------
for pizza_idx in pizzas_idxs:
    # Find add button, scroll to it and click it
    pizza_selector = PATHS["menu_screen"]["pizza_card"].format(pizza_idx)
    pizza_add_button = driver.find_element_by_css_selector(pizza_selector)
    time.sleep(WAITING_TIME)
    ActionChains(driver).move_to_element(pizza_add_button).perform()
    time.sleep(WAITING_TIME)
    pizza_add_button.click()
    time.sleep(WAITING_TIME)
    
    # Familiar is default size; change to medium if desired
    if not familiars:
        select_medium_radio = driver.find_element_by_css_selector(PATHS["pizza_screen"]["select_medium_radio"])
        select_medium_radio.click()
    
    # Submit addition to cart
    add_button = driver.find_element_by_css_selector(PATHS["pizza_screen"]["submit_addition"])
    add_button.click()
    time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Go to cart
# --------------------------------------------------
cart_icon_button = driver.find_element_by_css_selector(PATHS["menu_screen"]["go_to_cart_button"])
cart_icon_button.click()
time.sleep(WAITING_TIME)

# --------------------------------------------------
#   Display order info, and ask for confirmation
# --------------------------------------------------
final_price = driver.find_elements_by_css_selector(PATHS["cart_screen"]["price_text"])[1]
delivery_hour = driver.find_element_by_css_selector(PATHS["cart_screen"]["delivery_hour_text"])
delivery_hour_text = re.search("\[(.*?)\]", delivery_hour.text).group(0).replace("[", "").replace("]", "")

print("Pizzas: {}".format(len(pizzas_idxs)))
print("Price: {}".format(final_price.text))
print("Delivery hour: {}".format(delivery_hour_text))

# Check for "detached mode"
if "-y" not in sys.argv:
    confirmation = input("Confirm (y/n): ")
    if confirmation != "y":
        print("Canceled.")

# --------------------------------------------------
#   Issue order
# --------------------------------------------------
complete_order_button = driver.find_element_by_css_selector(PATHS["cart_screen"]["submit_order_button"])
ActionChains(driver).move_to_element(complete_order_button).perform()
complete_order_button.click()

time.sleep(WAITING_TIME * 10)
driver.quit()