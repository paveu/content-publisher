# Elastic Beanstalk Django

Launching a Django Project on Amazon Web Services (AWS) Elastic Beanstalk.


1. Setup Virtual Environment, GIT, & Django.
	**Create Virtualenv**
	```
	virtualenv content-publisher
	```
	
	**Activate Virtualenv** 
	`source bin/activate`

	**git clone project**
	```
	git clone https://github.com/paveu/content-publisher.git tmp && mv tmp/.git . && rm -rf tmp && git reset --hard
	```
	
	**Install pip packages**
	```
	sudo pip install -r requirements.txt
	```
		
	__Test installation__
	
	```
	eb --version
	```
	
	**Returns** something like 
	```
	EB CLI 3.6.1 (Python 2.7.9)
	```

2. **Create AWS User Credentials**
	
	1. Navigate to [IAM Users](https://console.aws.amazon.com/iam/home?#users)
	
	2. Select `Create New Users`
	
	3. Enter `awsbean` as a username (or whatever you prefer)
	
	4. Ensure `Generate an access key for each user` is **selected**.
	
	5. Select `Download credentials` and keep them safe. 
	
	6. Open the `credentials.csv` file that was just downloaded/created 

	7. Note the `Access Key Id` and `Secret Access Key` as they are needed for a future step. These will be referred to as `<your_access_key_id>` and `<your_secret_access_key>`


3. **Create Elastic Beanstalk Application via Command Line (aka Terminal/Command Prompt)**
	** Ensure virtualenv is activated **
	```
	cd /path/to/root/of/your/virtualenv/
	source bin/activate # if Mac/Linux
	.\Scripts\activate * if Windows
	```
	Initialize EB:

	```
	eb init 
	```

	Here's what we did. If you don't see this questions don't worry config.yml had been already set up for you.
	```
		Select a default region
		1) us-east-1 : US East (N. Virginia)
		2) us-west-1 : US West (N. California)
		3) us-west-2 : US West (Oregon)
		4) eu-west-1 : EU (Ireland)
		5) eu-central-1 : EU (Frankfurt)
		6) ap-southeast-1 : Asia Pacific (Singapore)
		7) ap-southeast-2 : Asia Pacific (Sydney)
		8) ap-northeast-1 : Asia Pacific (Tokyo)
		9) sa-east-1 : South America (Sao Paulo)
		10) cn-north-1 : China (Beijing)
		(default is 3): 5               # this is my answer

		You have not yet set up your credentials or your credentials are incorrect
		You must provide your credentials.
		(aws-access-id): <your_access_key_id>
		(aws-secret-key): <your_secret_access_key>

		Select an application to use
		1) [ Create new Application ]
		(default is 1): 1                # We created a new one

		Enter Application Name
		(default is "content-publisher"):           # We pressed enter to use the default
		Application content-publisher has been created.

		Select a platform.
		1) Node.js
		2) PHP
		3) Python
		4) Ruby
		5) Tomcat
		6) IIS
		7) Docker
		8) Multi-container Docker
		9) GlassFish
		10) Go
		11) Java
		(default is 1): 3                  # Select 3 for Python.

		Select a platform version.
		1) Python 3.4
		2) Python
		3) Python 2.7
		4) Python 3.4 (Preconfigured - Docker)
		(default is 1): 3					# Select 3 for 2.7 if that is what you use locally
		Do you want to set up SSH for your instances?
		(y/n): y                            # Optional, not needed at this point.

		Select a keypair.
		1) aws-eb
		2) aws-eb2
		3) [ Create new KeyPair ]           # If you said yes to SSH, this is required.
	```

4.	**Create Elastic Beanstalk** 
	```
	eb create
	```

5.	**Configuring our Python environment** 
	Configuring our Python environment
	```
	eb config
	```
	This command will open your default editor, editing a configuration file called .elasticbeanstalk/iod-test.env.yml. This file doesn’t actually exist locally; eb pulled it down from the AWS servers and presented it to you so that you can change settings in it. If you make any changes to this pseudo-file and then save and exit, eb will update the corresponding settings in your Beanstalk environment.
	If you search for the terms ‘WSGI’ in the file, and you should find a configuration section that looks like this:
	```
	aws:elasticbeanstalk:container:python:
    NumProcesses: '1'
    NumThreads: '15'
    StaticFiles: /static/=static/
    WSGIPath: src/srvup/wsgi.py
	```
	
6.	**Configuring a Database** 
	```
	eb open
	```
	This command will show the deployed application in your default browser. You should see a connection refused error:
	```	
	OperationalError at /
	could not connect to server: Connection refused
    Is the server running on host "localhost" (127.0.0.1) and accepting
    TCP/IP connections on port 5432?
	```
	
7.	**Database setup** 

	From there, do the following:

    1. Click the Configuration link.
    2. Scroll all the way to the bottom of the page, and then under the “Data Tier” section, click the link “create a new RDS database”.
    3. On the RDS setup page change the “DB Engine” to “postgres”.
    4. Add a “Master Username” and “Master Password”.
    5. Save the changes.

8.	**Setup shell environment settings** 
    1. Click the Configuration link.
    2. Select 'Software Configuration' and edit
    3. Scroll down to 'Environment Properties' and add following env vars:
 ```
	AWS_ACCESS_KEY_ID=''
	AWS_SECRET_ACCESS_KEY=''
	DJANGO_SECRET_KEY=''
	EMAIL_USERNAME=''
	EMAIL_PASSWORD=''
	CONFIG_ENV='AWS_ELASTIC_BEANSTALK'
```

9. **Django Production `settings.py`:**
	* These credentials are needed for deployment* 
	* In many cases, you will have a `production` version of your `settings.py` instead of the default `Django` install.


	```
	AWS_ACCESS_KEY_ID = "<your_access_key_id>"
	AWS_SECRET_ACCESS_KEY = "<your_secret_access_key>"
	```

	```
	if 'RDS_DB_NAME' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
        }
	```

10 **Handling database migrations**

	1. Add a new file called `02_python.config ` in `.ebextensions` with contents of:
	```
	container_commands:
	  01_migrate:
	    command: "source /opt/python/run/venv/bin/activate && python iotd/manage.py migrate --noinput"
	    leader_only: true
	  02_createsu:
	    command: "source /opt/python/run/venv/bin/activate && python iotd/manage.py createsu"
	    leader_only: true
	  03_collectstatic:
	    command: "source /opt/python/run/venv/bin/activate && python iotd/manage.py collectstatic --noinput"
	```
	2. Commit in git:
	```
	git add .ebextensions/
	git commit -m "Created EB Extensions"
	```

11. **1st Deploy to Elastic Beanstalk**
	Do Deployment:
	```
	eb deploy
	```
11. **configuring socialapp**
	After you deploy you'll get Server Error 500, then you'll have to go to <you're location>.elasticbeanstalk.com/admin/ and fill in social aps. and site

