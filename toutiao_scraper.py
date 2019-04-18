#Describtion A mini scraper to scrape toutiao.com
#Author: Junhan Wang
#Date: April 17th, 2019
import time
from splinter import Browser
import csv

def scroll_down(browser):  #scroll web page down to current bottom
    return browser.execute_script('window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage;')
    
def scroll_to_end(browser): #scroll web page down to the end
    lenOfPage = scroll_down(browser)
    flag = False
    while(flag == False):
        print("scrolling page down")
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = scroll_down(browser)
        if lastCount == lenOfPage:
            print("scrolled page down to end")
            flag = True

def get_full_page(browser, url): #get full page for dynamic loading
    # Visit URL
    browser.visit(url)
    # find "微头条" element and click it
    tou_tiao_el = browser.find_by_xpath('//div[@id="wrapper"]/div[2]/div/ul/li[3]')
    time.sleep(1)
    tou_tiao_el.first.click()
    if browser.is_text_present('暂无内容'):
        print("fail to load page")
    else:
        print("page load success")
        scroll_to_end(browser)

def extract_num(message):   #extract number from a string
    return list(filter(str.isdigit, message))

def main():
    browser  = Browser('chrome', headless= True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    url = 'https://www.toutiao.com/c/user/5551493118/#mid=5551493118'
    get_full_page(browser,url)
    name = browser.find_by_css('span[class="name"]')[0].text       #get author anme
    contents = browser.find_by_css('div[class="ugc-content"]')     #get contents of each blog
    time_stamps = browser.find_by_css('span[class="lbtn"]')        #get time stamps of each 
    results = browser.find_by_css('div[class="y-left"] a')         #get views, likes, comments 
    num_of_toutiao = len(contents)

    total_num_of_likes = 0
    total_num_of_comments = 0
    total_num_of_views = 0.0

    # extract the data from the strings
    print("parsing the data")
    for result in results:
        if "阅读" in result.text:
            if "万" in result.text:
                total_num_of_views += float(extract_num(result.text)[0])+float(extract_num(result.text)[1])/10
            else:
                total_num_of_views += float(extract_num(result.text)[0])/10000
        elif "赞" in result.text:
            total_num_of_likes += int(extract_num(result.text)[0])
        elif "评论" in result.text:
            total_num_of_comments += int(extract_num(result.text)[0])

    total_num_of_views = round(total_num_of_views,4)
            
    avg_num_of_likes = round(total_num_of_likes/num_of_toutiao,2)
    avg_num_of_comments = round(total_num_of_comments/num_of_toutiao, 2)
    avg_num_of_views = round(total_num_of_views/num_of_toutiao,2)


    # write data to csv file
    print("writing the data to the csv file")
    with open('tou_tiao2.csv', mode='w',encoding="utf-8-sig") as file:
        file = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        x = 0
        for i in range(num_of_toutiao):
            content = contents[i].text
            view = results[x].text
            like = results[x+1].text[3:]
            comment = results[x+2].text[3:]
            time_stamp = time_stamps[i].text[3:]
            file.writerow([name, content, view, like, comment, time_stamp])
            x += 3
        file.writerow(["总阅读数: "+str(total_num_of_views)+"万", "总赞数: "+str(total_num_of_likes), "总评论数: "+ str(total_num_of_comments)])
        file.writerow(["平均阅读数: "+str(avg_num_of_views)+"万", "平均赞数: "+str(avg_num_of_likes), "平均评论数: "+ str(avg_num_of_comments)])

    print("平均阅读数：",avg_num_of_views, "万 ", "平均赞数：", avg_num_of_likes, "平均评论数：", avg_num_of_comments)
    print("总阅读数：",total_num_of_views, "万 ", "总赞数：", total_num_of_likes, "总评论数：", total_num_of_comments)

if __name__ == "__main__": main()
    
