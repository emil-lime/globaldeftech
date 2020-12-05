from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Embedding, Conv1D, Flatten, Dense
import pandas as pd
from preprocess import clean, remove_blanks, tokenize, one_hot_encoding

df = pd.read_csv("ALL_COMMENTS - Sheet1.csv")
df["clean_comment"] = list(map(clean, df["comment"]))
df["clean_comment"] = remove_blanks(df["clean_comment"])
df = df.dropna(subset=['label', 'clean_comment'])
word_index, maxlen, train_padded = tokenize(df["clean_comment"])
df['clean_comment'] = [' '.join(t) for t in df['clean_comment']]
df['label'] = df['label'].astype(int)
df["label"] = [int(i) for i in df["label"]]
labels = one_hot_encoding(df["label"])

print(train_padded.shape)

def create_model():

    global word_index
    global maxlen

    """
    Creates AI Model for sentiment Analysis
    """

    max_voc = len(word_index)+1

    model = Sequential()
    model.add(Embedding(max_voc, 128, input_length=maxlen))
    model.add(Conv1D(32, 3))
    model.add(Flatten())
    model.add(Dense(3, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy',metrics='accuracy')

    return model

model = create_model()

history = model.fit(train_padded, labels, batch_size=1, epochs=4, validation_split=0.2)

model.save('polarity_class_model')