import re
from jieba import posseg as pseg
from vocabulary import DEGREE_ADVERB_DICT, ADJ_DICT, VERB_DICT, NOUN_DICT, NEGATION_DICT

# Split a sentence `text` to several parts
# Return an array containing every part of the sentence
def split_sentences(text: str):
    parts = re.split(r'[，；。！？]', text)
    return [s.strip() for s in parts if s.strip()]

# Search the given token `word` in vocabulary
# Return (token_type, token_value) if found
# Return ("none", 0) if not found
def classify_token(word: str) -> tuple[str, float]:
    if word in DEGREE_ADVERB_DICT:
        return "degree", DEGREE_ADVERB_DICT[word]
    if word in ADJ_DICT:
        return "adj", ADJ_DICT[word]
    if word in VERB_DICT:
        return "trend", VERB_DICT[word]
    if word in NOUN_DICT:
        return "noun", NOUN_DICT[word]
    if word in NEGATION_DICT:
        return "negation", NEGATION_DICT[word]
    return "none", 0

# Analyse the sentiment of a sentence
# Return (tokens, sentence_score) if the sentence is valuable
# Return ([], 0) otherwise
def analyse_sentence(sentence: str) -> tuple[list[tuple[str, str, float]], float]:
    # `tokens` is an array of tokens, where each token contains (token, token_type, token_score)
    tokens: list[tuple[str, str, float]] = []
    sentence_score = 1.0

    # Use pseg.cut() method to cut the sentence into several tokens
    for w in pseg.cut(sentence):
        token_type, token_score = classify_token(w.word)

        # Add the token into `tokens` if token is founded in vocabulary
        if token_type != "none":
            tokens.append((w.word, token_type, token_score))

    # Ignore sentences that only catch negation words
    only_negation = all(word_type == "negation" for word, word_type, score in tokens)
    if only_negation:
        return [], 0

    # Calculate the `sentence_score` by multiplying all found tokens
    for word, word_type, score in tokens:
        sentence_score *= score

    return tokens, sentence_score

# Analyse the sentiment of the whole article
# Return "利好" if the article is positive
# Return "利空" if the article is negative
# Return "中性" otherwise
def analyse_article(article_content: str) -> str:
    # Split the sentence by calling the function split_sentence() and count the number of sentences
    sentences = split_sentences(article_content)
    num_sentence = len(sentences)

    # Initialize analyse variables
    positive_count = negative_count = 0
    article_score = 0

    # An array of all found_tokens, where each found_tokens contains (token, token_type, token_score)
    found_tokens:  list[list[tuple[str, str, float]]] = []

    # Calculate article score by adding scores of all sentences
    for sentence in sentences:
        tokens, sentence_score = analyse_sentence(sentence)

        # Skip a sentence if no keywords are found in vocabulary
        if not tokens:
            continue

        # Add the current sentence score to the total score
        article_score += sentence_score
        found_tokens.append(tokens)

        if sentence_score > 0:
            positive_count += 1
        elif sentence_score < 0:
            negative_count += 1

    percentage = article_score / num_sentence

    if article_score == 0:
        return "中性"

    if (negative_count == 0) and (percentage >= 0.3):
        return "利好"

    if positive_count == 0:
        return "利空"

    if (negative_count > 2 * positive_count) and (percentage <= -0.2):
        return "利空"

    return "中性"