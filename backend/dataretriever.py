import os
import pymongo
import json

def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    # request_json = request.get_json()
    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db = client['oceansavr']
    col = db.data
    results = []
    maxid = 0

    retjson = {}
    
    found = 0
    payload = {}

    transactions = []
        
    for x in col.find():

        tx = {}
        tx ['ts'] = x['ts']
        tx['watertemp'] = x['airtemp']
        tx['airtemp'] = x['airtemp']
        tx['ph'] = x['ph']
        tx['turbidity'] = x['turbidity']
        tx['tds'] = x['tds']
        tx['humidity'] = x['humidity']
        tx['waterlevel'] = x['waterlevel']
        location = {}
        location['lat'] = x['lat']
        location['lng'] = x['lng']
        tx['location'] = location
        

        
        

        transactions.append(tx)

    # retjson['dish'] = userid
    retjson['data'] = transactions
    # retjson['id'] = x['id']
    # retjson['name'] = x['name']
    return json.dumps(retjson)



    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
