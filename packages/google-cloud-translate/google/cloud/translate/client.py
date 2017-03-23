# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for interacting with the Google Cloud Translation API."""


import six

from google.cloud._helpers import _to_bytes
from google.cloud.client import Client as BaseClient

from google.cloud.translate._http import Connection


ENGLISH_ISO_639 = 'en'
"""ISO 639-1 language code for English."""

BASE = 'base'
"""Base translation model."""

NMT = 'nmt'
"""Neural Machine Translation model."""


class Client(BaseClient):
    """Client to bundle configuration needed for API requests.

    :type target_language: str
    :param target_language: (Optional) The target language used for
                            translations and language names. (Defaults to
                            :data:`ENGLISH_ISO_639`.)

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type http: :class:`~httplib2.Http`
    :param http: (Optional) HTTP object to make requests. Can be any object
                 that defines ``request()`` with the same interface as
                 :meth:`~httplib2.Http.request`. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    SCOPE = ('https://www.googleapis.com/auth/cloud-platform',)
    """The scopes required for authenticating."""

    def __init__(self, target_language=ENGLISH_ISO_639,
                 credentials=None, http=None):
        self.target_language = target_language
        super(Client, self).__init__(credentials=credentials, http=http)
        self._connection = Connection(self)

    def get_languages(self, target_language=None):
        """Get list of supported languages for translation.

        Response

        See:
        https://cloud.google.com/translate/docs/discovering-supported-languages

        :type target_language: str
        :param target_language: (Optional) The language used to localize
                                returned language names. Defaults to the
                                target language on the current client.

        :rtype: list
        :returns: List of dictionaries. Each dictionary contains a supported
                  ISO 639-1 language code (using the dictionary key
                  ``language``). If ``target_language`` is passed, each
                  dictionary will also contain the name of each supported
                  language (localized to the target language).
        """
        query_params = {}
        if target_language is None:
            target_language = self.target_language
        if target_language is not None:
            query_params['target'] = target_language
        response = self._connection.api_request(
            method='GET', path='/languages', query_params=query_params)
        return response.get('data', {}).get('languages', ())

    def detect_language(self, values):
        """Detect the language of a string or list of strings.

        See: https://cloud.google.com/translate/docs/detecting-language

        :type values: str or list
        :param values: String or list of strings that will have
                       language detected.

        :rtype: str or list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys

                  * ``confidence``: The confidence in language detection, a
                    float between 0 and 1.
                  * ``input``: The corresponding input value.
                  * ``language``: The detected language (as an ISO 639-1
                    language code).

                  though the key ``confidence`` may not always be present.

                  If only a single value is passed, then only a single
                  dictionary will be returned.
        :raises: :class:`ValueError <exceptions.ValueError>` if the number of
                 detections is not equal to the number of values.
                 :class:`ValueError <exceptions.ValueError>` if a value
                 produces a list of detections with 0 or multiple results
                 in it.
        """
        single_value = False
        if isinstance(values, six.string_types):
            single_value = True
            values = [values]

        query_params = []
        query_params.extend(('q', _to_bytes(value, 'utf-8'))
                            for value in values)
        response = self._connection.api_request(
            method='GET', path='/detect', query_params=query_params)
        detections = response.get('data', {}).get('detections', ())

        if len(values) != len(detections):
            raise ValueError('Expected same number of values and detections',
                             values, detections)

        for index, value in enumerate(values):
            # Empirically, even clearly ambiguous text like "no" only returns
            # a single detection, so we replace the list of detections with
            # the single detection contained.
            if len(detections[index]) == 1:
                detections[index] = detections[index][0]
            else:
                message = ('Expected a single detection per value, API '
                           'returned %d') % (len(detections[index]),)
                raise ValueError(message, value, detections[index])

            detections[index]['input'] = value
            # The ``isReliable`` field is deprecated.
            detections[index].pop('isReliable', None)

        if single_value:
            return detections[0]
        else:
            return detections

    def translate(self, values, target_language=None, format_=None,
                  source_language=None, customization_ids=(),
                  model=None):
        """Translate a string or list of strings.

        See: https://cloud.google.com/translate/docs/translating-text

        :type values: str or list
        :param values: String or list of strings to translate.

        :type target_language: str
        :param target_language: The language to translate results into. This
                                is required by the API and defaults to
                                the target language of the current instance.

        :type format_: str
        :param format_: (Optional) One of ``text`` or ``html``, to specify
                        if the input text is plain text or HTML.

        :type source_language: str
        :param source_language: (Optional) The language of the text to
                                be translated.

        :type customization_ids: str or list
        :param customization_ids: (Optional) ID or list of customization IDs
                                  for translation. Sets the ``cid`` parameter
                                  in the query.

        :type model: str
        :param model: (Optional) The model used to translate the text. The
                      only accepted values are :attr:`BASE` and :attr:`NMT`.

        :rtype: str or list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys (though not
                  all will be present in all cases)

                  * ``detectedSourceLanguage``: The detected language (as an
                    ISO 639-1 language code) of the text.
                  * ``translatedText``: The translation of the text into the
                    target language.
                  * ``input``: The corresponding input value.
                  * ``model``: The model used to translate the text.

                  If only a single value is passed, then only a single
                  dictionary will be returned.
        :raises: :class:`~exceptions.ValueError` if the number of
                 values and translations differ.
        """
        single_value = False
        if isinstance(values, six.string_types):
            single_value = True
            values = [values]

        if target_language is None:
            target_language = self.target_language
        if isinstance(customization_ids, six.string_types):
            customization_ids = [customization_ids]

        query_params = [('target', target_language)]
        query_params.extend(('q', _to_bytes(value, 'utf-8'))
                            for value in values)
        query_params.extend(('cid', cid) for cid in customization_ids)
        if format_ is not None:
            query_params.append(('format', format_))
        if source_language is not None:
            query_params.append(('source', source_language))
        if model is not None:
            query_params.append(('model', model))

        response = self._connection.api_request(
            method='GET', path='', query_params=query_params)

        translations = response.get('data', {}).get('translations', ())
        if len(values) != len(translations):
            raise ValueError('Expected iterations to have same length',
                             values, translations)
        for value, translation in six.moves.zip(values, translations):
            translation['input'] = value

        if single_value:
            return translations[0]
        else:
            return translations
