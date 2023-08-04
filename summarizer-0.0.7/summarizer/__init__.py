# -*- coding: utf-8 -*-
from .parser import Parser
from .summarizer import Summarizer


def summarize(title, text, count=3, summarizer=None):
	summarize= Summarizer()
    result = summarizer.get_summary(text, title)
    result = summarizer.sort_sentences(result[:count])
    result = [res['sentence'] for res in result]

    return result

