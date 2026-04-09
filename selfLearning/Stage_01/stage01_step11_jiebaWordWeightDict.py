import jieba
from jieba import analyse
from typing import List, Tuple, Dict
from stage01_step07_textExtractFromLink import text_extract
from stage01_step08_textExtractFromAllLinks import fetch_articles, fetch_links

POSITIVE_WORDS = {
    "增长": 1.2,
    "提升": 1.0,
    "回购": 2.0,
    "创新高": 2.0,
    "盈利": 1.5,
    "扭亏为盈": 2.0,
    "大幅增长": 2.0,
    "扩产": 1.2,
    "订单": 1.0,
    "营收": 1.5,
    "创新": 1.2,
    "利润": 1.5,

}

NEGATIVE_WORDS = {
    "下滑": 1.2,
    "下降": 1.0,
    "减少": 1.0,
    "亏损": 1.5,
    "亏损扩大": 2.0,
    "预警": 1.2,
    "警示": 1.2,
    "下调": 1.0,
    "大幅下降": 2.0,
    "终止": 1.5,
    "失败": 1.5,
    "风险": 1.2,
    "诉讼": 1.5,
    "纠纷": 1.2,
    "判决": 1.0,
    "资产重组": 1.5,
    "扣除": 1.2,
    "退市": 1.5,
    "生死线": 1.2,
    "娄底": 1.2,
    "不良资产": 1.5,
}

def extract_keywords(text: str, top_k: int = 30) -> List[Tuple[str, float]]:
    return jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)

def score_sentiment(keywords_with_weight: List[Tuple[str, float]]) -> Tuple[float, List[Tuple[str, float]]]:
    score = 0.0
    matches: List[Tuple[str, float]] = []

    for word, weight in keywords_with_weight:
        if (word in POSITIVE_WORDS) or (word in NEGATIVE_WORDS):
            if word in POSITIVE_WORDS:
                temp_score = weight * POSITIVE_WORDS[word]
            else:
                temp_score = -weight * NEGATIVE_WORDS[word]
            matches.append((word, temp_score))
            score += temp_score

    return score, matches

def matches_analyse(matches: List[Tuple[str, float]]) -> Dict[str, int]:
    dict: Dict[str, int] = { "positive": 0, "negative": 0 }

    dict["positive"] = len([w for w, s in matches if s > 0])
    dict["negative"] = len([w for w, s in matches if s < 0])

    return dict

def judge_sentiment(text: str) -> str:
    keywords_list = extract_keywords(text, 30)
    score, matches = score_sentiment(keywords_list)

    analyse_dict = matches_analyse(matches)
    positive_count = analyse_dict["positive"]
    negative_count = analyse_dict["negative"]

    print("keywords_list:")
    print(keywords_list)
    print("matches and contributions:")
    print(matches)
    print("total score:")
    print(score)
    print("positive count: ", positive_count)
    print("negative count: ", negative_count)

    if (positive_count == 0) and (negative_count == 0):
        return "中性"

    if (positive_count == 0) or (negative_count == 0):
        if positive_count == 0:
            return "利空"
        else:
            return "利好"

    if score > 0.5:
        return "利好"
    elif score < -0.5:
        return "利空"
    else:
        return "中性"

def print_text_sentiment(text: str) -> None:
    sentiment = judge_sentiment(text)
    print("article sentiment: ", sentiment)

if __name__ == "__main__":
    text1 = "公告显示，公司营收同比增长30%，利润创新高，未来将保持稳定向好趋势"
    print_text_sentiment(text1)

    article_url = "https://stock.10jqka.com.cn/20251209/c673062866.shtml"
    text2 = text_extract(article_url)
    print_text_sentiment(text2)

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