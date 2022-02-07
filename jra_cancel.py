# ライブラリのインポート
import selenium
import time
import urllib.request, urllib.error
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import winsound
from selenium import webdriver

# ログインする
def login(userid, password):
    # 会員番号入力欄を探す
    usr = driver.find_element_by_name("vupi001pc[userid]")
    # 会員番号を入力
    usr.send_keys(userid)
    # パスワード入力欄を探す
    pwd = driver.find_element_by_name("vupi001pc[passwd]")
    # パスワードを入力
    pwd.send_keys(password)
    # ログインボタンを探す
    link = driver.find_element_by_name("login")
    # ログインボタンを押す
    link.click()

# アクセス集中時のログイン
def return_login():
    login_return = driver.find_element_by_link_text("ログイン")
    login_return.click()
    
# お知らせを確認する
def notion():
    # 確認したチェックボックスを入れる
    lbl = driver.find_element_by_tag_name("label")
    lbl.click()
    # 次へ進むボタンを押す
    nxt = driver.find_element_by_id("attention_button_0")
    nxt.click()

# 競馬場リンクがあるか(満席ではないか)調べる
def check_racecourse(year, month, day, weekday, place):
    course_text = "{}年{}月{}日({}) {}競馬場".format(year, month, day, weekday, place) # 場所,時間変えたかったらここ編集する    
    try:
        tokyo = driver.find_element_by_link_text(course_text)    
        tokyo.click()
    
    except NoSuchElementException: # 満席だったら自動更新して空席になるまで待つ
        time.sleep(2)
        driver.refresh()
        notion()
        return check_racecourse(year, month, day, weekday, place)
    
    else:
        return True
    
def check_notion(): # 競馬場のページに入ったときのお知らせの確認
    time.sleep(2)
    # 確認したチェックボックスを入れる
    labl = driver.find_element_by_tag_name("label")
    labl.click()
    #次へ進むを押す
    nxt1 = driver.find_element_by_id("attention_button_1")
    nxt1.click()

# おまかせを開く
def omakase():
    omakase = driver.find_element_by_id("p03A_auto_open")
    omakase.click()
    
# 選択リンクを押す,
def choice(price):
    try:
#         seat = driver.find_element_by_class_name("ticket_auto_link")
        seat = driver.find_element_by_tag_name("[ticketprice = '{}']".format(price))
        seat.click()
        time.sleep(1)
        ok = driver.find_element_by_class_name("ajs-button")
        ok.click()
    
    except NoSuchElementException: # 満席だったら自動更新して空席になるまで待つ
        time.sleep(1)
        driver.refresh()
        check_notion()
        return choice()
    
    else:
        return True
    
# 座席数を選択する
def zaseki():
    zaseki = driver.find_element_by_class_name("select_checked_auto_aasign")    
    zaseki_element = Select(zaseki)
#     zaseki_element.select_by_value("1")

# 仮予約を押す
def book():
    # 仮予約ボタン押す
    book = driver.find_element_by_id("submitAButton")
    book.click()
    # OKボタンオ押す
    ok2 = driver.find_element_by_class_name("ajs-button")
    ok2.click()

def go_next():
    try:
        # 次の購入に進むページを押す
        next_step = driver.find_element_by_id("need_attention")
        next_step.click()
    
    except NoSuchElementException: # 取れなかったらやり直す
        time.sleep(2)
        driver.refresh()
        return yoyaku()
    
    else:
        return True
    
# 予約のループ
def yoyaku(price):
    # 競馬場ごとのお知らせ確認
    check_notion()
    
    # おまかせ選択をクリックする
    omakase()

    # 有効な選択ボタンが存在するか調べる。なければ更新。
    # 選択ボタンを押す、OKボタンを押す
    choice(price)

    # 自動で割り当て仮予約にするを押す。
    book()
    
    # 次に進む
    go_next()
    
    
def ultimate():
    # urlはJRAの指定席ログイン画面
    url = "https://jra.flpjp.com/"
    driver.get(url)
    
    # ログイン後の画面かどうか確認。違ったらやり直す
    current_page = driver.current_url
    while current_page != "https://jra.flpjp.com/":
        # ログインからやり直す
        return ultimate()
    
    # ログインを行う
    login(userid, password)
    
    # ログイン後の画面を確認する。違ったらまたログイン画面へ
    current_page = driver.current_url
    while current_page != "https://jra.flpjp.com/ticketTop":
        # ログインからやり直す
        return ultimate()
    
    # ログインできたら、お知らせ画面でチェック。次へ進む
    notion()

    # 該当競馬場のリンクが有効かどうか調べる。有効でなければループ。
    check_racecourse(year, month, day, weekday, place)
    
    # 該当競馬場に移動
    yoyaku(price)

    # 完了したら音を鳴らす
    winsound.Beep(400,1000)
    

print("これは、キャンセル席を仮押さえするためのプログラムです。仮押さえに成功した場合は、手動で購入をしてください。")
print("")
print("")
print("★★事前準備をします★★")
print("数字はすべて半角で入力してください")
print("")
userid = input("会員番号を入力してください")
password = input("パスワードを入力してください")
year = input("何年(4桁)")
month = input("何月(2桁)")
day = input("何日(2桁)")
weekday = input("土日どっち(1文字)")
place = input("場所(2文字)")
price = input("席の値段")

print("=======================================")
print("{}年{}月{}日({}) {}競馬場の{}円のキャンセル席を探します".format(year, month, day, weekday, place, price))
print("=======================================")

# chomedriver
driver = webdriver.Chrome()

# 実際の運用
ultimate()

# 完了したら音を鳴らす
winsound.Beep(400,1000)

print("=======================================")
print("{}年{}月{}日({}) {}競馬場の{}円のキャンセル席の仮押さえに成功しました".format(year, month, day, weekday, place, price))
print("このあとは、手動で購入を行ってください")
print("=======================================")
