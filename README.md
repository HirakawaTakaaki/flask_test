# WordCloud作成（テスト段階）
## 概要
* テキストファイルを与えることでワードクラウドを生成
* ワードクラウドはHTMLで出力しており、ワードをクリックするとGoogle検索ができるようになっている
* ファイルから抽出したワードはリストで表示
* チェックボックスで選択したワードを除外してワードクラウドを再生成することができる
  
## 実行画面
![実行画面](https://github.com/user-attachments/assets/e3f4d4f2-ffab-48da-a349-13d197befe0d)

## demo
![デモ](https://github.com/user-attachments/assets/46b33579-7b94-4869-b254-a6942c22abe5)

## 技術スタック
* 主にPython、Flaskを使い実装
* 形態素解析にはMeCabを使用
