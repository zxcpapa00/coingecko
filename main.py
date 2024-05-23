import requests
from bs4 import BeautifulSoup
import csv


def write_exel(datas) -> None:
    with open("result.csv", "w", newline='', encoding='cp1251') as file:
        fieldnames = ["Ссылка", "ID", "Монета", "Цена", "Капитализация", "Торги 24", "Цена мин", "Дата мин цены",
                      "Цена макс", "Дата макс цены"]
        writer = csv.writer(file, delimiter=';', lineterminator='\n')

        writer.writerow(fieldnames)
        for row in datas:
            writer.writerow(list(row.values()))


def parse():
    url = "https://www.coingecko.com"

    req = requests.get(url)

    soup = BeautifulSoup(req.text, "lxml")
    all_coins = soup.find("tbody", class_="tw-divide-y").find_all("tr")
    result = []
    for coin in all_coins:
        coin_url = f'{url}{coin.find("a", class_="tw-flex")["href"]}'
        coin_req = requests.get(coin_url)
        coin_soup = BeautifulSoup(coin_req.text, "lxml")
        price = coin_soup.findAll(attrs={"data-converter-target": "price"})[0].text.strip()
        id_ = coin_soup.findAll(attrs={"data-converter-target": "price"})[0]["data-coin-id"]
        name = coin_soup.find("h1", class_="tw-flex").find("div").text.strip()
        panel_info = coin_soup.find("tbody", class_="tw-grid").findAll("tr", class_="tw-flex")
        capital = panel_info[0].find_all("span")[-1].text.strip()
        day_trading = panel_info[3].find_all("span")[-1].text.strip()

        panel_info_max_min = coin_soup.find_all("tbody", class_="tw-grid")[1].find_all("tr")
        min_price = panel_info_max_min[-1].find_all("span")[0].text.strip()
        min_price_date = panel_info_max_min[-1].find_all("div")[-1].text.strip()
        max_price = panel_info_max_min[-2].find_all("span")[0].text.strip()
        max_price_date = panel_info_max_min[-2].find_all("div")[-1].text.strip()

        data = {
            "coin_url": coin_url,
            "id": id_,
            "name": name,
            "price": price,
            "capital": capital,
            "day_trading": day_trading,
            "min_price": min_price,
            "min_price_date": min_price_date,
            "max_price": max_price,
            "max_price_date": max_price_date
        }
        result.append(data)

    write_exel(result)


if __name__ == "__main__":
    parse()
