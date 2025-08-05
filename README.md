```
curl --location 'http://localhost:8000/chat' \
--header 'Content-Type: application/json' \
--data '{
    "message": "I have headache",
    "session_id": "702c86dc-af94-4972-a195-a95d3811fcc5"
}'
```


uvicorn main:app --reload