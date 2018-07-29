from operator import itemgetter
from utilities.async_encryptor import AsyncEncryptor
from utilities.word_hasher import WordHasher
from stop_words import get_stop_words


class WordCounter(object):
    @staticmethod
    def get_sorted_and_hashed_word_count_list(text, select_size=100, url=''):
        """

        :param text:
        :param select_size:
        :param url:
        :return:
        """
        ''' hash words, encrypt them, sort them and return counter as required. '''

        # Cleaning text and lower casing all words
        for char in '()*#~!$^&_+=[]{}\\"/:;|<>?%-.,\'\n",':
            text = text.replace(char, '')
        text = text.lower()
        word_list = text.split()
        word_count_dict = {}

        # counting number of times each word comes up in list of words
        for word in word_list:
            if word not in word_count_dict.keys():
                word_count_dict[word] = 1
            else:
                word_count_dict[word] += 1

        word_count_list = []
        data_list_for_template = []
        cipher = AsyncEncryptor.generate_keys()
        stop_words = get_stop_words('en')
        for each_word in word_count_dict.keys():
            if each_word not in stop_words:

                newdata = dict({
                    'text': each_word,
                    'size': word_count_dict[each_word],
                    'saltedhash': WordHasher.hash(each_word), # hash word
                    'url': url,
                    'encryptedword': AsyncEncryptor.encrypt_message(each_word, cipher) # encrypt word
                })

                word_count_list.append(newdata)

        # sort words by count
        sorted_word_count_list = sorted(word_count_list, key=itemgetter('size'), reverse=True)[0:select_size]

        for each_word in sorted_word_count_list:
            data = dict({
                'text': each_word['text'],
                'size': each_word['size'],
                'saltedhash': each_word['saltedhash'],
                'url': each_word['url']
            })

            data_list_for_template.append(data)

        return sorted_word_count_list, cipher, data_list_for_template