from ibm_watson_machine_learning import APIClient
import math
import PIL
from PIL import Image
import numpy as np
from flask import Flask, request, json, jsonify
import os
import requests

token = os.environ['TOKEN']
deployment_id = os.environ['DEPLOYMENT_ID']
model_deployment_endpoint_url    = f'https://cpd-cpd-instance.itzroks-666000bp6z-7yydnn-4b4a324f027aea19c5cbc0c3275c4656-0000.eu-de.containers.appdomain.cloud/ml/v4/deployments/{deployment_id}/predictions?version=2022-04-21';

def createPayload( canvas_data ):
    import numpy as np
    rgba_data = canvas_data['values'][0]
    rgba_arr  = np.asarray(rgba_data).astype('uint8')
    rgba_arr = rgba_arr.reshape(1, 28, 28,1)
    model_payload = {"input_data": [{"values" : rgba_arr.tolist()}]} 
    return model_payload

app = Flask( __name__, static_url_path='' )

port = int( os.getenv( 'PORT', 8000 ) )

@app.route('/')
def root():
    return app.send_static_file( 'index.html' )

@app.route( '/sendtomodel', methods=['POST'] )
def sendtomodel():
    try:
        print( "sendtomodel..." )
        if model_deployment_endpoint_url:
            canvas_data = json.loads(request.data)
            payload = createPayload(canvas_data)
            header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
            response_scoring = requests.post(model_deployment_endpoint_url, json=payload, headers=header, verify=False).text
            return json.dumps(json.loads(response_scoring)['predictions'][0])
        else:
            err = "Model endpoint URL not set in 'server.py'"
            print( "\n\nError:\n" + err )
            return jsonify( { "error" : err } )
    except Exception as e:
        print( "\n\nError:\n" + str( e ) )
        return jsonify( { "error" : str( e ) } )

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=port, debug=True)
