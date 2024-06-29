import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
import re
import pickle

dataset_path = 'sentiment-analysis\\Twitter_Data.csv'

# Reads the csv file 
df = pd.read_csv(dataset_path)

# Drop empty rows from both the columns
df.dropna(inplace=True)

# Prints first 5 rows
print(df.head())

# Labels for training
# labels = df['category']

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = stopwords.words('english')
    tokens = [word for word in tokens if word not in stop_words]
    lemmatize = WordNetLemmatizer()
    lemmatized_words = [lemmatize.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_words)

# sample_text = 'this could have happened in the following days but living happily was better'
# processed_text = clean_text(sample_text)

# print(processed_text)

df['clean_text'] = df['clean_text'].apply(clean_text)
print(df.head())

x_train, x_test, y_train, y_test = train_test_split(df['clean_text'],df['category'], shuffle=True, test_size=0.2)

vectorizer = TfidfVectorizer(max_features=10000)
x_train_vec = vectorizer.fit_transform(x_train)
x_test_vec = vectorizer.transform(x_test)

model = LogisticRegression()

model.fit(x_train_vec,y_train)

y_pred = model.predict(x_test_vec)

print(f"accuracy: {accuracy_score(y_test,y_pred)}\nclassification report: {classification_report(y_test,y_pred)}")

with open('sentiment-analyzer.pkl','wb') as model_file:
    pickle.dump(model,model_file)
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)