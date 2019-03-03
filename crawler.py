import requests
from bs4 import BeautifulSoup
import csv
import threading


class myThread(threading.Thread):
    def __init__(self, thread_num, ticker_list_address):
        threading.Thread.__init__(self)
        self.thread_num = thread_num
        self.ticker_list_address = ticker_list_address

    def run(self):
        print("start:thread" + str(self.thread_num))
        multi_threads_crawl_and_save(self.thread_num, self.ticker_list_address)
        print("end:thread" + str(self.thread_num))


def multi_threads_crawl_and_save(thread_num, ticker_list_address):
    output = open('dividendData/dividend' + str(thread_num) + '.csv', 'w')
    f = open(ticker_list_address)
    try:
        reader = csv.reader(f)
        for row in reader:
            crawl_and_save(row[0], output)
            print(row[0])
    finally:
        f.close()
        output.close()


def crawl_and_save(symbol, out):
    count = 0
    url = 'http://www.nasdaq.com/symbol/%s/dividend-history' % symbol
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    if soup.find(id='quotes_content_left_dividendhistoryGrid') is not None:
        entries = soup.find(id='quotes_content_left_dividendhistoryGrid').find_all('tr')
        for entry in entries:
            for item in entry.find_all('td'):
                out.write(item.get_text().strip() + ',')
            if count != 0:
                out.write(',' + symbol)
                out.write('\n')
            count += 1


def main():
    thread_list = []
    for i in range(1, 3):
        thread = myThread(i, str(i) + '.csv')
        thread_list.append(thread)
    for i in range(1, 3):
        thread_list[i - 1].start()


if __name__ == '__main__':
    main()
