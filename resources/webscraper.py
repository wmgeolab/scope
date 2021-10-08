from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import time

def get_only_text(p_array):
    output = ''
    for para in p_array:
        output += ' ' + para.get_text()

    return output

if __name__ == "__main__":

    # initializing selenium webdriver
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(10)

    # getting list of relevant sources
    file1 = open('relevant_sources.txt', 'r')
    Lines = file1.readlines()

    data = []   # fill with text from sources both relevant and not (string array)
    target = [] # fill with 1s and 0s if source is relevant or not (int array)

    t0 = time() # tracking progress variables
    count = 0   #

    for line in Lines:

        if (count != 0 and count % 10 == 0):
            print("done " + str(count) + " jobs in %0.3fs" % (time() - t0))

        count += 1

        url = line.strip()
        print(url)
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except KeyboardInterrupt:
            break
        except:
            print("AAAAAAAAAAAAAAAAA", url, " didn't work")
        else:
            data.append(get_only_text(soup.find_all("p")))
            target.append(1)

    print("Completed " + str(count) + " jobs in %0.3fs" % (time() - t0))
    #print(target)
