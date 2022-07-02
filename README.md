# aws-cat-homework

This project is a little assignment for a coding showcase to demonstrate how a simple event driven python application hosted in the AWS cloud would work, several points to take into consideration on the datapipe of this repo:

* There is a public AWS bucket containing top 250 movies: https://top-movies.s3.eu-central-1.amazonaws.com/Top250Movies.json from which I get some movie data
* This will be a two-step process:
    1. Get the data, obtain the top ten movies, and send a message to the second process
    2. Receive message, enrich it with data from the OMDb API and finally save the enriched data in a private owned bucket

The AWS services that will be used for this little showcase are the following:

* S3
* SNS
* SQS
* Lambda
* CloudFormation
* SSM secure parameters
* Event Bridge Rule for triggering one of the lambdas daily


You need to install the following dependencies

* aws cli (you can verify your installation running "aws --version")
* aws sam (you can verify your installation running "sam --version")
* python 3.* (preferably you can use a virtual environment to make life better :) )
* Some code editor of your preference (not strictly necessary but we don't live in the ice age anymore :D )

From your AWS account you will need the following to be able to configure this project:

* A user with the relevant privileges to be able to run sam, specifically you will need:
  * Access key ID
  * Access key Secret
* Before you start configuring you got to decide which AWS region you will use (Important to note that this is configured also in the template and should be the same that you configure in the AWS cli)
* Configure the aws cli in your local environment, to do this just run "aws configure"
* Get a kms key from you AWS account to be able to decrypt our secure parameters :) we don't like to hard code anything sensible in our code (for this specific case I use it to protect an API key)

To be able to deploy the code use the magic of cloud formation by running the following:

sam build  --template template.yaml
sam deploy --stack-name cat-lambda-deploy --s3-bucket cat-aws-lambda-deploy --region eu-central-1 --no-confirm-changeset --capabilities "CAPABILITY_IAM"


What to Improve in the future:
* Get some testing 
* There are some parameter that could be also in the AWS parameter store
* Create some specific long-lasting roles in the cloud formation template instead of those in-line policies there
* Create some more parameters in the cloud formation template instead of having them directly in the resources
* ... any other thing that could come from valuable feedback ...
