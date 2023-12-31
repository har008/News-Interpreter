# -*- coding: utf-8 -*-
from .parser import Parser

class Summarizer(object):
        parser = Parser()
        self.parser = parser

    def get_summary(self, text, title):
        sentences = self.parser.sentences(text)
        title_words = self.parser.remove_punctations(title)
        title_words = self.parser.words(title)
        (keywords, word_count) = self.parser.get_keywords(text)

        top_keywords = self.get_top_keywords(keywords[:10], word_count)

        result = self._compute_score(sentences, title_words, top_keywords)
        result = self.sort_score(result)

        return result

    def get_top_keywords(self, keywords, word_count):
        # Add getting top keywords in the database here
        for keyword in keywords:
            article_score = 1.0 * keyword['count'] / word_count
            keyword['total_score'] = article_score * 1.5

        return keywords

    def sort_score(self, dict_list):
        return sorted(dict_list, key=lambda x: -x['total_score'])

    def sort_sentences(self, dict_list):
        return sorted(dict_list, key=lambda x: x['order'])

    def _compute_score(self, sentences, title_words, top_keywords):
        keyword_list = [keyword['word'] for keyword in top_keywords]
        summaries = []

        for i, sentence in enumerate(sentences):
            sent = self.parser.remove_punctations(sentence)
            words = self.parser.words(sent)

            feature = self._sbs(words, top_keywords, keyword_list)

            title_feature = self.parser.get_title_score(title_words, words)
            sentence_length = self.parser.get_sentence_length_score(words)
            sentence_position = self.parser.get_sentence_position_score(i, len(sentences))
            keyword_frequency = (feature) / 10.0
            total_score = (title_feature * 1.5 + keyword_frequency * 2.0 + sentence_length * 0.5 + sentence_position * 1.0) / 4.0

            summaries.append({
                'total_score': total_score,
                'sentence': sentence,
                'order': i
            })

        return summaries

    def feature(self, words, top_keywords, keyword_list):
        score = 0.0

        if len(words) == 0:
            return 0

        for word in words:
            word = word.lower()
            index = -1

        if word in keyword_list:
            index = keyword_list.index(word)

        if index > -1:
            score += top_keywords[index]['total_score']

        return 1.0 / abs(len(words)) * score


