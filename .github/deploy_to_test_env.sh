#!/bin/bash

# Zmienna z tagiema
IMAGE_TAG=pdfapp:latest

# Zbuduj obraz
docker build -t $IMAGE_TAG .

# Zaloguj się do ECR
aws ecr get-login-password | docker login --username AWS --password-stdin 384782264249.dkr.ecr.eu-central-1.amazonaws.com

# Oznacz obraz ECR-em
docker tag $IMAGE_TAG 384782264249.dkr.ecr.eu-central-1.amazonaws.com/pdfapp:latest

# Wyślij do ECR
docker push 384782264249.dkr.ecr.eu-central-1.amazonaws.com/pdfapp:latest

# Zrestartuj usługę ECS (lub inne polecenie do wdrożenia)
aws ecs update-service --cluster pdfapp-cluster --service pdfapp-service --force-new-deployment
