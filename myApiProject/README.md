Prior to running the program, you will need to install the following:
	Python3: https://www.python.org/downloads/
	Django: https://www.djangoproject.com/download
	Django Rest Framework: https://www.django-rest-framework.org/#installation

Follow the specific instruction for your chosen OS prior to running the API.
To run the API, you will first need to download it. After download, you will use your command line or terminal to navigate to the myApiProject 
directory. You will then enter the following commands:

	python manage.py makemigrations
	python manage.py migrate
    python manage.py runserver
    
These commands will initialize your server and run it. After the server is running, you can use Postman to make queries and access the API. 
In Postman, you will enter http://localhost:8000/api/v1/*tablename*/ to access a specific table, replacing tablename with the name of the table. To generate a token, you will need to change the request to a Post request. You will need to post to the url: http://localhost:8000/api/v1/api-token-auth/. If you are already authenticated, it will create you an auth-token. You will include this in the header of all your requests. 
For additional detail on security user instructions (including testing user groups), please refer to the READ_ME_Project_Security_Testing.pdf file in the source code zip file
