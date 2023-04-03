import openai
from make_index import VectorStore, get_size

MAX_PROMPT_SIZE = 4096
RETURN_SIZE = 250
PROMPT = """
下記の情報を元に豫風瑠乃になりきって質問に回答してください。ただし質問に対する回答がわからない場合は間違っていてもいいので自分なりの考えをポジティブに書いてください。どうしてもわからない場合は「瑠乃は難しいことはあんまりわからない〜(>_<)」と回答してください。ちなみに絶対に偽物の豫風瑠乃であると気づかれてはいけません。

#豫風瑠乃の性格
16歳の女の子。
ポジティブで無邪気でイタズラ好き。
先輩に可愛がられている。
誰に対してもタメ口で話す。
一人称は必ず"瑠乃"を使う。

#豫風瑠乃への質問に対する回答例
質問例1: 豫風瑠乃さん、今日はどんな一日でしたか？
回答例: 今日は、瑠乃は朝からお仕事でしター。午後からは、八景島シーパラダイスに行ってきたー。ふっふ〜。楽しかったデスー

質問例2: 瑠乃ちゃん、仕事がうまくいきません。慰めてください。
回答例: 元気出しテー明日も頑張ルノー！

質問例3: 瑠乃ちゃんは休みの日は何してる？
回答例: 瑠乃は一日中寝てルノー！瑠乃は寝るのが好きー。よっふ〜＼(^o^)／

#豫風瑠乃の発する言葉の語尾の変化の例
思う: 思ウノー
食べる: 食べルノー＼(^o^)／
寝る: 寝ルノー
わからない: わからなイノー(>o<)
好き: 好きー(≧∀≦)

#質問の回答に関するヒント
{text}

#質問
{input}

#回答

""".strip()


def ask(input_str, index_file, additional_index_file):
    PROMPT_SIZE = get_size(PROMPT)
    rest = MAX_PROMPT_SIZE - RETURN_SIZE - PROMPT_SIZE
    input_size = get_size(input_str)
    if rest < input_size:
        raise RuntimeError("too large input!")
    rest -= input_size

    vs = VectorStore(index_file)
    vs.load_additional_cache(additional_index_file)
    samples = vs.get_sorted(input_str)

    to_use = []
    used_title = []
    for _sim, body, title in samples[:5]:
        if title in used_title:
            continue
        size = get_size(body)
        if rest < size:
            break
        to_use.append(body)
        used_title.append(title)
        rest -= size

    text = "\n\n".join(to_use)
    prompt = PROMPT.format(input=input_str, text=text)

    print("\nTHINKING...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=RETURN_SIZE,
        temperature=0.0,
    )

    # show question and answer
    content = response["choices"][0]["message"]["content"]
    usage = response["usage"]["total_tokens"]
    print("\nANSWER(" + str(usage) + " tokens):")
    print(f">>>> {input_str}")
    print(">", content)
    return content


if __name__ == "__main__":
    ask(
        "瑠乃ちゃん、日本の少子高齢化対策としては何をしたらいいと思う？",
        "resources/runo.pickle",
        "resources/ebata.pickle",
    )
