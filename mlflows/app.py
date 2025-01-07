from flask import Flask, request, jsonify
import mlflow

registry_name = 'registry_model'
model_version = '1'
stage = 'Production'
model_uri = f'models:/{registry_name}/{model_version}'
model = mlflow.pyfunc.load_model(model_uri)

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    predicts = model.predict(data['input'])
    return jsonify({'prediction':predicts.tolist()})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
