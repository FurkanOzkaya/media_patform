# Media Platform

[![MediaPlatform CI](https://github.com/FurkanOzkaya/media_platform/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/FurkanOzkaya/media_platform/actions/workflows/django.yml)

## API's
- [GET]  /api/v1/all-info/            
--> Retrieve all Channels, SubChannels and Contents
- [GET]  /api/v1/channel/             
--> Retrieve Channels
- [GET]  /api/v1/sub-channel/{id}     
--> Retrieve SubChannell which connected to given id
- [GET]  /api/v1/contents/{id}        
--> Retrieve Contents of given SubChannel or Channel id

## Scripts
- start.sh        
--> Make migration operations and start app.
- run_test.sh     
--> Run Unit Test
- run_coverage    
--> Run Coverage and Coverage Report
- init.sql        
--> Database creation for docker-compose
- run_pylint.sh        
--> Pylint report for repository


# [Django-Admin Commands](https://furkanozkaya.com/software-languages/python/django/django-admin-komut-olusturma/)
- generate_report   
--> Generate Rating report (report.csv)
- create_admin      
--> Create Admin User (admin, admin)


## About Generate Report

- Firstly fetched all data with all subchannel information
- Changing Model Calculating Average for each subchannel and channel
- SubChannel Calculation which doens't have subchanel is that Avg(Contents)
- Channel calculation which has contents and subchannel is  Avg(average of contents + average of subchannel)
- Generating list which contains title's and average.
- Writing to csv file.

If Channel has SubChannel and contents calculation based on this Avg(average of contents + average of subchannel) formule.
if Channel has only Contents formule is Avg(Contents).

Model Helps to calculate all average_ratings and then we just pointing it in serializer.

# Deployment

## Docker Automated

```
docker-compose up
```
Restart Backend after you see database is ready to accept connections log on console.

## Docker  Manual

Run postgresql instance


```
docker run -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 -v {your_path}:/var/lib/postgresql/data postgres
```

Build your image
```
Docker build .
```

Run Docker image
```
Docker run  --network=host {image_id}
```
you can set volumes with -v.
if you are using sqllite you can delete --network option and add -p 8000:8000.

## Manual

- Choose your database and configure settings. 

for easy integration you can uncomment sqllite configs

- Run App in VSCode Launch section. (Python: Django)


# Media and Static Files

- Media and Static Files are will create previous folder from django base folder.

# TODO

- Add Swagger support
- Insert API's
