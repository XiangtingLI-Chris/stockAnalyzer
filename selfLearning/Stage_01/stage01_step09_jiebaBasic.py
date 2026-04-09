import jieba
from jieba import analyse

text1 = "公司主营业务稳定增长，营收提升明显"
print(text1)
words = jieba.lcut(text1)
print(words)

text2 = "公告显示，公司营收同比增长30%，利润创新高，未来将保持稳定向好趋势"
print(text2)
key_words2 = jieba.analyse.extract_tags(text2, topK=10)
print(key_words2)

text3 = "公告显示，公司营收同比增长30%，利润创新高，未来将保持稳定向好趋势"
print(text3)
key_words3 = jieba.analyse.extract_tags(text3, topK=20, withWeight=True)
print(key_words3)