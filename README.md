# content-publisher

content-publisher is a project for selling out video content. All the videos we sell out are hosted on an external servers and their links are emebed to the page. After we embed it as a video object we can cover it with a descriptiona and comments. If a user drop a comment we get notifcation. Braintree payments are used to pay for an access to premium videos. Project started in 08/05/2015.

### Project features
  - Django 1.9.5
  - support for vimeo and youtube videos
  - comments system
  - notifications system
  - full billing history along with transactions made by braintree
  - full REST API for category, video, comment models
  - facebook, twitter and linkedin social links

### Todos
  - OAuth2
  - payu payments
  - improving register (email confirm registration system)
  - covering all models by unit-tests
  - function testing by selenium
  - deyployed to heroku and AWS elastic beanstalk

### Version
project ver: 1.1

### Tech
content-publisher uses a number of open source projects to work properly:

* [braintree] - Payment system, ver: 3.25.0
* [colorama] - Cross-platform colored terminal text, ver: 0.3.7
* [Django] - The Web framework for perfectionists with deadlines, ver: 1.9.5
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

1. Create a Python 2.7 virtualenv
2. Inside virtualenv perform following commands:

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

License
----

MIT


**Free Software, Hell Yeah!**

