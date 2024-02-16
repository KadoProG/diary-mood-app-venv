import MeCab
from nltk.sentiment import SentimentIntensityAnalyzer
import ipadic

mecab = MeCab.Tagger(ipadic.MECAB_ARGS)  # インストールした辞書を指定


def _parse_mecab_line(line: str):
    """
    行ごとにデータを辞書配列化
    """
    parts = line.split()
    info = parts[1].split(",")

    return {
        "surface": parts[0],
        "pos": info[0],
        "pos_detail1": info[1],
        "pos_detail2": info[2] if len(info) > 2 else "",
        "pos_detail3": info[3] if len(info) > 3 else "",
        "conjugated_form": info[4] if len(info) > 4 else "",
        "basic_form": info[5] if len(info) > 5 else "",
        "reading": info[6] if len(info) > 6 else "",
        "pronunciation": info[7] if len(info) > 7 else "",
        "pronunciation_extended": info[8] if len(info) > 8 else "",
        "polarity_score": _sentiment_analysis(parts[0]),
    }


def out_parse_object(target_text: str):
    """
    文字列をMecabで形態素解析・感情分析し、配列を返す関数
    @params
    - target_text: 感情分析したいテキストを格納

    @returns
    - "words": 形態素分析した配列
      - "surface": 原文
      - "pos": 品詞名
      - "pos_detail1": 品詞の詳細１
      - "pos_detail2": 品詞の詳細２
      - "pos_detail3": 品詞の詳細３
      - "conjugated_form":
      - "basic_form": ?
      - "reading": 動詞の場合、原形
      - "pronunciation": カタカナ読み
      - "pronunciation_extended": カタカナ読み 伸ばし棒
      - "polarity_score": -1~1の範囲でポジティブ・ネガティブ度を格納
    - "meta": メタ情報
      - "word_count": 単語の個数
      - "polarity_average": 感情分析の平均
      - "polarity_notnull_average": 感情分析の平均（0を含まない）
    """
    # 形態素解析
    mecab_output = mecab.parse(target_text)

    # MeCabの純粋な行をリストとして格納 最後の行はEOSのため飛ばす
    lines = mecab_output.strip().split("\n")[:-1]

    # 行ごとにデータを辞書配列化
    result_lines = list(map(_parse_mecab_line, lines))

    polarity_score_list = list(entry["polarity_score"] for entry in result_lines)
    polarity_notnull_scores_list = list(
        entry["polarity_score"]
        for entry in result_lines
        if entry["polarity_score"] != 0
    )

    return {
        "words": result_lines,
        "meta": {
            "word_count": len(result_lines),
            "polarity_average": (
                sum(polarity_score_list) / len(result_lines)
                if len(result_lines) != 0
                else 0
            ),
            "polarity_notnull_average": (
                sum(polarity_notnull_scores_list) / len(polarity_notnull_scores_list)
                if len(polarity_notnull_scores_list) != 0
                else 0
            ),
        },
    }


def _load_data(file_path: str):
    """
    日本語P/Nデータのロード
    """
    data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            word, _, _, score = line.strip().split(":")
            data[word] = float(score)
    return data


def _sentiment_analysis(word: str):
    """
    感情分析して数値化する関数
    """
    # 日本語はこっちでfetch
    if word in emotion_data:
        return emotion_data[word]
    else:
        sid = SentimentIntensityAnalyzer()
        return sid.polarity_scores(word)["compound"]


# データの読み込み
data_file_path = "api/emotion/dictionary/PN_Table/pn_ja.dic.txt"
emotion_data = _load_data(data_file_path)

if __name__ == "__main__":
    result = out_parse_object("こんにちは今回はタイピング練習をしていこうと思います")
