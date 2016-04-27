# content-publisher

content-publisher is a project for selling out video content. All the videos we sell out are hosted on an external servers and their links are emebed to the page. After we embed it as a video object we can cover it with a descriptiona and comments. If a user drop a comment we get notifcation. Braintree payments are used to pay for an access to premium videos. Project started in 08/05/2015.

### Project features
  - support for vimeo and youtube
  - comments system
  - notifications
  - full billing history along with transactions made by braintree
  - full REST API for category, video, comment models
  - facebook, twitter and linkedin social links

### Todos
  - OAuth2
  - payu payments
  - django 1.9.5
  - Django REST framework 3.3
  - improving register (email confirm registration system)
  - covering all models by unit-tests
  - function testing by selenium
  - deyployed to heroku and AWS elastic beanstalk

### Version
project ver: 1.0

### Tech
content-publisher uses a number of open source projects to work properly:

* [braintree] - Payment system, ver: 3.12.0
* [colorama] - Cross-platform colored terminal text, ver: 0.3.3
* [Django] - The Web framework for perfectionists with deadlines, ver: 1.7.5
* [django-cors-headers] - A Django App that adds CORS (Cross-Origin Resource Sharing) headers to responses, ver: 1.1.0
* [django-crispy-forms] - Better formatted form template, ver: 1.4.0
* [django-filter] - Django-filter provides a simple way to filter down a queryset based on parameters a user provides, ver: 0.10.0
* [djangorestframework] - Django REST framework is a powerful and flexible toolkit for building Web APIs, ver: 3.1.2
* [djangorestframework-jwt] - JSON Web Token Authentication support for Django REST Framework, ver: 1.5.0
* [httpie] - HTTPie (pronounced aitch-tee-tee-pie) is a command line HTTP client, ver: 0.9.2
* [Markdown] - Python implementation of Markdown, ver: 2.6.2
* [Pillow] - Python Imaging Library, ver: 2.7.0
* [Pygments] - Python syntax highlighter, ver: 2.0.2
* [PyJWT] - A Python implementation of RFC 7519. Original implementation was written by @progrium, ver: 1.1.0
* [requests] - Requests is the only Non-GMO HTTP library for Python, safe for human consumption, ver: 2.6.0
* [Bootstrap] - is the most popular HTML, CSS, and JS framework for developing responsive, mobile first projects on the web, ver: 3.1.1
* [jQuery] -  is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers ver: 1.11.0

And of course content-publisher itself is open source with a [public repository][dill]
 on GitHub.

### Installation

You need Gulp installed globally:

```sh
$ npm i -g gulp
```

```sh
$ git clone [git-repo-url] dillinger
$ cd dillinger
$ npm i -d
$ gulp build --prod
$ NODE_ENV=production node app
```


### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```

License
----

MIT


**Free Software, Hell Yeah!**

