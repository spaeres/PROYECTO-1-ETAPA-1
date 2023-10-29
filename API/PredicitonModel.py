from joblib import load

class Model:

    def __init__(self):
        self.model = load("assets/tfidf_model.joblib")
        self.transform = load("assets/tfidf_transform.pkl")

    def make_predictions(self, data):
        # Se transforman los datos con el transformador de TF-IDF:
        self.transform.transform(data)
        result = self.model.predict(data)
        return result
