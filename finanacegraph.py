import requests
import re
import pymysql.cursors
from bs4 import BeautifulSoup


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='oracle',
                             db='jusick',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

def get_bs_obj(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj

def get_bs_obj2(company_code):
    url2 = "https://finance.naver.com/item/frgn.nhn?code=" + company_code
    result2 = requests.get(url2)
    bs_obj2 = BeautifulSoup(result2.content, "html.parser")
    return bs_obj2

def get_name(company_code):
    bs_obj = get_bs_obj(company_code)
    name = bs_obj.find("div",{"class":"wrap_company"})
    fin_name = name.find("h2")
    return fin_name.text

def get_date(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    wrap_date = bs_obj2.findAll("table",{"class":"type2"})
    wrap1_date = wrap_date[1].findAll("tr")
    today_date = wrap1_date[3].findAll("span")
    return today_date[0].text[:10]

def get_end(company_code):
    bs_obj = get_bs_obj(company_code)
    end0_price = bs_obj.find("div", {"id": "chart_area"})
    end1_price = end0_price.find("div", {"class": "today"})
    end2_price = end1_price.findAll("span")
    return end2_price[0].text.replace(",", "")

def get_high(company_code):
    bs_obj = get_bs_obj(company_code)
    high0_price = bs_obj.find("div", {"id": "chart_area"})
    high1_price = high0_price.find("table", {"class":"no_info"})
    high2_price = high1_price.findAll("span", {"class": "blind"})
    return high2_price[1].text.replace(",", "")

def get_start(company_code):
    bs_obj = get_bs_obj(company_code)
    start0_price = bs_obj.find("div", {"id": "chart_area"})
    start1_price = start0_price.find("table", {"class":"no_info"})
    start2_price = start1_price.findAll("span", {"class": "blind"})
    return start2_price[4].text.replace(",", "")

def get_low(company_code):
    bs_obj = get_bs_obj(company_code)
    low0_price = bs_obj.find("div", {"id": "chart_area"})
    low1_price = low0_price.find("table", {"class":"no_info"})
    low2_price = low1_price.findAll("span", {"class": "blind"})
    return low2_price[5].text.replace(",", "")

IT = ["005930","034220","000660","066570","006400"] # IT대표주
BIO = ["043090","086890","068270","128940","003060","095700","009420"] # 바이오시밀러
EDU = ["215200","068930","057030","095720","072870","019680","033110","100220","040420","134060","053290","067280","096240","035290","036000"] # 교육주
FLEX = ["027580","108230","020760","077360","066980","059100","068790","005290","056190"] # 플랙서블 디스플레이주
ELB = ["091580","004490","054210","047310","011790","023890","009830","003670","036830","086520","102710","066970","131390"] # 2차전지주

for item in IT:
    name = get_name(item)
    date = get_date(item)
    start = get_start(item)
    end = get_end(item)
    high = get_high(item)
    low = get_low(item)
    with connection.cursor() as cursor:
        sql = "INSERT INTO IT_GRAPH (name, date, start, end, high, low) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, date, start, end, high, low))
    connection.commit()
print("IT_GRAPH끝")

for item in BIO:
    name = get_name(item)
    date = get_date(item)
    start = get_start(item)
    end = get_end(item)
    high = get_high(item)
    low = get_low(item)
    with connection.cursor() as cursor:
        sql = "INSERT INTO BIO_GRAPH (name, date, start, end, high, low) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, date, start, end, high, low))
    connection.commit()
print("BIO_GRAPH끝")

for item in EDU:
    name = get_name(item)
    date = get_date(item)
    start = get_start(item)
    end = get_end(item)
    high = get_high(item)
    low = get_low(item)
    with connection.cursor() as cursor:
        sql = "INSERT INTO EDU_GRAPH (name, date, start, end, high, low) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, date, start, end, high, low))
    connection.commit()
print("EDU_GRAPH끝")

for item in FLEX:
    name = get_name(item)
    date = get_date(item)
    start = get_start(item)
    end = get_end(item)
    high = get_high(item)
    low = get_low(item)
    with connection.cursor() as cursor:
        sql = "INSERT INTO FLEX_GRAPH (name, date, start, end, high, low) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, date, start, end, high, low))
    connection.commit()
print("FLEX_GRAPH끝")

for item in ELB:
    name = get_name(item)
    date = get_date(item)
    start = get_start(item)
    end = get_end(item)
    high = get_high(item)
    low = get_low(item)
    with connection.cursor() as cursor:
        sql = "INSERT INTO ELB_GRAPH (name, date, start, end, high, low) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, date, start, end, high, low))
    connection.commit()
print("ELB_GRAPH끝")