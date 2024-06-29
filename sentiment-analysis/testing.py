import pickle
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize
    stop_words = stopwords.words('english')
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords

    lemmatize = WordNetLemmatizer()
    lemmatized_words = [lemmatize.lemmatize(token) for token in tokens]  # Lemmatize

    return ' '.join(lemmatized_words)

def predict_sentiment(text):
    with open('sentiment-analyzer.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)

    cleaned_text = clean_text(text)
    text_vec = vectorizer.transform([cleaned_text])
    prediction = model.predict(text_vec)

    return prediction

# Test the prediction function
test_text = "I Love this product!"
print(predict_sentiment(test_text))