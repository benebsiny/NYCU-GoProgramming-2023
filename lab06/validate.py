import os
import time
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class text_to_be_changed(object):
    def __init__(self, locator, original_text):
        self.locator = locator
        self.original_text = original_text

    def __call__(self, driver):
        element_text = driver.find_element(*self.locator).text
        return element_text != self.original_text


def main() -> int:
    PRIME = "It's prime"
    NOTPRIME = "It's not prime"

    test_cases = [
        ("1", NOTPRIME),
        ("2", PRIME),
        ("3", PRIME),
        ("977", PRIME),
        ("1021", PRIME),
        ("7139", NOTPRIME),
        ("28669", PRIME),
        ("34860283", PRIME),
        ("76351879", NOTPRIME),
        ("93416783", PRIME),
        ("672541787", PRIME),
        ("896871567", NOTPRIME),
        ("3472666597", PRIME),
        ("8632541253", NOTPRIME),
        ("9633251477", NOTPRIME),
        ("77265818857", PRIME),
        ("99999985837", PRIME),
        ("99999999997", NOTPRIME),
        ("172658105531", PRIME),
        ("267714526633", NOTPRIME),
        ("201423710699", PRIME),
        ("314159265359", PRIME),
        ("496635874121", NOTPRIME),
        ("588736214479", NOTPRIME),
        ("786632547711", NOTPRIME),
        ("538941033881", PRIME),
        ("6322571574869", NOTPRIME),
        ("23674586397841", PRIME),
        ("47763354178559", NOTPRIME),
        ("99887766554433", NOTPRIME),
        ("124475899632119", NOTPRIME),
        ("375593357415211", NOTPRIME),
        ("923174692024939", PRIME),
        ("1000000000000007", NOTPRIME),
        ("10000000000000061", PRIME),
        ("789663254110256361", NOTPRIME),
        ("1056325741526369751", NOTPRIME),
        ("1000000000000000003", PRIME),
        ("10000000000000000003", NOTPRIME),
        ("18446744073709551615", NOTPRIME),
    ]

    inp = ""

    if not os.path.exists("wasm_exec.js"):
        print("\033[1;31m[ERROR]\033[0m wasm_exec.js not found!")
        return 1
    if not os.path.exists("wasm/lib.wasm"):
        print("\033[1;31m[ERROR]\033[0m wasm/lib.wasm not found!")
        return 1

    try:
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 3)
        url = "http://localhost:8086"

        for _ in range(30):
            try:
                code = urllib.request.urlopen(url).getcode()
                if code == 200:
                    break
            except Exception as e:
                print(
                    "\033[1;36m[INFO]\033[0m Unable to connect to Go server, try again..."
                )
                time.sleep(2)
        else:
            print("\033[1;31m[ERROR]\033[0m Unable to connect to Go server!")
            return 1

        driver.get(url)
        print("\033[1;36m[INFO]\033[0m Start testing!")

        for tc in test_cases:
            input_field = driver.find_element(By.ID, "value")
            input_field.send_keys(tc[0])

            check_button = driver.find_element(By.ID, "check")
            check_button.click()

            inp = tc[0]

            wait.until(text_to_be_changed((By.ID, "answer"), ""))
            answer = driver.find_element(By.ID, "answer")
            if answer.text != tc[1]:
                print(
                    '\033[1;31m[ERROR]\033[0m Input: "%s", expected: "%s", got: "%s"'
                    % (tc[0], tc[1], answer.text)
                )
                return 1
            driver.refresh()
        return 0

    except TimeoutException as e:
        print('\033[1;31m[ERROR]\033[0m Time limit excceed!! Last input: "%s"' % inp)
        return 1

    except Exception as e:
        print("\033[1;31m[ERROR]\033[0m")
        print(e)
        return 1
    finally:
        driver.quit()


if __name__ == "__main__":
    status = main()
    if status == 0:
        print("\033[1;32mPASS\033[0m")
    exit(status)
