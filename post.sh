#!/bin/bash -xe

curl -X POST http://localhost:8080/comment -d '{"author": "author1", "text": "сообщение 1"}'
curl -X POST http://localhost:8080/comment -d '{"author": "author2", "text": "сообщение 2"}'