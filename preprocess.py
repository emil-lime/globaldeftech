from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

def clean(text):

    """
    REMOVES PRONOUNS AND NAMES FROM TEXT TO REDUCE BIAS
    """

    pronouns = ["mən", "sən", "sen", "o", "onlar", "bu", "biz", "menim", "mənim",
            "bizim", "senin", "sənin", "onun", "onların", "onlarin", "sizin", 
            "niyə", "niye"]

    names = ["rəhim", "ilham", "rehim", "eliyev", "aliyev", "əliyev", "ilhamin",
            "ilhamın"]

    if isinstance(text, str):
        text = text.lower()
        text = text.replace("w", "ş")
        text = text.replace("sh", "ş")
        text = text.replace(",", " ")
        text = text.replace(".", " ")
        text = text.split(" ")
        for word in text:
            if word in names or word in pronouns:
                text.remove(word)
            elif word in ("yasasin", "yaşasin", "yashasin", "yashasın"):
                text[text.index(word)] = "yaşasın"
            elif word in ("azerbaycan", "azerbaijan"):
                text[text.index(word)] = "azərbaycan"
        
        return text

def remove_blanks(corpus):

    """
    REMOVES UNWANTED BLANK SPACES FROM TEXT
    """

    clean_text = []
    for sentence in corpus:
        temp = []
        for word in sentence:
            if word:
                temp.append(word)
        clean_text.append(temp)

    return clean_text

def tokenize(text):

    """
    TURNS TEXT INTO VECTOR
    """

    num_words = 1500
    oov_token = '<UNK>'
    pad_type, trunc_type = 'post', 'post'

    tokenizer = Tokenizer(num_words=num_words, oov_token=oov_token, char_level=False,
                        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
    
    tokenizer.fit_on_texts(text)

    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(text)

    maxlen = 50 #max([len(x) for x in train_sequences])

    train_padded = pad_sequences(train_sequences, padding=pad_type, truncating=trunc_type, maxlen=50)

    return (word_index, maxlen, train_padded)

def one_hot_encoding(labels):
    encoded = to_categorical(labels, num_classes=3)
    return encoded
    