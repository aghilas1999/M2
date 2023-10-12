Image classification using a deep learning model.

To start the server, type this command in the /scripts directory:

```bash
python app.py
```
In another terminal, you can interact with the server by retrieving images and their predictions.

```bash
data\raw>curl -X POST -F "image=@Dataset/chest_xray/test/NORMAL/IM-0083-0001.jpeg" http://localhost:5000/predict
```

