1. Setup Virtual Environment, GIT, & Django.
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
2. Check correctness of Procfile file, it should be similiar to:
	```
	web: gunicorn --pythonpath src srvup.wsgi
    worker: celery worker --workdir=src --app=srvup.celery:app --loglevel=INFO
	```
3. Check correctness of runtime.txt file, it should be similiar to:
	```
	python-2.7.10
	```
4. Sign in to heroku (if you don't have heroku account, sign up there):
	```
	$ heroku login
	```
5. Create two new heroku apps:
	**One for production**
	```
	$ heroku create contentpub-pro
	```
	**One for staging**
	```
	$ heroku create contentpub-stage
	```
6. Add your new apps to your git remotes. Make sure to name one remote pro (for “production”) and the other stage (for “staging”)
	```
    $ git remote add pro https://git.heroku.com/contentpub-pro.git
    $ git remote add stage https://git.heroku.com/contentpub-stage.git
	```

7. Now we can push both of our apps live to Heroku
	**One for production**
	```
	$ git push stage master
	```
	**One for staging**
	```
	$ git push pro master
	```

8. Creating plugins for heroku (production and staging)
	**One for production**
	```
	$ heroku addons:create heroku-postgresql:hobby-dev --app contentpub-pro
	$ heroku addons:create heroku-redis:hobby-dev --app contentpub-pro
	```	
	**One for staging**
	```
	$ heroku addons:create heroku-postgresql:hobby-dev --app contentpub-stage
	$ heroku addons:create heroku-redis:hobby-dev --app contentpub-stage
	```	

9. Set environment variables for both production and staging
	**One for production**
	```
    $ heroku config:set AWS_ACCESS_KEY_ID='' --app contentpub-pro ### AWS S3
    $ heroku config:set AWS_SECRET_ACCESS_KEY='' --app contentpub-pro # AWS S3
    $ heroku config:set CONFIG_ENV='HEROKU' --app contentpub-pro
    $ heroku config:set DJANGO_SECRET_KEY='' --app contentpub-pro # openssl rand -base64 32
    $ heroku config:set EMAIL_PASSWORD='' --app contentpub-pro
    $ heroku config:set EMAIL_USERNAME='' --app contentpub-pro
	```	

	**One for staging**
	```
    $ heroku config:set AWS_ACCESS_KEY_ID='' --app contentpub-stage
    $ heroku config:set AWS_SECRET_ACCESS_KEY='' --app contentpub-stage
    $ heroku config:set CONFIG_ENV='HEROKU' --app contentpub-stage
    $ heroku config:set DJANGO_SECRET_KEY='' --app contentpub-stage
    $ heroku config:set EMAIL_PASSWORD='' --app contentpub-stage
    $ heroku config:set EMAIL_USERNAME='' --app contentpub-stage
	```	

10. Now we can push both of our apps live to Heroku.
	**One for production**
	```
    $ git push pro master

	```
	**One for staging**
	```
    $ git push stage master
	```

11. Apply migration, create user, collectstatic
	**One for production**
	```
	$ heroku run python src/manage.py migrate --noinput --app contentpub-pro
	$ heroku run python src/manage.py createsu --app contentpub-pro # it will create superuser with login:admin,pw:admin
	$ heroku run python src/manage.py collectstatic --noinput --app contentpub-pro
	```
	**One for staging**
	```
	$ heroku run python src/manage.py migrate --noinput --app contentpub-stage
	$ heroku run python src/manage.py createsu --app contentpub-stage # it will create superuser with login:admin,pw:admin
	$ heroku run python src/manage.py collectstatic --noinput --app contentpub-stage
	```

12. Scale celery workers for both production and staging
	**One for production**
	```
    $ heroku ps:scale worker=1 --app contentpub-pro
	```
	**One for staging**
	```
    $ heroku ps:scale worker=1 --app contentpub-stage
	```

13. For all config envoirments(local,heroku,aws eb) you will have to setup SocialApp settings. So in order to get the project up and running please add Facebook SocialApp to the the Django admin. Do following steps:

1. Go to admin http://project/admin/ page use login:admin, pw:admin and click at Sites.
2. DO NOT REMOVE example.com, just edit example.com row and change example.com domain to your current project domain.
3. Click save.
4. Go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page
5. After you filled in these four steps project should be up and running.

