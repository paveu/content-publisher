
## Launching a Django Project on Amazon Web Services (AWS) Elastic Beanstalk.

1. Setup Virtual Environment, GIT, & Django.

	**Create Virtualenv**
	```sh
	$ pip install virtualenv
	$ virtualenv content-publisher
	```
	
	**Activate Virtualenv** 
	```sh
	$ cd content-publisher
	$ source bin/activate
	```

	**git clone project**
	```
	$ mkdir proj && cd proj
	$ git clone https://github.com/paveu/content-publisher.git .
	```
	
	**Install pip packages**
	```
	$ sudo pip install -r requirements.txt
	```
		
	**Test installation**
	
	```
	$ eb --version
	```
	
	**Returns** something like 
	```
	EB CLI 3.7.6 (Python 2.7.6)
	```

2. Create AWS User Credentials
	1. Navigate to [IAM Users](https://console.aws.amazon.com/iam/home?#users)
	2. Select `Create New Users`
	3. Enter `awsbean` as a username (or whatever you prefer)
	4. Ensure `Generate an access key for each user` is **selected**.
	5. Select `Download credentials` and keep them safe. 
	6. Open the `credentials.csv` file that was just downloaded/created 
	7. Note the `Access Key Id` and `Secret Access Key` as they are needed for a future step. These will be referred to as `<your_access_key_id>` and `<your_secret_access_key>`

3. Create Elastic Beanstalk Application via Command Line (aka Terminal/Command Prompt)

	** config.yml had been already created. Please edit below file according to your AWS settings**
	.elasticbeanstalk/config.yml

	```
	branch-defaults:
	  master:
	    environment: null
	    group_suffix: null
	  prod:
	    environment: content-publisher-prod
	  stage:
	    environment: content-publisher-stage
	    group_suffix: null
	global:
	  application_name: content-publisher
	  default_ec2_keyname: cp-eb
	  default_platform: Python 2.7
	  default_region: eu-central-1
	  profile: eb-cli
	  sc: git
	```

	**Initialize EB**

	```
	eb init 
	```

4.	**Create Elastic Beanstalk environments (stage and production)** 
	```
	eb create content-publisher-prod --instance_type t2.micro --database --database.engine postgresql --database.instance db.t2.micro 
	eb create content-publisher-stage --instance_type t2.micro --database --database.engine postgresql --database.instance db.t2.micro
	```

5. 	**Both environments WILL faill because of lack of linux environment settings. So you will have to go to your envoirments(for both production and stage) and add those varaibles to -> Configuration > Software Configuration > Environment Properties **
	```
	AWS_ACCESS_KEY_ID=''
	AWS_SECRET_ACCESS_KEY=''
	CONFIG_ENV='AWS_ELASTIC_BEANSTALK'
	DJANGO_SECRET_KEY=''
	EMAIL_PASSWORD=''
	EMAIL_USERNAME=''
	FULL_DOMAIN_NAME=''
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

