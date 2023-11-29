# Chat node


## How to install  
To install:  
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run locally:  
```
    uvicorn chat_node.main:app --port 8001 --reload
```