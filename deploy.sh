IMAGE_TAG=pdfapp:latest

Zbuduj obraz,
docker build -t $IMAGE_TAG .

Zaloguj się do ECR,
aws ecr get-login-password | docker login --username AWS --password-stdin <your_aws_account_id>.dkr.ecr.eu-central-1.amazonaws.com

Oznacz obraz ECR-em,
docker tag $IMAGE_TAG <your_aws_account_id>.dkr.ecr.eu-central-1.amazonaws.com/pdfapp:latest

Wyślij do ECR,
docker push <your_aws_account_id>.dkr.ecr.eu-central-1.amazonaws.com/pdfapp:latest

Zrestartuj usługę ECS (lub inne polecenie do wdrożenia),
aws ecs update-service --cluster pdfapp-cluster --service pdfapp-service --force-new-deployment