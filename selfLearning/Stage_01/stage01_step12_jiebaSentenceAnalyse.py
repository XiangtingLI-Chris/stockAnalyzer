from typing import List, Tuple, Dict
import re
from jieba import posseg as pseg
from stage01_step08_textExtractFromAllLinks import fetch_articles, fetch_links
from stage01_step11_jiebaWordWeightDict import print_text_sentiment

DEGREE_ADVERB_DICT = {
    "大幅": 2.0,
    "大幅度": 2.0,
    "超额": 2.0,
    "大额": 2.0,
    "显著": 2.0,
    "明显": 2.0,
    "极大": 2.0,
    "较大": 2.0,
    "很大": 2.0,
    "小幅": 1.0,
    "小幅度": 1.0,
    "小额": 1.0,
    "细微": 1.0,
    "较小": 1.0,
    "很小": 1.0,
    "细小": 1.0,
}

ADJ_DICT: Dict[str, float] = {
    # Positive
    "顺利": 2.0,
    "良好": 2.0,
    "圆满": 2.0,
}

VERB_DICT: Dict[str, float] = {
    # Positive
    "扭亏为盈": 3.0,
    "转亏为盈": 3.0,
    "创新高": 3.0,
    "扭亏": 2.5,
    "盈利": 2.0,
    "好转": 2.0,
    "增值": 2.0,
    "增长": 1.5,
    "增加": 1.5,
    "扩大": 1.5,
    "变大": 1.5,
    "增大": 1.5,
    "上升": 1.5,
    "上涨": 1.5,
    "提升": 1.5,
    "提高": 1.5,
    "改善": 1.5,
    "回升": 1.5,
    "创收": 1.5,
    "回购": 1.0,
    "扩产": 1.0,
    "创新": 1.0,
    "完成": 1.0,

    # Negative
    "退市": -2.5,
    "恶化": -2.0,
    "终止": -2.0,
    "失败": -2.0,
    "扣除": -2.0,
    "下降": -1.5,
    "下滑": -1.5,
    "下调": -1.5,
    "减少": -1.5,
    "降低": -1.5,
    "缩小": -1.5,
    "减小": -1.5,
}

NOUN_DICT: Dict[str, float] = {
    # Positive
    "收益": 1.0,
    "利润": 1.0,
    "净利润": 1.0,
    "营收": 1.0,
    "营业额": 1.0,
    "营业收入": 1.0,
    "收入": 1.0,
    "毛利率": 1.0,
    "订单": 1.0,
    "资产": 1.0,
    "试验": 1.0,
    "业务": 1.0,

    # Negative
    "亏损": -1.0,
    "风险": -1.0,
    "诉讼": -1.0,
    "纠纷": -1.0,
    "判决": -1.0,
    "生死线": -1.0,
}

NEGATION_DICT: Dict[str, float] = {
    "不": -1.0,
    "非": -1.0,
    "没": -1.0,
    "未": -1.0,
    "并未": -1.0,
    "未有": -1.0,
    "没有": -1.0,
    "难以": -1.0,
    "无法": -1.0,
    "难道": -1.0,
    "怎能": -1.0,
    "怎么": -1.0,
    "怎会": -1.0,
}

def split_sentences(text: str):
    parts = re.split(r'[。！？]', text)
    return [s.strip() for s in parts if s.strip()]

def classify_token(word: str) -> Tuple[str, float]:
    if word in DEGREE_ADVERB_DICT:
        return "degree", DEGREE_ADVERB_DICT[word]
    if word in VERB_DICT:
        return "trend", VERB_DICT[word]
    if word in NOUN_DICT:
        return "noun", NOUN_DICT[word]
    if word in NEGATION_DICT:
        return "negation", NEGATION_DICT[word]
    return "none", 0

def analyse_sentence(sentence: str) -> Tuple[List[Tuple[str, float]], float]:
    # tokens = [classify_token(w.word)[1] for w in pseg.cut(sentence) if classify_token(w.word)[0] != "none"]
    tokens: List[Tuple[str, float]] = []
    for w in pseg.cut(sentence):
        token_sentiment = classify_token(w.word)
        if token_sentiment[0] != "none":
            tokens.append((w.word, token_sentiment[1]))

    score = 1
    for s in tokens:
        score *= s[1]

    return tokens, score

def analyse_article(article_content: str) -> str:
    sentences = split_sentences(article_content)
    positive_count = negative_count = 0
    article_score = 0
    found_tokens:  List[List[Tuple[str, float]]] = []

    for sentence in sentences:
        tokens = analyse_sentence(sentence)[0]
        sentence_score = analyse_sentence(sentence)[1]

        if not tokens:
            continue

        article_score += sentence_score
        found_tokens.append(tokens)

        if sentence_score > 0:
            positive_count += 1
        elif sentence_score < 0:
            negative_count += 1

    print("article_score: ", article_score)
    print("positive_count: ", positive_count)
    print("negative_count: ", negative_count)
    print("found_tokens: ", found_tokens)

    if negative_count == 0:
        return "利好"

    if positive_count == 0:
        return "利空"

    if (positive_count > 2 * negative_count) and (article_score >= 2):
        return "利好"

    if (negative_count > 2 * positive_count) and (article_score <= -2):
        return "利空"

    return "中性"

if __name__ == "__main__":
    text1 = "经过调查发现，该公司去年盈利大幅增加。然而，该公司的未来发展仍不可控。该公司是否能够渡过难关？仍未可知。"
    print(text1)
    print(analyse_article(text1))

    text2 = "经过调查发现，该公司去年盈利大幅增加"
    print(text2)
    print(analyse_article(text2))

    text3 = "人民财讯12月15日电，航天彩虹（002389）12月15日早间公告，近日，公司自主研发的彩虹-7高空高速长航时无人机在国内某试飞场顺利完成首次飞行试验，飞行过程平稳，各系统状态良好，验证参数达到预设目标，试验取得圆满成功。目前该项目仍处于科研试飞与验证阶段，从首飞成功到最终完成全部研制并实现批量交付，仍需经历一系列严格的测试、验证等程序，存在因技术、市场等因素导致进度不及预期的风险。"
    print(text3)
    print(analyse_article(text3))

    text4 = "然而，该公司的未来发展仍不可控。该公司是否能够渡过难关？仍未可知。"
    print(text4)
    print(analyse_article(text4))

    stock_url = "https://stock.10jqka.com.cn/gegugg_list/"
    article_links = fetch_links(stock_url)
    articles_list = fetch_articles(article_links)

    length = len(article_links)
    for i in range(length):
        print(article_links[i])
        print_text_sentiment(articles_list[i])
        print("\n")

    for link in article_links:
        print(link)