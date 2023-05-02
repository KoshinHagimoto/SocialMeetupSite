# Social Media Meetup Site
Djangoを用いて個人開発したWebサイト(アプリケーション)

## About
同じような興味を持つ人々の間でグループや対面ミーティングの発足を目的とした、ソーシャルメディアのウェブサイト

## Usage
会員登録をしたユーザーはグループに参加もしくは作成することが可能。グループ内では, イベントを作成することが出来る。イベントの詳細ページではイベントに参加しているユーザ同士でコメントすることが出来る。

### Examples
出会いを目的としたグループ→クリスマスパーティーのイベント

## Points
1. 会員登録機能と権限の付与（GroupやEventのホストは解散や更新の権限）
2. indexページの検索機能
3. Group,Event詳細ページにおいて, ボタンによりグループ参加離脱が可能
4. Event詳細ページの掲示板スレッド機能
5. ユーザーのEmailを用いたパスワードリセット機能
6. celeryを用いた非同期処理による管理者へのメール機能(ユーザーがグループに参加したり, Eventが作成した場合)
7. Sessionを用いた現在ログインしているユーザの表示機能