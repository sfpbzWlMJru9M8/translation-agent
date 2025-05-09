from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk


# 首次使用时需要下载tokenizer
# nltk.download('punkt')

def calculate_english_bleu_complete(reference, candidate):
    """
    计算英文BLEU得分，可以分别计算单词和二元词的BLEU，或者组合得分
    """
    # 确保reference是列表形式
    if isinstance(reference, str):
        reference = [reference]

    # 单词分割
    def segment_unigrams(text):
        return nltk.word_tokenize(text.lower())

    # 二元词分割
    def segment_bigrams(text):
        words = nltk.word_tokenize(text.lower())
        bigrams = []
        for i in range(len(words) - 1):
            bigrams.append(words[i] + " " + words[i + 1])
        return bigrams

    # 分别处理单词和二元词
    ref_unigrams = [segment_unigrams(ref) for ref in reference]
    cand_unigrams = segment_unigrams(candidate)

    ref_bigrams = [segment_bigrams(ref) for ref in reference]
    cand_bigrams = segment_bigrams(candidate)

    # 使用NLTK计算BLEU得分
    smoothing = SmoothingFunction().method1

    # 计算单词BLEU
    unigram_bleu = sentence_bleu(ref_unigrams, cand_unigrams,
                                 weights=(1, 0, 0, 0),
                                 smoothing_function=smoothing)

    # 计算二元词BLEU
    bigram_bleu = sentence_bleu(ref_bigrams, cand_bigrams,
                                weights=(0, 1, 0, 0),
                                smoothing_function=smoothing)

    # 计算综合BLEU (可以自定义权重)
    # 这里使用0.7和0.3的权重
    combined_bleu = 0.7 * unigram_bleu + 0.3 * bigram_bleu

    return {
        'unigram_bleu': unigram_bleu,
        'bigram_bleu': bigram_bleu,
        'combined_bleu': combined_bleu
    }


# 示例
reference = ["This is a test sentence."]
candidate = "This is the test sentence."

results = calculate_english_bleu_complete(reference, candidate)
print(f"单词BLEU得分: {results['unigram_bleu']}")
print(f"二元词BLEU得分: {results['bigram_bleu']}")
print(f"组合BLEU得分: {results['combined_bleu']}")