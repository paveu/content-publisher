# content-publisher

content-publisher is a project for selling out video content. All videos we sell are hosted on an external servers(wistia.com) and their links are embedded to a website as a iframe code. If we mark video as a premium then we can sell it out for money by using braintree and payu payment systems.

  - Heroku deyployment with AWS S3: [Link](http://contentpub-pro.herokuapp.com)
  - AWS Elastic Beanstalk deployment with AWS S3: [Link](http://content-publisher-prod.mrcd6tpmj3.eu-central-1.elasticbeanstalk.com/)

### Project features
  - Selling out premium accounts via Braintree(Credit Card, PayPal) and PayU(Polish bank trasfer)
  - Full user authentication system
  - Posibility to register/login with facebook
  - Full REST API for category, video and comment models
  - Transaction history for braintree and payu systems
  - Posibility to embed vimeo and youtube, wistia iframes
  - Videos can be commented by users
  - Notification when action happens(e.g. comments is made in a thread)
  - Analytic systems are implemented

### Technical features
  - Django framework 1.9.5
  - PostgreSQL 9.3 configuration database for production
  - static and media files are hosted in AWS S3 (for both AWS Elastic Beanstalk and Heroku)
  - Redis is used as a Celery broker for Heroku
  - Amazon SQS is used as a Celery broker for AWS Elastic Beanstalk
  - AWS ElastiCache(Redis) is used for session caching in AWS Elastic Beanstalk
  - Redis is used for session caching in Heroku
  - OAuth2 is implemented with Facebook authentication
  - Rest APIs are exposed via Django Rest Framework with JWT token
  - email service is provied via Google Gmail account
  - django-debug-toolbar is implemented

### Local deployment tutorial

[---> Link <---](https://github.com/paveu/content-publisher/blob/master/docs/deployment_to_local.md)

### Heroku deployment tutorial

[---> Link <---](https://github.com/paveu/content-publisher/blob/master/docs/deployment_to_heroku.md)

### AWS Elastic Beanstalk deployment tutorial

[---> Link <---](https://github.com/paveu/content-publisher/blob/master/docs/deployment_to_aws_elastic_beanstalk.md)

### Version
* version: 1.4.0
* project started in 08/may/2015. 
* code taken from my old repo: [https://github.com/paveu/srvup](https://github.com/paveu/srvup)

### Todos
  - Add Flower to monitor Celery tasks - top priority
  - Fix comment thread with angular.js - top priority
  - Add fabric script to deploy project to heroku(stage and production scripts)
  - Add celery task for exchange_rate function. Make it run periodicaly and save result to database
  - Add Sentry for monitoring exepctions happen within a project
  - Improve user account panel with angular.js
  - Add braintree and payu tutorials for those who wants to run it in production
  - Add tox, coverage, pytest
  - Cover all models along with payment systems with unit and functional tests
  - Expose transaction model with REST API only for those users who has permision
  - Add function for automatic resize and compress images with PIL after they are attached to video or category item

License
----

MIT

**Free Software, Hell Yeah!**

