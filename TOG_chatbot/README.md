# TOG_CHATBOT

## Jupyter Notebook
```bash
jupyter notebook --allow-root --no-browser --notebook-dir=/workspaces/rag-marine-dept --port=9090 --ip=0.0.0.0
```



## How to run 

run api 

```python 
fastapi run  app/main.py --host 0.0.0.0 --port 8000
```

## How to Build and Run

### Build the Docker Image
```python
docker build -t fastapi-app .
```
### Build the Docker Image
```python
docker run -d -p 8000:80 --name fastapi-container fastapi-app
```