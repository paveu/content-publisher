### GET TOKEN for JWT Authentication ###
curl -X POST -d "username=paveu&password=123" http://127.0.0.1:8000/api/auth/token/
{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzU2NDEyMjd9.5oketGtnvxivf6cdMM_daIB_OIOvovzUEZpZ-EUNvOA"}

### JWT AUTH NOT PROVIDED ###
curl -X POST -d "text='Some text'" http://127.0.0.1:8000/api/comments/.json
{"detail":"Authentication credentials were not provided."}

### User field not provided ###
curl -X POST -d "text='Some text'" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"user":["This field is required."]}

## User must be pk id not a user name ###
curl -X POST -d "text='Some text'&user='paveu'" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"user":["Incorrect type. Expected pk value, received unicode."]}

### Comment has been created with ID equals to 129 ###
curl -X POST -d "text='Some text'&user=1" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"url":"http://127.0.0.1:8000/api/comments/129/.json","id":129,"replies":[],"user":1,"text":"'Some text'"}

### Deleting comment with ID 129 ###
curl -X DELETE http://127.0.0.1:8000/api/comments/129/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
# return null_flag

### Checking whether comment is deleted or not ###
curl -X GET http://127.0.0.1:8000/api/comments/129/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"detail":"Not found."}

### Adding comment to VIDEO entry. Video field must be URL not its ID name ###
curl -X POST -d "text='Some text'&user=1&video=7" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"video":["Invalid hyperlink - No URL match."]}

### Comment has been added to the video ###
curl -X POST -d "text='great video comment'&user=1&video=http://127.0.0.1:8000/api/videos/7/" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"url":"http://127.0.0.1:8000/api/comments/134/.json","id":134,"replies":[],"user":1,"video":"http://127.0.0.1:8000/api/videos/7/.json","text":"'great video comment'"}

### Adding child comment to its parent comment with id=134 ###
curl -X POST -d "text='great video comment CHILD CHILD'&user=1&parent=http://127.0.0.1:8000/api/comments/134/" http://127.0.0.1:8000/api/comments/.json -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzI5Njc2OTB9.sNOCSV6H89XOoWHVqTVGqet2btbFbPb5U_zT1tAheWg"
{"url":"http://127.0.0.1:8000/api/comments/137/.json","id":137,"replies":[],"parent":"http://127.0.0.1:8000/api/comments/134/.json","user":1,"video":null,"text":"'great video comment CHILD CHILD'"}


# API 2 with CBViews
curl -X POST -d "text='great video comment CHILD CHILD'&user=1&parent=http://127.0.0.1:8000/api/comments/134/" http://127.0.0.1:8000/api2/categories/abc/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzMwNTMzODl9.vbe79XMAtY2iFZFOUDei-Oi2jxIdVHevOR0zpK1XF2E"
{"detail":"Method \"POST\" not allowed."}

curl -X DELETE -d "text='great video comment CHILD CHILD'&user=1&parent=http://127.0.0.1:8000/api/comments/134/" http://127.0.0.1:8000/api2/categories/abc/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzMwNTMzODl9.vbe79XMAtY2iFZFOUDei-Oi2jxIdVHevOR0zpK1XF2E"
{"detail":"Method \"DELETE\" not allowed."}

curl -X PUT -d "text='great video comment CHILD CHILD'&user=1&parent=http://127.0.0.1:8000/api/comments/134/" http://127.0.0.1:8000/api2/categories/abc/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzMwNTMzODl9.vbe79XMAtY2iFZFOUDei-Oi2jxIdVHevOR0zpK1XF2E"
{"detail":"Method \"PUT\" not allowed."}

curl -X GET http://127.0.0.1:8000/api2/categories/abc/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzMwNTMzODl9.vbe79XMAtY2iFZFOUDei-Oi2jxIdVHevOR0zpK1XF2E"

curl -X PUT -d "text='YET ANOTHER AWESOME NEW  COMMENT'" http://127.0.0.1:8000/api2/comment/134/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzU2NDEyMjd9.5oketGtnvxivf6cdMM_daIB_OIOvovzUEZpZ-EUNvOA"
{"id":134,"user":"paveu","text":"'YET ANOTHER AWESOME NEW  COMMENT'"}

curl -X DELETE http://127.0.0.1:8000/api2/comment/134/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzU2NDEyMjd9.5oketGtnvxivf6cdMM_daIB_OIOvovzUEZpZ-EUNvOA"
{"detail":"Method \"DELETE\" not allowed."}

curl -X DELETE http://127.0.0.1:8000/api2/comment/131/ -H "Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InBhdmV1IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhc2RAbzIucGwiLCJleHAiOjE0MzU2NDEyMjd9.5oketGtnvxivf6cdMM_daIB_OIOvovzUEZpZ-EUNvOA"
{"detail":"You do not have permission to perform this action."}