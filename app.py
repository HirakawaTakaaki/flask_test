from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import MeCab
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from collections import Counter
# import termextract.mecab
# import termextract.core

import const

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("iframe2.html", wordcloud_url=None)

@app.route('/upload_and_generate', methods=['POST'])
def upload_and_generate():
    uploaded_file = request.files["file"]
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        # file_name = uploaded_file.filename.split(".")[0]
        # no_display_words = request.form.get("stop_words", "").split("、")
        no_display_words = []
        word_list = generate_wordcloud(file_content, no_display_words)
        return render_template("iframe2.html", content=file_content, wordcloud_url="/generated.html", word_list=word_list, ng_words=no_display_words)
    else:
        # JavaScriptを使用してアラートダイアログを表示するために、JSON形式でエラーメッセージを返す
        return jsonify({"error": "ファイルがアップロードされていません。"}), 400

@app.route('/regenerate', methods=['POST'])
def regenerate():
    file_content = request.form.get("content", "")
    no_display_words  = request.form.get("ng_words", "").split(",")
    if file_content:
        no_display_words += request.form.getlist("no_display_words")
        word_list = generate_wordcloud(file_content, no_display_words)
        return render_template("iframe2.html", content=file_content, wordcloud_url="/generated.html", word_list=word_list, ng_words=no_display_words)
    return "ファイルがアップロードされていません。"

def output_excel(words_chain):
    noun_count_df = pd.DataFrame(words_chain.items(), columns=["ワード", "出現回数"])
    sorted_noun_count_df = noun_count_df.sort_values(by="出現回数", ascending=False)
    output_filename = os.path.join(const.RESULT_DIR_CLOUD, "ワード出現回数.xlsx")
    sorted_noun_count_df.to_excel(output_filename, index=False)
    print(f"出力が完了しました。ファイル名: {os.path.abspath(output_filename)}")

# 形態素解析で単語を抽出
def get_mecab_tagged(text, stop_words):
    tagger = MeCab.Tagger()
    tagger.parse('')
    
    node = tagger.parseToNode(text)
    word_list = []
    
    while node:
        if node.surface and node.surface not in stop_words:
            # 名詞だけを抽出
            feature = node.feature.split(',')[0]  # 品詞情報（名詞）を取得
            if feature == '名詞':
                word_list.append(node.surface)
        node = node.next
    
    return word_list

def get_word_frequencies(word_list):
    return Counter(word_list)

def generate_wordcloud(text, no_display_words):
    
    word_list = get_mecab_tagged(text, no_display_words)
    word_frequencies = get_word_frequencies(word_list)
    
    fontpath = const.FONT_PATH
    wordcloud = WordCloud(
            background_color="white",
            colormap="nipy_spectral",  # 文字色のカラーマップ指定
            # prefer_horizontal=1,
            font_path=fontpath,  # 日本語フォントの設定
            min_font_size=8,
            width=800,
            height=600,
            contour_width=1,
            contour_color="black"
        ).fit_words(word_frequencies)
    
    # textタグたちに、クリック時にGoogle検索結果を開くイベントリスナーを追加するJavaScript
    link_script = """
<script>
    svg = document.getElementsByTagName("svg")[0];
    text_tags =  svg.getElementsByTagName("text")
    for(var i=0; i<text_tags.length; i++){
        text_tags[i].addEventListener(
            "click",
            function(){
                word = this.textContent;
                word_uri = encodeURI(word);
                url = "https://www.google.com/search?q=" + word_uri;
                window.open(url, "_bkank");
            }
        )
    }
</script>"""

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
</head>
<body>

{wordcloud.to_svg()}
{link_script}

</body>
</html>
"""
    
    html_path = os.path.join(const.RESULT_DIR_CLOUD, "generated2.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 出現数の降順で並び替え
    sorted_word_counts = word_frequencies.most_common()
    return sorted_word_counts

@app.route('/generated.html')
def generated_html():
    directory = os.path.abspath(const.RESULT_DIR_CLOUD)
    filename = "generated2.html"
    print(f"path: {directory}\nfilename: {filename}\n")
    
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)
