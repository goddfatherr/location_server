import joblib
import socket
import asyncio
import sqlite3
import websockets
import process_aps_online

async def server_handler(websocket, path):
    global knn_loc_algorithm

    #connect to database
    db = "devdb.db"
    connection = sqlite3.connect(db)

    while True:
        try:
            request = await websocket.recv()
            print(f"Received Request: {request}")

            process_aps_online.process_request(request)
            fingerprint = process_aps_online.construct_fingerprint_online(connection)
            fingerprint = list(fingerprint)
            
            #Guard against target being Out Of Range
            non_zero = 0
            len_fingerprint = len(fingerprint)
            for j in range(len_fingerprint):
                if fingerprint[j] != 0:
                    non_zero = non_zero + 1
            ##################################################

            
            #if non_zero < (0.1 * len_fingerprint):
            samples_thresh = 10
            #if WAP count in a fingeprint is less than this figure, no reliable inference can be run
            #return insufficient data (insuff) to the client
            if non_zero < (samples_thresh):
                message = "insuff"
                await websocket.send(message)
            else:
            #if True:
                #make predictions multiple times and pick the output class with highest occurence. 
                n_inferences = 10
                output_classes = []
                for i in range(n_inferences):
                    message = knn_loc_algorithm.predict([fingerprint])
                    output_classes.append(message)
                message = max(output_classes, key = output_classes.count)
                
                await websocket.send(message[0])
            
            print(f"Sent message back: {message}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed by the client.")
            break
        
        except websockets.exceptions.ConnectionClosedError:
            print("Ping Timeout: Connection closed")
            break

        except Exception as e:
            print("Unexpected error:", e)
            break


if __name__ == "__main__":
    #load small model: 4 distinct classes: n_neighbors = 10
    #knn_loc_algorithm = joblib.load('knn_loc_algorithm.sav')

    #load expanded model: ~ 10 distinct classes: n_neighbors = 10
    #knn_loc_algorithm = joblib.load('knn_loc_algorithmV2_10n.sav')

    #load expanded model: ~ 10 distinct classes: n_neighbors = 20
    knn_loc_algorithm = joblib.load('knn_loc_algorithmV2_20n.sav')
    
    #Get IP address of machine
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except socket.error:
        print("Unable to retrieve local IP address of this machine.")
        local_ip = None

    if local_ip:
        start_server = websockets.serve(server_handler, local_ip, 80)
        print(f"WebSocket Server running at ws://{local_ip}:80")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    else:
        print("Exiting...")

    
