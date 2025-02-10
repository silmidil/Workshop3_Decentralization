from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np
import pickle
import random

app = Flask(__name__)

iris = load_iris()
X = iris.data
y = iris.target
seed=random.randint(0,4096)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.90, random_state=seed)

scaler=StandardScaler()
X_train = scaler.fit_transform(X_train)  
X_test = scaler.transform(X_test)  

model = DecisionTreeClassifier(random_state=seed)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Précision du modèle : {accuracy:.2f}') 

model_pickle = pickle.dumps(model)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict', methods=['GET'])
def predict():
    try:
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))

        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        features_scaled = scaler.transform(features)


        prediction = model.predict(features_scaled)
        probabilities = model.predict_proba(features_scaled).tolist()[0]
        predicted_class = int(prediction[0])

        response = {
            "class_name": "Iris-" + ["setosa", "versicolor", "virginica"][predicted_class],
            "probabilities": probabilities
        }

        return jsonify(response)


    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5004, debug=True)
