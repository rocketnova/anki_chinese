#!/usr/bin/env python
"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
See https://cloud.google.com/translate/docs/basic/translating-text
"""
from google.cloud import translate_v2
import six
import logging
import html

def trans(text, target):
    translate_client = translate_v2.Client()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    logging.debug(u'Text: {}'.format(result['input']))
    logging.debug(u'Translation: {}'.format(result['translatedText']))
    logging.debug(u'Detected source language: {}'.format(result['detectedSourceLanguage']))

    return html.unescape(result['translatedText'])
