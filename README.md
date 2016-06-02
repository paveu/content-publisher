# content-publisher

content-publisher is a project for selling out video content. All videos we sell are hosted on an external servers(wistia.com) and their links are embedded to a website as a iframe code. If we mark video as a premium then we can sell it out for money by using braintree and payu payment systems.

  - Heroku deyployment with AWS S3: [http://content-publisher-pro.herokuapp.com](http://content-publisher-pro.herokuapp.com/)
  - AWS Elastic Beanstalk deployment with AWS S3: [http://content-publisher-depl.eu-central-1.elasticbeanstalk.com](http://content-publisher-depl.eu-central-1.elasticbeanstalk.com/)

### Project features
  - selling premium accounts via Braintree and PayU systems
  - full user account system
  - posibility to register/login with facebook
  - full REST API for category, video and comment models
  - transaction history for braintree and payu systems
  - posibility to embed vimeo and youtube, wistia iframes
  - videos can be commented by users
  - notification when action happens
  - analytics system implemented

### Technical features
  - django 1.9.5
  - configuration for PostgreSQL 9.3 database for production
  - static and media files hosted in AWS S3 (for both AWS EB and Heroku)
  - Redis is used for celery broker in heroku
  - Amazon SQS is used for celery broker in elasticbeanstalk
  - for session caching AWS ElastiCache(Redis) is used for elasticbeanstalk
  - for session caching Redis is used for heroku
  - OAuth2 implemented along with Facebook athentication
  - django Rest Framework and JWT
  - email service via Gmail account
  - posibility to host project source code on heroku with static and media files on AWS S3 bucket
  - django-debug-toolbar implemented


### Todos
  - add Flower for monitor Celery tasks
  - fixing comment thread with angular.js - top priority
  - add fabric deployment script with filling in site id=1 for facebook socialapp
  - add celery for getting exchange rate from usd->pln. do it periodicaly and save a result to database
  - add Sentry for monitoring exepctions happen within the project
  - improving user account panel with angular.js
  - deploying project with fabric script for local/stage and production
  - braintree and payu tutorials for those who wants to run it in production mode
  - add tox, coverage, pytest
  - covering all models along with payment systems with unit and functional tests
  - exposing transaction model with REST API only for thoe users who has permision
  - add automatic resize and compress images with PIL

### Todos: Status bars
  - https://requires.io/plans/
  - https://coveralls.io
  - https://docs.travis-ci.com/user/status-images/
  - http://shields.io/ (reelase image)

### Setting up config variables and plugins

* NOTE #1: You will have to set up django secret key, use 'openssl rand -base64 64' to generate your key and export it as a linux variable. If you're running it locally keep it safe in shell .profile file.

```sh
$ export DJANGO_SECRET_KEY='' # generate new secret key for django project. you can use following command: openssl rand -base64 64
```

* NOTE #2: Create an account at gmail.com and go to google email settings and selecet "turning on access for less secure apps"[link](https://support.google.com/accounts/answer/6010255). If you are running project locally I recommend adding gmail login/pw to shell .profile file. 
```sh
$ export EMAIL_USERNAME='' 
$ export EMAIL_PASSWORD=''
```

* NOTE #3: You will have to define config enviroment, for local development please select 'local'. If you are running project locally I recommend adding it to shell .profile file:

```sh
$ export CONFIG_ENV='local' # for local development
```

### Local Installation for Python 2.7.x

	**Create Virtualenv**
	```
	$ pip install virtualenv
	$ virtualenv content-publisher
	```
	
	**Activate Virtualenv** 
	```
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
	
	**Apply migration, create user, collectstatic**
	```
  $ cd src
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python manage.py collectstatic --noinput
  $ python manage.py createsu # it will create superuser with login:admin,pw:admin
  $ python manage.py runserver
  ```

NOTE #4 For all config envoirments(local,heroku,aws eb) you will have to setup SocialApp settings. So in order to get the project up and running please add Facebook SocialApp to the the Django admin. Do following steps:
	* Go to admin http://project/admin/ page use login:admin, pw:admin and click at Sites.
	* DO NOT REMOVE example.com, just edit example.com row and change example.com domain to your current project domain.
	* Click save.
	* Go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page
	* After you filled in these four steps project should be up and running.

### Heroku Installation

[https://github.com/paveu/content-publisher/blob/master/docs/deployment_to_heroku.md](https://github.com/paveu/content-publisher/blob/master/docs/deployment_to_heroku.md)

### AWS EB Installation
Link to tutorial will be added here soon

1. add redis service with permission

2. add SQS queue with permission: https://www.calazan.com/using-amazon-sqs-with-django-and-celery/
ssh to the bean and run celery worker in a background
```sh
eb ssh
source /opt/python/run/venv/bin/activate
cd /opt/python/current/app
celery worker --workdir=src --app=srvup.celery:app --loglevel=INFO & 
```

In order to set up Celery for AWS SQS, please follow this tutorial:
http://docs.celeryproject.org/en/latest/getting-started/brokers/sqs.html

AWS troubleshooting:
https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/


### External libraries used in the project
content-publisher uses a number of open source projects to work properly:

* [braintree] - Payment system, ver: 3.25.0
* [colorama] - Cross-platform colored terminal text, ver: 0.3.7
* [Django] - The Web framework for perfectionists with deadlines, ver: 1.9.5
* [django-allauth] - Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication, ver: 0.25.2
* [django-debug-toolbar] - The Django Debug Toolbar is a configurable set of panels that display various debug information about the current request/response and when clicked, display more details about the panel's content, ver: 1.4
* [django-ipware] - Best attempt to get user's (client's) real ip-address while keeping it DRY, ver: 1.1.5
* [django-cors-headers] - A Django App that adds CORS (Cross-Origin Resource Sharing) headers to responses, ver: 1.1.0
* [django-crispy-forms] - Better formatted form template, ver: 1.6.0
* [django-filter] - Django-filter provides a simple way to filter down a queryset based on parameters a user provides, ver: 0.13.0
* [djangorestframework] - Django REST framework is a powerful and flexible toolkit for building Web APIs, ver: 3.3.3
* [djangorestframework-jwt] - JSON Web Token Authentication support for Django REST Framework, ver: 1.8.0
* [httpie] - HTTPie (pronounced aitch-tee-tee-pie) is a command line HTTP client, ver: 0.9.3
* [Markdown] - Python implementation of Markdown, ver: 2.6.6
* [Pillow] - Python Imaging Library, ver: 3.2.0
* [Pygments] - Python syntax highlighter, ver: 2.0.2
* [PyJWT] - A Python implementation of RFC 7519. Original implementation was written by @progrium, ver: 1.4.0
* [requests] - Requests is the only Non-GMO HTTP library for Python, safe for human consumption, ver: 2.9.1
* [Bootstrap] - is the most popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web, ver: 3.1.1
* [jQuery] -  is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers ver: 1.11.0

### Version
* version: 1.3
* project started in 08/may/2015. 
* code taken from my old repo: [https://github.com/paveu/srvup](https://github.com/paveu/srvup)

License
----

MIT

**Free Software, Hell Yeah!**

