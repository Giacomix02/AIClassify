from bottle import run, route, get, post, request, FormsDict, response
from joblib import load
from sklearn.pipeline import Pipeline as Pipeline
from NLTKVectorizer import NLTKVectorizer
from numpy import ndarray
from json import dumps as jsondump

# decidere se avere cambiamenti del server in realtime mentre si modifica il .py (True)
DEBUG = True

# decidere se usare direttamente il modello presettato (True) o obbligare l'utente a caricare il modello
CUSTOM = False

model_pipeline: Pipeline = None if CUSTOM else load("./ai/src/dump/model.joblib")

NLTKVectorizer = NLTKVectorizer()


###################### metodi e classi di supporto
def ndarray_to_dict(array: ndarray) -> dict:
    i = 0
    array = array[0]
    dictionary = dict()
    while i < len(array):
        dictionary[i] = array[i]
        i += 1
    return dictionary


###################### metodi per le richieste al server

@route("/load_model")
def load_server():
    global model_pipeline
    model_Pipeline = load('./ai/src/dump/model.joblib')  # official model
    if model_pipeline is not None:
        return "model Loaded"


@get("/predict_form")
def predict_get():
    global model_pipeline
    if model_pipeline is None:
        return "model not loaded"

    return '''
        <form action="/predict_form" method="post">
            input: <input name="prediction" type="text" />
            <input value="Predict" type="submit" />
        </form>
    '''


# i metodi dichiarati sopra e sotto servono come debug
@post("/predict_form")
def predict_post():
    global model_pipeline

    submitted: FormsDict = request.forms.get('prediction')  # se mandato via forms

    prediction = model_pipeline.predict_proba([submitted])

    prediction_dict: dict = ndarray_to_dict(prediction)

    return jsondump(prediction_dict)

@post("/predict")  # predict ufficiale
def predict_post():
    global model_pipeline
    submitted: FormsDict = request.query["text"]

    if submitted is None:
        return "no text"

    prediction = model_pipeline.predict_proba([submitted])

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    prediction_dict: dict = ndarray_to_dict(prediction)

    return jsondump(prediction_dict)


run(host='localhost', port=8080, debug=True, reloader=True if DEBUG else None)
