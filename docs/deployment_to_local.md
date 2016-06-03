### Local deployment tutorial


**Setting up config variables**

* NOTE #1: You will have to set up django secret key, use 'openssl rand -base64 64' to generate your key and export it as a linux variable. If you're running it locally keep it safe in shell .profile file.

```sh
$ export DJANGO_SECRET_KEY='' # generate new secret key for django project. you can use following command: openssl rand -base64 64
```

* NOTE #2: Create an account at gmail.com and go to google email settings and selecet "turning on access for less secure apps" -> [link](https://support.google.com/accounts/answer/6010255). If you are running project locally I recommend adding gmail login/pw to shell .profile file. 
```sh
$ export EMAIL_USERNAME='' 
$ export EMAIL_PASSWORD=''
```

* NOTE #3: You will have to define config enviroment, for local development please select 'local'. If you are running project locally I recommend adding it to shell .profile file:

```sh
$ export CONFIG_ENV='local' # for local development
```

* NOTE #4: Set your FULL DOMAIN NAME. If you are running project locally I recommend adding it to shell .profile file:

```sh
$ export FULL_DOMAIN_NAME=''
```

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
```sh
$ mkdir proj && cd proj
$ git clone https://github.com/paveu/content-publisher.git .
```

**Install pip packages**
```sh
$ sudo pip install -r requirements.txt
```

**Apply migration, create user, collectstatic**
```sh
  $ cd src
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python manage.py collectstatic --noinput
  $ python manage.py createsu # it will create superuser with login:admin,pw:admin
  $ python manage.py runserver
  ```

* NOTE #5 For all config envoirments(local,heroku,aws eb) you will have to setup SocialApp settings. So in order to get the project up and running please add Facebook SocialApp to the the Django admin. Do following steps:
	* Go to admin http://project/admin/ page use login:admin, pw:admin and click at Sites.
	* DO NOT REMOVE example.com, just edit example.com row and change example.com domain to your current project domain.
	* Click save.
	* Go to 'Social applications' tab and fill in facebook authentication keys. Those keys can be found in facebook developer page
	* After you filled in these four steps project should be up and running.
