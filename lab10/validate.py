import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request


def get_msg(text: str):
    pattern = r'表示: (.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def main():
    try:
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=service, options=options)
        url = "http://localhost:8090"

        for _ in range(30):
            try:
                code = urllib.request.urlopen(url).getcode()
                if code < 400:
                    break
            except Exception as e:
                print(
                    "\033[1;36m[INFO]\033[0m Unable to connect to Go server, try again...")
                sleep(2)
        else:
            print("\033[1;31m[ERROR]\033[0m Unable to connect to Go server!")
            return 1

        test_cases = [
            ("你好", "你好"),
            ("我是賴清德", "我是賴*德"),
            ("哈哈騙你的啦", "哈哈騙你的啦"),
            ("其實我是陳菊", "其實我是陳*"),
            ("好啦，朱立倫才是我的真實身份", "好啦，朱*倫才是我的真實身份"),
            ("沒啦", "沒啦"),
            ("其實我都在唬爛", "沒啦"),
            ("呵呵", "呵呵"),
            ("我是白痴", "呵呵"),
        ]

        driver.get(url)
        for tc in test_cases:
            driver.find_element(By.ID, "chat_input").send_keys(tc[0])
            driver.find_element(By.ID, "chat_input").send_keys(Keys.ENTER)
            sleep(0.5)

            chatbox = driver.find_element(By.ID, "chatbox")
            last_full_msg = chatbox.find_elements(By.TAG_NAME, "b")[-1].text
            msg = get_msg(last_full_msg)
            if msg != tc[1]:
                print("\033[1;31m[ERROR]\033[0m", end=" ")
                print("Expected: %s, got: %s" % (tc[1], msg))
                return 1
        return 0
    except Exception as e:
        print("\033[1;31m[ERROR]\033[0m")
        print(e)
        return 1
    finally:
        driver.quit()


if __name__ == "__main__":
    status = main()
    if status == 0:
        print("\033[1;32m[PASS]\033[0m")
    exit(status)
