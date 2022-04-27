from flask import Flask, request
from .utils import get_ndvi_tseries
import descarteslabs as dl
import os.path as osp
from joblib import load

app = Flask(__name__)

@app.route("/getclass", methods=["POST", "GET"])
def get_field_class():
    content = request.json
    print(f"Recieved request: {content}")
    
    geom = content["geometry"]
    if "fid" in content.keys():
        fid = content["fid"]
    else:
        fid = ""
    
    print("Loading classifier")
    if not osp.exists("../models/classifier.joblib"):
        print("Classifier not found locally. Pulling from dl.Storage")
        dl.storage.get_file("classifier.joblib", "../models/classifier.joblib")
        
    clf = load("../models/classifier.joblib")
    
    print("Retrieving timeseries")
    ndvi_ts, ndvi_dates = get_ndvi_tseries(geom)
    
    result = {
        "class": clf.predict(ndvi_ts.reshape(1,-1))[0], 
        "fid": fid
    }
    
    return result