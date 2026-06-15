import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


df = pd.read_csv("Indian_Travel.csv")


nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


def tokenize(question):
    return word_tokenize(question.lower())

def remove_stopwords(words):
    return [w for w in words if w not in stop_words]

def detect_destination(words):
    for w in words:
        match = df[df["Destination Name"].str.contains(w, case=False, na=False)]
        if not match.empty:
            return match.iloc[0]
    return None

def detect_intent(words):
    
    if "state" in words or "where" in words:
        return "state"
    
    elif "airport" in words:
        return "airport"
    
    elif "railway" in words or "station" in words:
        return "railway"
    
    elif "category" in words or "type" in words:
        return "category"
    
    elif "attraction" in words or "famous" in words:
        return "attraction"
    
    elif "easy" in words or "difficult" in words or "accessibility" in words:
        return "accessibility"
    
    elif "region" in words:
        return "region"
    
    return None


def get_answer(destination, intent):
    
    if intent == "state":
        return destination["State"]
    
    elif intent == "airport":
        return destination["Nearest Airport"]
    
    elif intent == "railway":
        return destination["Nearest Railway Station"]
    
    elif intent == "category":
        return destination["Category"]
    
    elif intent == "attraction":
        return destination["Popular Attraction"]
    
    elif intent == "accessibility":
        return destination["Accessibility"]
    
    elif intent == "region":
        return destination["Region"]
    
    return "Sorry, information not available."


while True:
    
    question = input("Ask a question: ")
    
    tokens = tokenize(question)
    keywords = remove_stopwords(tokens)
    
    destination = detect_destination(keywords)
    intent = detect_intent(keywords)
    
    print("Tokens:", tokens)
    print("Keywords:", keywords)
    
    if destination is not None and intent is not None:
        
        answer = get_answer(destination, intent)
        
        print("Answer:", answer)
    
    else:
        print("Sorry, I couldn't understand the question.")
