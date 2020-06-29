import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import plots
import tensorflow.compat.v1 as tf
tf.disable_eager_execution()

module_url = "https://tfhub.dev/google/universal-sentence-encoder/1?tf-hub-format=compressed"

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module(module_url)

def similarityWithUSE(messages, countries):
    similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
    similarity_message_encodings = embed(similarity_input_placeholder)
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        session.run(tf.tables_initializer())
        message_embeddings_ = session.run(similarity_message_encodings, feed_dict={similarity_input_placeholder: messages})

        corr = np.inner(message_embeddings_, message_embeddings_)
        print("correlations")

        for i in range(0,len(countries)):
            print(countries[i], corr[i])
        plots.heatmap(countries, countries, corr)

