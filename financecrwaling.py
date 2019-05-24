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

def get_bs_obj1(company_code):
    url1 = "https://finance.naver.com/item/coinfo.nhn?code=" + company_code
    result1 = requests.get(url1)
    bs_obj1 = BeautifulSoup(result1.content, "html.parser")
    return bs_obj1

def get_bs_obj2(company_code):
    url2 = "https://finance.naver.com/item/frgn.nhn?code=" + company_code
    result2 = requests.get(url2)
    bs_obj2 = BeautifulSoup(result2.content, "html.parser")
    return bs_obj2

def get_name(company_code):
    bs_obj1 = get_bs_obj1(company_code)
    wrap_company = bs_obj1.find("div", {"class": "wrap_company"})
    num_company = wrap_company.find("h2")
    return num_company.text

def get_price(company_code):
    bs_obj1 = get_bs_obj1(company_code)
    no_today = bs_obj1.find("div", {"class": "today"})
    blind_now = no_today.find("p", {"class": "no_today"})
    fin_now = blind_now.find("span",{"class":"blind"})
    return fin_now.text.replace(",", "")

def get_trade_num(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    no0_trade = bs_obj2.findAll("table", {"class": "type2"})
    no1_trade = no0_trade[1].findAll("tr")
    no_trade = no1_trade[3].findAll("span")
    return no_trade[4].text

def get_govern_trade(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    gv0_trade = bs_obj2.findAll("table", {"class": "type2"})
    gv1_trade = gv0_trade[1].findAll("tr")
    gv_trade = gv1_trade[3].findAll("span")
    return gv_trade[5].text

def get_foreign_trade(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    fr0_trade = bs_obj2.findAll("table", {"class": "type2"})
    fr1_trade = fr0_trade[1].findAll("tr")
    fr_trade = fr1_trade[3].findAll("span")
    return fr_trade[6].text

def get_per(company_code):
    bs_obj1 = get_bs_obj1(company_code)
    no_per = bs_obj1.find("em", {"id": "_per"})
    return no_per.text

def get_pbr(company_code):
    bs_obj1 = get_bs_obj1(company_code)
    no_pbr = bs_obj1.find("table", {"class": "per_table"})
    pbr_now = no_pbr.findAll("td")
    pbr_bar = pbr_now[3].findAll("em")
    return pbr_bar[1].text.replace(",", "")

def get_foreign(company_code):
    bs_obj1 = get_bs_obj1(company_code)
    no_foreign = bs_obj1.find("table", {"class": "lwidth"})
    foreign = no_foreign.findAll("td")
    return foreign[2].text

def get_date(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    wrap_date = bs_obj2.findAll("table",{"class":"type2"})
    wrap1_date = wrap_date[1].findAll("tr")
    today_date = wrap1_date[3].findAll("span")
    return today_date[0].text[:10]

def get_issue(company_code):
    return 0

def get_yester(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    no_yester = bs_obj2.findAll("table",{"class":"type2"})
    no1_yester = no_yester[1].findAll("tr")
    fin_yester = no1_yester[3].findAll("span")
    return fin_yester[2].text.strip().replace(",", "")

def get_updown(company_code):
    bs_obj2 = get_bs_obj2(company_code)
    no_updown = bs_obj2.findAll("table",{"class":"type2"})
    no1_updown = no_updown[1].findAll("tr")
    fin_updown = no1_updown[3].findAll("span")
    return fin_updown[3].text.strip()

def get_recommend(company_code):
    result = (float(per)*-2) + (float(pbr)*-6) + float(re.sub('[%]', '', foreign))
    return result

IT = ["005930","034220","000660","066570","006400"] # IT대표주
BIO = ["043090","086890","068270","128940","003060","095700","009420"] # 바이오시밀러
EDU = ["215200","068930","057030","095720","072870","019680","033110","100220","040420","134060","053290","067280","096240","035290","036000"] # 교육주
FLEX = ["027580","108230","020760","077360","066980","059100","068790","005290","056190"] # 플랙서블 디스플레이주
ELB = ["091580","004490","054210","047310","011790","023890","009830","003670","036830","086520","102710","066970","131390"] # 2차전지주

for item in IT:
    name = get_name(item)
    price = get_price(item)
    yst = get_yester(item)
    updn = get_updown(item)
    trade = get_trade_num(item)
    gv_trade = get_govern_trade(item)
    fr_trade = get_foreign_trade(item)
    per = get_per(item)
    pbr_0 = get_pbr(item)
    pbr = round(float(pbr_0) / float(price), 2)
    foreign = get_foreign(item)
    date = get_date(item)
    issue = get_issue(item)
    if float(per) > 0:
        recommend = get_recommend(item)
    else:
        recommend = -9999
    with connection.cursor() as cursor:
        sql = "INSERT INTO IT (name,price,yst,updn,trade,gv_trade,fr_trade,per,pbr,forein,issue,date,recom) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (name, price, yst, updn, trade, gv_trade, fr_trade, per, pbr, foreign, issue, date, recommend))
    connection.commit()
print("IT끝")

for item in BIO:
    name = get_name(item)
    price = get_price(item)
    yst = get_yester(item)
    updn = get_updown(item)
    trade = get_trade_num(item)
    gv_trade = get_govern_trade(item)
    fr_trade = get_foreign_trade(item)
    per = get_per(item)
    pbr_0 = get_pbr(item)
    pbr = round(float(pbr_0) / float(price), 2)
    foreign = get_foreign(item)
    date = get_date(item)
    issue = get_issue(item)
    if float(per) > 0:
        recommend = get_recommend(item)
    else:
        recommend = -9999
    with connection.cursor() as cursor:
        sql = "INSERT INTO BIO (name,price,yst,updn,trade,gv_trade,fr_trade,per,pbr,forein,issue,date,recom) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (name, price, yst, updn, trade, gv_trade, fr_trade, per, pbr, foreign, issue, date, recommend))
    connection.commit()
print("BIO끝")

for item in EDU:
    name = get_name(item)
    price = get_price(item)
    yst = get_yester(item)
    updn = get_updown(item)
    trade = get_trade_num(item)
    gv_trade = get_govern_trade(item)
    fr_trade = get_foreign_trade(item)
    per = get_per(item)
    pbr_0 = get_pbr(item)
    pbr = round(float(pbr_0) / float(price), 2)
    foreign = get_foreign(item)
    date = get_date(item)
    issue = get_issue(item)
    if float(per) > 0:
        recommend = get_recommend(item)
    else:
        recommend = -9999
    with connection.cursor() as cursor:
        sql = "INSERT INTO EDU (name,price,yst,updn,trade,gv_trade,fr_trade,per,pbr,forein,issue,date,recom) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (name, price, yst, updn, trade, gv_trade, fr_trade, per, pbr, foreign, issue, date, recommend))
    connection.commit()
print("EDU끝")

for item in FLEX:
    name = get_name(item)
    price = get_price(item)
    yst = get_yester(item)
    updn = get_updown(item)
    trade = get_trade_num(item)
    gv_trade = get_govern_trade(item)
    fr_trade = get_foreign_trade(item)
    per = get_per(item)
    pbr_0 = get_pbr(item)
    pbr = round(float(pbr_0) / float(price), 2)
    foreign = get_foreign(item)
    date = get_date(item)
    issue = get_issue(item)
    if float(per) > 0:
        recommend = get_recommend(item)
    else:
        recommend = -9999
    with connection.cursor() as cursor:
        sql = "INSERT INTO FLEX (name,price,yst,updn,trade,gv_trade,fr_trade,per,pbr,forein,issue,date,recom) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (name, price, yst, updn, trade, gv_trade, fr_trade, per, pbr, foreign, issue, date, recommend))
    connection.commit()
print("FLEX끝")

for item in ELB:
    name = get_name(item)
    price = get_price(item)
    yst = get_yester(item)
    updn = get_updown(item)
    trade = get_trade_num(item)
    gv_trade = get_govern_trade(item)
    fr_trade = get_foreign_trade(item)
    per = get_per(item)
    pbr_0 = get_pbr(item)
    pbr = round(float(pbr_0) / float(price), 2)
    foreign = get_foreign(item)
    date = get_date(item)
    issue = get_issue(item)
    if float(per) > 0:
        recommend = get_recommend(item)
    else:
        recommend = -9999
    with connection.cursor() as cursor:
        sql = "INSERT INTO ELB (name,price,yst,updn,trade,gv_trade,fr_trade,per,pbr,forein,issue,date,recom) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (name, price, yst, updn, trade, gv_trade, fr_trade, per, pbr, foreign, issue, date, recommend))
    connection.commit()
print("ELB끝")