import jieba
from jieba import analyse
from typing import List
from stage01_step07_textExtractFromLink import text_extract

POSITIVE_WORDS = ["增长", "提升", "回购", "创新高", "盈利", "扩产", "订单"]
NEGATIVE_WORDS = ["下滑", "亏损", "减少", "预警", "下降", "失败", "降低"]

def extract_keywords(text: str, top_k=20) -> List[str]:
    return jieba.analyse.extract_tags(text, topK=top_k)

def judge_sentiment(keywords: List[str]) -> str:
    positive_score = negative_score = 0

    for word in keywords:
        if word in POSITIVE_WORDS:
            positive_score += 1
        elif word in NEGATIVE_WORDS:
            negative_score += 1

    if positive_score > negative_score:
        return "利好"
    elif positive_score < negative_score:
        return "利空"
    else:
        return "中性"

def print_text_sentiment(text: str) -> None:
    key_words = extract_keywords(text)
    print("key_words:")
    print(key_words)
    sentiment = judge_sentiment(key_words)
    print("公告性质：", sentiment)

if __name__ == "__main__":
    text1 = "公告显示，公司营收同比增长30%，利润创新高，未来将保持稳定向好趋势"
    print_text_sentiment(text1)

    article_url = "https://stock.10jqka.com.cn/20251209/c673062866.shtml"
    text2 = text_extract(article_url)
    print_text_sentiment(text2)