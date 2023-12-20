from flask import Flask, request, jsonify


from helper.openai_api import text_complition


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/dialogflow/es/receiveMessage', methods=['POST'])
def esReceiveMessage():
    try:
        data = request.get_json()
        # Вы можете использовать это действие, чтобы делать разные вещи
        # action = data['queryResult']['action']
        query_text = data['queryResult']['queryText']

        result = text_complition(query_text)

        if result['status'] == 1:
            return jsonify(
                {
                    'fulfillmentText': result['response']
                }
            )
    except:
        pass
    return jsonify(
        {
            'fulfillmentText': 'Something went wrong.'
        }
    )


@app.route('/dialogflow/cx/receiveMessage', methods=['POST'])
def cxReceiveMessage():
    try:
        data = request.get_json()
        # Используйте этот тег, чтобы выбрать действие
        # tag = data['fulfillmentInfo']['tag']
        query_text = data['text']

        result = text_complition(query_text)

        if result['status'] == 1:
            return jsonify(
                {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [result['response']],
                                    'redactedText': [result['response']]
                                },
                                'responseType': 'HANDLER_PROMPT',
                                'source': 'VIRTUAL_AGENT'
                            }
                        ]
                    }
                }
            )
    except:
        pass
    return jsonify(
        {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': ['Something went wrong.'],
                            'redactedText': ['Something went wrong.']
                        },
                        'responseType': 'HANDLER_PROMPT',
                        'source': 'VIRTUAL_AGENT'
                    }
                ]
            }
        }
    )
