# content-publisher

content-publisher is a project for selling out video content. All videos we sell are hosted on an external servers(wistia.com) and their links are emebed to a form as a iframe html code. After we embed it as a video object we can cover it with a description and comments. If a user drop a comment we get notifcation. Braintree payment is used to pay for an access to premium videos(restricted to those who buy premium membership). 

Heroku deyployment along with AWS S3: [http://content-publisher-pro.herokuapp.com](http://content-publisher-pro.herokuapp.com/)

### Project features
  - Django 1.9.5
  - full REST API for category, video and comment models
  - Braintree and PayU systems implemented
  - OAuth2 (signing in via facebook auth) implemented
  - full payment transaction history
  - vimeo and youtube, wistia
  - videos can be commented
  - notification system
  - posibility to host project source code on heroku with static and media files on AWS S3 bucket

### Todos
  - improving registration system (adding email activation system)
  - covering all models along with payment system with unit-tests
  - function testing wiyh selenium
  - deploying project to heroku and AWS elastic beanstalk
  - deploying project with fabric
  - exposing transaction model with REST API only for thoe users who has permision
  - fixing comment thread, add bootstrap
  - braintree tutorial for those who wants to run it in production mode
  - add automatic resize and compress images with PIL
  - https://requires.io/plans/
  - https://coveralls.io
  - https://docs.travis-ci.com/user/status-images/
  - http://shields.io/ (reelase image)
 
### Version
* version: 1.2
* project started in 08/may/2015.

### Tech
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


### Installation

NOTE #1: If you're running project locally then Redis-server must be running with socket left in '/var/run/redis/redis.sock'.
NOTE #2: If you're running project on heroku then Redis and postgress plugins must be set on.
NOTE #3: Three environment variables must be set in your shell to get project up and running:

1. Create a Python 2.7 virtualenv
2. 2. Install latest pip package
3. 3. Inside virtualenv perform following commands:

```sh
export AWS_ACCESS_KEY_ID='' # put here AWS AWS_ACCESS_KEY_ID setting
export AWS_SECRET_ACCESS_KEY='' #  put here AWS AWS_SECRET_ACCESS_KEY setting
export DJANGO_SECRET_KEY='openssl rand -base64 64' # generate new secret for django project
```

If you have set up above vars then type following commands:
```sh
$ git clone https://github.com/paveu/content-publisher.git tmp && mv tmp/.git . && rm -rf tmp && git reset --hard
$ sudo pip install -r requirements.txt
$ cd src
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py collectstatic
$ python manage.py runserver
```
NOTE #4: In order to get the project running please add Facebook SocialApp to the the Django admin. Do following steps:
1) Go to admin page and click at Sites.
2) DO NOT REMOVE example.com, just edit example.com row and put there your current project domain name.
3) click save.
4) go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page.

License
----

MIT

**Free Software, Hell Yeah!**

