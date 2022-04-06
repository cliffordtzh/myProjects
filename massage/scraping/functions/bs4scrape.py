from bs4 import BeautifulSoup
import requests

URL = "https://www.google.com/search?rlz=1C1CHBF_enSG861SG861&sxsrf=AOaemvK5e3A2oQQU0sfzRR2062ecehSySQ:1643213918874&q=massage+parlours+in+singapore&npsic=0&rflfq=1&rldoc=1&rllag=1327222,103843803,5287&tbm=lcl&sa=X&ved=2ahUKEwirkrLv6M_1AhULgtgFHd9GAecQtgN6BAgMEHQ"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
print(soup.find("div").text)