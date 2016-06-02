
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

	**Initialize EB**

	```
	eb init -i
	```

	Answer on following questions according to your location and settings. Create keys with name: aws-deploy-keys

	```
	(content-publisher)pawelste:~/workspace/content-publisher/proj (master) $ eb init -i
	
	Select a default region
	1) us-east-1 : US East (N. Virginia)
	2) us-west-1 : US West (N. California)
	3) us-west-2 : US West (Oregon)
	4) eu-west-1 : EU (Ireland)
	5) eu-central-1 : EU (Frankfurt)
	6) ap-southeast-1 : Asia Pacific (Singapore)
	7) ap-southeast-2 : Asia Pacific (Sydney)
	8) ap-northeast-1 : Asia Pacific (Tokyo)
	9) ap-northeast-2 : Asia Pacific (Seoul)
	10) sa-east-1 : South America (Sao Paulo)
	11) cn-north-1 : China (Beijing)
	(default is 3): 5
	
	Select an application to use
	1) content-publisher
	2) content-publisher-deploy
	3) [ Create new Application ]
	(default is 3): 1
	
	It appears you are using Python. Is this correct?
	(y/n): y
	
	Select a platform version.
	1) Python 3.4
	2) Python
	3) Python 2.7
	4) Python 3.4 (Preconfigured - Docker)
	(default is 1): 3
	Do you want to set up SSH for your instances?
	(y/n): y
	```

	**config.yml had been already created. Please edit below file according to your AWS settings**
	.elasticbeanstalk/config.yml

	```
	branch-defaults:
	  master:
	    environment: content-publisher-prod
	    group_suffix: null
	  prod:
	    environment: content-publisher-prod
	  stage:
	    environment: content-publisher-stage
	    group_suffix: null
	global:
	  application_name: content-publisher
	  default_ec2_keyname: aws-deploy-keys
	  default_platform: Python 2.7
	  default_region: eu-central-1
	  profile: eb-cli
	  sc: git
	```


4.	**Create Elastic Beanstalk environments (stage and production)**

	```
	eb create content-publisher-prod
	eb create content-publisher-stage
	```
	
	In your environment/configuration/instances/EC2 key pair - check whether 'aws-deploy-keys' is used for this env(prod and stage)

5. 	**Both environments(production and stage) WILL fail because of lack of linux environment settings. So you will have to go to your envoirments(for both production and stage) and add those varaibles to -> Configuration > Software Configuration > Environment Properties**
	
	Create an account at gmail.com and go to google email settings and selecet "turning on access for less secure apps"
	
	```
	AWS_ACCESS_KEY_ID=''
	AWS_SECRET_ACCESS_KEY=''
	CONFIG_ENV='AWS_ELASTIC_BEANSTALK'
	DJANGO_SECRET_KEY='' # openssl rand -base64 64'
	EMAIL_PASSWORD='' # gmail login
	EMAIL_USERNAME='' # gmail pw
	FULL_DOMAIN_NAME='' # full domain for example: http://localhost.com
	```
	
	Wait until 'Health' turns into "OK". It may take 10-20min
	
6.	**Configuring our Python environment** 

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

7.	**Database setup** 

	From there, do the following:

    1. Go to your application i.e (content-publisher-prod or content-publisher-stage)
    2. Click the Configuration link.
    3. Scroll all the way to the bottom of the page, and then under the "Data Tier" section, click the link "create a new RDS database".
    4. On the RDS setup page change the "DB Engine” to "postgres".
    5. Add a "Master Username" and "Master Password".
    6. Save the changes.

	Wait until 'Health' turns into "OK". It may take 10-20min

8. **Django Production `settings.py`:**
	* These credentials are needed for deployment* 
	* In many cases, you will have a `production` version of your `settings.py` instead of the default `Django` install.

	It should look something like below:

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

9.	**Handling pacakages**

	* file called `01_packages.config` in `.ebextensions` with contents of:

	```
	packages:
	  yum:
	    git: []
	    postgresql93-devel: []
	    libjpeg-turbo-devel: []
	```	
	
	* file called `02_python.config ` in `.ebextensions` with contents of:

	```
	container_commands:
	  01_migrate:
	    command: "source /opt/python/run/venv/bin/activate && python src/manage.py migrate --noinput"
	    leader_only: true
	  02_createsu:
	    command: "source /opt/python/run/venv/bin/activate && python src/manage.py createsu"
	    leader_only: true
	  03_collectstatic:
	    command: "source /opt/python/run/venv/bin/activate && python src/manage.py collectstatic --noinput"
	
	option_settings:
	  "aws:elasticbeanstalk:application:environment":
	    DJANGO_SETTINGS_MODULE: "srvup.settings"
	    "PYTHONPATH": "/opt/python/current/app/src:$PYTHONPATH"
	  "aws:elasticbeanstalk:container:python":
	    WSGIPath: src/srvup/wsgi.py
	    NumProcesses: 3
	    NumThreads: 20
	```

11. **Add AWS Elasticache service with Redis**

	To be added

12. **Add AWS SQS for Celery**
	
	Tutorial how to add SQS to django project:
	https://www.calazan.com/using-amazon-sqs-with-django-and-celery/

13. **Add celery worker in the background**

	Do Staging:
	```
	eb ssh content-publisher-stage
	source /opt/python/run/venv/bin/activate
	cd /opt/python/current/app
	celery worker --workdir=src --app=srvup.celery:app --loglevel=INFO & 
	```	

	Do Production:
	```
	eb ssh content-publisher-prod
	source /opt/python/run/venv/bin/activate
	cd /opt/python/current/app
	celery worker --workdir=src --app=srvup.celery:app --loglevel=INFO & 
	```	


13. **Deploy to Elastic Beanstalk**

	Do Staging:
	```
	eb deploy content-publisher-stage
	```

	Do Production:
	```
	eb deploy content-publisher-prod
	```

14. **For all config envoirments(local,heroku,aws eb) you will have to setup SocialApp settings. So in order to get the project up and running please add Facebook SocialApp to the the Django admin. Do following steps:**

	* Go to admin http://project/admin/ page use login:admin, pw:admin and click at Sites.
	* DO NOT REMOVE example.com, just edit example.com row and change example.com domain to your current project domain.
	* Click save.
	* Go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page
	* After you filled in these four steps project should be up and running.


15. **Troubleshooting**

Don’t forget the very helpful eb ssh command, which will get you into the EC2 instance so you can poke around and see what’s going on. When troubleshooting, there are a few directories you should be aware of:

    /opt/python – Root of where you application will end up.
    /opt/python/current/app – The current application that is hosted in the environment.
    /opt/python/on-deck/app – The app is initially put in on-deck and then, after all the deployment is complete, it will be moved to current. If you are getting failures in your container_commands, check out out the on-deck folder and not the current folder.
    /opt/python/current/env – All the env variables that eb will set up for you. If you are trying to reproduce an error, you may first need to source /opt/python/current/env to get things set up as they would be when eb deploy is running.
    opt/python/run/venv – The virtual env used by your application; you will also need to run source /opt/python/run/venv/bin/activate if you are trying to reproduce an error
