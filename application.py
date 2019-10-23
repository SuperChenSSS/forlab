#!/usr/bin/env python3
 
import argparse
import asyncio
import logging
import websockets
import time
import config as cnf
import http
 
#from pymongo import MongoClient
#from azure.eventhub import EventHubClient, Sender, EventData
 
logging.basicConfig(
    #filename='app.log',
    #filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger(__name__)
logging.getLogger('websockets').setLevel(logging.INFO)
logging.getLogger('asyncio').setLevel(logging.INFO)
 
#from data_handler.binary import DataHandlerBinary
 
DEFAULT_PORT=8000
#testing
#Event Hub Connection Establishment
#event_client = EventHubClient(cnf.EVENT_HUB_CONFIG['address'], debug=False, username=cnf.EVENT_HUB_CONFIG['user'], password=cnf.EVENT_HUB_CONFIG['key'])
#event_sender = event_client.add_sender()
#event_client.run()
 
async def process_request(path, request_headers):
    if request_headers.get('Connection', '').lower() == 'upgrade':
        return None
    return http.HTTPStatus.OK, [], b'OK'
 
def server(host, port):
    #dataHandler = DataHandlerBinary(event_sender, db)
    async def process(websocket, path):
        
        try:
            async for message in websocket:
                result = 'fail'
                
                response = "{}" #dataHandler.save(message)
                #logger.info(f'response {response}')
                #if not result:
                #    logger.warning(f'failed to save data')
                #    items = []
                #    for index in range(0, len(message)):
                #        items.append(f'{message[index]:02x}')
                #    message_text = ' '.join(items)
                #    logger.warning(f'message: {message_text}')
                #except Exception as e:
                #logger.error(f'failed to parse message {e}')
                await websocket.send(response)
        except Exception as e:
            logger.error(f'error: {e}')
        
 
    logger.debug(f'listening on host {host} port {port}')
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(process, host, port, process_request=process_request))
 
    asyncio.get_event_loop().run_forever()
 
def main():
 
    parser = argparse.ArgumentParser(description='WebSocket Server for Fitbit.')
    parser.add_argument('-p', '--port',
        help=f'Port number to listen on. Default {DEFAULT_PORT}',
        default=DEFAULT_PORT
    )
 
    #db = None
    #mongodb = MongoClient(cnf.EVENT_HUB_CONFIG['mongo_uri'])
    #db = mongodb[cnf.EVENT_HUB_CONFIG['db_name']]
 
    args = parser.parse_args()
    server('0.0.0.0', args.port)
 
if __name__ == '__main__':
    main()
