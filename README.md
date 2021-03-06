# jra_cancel
指定席のキャンセル席を自動で仮押さえするプログラムです。

## 概要
指定席のキャンセル席の先着販売が毎週月曜日の17:00からスタートしますが、毎度アクセス集中によりログインもままならない場合が多く発生します。<br>
そこで、ログインから目的の指定席の仮押さえまでの作業を自動で行うプログラムを作成しました。<br>
ログインに失敗すれば自動でログインのやり直しをしますし、狙いの席が満席の場合は、空席になるまで待って空席になった瞬間仮押さえの作業を開始します。<br>
仮押さえに成功した後は、個人でカード情報を手動入力すれば購入できるようになっています。<br>

## 操作手順
※googlechromeが使用できるPC環境で実施ください。<br>
1. jra_cancel.exe, chromedriver.exeをダウンロードする<br>
2. jra_cancel.exeをダブルクリックする
3. 下図のように、必要な情報を入力する<br>
![image](https://user-images.githubusercontent.com/87257802/152737822-ccd97766-e502-4082-9fba-db9d622ccaad.png)

   ※途中で入力を間違えた場合は、一度「✕」ボタンで閉じたあと、再度実行してください。<br>

4. 必要事項を入力したらEnter。自動でログインから予約画面に行く。<br>
   ※予約ページがメンテナンス中の場合は、リロードを続けます。サーバーに負担がかかりますので、メンテナンス中の場合は長時間このプログラムを動かさないようにしてください。<br>
5. 仮押さえが成功したら、手動で購入してください。<br>

## このプログラムのメリット
このプログラムは、キャンセル争奪戦の開始数十秒で満席になってしまいログインすらできずに敗戦してしまう人が多い中で、なんとかキャンセル待ちの席を取ることができないかと考え作ったものです。<br>
まず、メンテナンスが開ける10秒前から準備し、メンテナンスが終わって通常ページが表示されたら、ログインできるまで無限にログイン自動でを続けます。<br>
これだけでも、ログインするために色々入力する面倒臭さと時間を一気に短縮し、ログイン試行回数を増やすことでいかに素早く仮押さえまで行けるかというところに注力しています。<br>
仮押さえの枚数は1枚。これは、キャンセル待ちで2枚を一気に仮押さえするのはかなりハードルが高いからです。1枚をどうにか抑えたい場合にご利用ください。

## 変更履歴
20220430 : 競馬場追加(福島、新潟、中京、京都、小倉) <br>
20220714 : 全競馬場対応完了
