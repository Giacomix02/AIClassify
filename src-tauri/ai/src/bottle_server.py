from bottle import run, route, get, post, request, FormsDict, response
from joblib import load
from sklearn.pipeline import Pipeline as Pipeline
from json import dumps as jsondump
from CSP_main import run_csp

# decidere se avere cambiamenti del server in real-time mentre si modifica il .py (True)
DEBUG = False

# decidere se usare direttamente il modello presettato (True) o obbligare l'utente a caricare il modello
CUSTOM = False

model_pipeline: Pipeline = None if CUSTOM else load("./ai/src/dump/model.joblib")


###################### metodi e classi di supporto
def list_to_dict(processing: list) -> dict:
    i = 0
    dictionary = dict()
    while i < len(processing):
        dictionary[i] = processing[i]
        i += 1
    return dictionary


###################### metodi per le richieste al server

@route("/load_model")
def load_server():
    global model_pipeline
    model_Pipeline = load('./ai/src/dump/model.joblib')  # official model
    if model_pipeline is not None:
        return "model Loaded"


@post("/predict")  # predict ufficiale
def predict_post():
    global model_pipeline
    submitted = request.query["text"]  # ricevo il testo per cui fare la prediction

    lover_limit_request = request.query["lower_limit"] # ricevo il limite minore per il filtro (opzionale)
    upper_limit_request = request.query["upper_limit"]  # ricevo il limite superiore per il filtro (opzionale)

    lower_limit = None
    upper_limit = None

    if(lover_limit_request != ""):
        lower_limit = int(lover_limit_request)
    if(upper_limit_request != ""):
        upper_limit = int(upper_limit_request)


    if submitted is None:
        return "no text"

    prediction = model_pipeline.predict_proba([submitted])  # faccio la previsione, ricevendo un numpy ndarray

    prediction = prediction[0]
    prediction_list = prediction.tolist()  # converto l'ndarray interno in una lista

    prediction_float = []  # riceverà i valori della prediction convertiti in float
    for pred in prediction_list:
        pred = float(pred)*100
        pred = round(pred, 2)
        prediction_float.append(pred)

    if lower_limit is not None or upper_limit is not None:  # se uno o più dei limiti sono specificati
        returned = run_csp(prediction_float,  # effettuo la ricerca dei valori entro i limiti inseriti
                           lower_limit=lower_limit,
                           upper_limit=upper_limit)
        # il risultato di run_csp sarà una tupla composta da: variabili di csp e risultati della computazione
        results: dict = returned[1]  # prendo i risultati
        variables: set = returned[0]  # prendo le variabili del csp, per interrogare i risultati dopo

        to_return: dict = {}  # dizionario che conterrà solo i risultati entro i limiti specificati
        while len(variables) != 0:  # fino a che ci sono variabili
            var_v = variables.pop()  # prendo il valore
            var_x = variables.pop()  # e il numero x associato al valore, esso determina se il valore è da scartare o no
            if results[var_x] == 1:  # se il numero x è 1, non va scartato
                number = int(str(var_x)[1])  # prendo il numero
                to_return[number] = results[var_v]  # lo aggiungo al dizionario da ritornare
    else:  # nel caso in cui non specifico limiti
        to_return: dict = list_to_dict(prediction_float)  # converto la lista della prediction in un dizionario

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    # il codice qui sopra serve per permettere la comunicazione tra interfaccia e server

    return jsondump(to_return)  # ritorno il json dei risultati all'interfaccia


################### i metodi dichiarati sotto servono per debug
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


@post("/predict_form")
def predict_post():
    global model_pipeline

    submitted: FormsDict = request.forms.get('prediction')  # se mandato via forms

    prediction = model_pipeline.predict_proba([submitted])

    prediction = prediction[0]

    prediction_list = prediction.tolist()
    prediction_integer = []
    for pred in prediction_list:
        pred = float(pred)
        pred *= 100
        pred = round(pred, 2)
        prediction_integer.append(pred)
    returned = run_csp(prediction_integer,
                       lower_limit=None, upper_limit=None)
    results: dict = returned[1]
    variables: set = returned[0]
    to_return: dict = {}
    while len(variables) != 0:
        var_v = variables.pop()
        var_x = variables.pop()
        if results[var_x] == 1:
            number = int(str(var_x)[1])
            to_return[number] = results[var_v]

    return jsondump(to_return)


run(host='localhost', port=8080, debug=True, reloader=True if DEBUG else None)
