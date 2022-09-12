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
import warnings
import PySimpleGUI as sg

warnings.simplefilter('ignore')

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
    lbl = driver.find_element_by_xpath("/html/body/div[5]/div[3]/label/input")
    lbl.click()
    # 次へ進むボタンを押す
    nxt = driver.find_element_by_id("attention_button_0")
    nxt.click()

# 競馬場リンクがあるか(満席ではないか)調べる
def check_racecourse(date, weekday, place):
    perform_date = date
    try:
        # 競馬場の選択
        kb = driver.find_element_by_name("vnts00102[venue_cd]")
        select = Select(kb)
        select.select_by_value(place)

        # 開催日の選択
        nt = driver.find_element_by_name("vnts00102[perform_date]")
        select = Select(nt)
        select.select_by_value(perform_date)

        # 検索ボタンを押す
        button = driver.find_element_by_id("search")
        button.click()

        # 受付中ボタンを押す
        enter = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div")
        enter.click()

    except NoSuchElementException: # 満席だったら自動更新して空席になるまで待つ
        time.sleep(2)
        driver.refresh()
        notion()
        return check_racecourse(date, weekday, place)
    
    else:
        return True
    
def check_notion(): # 競馬場のページに入ったときのお知らせの確認
    time.sleep(1)
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
        # time.sleep(1)
        ok = driver.find_element_by_class_name("ajs-button")
        ok.click()
    
    except NoSuchElementException: # 満席だったら自動更新して空席になるまで待つ
        # time.sleep(1)
        driver.refresh()
        check_notion()
        return choice(price)
    
    else:
        return True
    
# 座席数を選択する
def zaseki():
    zaseki = driver.find_element_by_class_name("select_checked_auto_aasign")    
    zaseki_element = Select(zaseki)
    # zaseki_element.select_by_value("1")

# 仮予約を押す
def book():
    # 仮予約ボタン押す
    book = driver.find_element_by_id("submitAButton")
    book.click()

def go_next():
    try:
        # 次の購入に進むページを押す
        next_step = driver.find_element_by_id("need_attention")
        next_step.click()
    
    except NoSuchElementException: # 取れなかったらやり直す
        # time.sleep(2)
        driver.refresh()
        return yoyaku(price)
    
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
    check_racecourse(date, weekday, place)
    
    # 該当競馬場に移動
    yoyaku(price)

    # 完了したら音を鳴らす
    winsound.Beep(400,1000)

# ウィンドウ色の指定
sg.theme("DarkGreen5")

# フレームの定義
frame = sg.Frame("",
                 [
                     [  # テキストレイアウト
                         sg.Text("JRA指定席のキャンセル分を自動で仮押さえします。")
                     ],
                     [
                         sg.Text("仮押さえ後は手動で購入をお願いします。")
                     ],
                     [
                         sg.Text("*" * 100)
                     ],
                     [
                         sg.Text("必要情報の入力(数字は半角)"),
                     ],
                     [
                         sg.Text("ネット予約確認番号"),
                         sg.In(key="ID", size=(20, 10))
                     ],
                     [
                         sg.Text("パスワード　　　　"),
                         sg.In(key="password", password_char="*", size=(20, 10))
                     ],
                     [
                         sg.Text("開催年月日(yyyymmdd)"),
                         sg.In(key="date", size=(20, 10))
                     ],
                     [
                         sg.Text("曜日(土・日)"),
                         sg.Radio("土", group_id="weekday", key="weekday_6"),
                         sg.Radio("日", group_id="weekday", key="weekday_7")
                     ],
                     [
                         sg.Text("開催競馬場"),
                         sg.Combo(["札幌", "函館", "福島", "新潟", "東京" ,"中山", "中京", "京都", "阪神", "小倉"], default_value="競馬場を選択", key="place", size=(20, 10))

                     ],
                     [
                         sg.Text("席の値段"),
                         sg.In(key="sheet_price", size=(20, 10))
                     ],
                     [
                         sg.Submit(button_text="GO!", size=(5,2), key="button")
                     ],
                     [
                         sg.Text("*" * 100)
                     ]

                 ], size=(500, 400)) # 幅、高さ

# 全体レイアウト
layout = [
    [
        frame
    ]
]

# GUIタイトルと全体レイアウトを乗せたウィンドウを定義する
window = sg.Window("JRAキャンセル席強奪プログラム", layout, resizable=True)

# GUI表示部分
while True:
    # ウィンドウ表示
    event, value = window.read()

    # クローズボタンの処理
    if event is None:
        print("exit")
        break

    # GOボタンが押された場合の挙動
    if event == "button":
        userid = value["ID"]
        password = value["password"]
        date = value["date"][:4] + "-" + value["date"][4:6] + "-" + value["date"][6:8]
        weekday = value["weekday_6"]
        place = value["place"]
        price = value["sheet_price"]
        if value["weekday_6"] == True:
            weekday = "土"
        elif value["weekday_7"] == True:
            weekday = "日"

        message = f"{date[:4]}年{date[5:7]}月{date[8:10]}日({weekday}) {place}競馬場の{price}円のキャンセル席を探します"
        sg.popup(message)

# window.close()



    if len(price) > 3:
        price = price[0] + "," + price[1:]


    # 競馬場IDを確定させる
    if place == "札幌":
        place = "SPKB"
    elif place == "函館":
        place = "HDKJ"
    elif place == "福島":
        place = "FKKB"
    elif place == "中山":
        place = "NYKB"
    elif place == "東京":
        place = "TKIJ"
    elif place == "新潟":
        place = "NKIB"
    elif place == "中京":
        place = "CKKB"
    elif place == "阪神":
        place = "HSKB"
    elif place == "京都":
        place = "KYKJ"
    elif place == "小倉":
        place = "KKKB"
    else:
        print("エラー")

    # chomedriver
    driver = webdriver.Chrome()

    # 読み込み待機
    driver.implicitly_wait(10)

    # 実際の運用
    ultimate()

    # 完了したら音を鳴らす
    winsound.Beep(400,1000)

    message1 = "キャンセル席の仮押さえに成功しました"
    message2 = "このあとは、手動で購入を行ってください"
    sg.popup(message1, message2)
    break

window.close()
