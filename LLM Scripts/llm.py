import tensorflow as tf
import numpy as np
import os
import time
import requests
from bs4 import BeautifulSoup

# Function to scrape text from a given URL
def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract text from HTML content (you may need to adjust this based on website structure)
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

# Load and preprocess text data from the web
url = 'https://example.com'
web_text = scrape_text_from_url(url)

# Concatenate web text with existing text data
text = open('your_text_data.txt', 'r').read() + ' ' + web_text

vocab = sorted(set(text))
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)
text_as_int = np.array([char2idx[c] for c in text])

# Create training examples and targets
seq_length = 100
examples_per_epoch = len(text)//(seq_length+1)
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)

# Batch size
BATCH_SIZE = 64

# Buffer size to shuffle the dataset
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

# Model parameters
vocab_size = len(vocab)
embedding_dim = 256
rnn_units = 1024
txt_speed = 50

# Define the model
def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                  batch_input_shape=[batch_size, None]),
        tf.keras.layers.LSTM(rnn_units,
                             return_sequences=True,
                             stateful=True,
                             recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model

model = build_model(vocab_size, embedding_dim, rnn_units, BATCH_SIZE)

# Compile the model
optimizer = tf.keras.optimizers.Adam()  # Define the optimizer
model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))

# Train the model
EPOCHS = 10

for epoch in range(EPOCHS):
    start = time.time()

    # Initialize the hidden state at the start of every epoch
    hidden = model.reset_states()

    for (batch_n, (inp, target)) in enumerate(dataset):
        with tf.GradientTape() as tape:
            predictions = model(inp)
            loss = tf.reduce_mean(tf.keras.losses.sparse_categorical_crossentropy(target, predictions, from_logits=True))

        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if batch_n % 100 == 0:
            print('Epoch {} Batch {} Loss {:.4f}'.format(epoch+1, batch_n, loss))

    # Save the model every 5 epochs
    if (epoch + 1) % 5 == 0:
        model.save_weights('checkpoint_{epoch}.h5'.format(epoch=epoch+1))

    print('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
    print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

model.save_weights('final_checkpoint.h5')

