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
  - session caching with Redis for heroku and ElastiCache Redis for AWS EB
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

* NOTE #1: If you're running project on heroku then Redis and postgres plugins must be enabled.
* NOTE #2: You will have to set up django secret key, use 'openssl rand -base64 64' to generate your key and save it as a shell variable. If you're running it locally keep it safe in shell .profile file.
```sh
$ export DJANGO_SECRET_KEY='' # generate new secret key for django project. you can use following command: openssl rand -base64 64
```
* NOTE #3: If you're running project on HEROKU or AWS ELASTIC BEANSTALK or LOCAL then you will have to set up following shell variables. Both Heroku and AWS EB have their own applcation admin control in terms of environment variables.
```sh
$ export AWS_ACCESS_KEY_ID='' # put here AWS AWS_ACCESS_KEY_ID setting
$ export AWS_SECRET_ACCESS_KEY='' #  put here AWS AWS_SECRET_ACCESS_KEY setting
```
* NOTE #4: Create an account at gmail.com and go to google email and check "turning on access for less secure apps"[link](https://support.google.com/accounts/answer/6010255). Project uses gmail account to send out emails so please fill in following environment variables:
if you are running project locally I recommend adding them to shell .profile file:
```sh
$ export EMAIL_USERNAME='' 
$ export EMAIL_PASSWORD=''
```
* NOTE #5: You will have to define main config enviroment for local, heroku or aws elastic beanstalk envoirments:
if you are running project locally I recommend adding it to shell .profile file:
```sh
$ export CONFIG_ENV='local' # for local development
```
https://dashboard.heroku.com/apps/{{app_name}}/settings
or
```sh
$ export CONFIG_ENV='HEROKU' # mainly used for heroku production, please add it to heroku env vars
```
{{ link to env vars settings to be added }}
or
```sh
$ export CONFIG_ENV='AWS_ELASTIC_BEANSTALK' # mainly used for heroku production, please add it to AWS ELASTI BEANSTALK env vars
```
### Local Installation

1. Create a Python 2.7 virtualenv
2. Install latest pip package
3. Inside virtualenv perform following commands:

If you have set up above vars then type following commands:
```sh
$ git clone https://github.com/paveu/content-publisher.git tmp && mv tmp/.git . && rm -rf tmp && git reset --hard
$ sudo pip install -r requirements.txt
$ cd src
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic --noinput
$ python manage.py createsu # it will create superuser with login:admin,pw:admin
$ python manage.py runserver
```
### Heroku Installation
Link to tutorial will be added here soon

In order to setup Celery for Heroku, please follow this tutoria:
https://devcenter.heroku.com/articles/celery-heroku

for celery you will have to scale your worker, please type this command in the console:
```sh
heroku ps:scale worker=1
```
to get worker logs please type:
```sh
heroku logs -t -p worker
```
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

* NOTE #6: For all config envoirments(local,heroku,aws eb) you will have to setup SocialApp settings. So in order to get the project up and running please add Facebook SocialApp to the the Django admin. Do following steps:

1. Go to admin http://project/admin/ page use login:admin, pw:admin and click at Sites.
2. DO NOT REMOVE example.com, just edit example.com row and change example.com domain to your current project domain.
3. Click save.
4. Go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page
5. After you filled in these four steps project should be up and running.

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

