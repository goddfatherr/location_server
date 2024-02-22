# Location Server
Implementation of the location engine. The server recieves fingerprints from nodes and returns a location estimated computed from the pretrained KNN-model.This is a common component for the wireless localization applications. 


## Dependencies
- python version used in development: 3.12.1

- sklearn
- joblib
- websockets
- pandas


## Setting Up 
1. Install dependencies
```
pip install scikit-learn==1.3.2
pip install joblib
pip install websockets
pip install pandas
```

2. The server needs a copy of the location map in the following format and stored in a db file named `devdb.db` in the `/server directory`. This is used for resolving location queries.  

3. Run Server
Example Output
```
PS server> py ws_server.py
WebSocket Server running at ws://112.16.0.2:80
```

## Notes
scikit-learn version (v1.3.2) used for developing the model should be the same as the one used in unpickling on the server to avoid risk of breaking the code. 



