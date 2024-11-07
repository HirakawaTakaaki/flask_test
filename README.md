# WordCloud作成（テスト段階）
## 概要
* テキストファイルを与えることでワードクラウドを生成する
* テキストから抽出したワードは出現回数と一緒にリストで表示
* チェックボックスで選択したワードを除外してワードクラウドを再生成することができる
* ワードクラウドはHTMLで出力しており、ワードをクリックすることでイベント発生。今回はクリックしたワードでGoogle検索にとぶ。
  
## 実行画面
![実行画面](https://github.com/user-attachments/assets/e3f4d4f2-ffab-48da-a349-13d197befe0d)

## Demo
![デモ](https://github.com/user-attachments/assets/46b33579-7b94-4869-b254-a6942c22abe5)

## 技術スタック
#### バックエンド
* Python
* フレームワークはFlask
* 形態素解析にはMeCabを使用
#### フロントエンド
* HTML（テスト用なので最低限の表示のみ）
* 本番ではjavascriptを使った処理を追加
