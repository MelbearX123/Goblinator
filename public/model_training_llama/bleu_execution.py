import json
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction

def compute_sentence_bleu(reference_sentences, candidate_sentence):
    smoothie = SmoothingFunction().method4
    return sentence_bleu(reference_sentences, candidate_sentence, smoothing_function=smoothie)


def compute_corpus_bleu(references, candidates):
    smoothie = SmoothingFunction().method4
    return corpus_bleu(references, candidates, smoothing_function=smoothie)


def tokenize(sentence):
    return sentence.lower().split()


def evaluate_model(reference_json_path, predicted_json_path):
    with open(reference_json_path, 'r') as ref_file:
        reference_texts = json.load(ref_file)

    with open(predicted_json_path, 'r') as pred_file:
        predicted_texts = json.load(pred_file)

    references_tokenized = [[tokenize(ref) for ref in refs] for refs in reference_texts]
    predictions_tokenized = [tokenize(pred) for pred in predicted_texts]

    bleu = compute_corpus_bleu(references_tokenized, predictions_tokenized)
    return bleu


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate model predictions using BLEU score")
    parser.add_argument('--reference', type=str, required=True, help='path/path') #ADD YOUR PATHS
    parser.add_argument('--predicted', type=str, required=True, help='path/path') #ADD YOUR PATHS
    args = parser.parse_args()

    bleu_score = evaluate_model(args.reference, args.predicted)
    print(f"Corpus BLEU score: {bleu_score:.4f}")
