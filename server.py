import os, uuid, json, boto3, datetime
from flask import Flask, request, jsonify, abort, Response
from jsonschema import Draft4Validator

app = Flask(__name__)

def load_file(name):
    with open(name) as f:
        data = json.load(f)
        return data

def beautify(path, instance, message, validator_value):
    if 'is not of type' in message:
        #return '\''+path[-1] +' = '  + str(instance) +'\' debe ser de tipo ' + type(validator_value)
        return 'El campo \''+path[-1] +'\' con el valor \''  + str(instance) +'\' debe ser de tipo ' + type(validator_value)
    elif 'is a required property' in message:
        return 'El campo '+message.replace('is a required property','es obligatorio')
    elif 'is too short' in message and len(instance)==0:
        return 'El campo \''+path[-1] +'\' es obligatorio'
    else:
        return message


def type(name):
    types = {'string' : 'caracter', 'number' : 'numérico'}
    if name in types:
        return types[name]

def validate(obj):
    v = Draft4Validator(schema)
    errors = []
    for error in sorted(v.iter_errors(obj), key=str):
        errors.append({'mensaje':beautify(error.path, error.instance,error.message, error.validator_value),
                        'ubicacion':'.'.join([str(elem) for elem in error.path ])})
    if len(errors) == 0:
        errors.append({'mensaje':'Recibido'})
    return errors

schema = load_file('factura.schema.json')
folder = 'XMLRecibidos'
efactura = 'EFactura'
extension = 'json'
@app.route('/FactElectronica', methods=['POST'])
def factElectronica():
    ## S3 connection
    session = boto3.Session(
        aws_access_key_id="ACCESS_KEY",
        aws_secret_access_key="SECRET",
    )
    resp = validate(request.json)
    if 'ubicacion' in resp[0]:
        return jsonify(resp)
        
    s3 = session.resource('s3')
    nit = request.json["Valorable"]["Invoice"][0]["IdentificacionEmisor"]
    fechaHora = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    s3.Bucket('BUCKET_NAME').put_object(Key=f'{folder}/{nit}/{nit}{efactura}/{nit}_{fechaHora}_{uuid.uuid4()}.{extension}', Body=json.dumps(request.json).encode('utf-8'))      
    #response = {'status': 'OK','message': 'Factura recibida.'}
    return jsonify(resp)
if __name__ == '__main__':
   app.run(debug = True, port='5002', host='0.0.0.0')