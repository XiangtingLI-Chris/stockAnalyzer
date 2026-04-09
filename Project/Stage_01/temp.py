# def analyse_sentence(sentence: str) -> tuple[list[tuple[str, float]], float]:
#     tokens: list[tuple[str, float]] = []
#     negation_factor = degree_factor = 1.0
#     score = 1.0
#
#     for w in pseg.cut(sentence):
#         token_type, token_score = classify_token(w.word)
#
#         if token_type == "none":
#             continue
#         elif token_type == "negation":
#             negation_factor *= token_score
#             continue
#         elif token_type == "degree":
#             degree_factor *= token_score
#             continue
#
#         applied_score = token_score * negation_factor * degree_factor
#         tokens.append((w.word, applied_score))
#         score += applied_score
#
#         negation_factor = degree_factor = 1.0
#
#     if not tokens:
#         return [], 0.0
#
#     return tokens, score

# if __name__ == "__main__":
#     print([])
#     print([1, 2, 3, 4, 5])