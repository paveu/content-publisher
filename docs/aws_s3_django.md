# S3 Static & Media Files for Django

Using Amazon Web Services (AWS) S3 For storing static and media files for a Django Project.

1. **Create AWS Account**: [here](http://aws.amazon.com/)

2. **Create AWS User Credentials**
	
	1. Navigate to [IAM Users](https://console.aws.amazon.com/iam/home?#users)
	
	2. Select `Create New Users`
	
	3. Enter `awsbean` as a username (or whatever you prefer)
	
	4. Ensure `Generate an access key for each user` is **selected**.
	
	5. Select `Download credentials` and keep them safe. 
	
	6. Open the `credentials.csv` file that was just downloaded/created 

	7. Note the `Access Key Id` and `Secret Access Key` as they are needed for a future step. These will be referred to as `<your_access_key_id>` and `<your_secret_access_key>`

3. **Create new S3 Bucket**
	1. Navigate to S3 through the [Console](https://console.aws.amazon.com) or this [Link](https://console.aws.amazon.com/s3)
	2. Click `Create Bucket`
	3. Create a unique `Bucket Name` such as `your-project-bucket` or any other name you choose.
	4. Select `Region` relative to your primary users' location.
	5. Click `Create`

	Make note of the `Bucket Name` you created here. It will replace `<your_bucket_name>` below.

4. **Add Default Access Policies to your IAM User**:
	1. Navigate to the user's account such as: [https://console.aws.amazon.com/iam/home?region=us-west-2#users/awsbean](https://console.aws.amazon.com/iam/home?region=us-west-2#users/awsbean)
	2. Click on `Permissions` tab.
	3. Click on `Attach Policies` and add any policies you'd like to give this user access to.

	This step, we're not going to do. Instead, we are going to limit what our IAM User has access to in our AWS account. So onto the next step.

5. **Add Custom Permissions to your IAM User**
	1. Navigate to the user's account such as: [https://console.aws.amazon.com/iam/home?region=us-west-2#users/awsbean](https://console.aws.amazon.com/iam/home?region=us-west-2#users/awsbean)
	2. Click on `Permissions` tab.
	3. Click tab for `Inline Policies` and create a new one.
	4. Select `Custom Policy`
	5. Set `Policy Name` to `S3Django` (or any name you decide)
	6. Set `Policy Document` to, make note of the `<your_bucket_name>` as we just set this bucket name:
		```
		{
			"Statement": [
			    {
			        "Effect": "Allow",
			        "Action": [
			            "s3:ListBucket",
			            "s3:GetBucketLocation",
			            "s3:ListBucketMultipartUploads",
			            "s3:ListBucketVersions"
			        ],
			        "Resource": "arn:aws:s3:::<your_bucket_name>"
			    },
			    {
			        "Effect": "Allow",
			        "Action": [
			            "s3:*Object*",
			            "s3:ListMultipartUploadParts",
			            "s3:AbortMultipartUpload"
			        ],
			        "Resource": "arn:aws:s3:::<your_bucket_name>/*"
			    }
				]
		}
		```

	7. The `Action`s that we choose to set are based on what we want this user to be able to do. The line `"s3:*Object*",` will handle a lot of our permissions for handling objects for the specified bucket within the `Recourse` Value.


6. **Django Setup**

	This assumes you have a `Django project` already started.
	1. Pip downloads:

		```
		pip install boto django-storages-redux
		```
	2. Add `'storages',` to `INSTALLED_APPS` in your Django Settings (such as in `settings.py`)
	3. Run `python manage.py migrate` to ensure `django-storages-redux` is installed. Django Storage Redux ([docs](https://pypi.python.org/pypi/django-storages-redux)) is a updated version of Django Storage ([docs](https://django-storages.readthedocs.org/en/latest/)) and should be considered as a viable replacement. 
	5. In your Django configuration folder where `settings.py` and `urls.py` are, create a new file called `customstorages.py`
	6. In `customstorages.py` add the following:

		```
        from django.conf import settings
        from storages.backends.s3boto import S3BotoStorage
        import os
        
        os.environ['S3_USE_SIGV4'] = 'True'
        
        class StaticStorage(S3BotoStorage):
            host = "s3-%s.amazonaws.com" % settings.AWS_REGION
            location = settings.STATICFILES_LOCATION
            @property
            def connection(self):
                if self._connection is None:
                    self._connection = self.connection_class(
                        self.access_key, self.secret_key,
                        calling_format=self.calling_format, host=self.host)
                return self._connection
        
        
        class MediaStorage(S3BotoStorage):
            location = settings.MEDIAFILES_LOCATION
            host = "s3-%s.amazonaws.com" % settings.AWS_REGION
        
            @property
            def connection(self):
                if self._connection is None:
                    self._connection = self.connection_class(
                        self.access_key, self.secret_key,
                        calling_format=self.calling_format, host=self.host)
                return self._connection

		```

	7. In your `settings.py` add the following:

		```
		## AWS S3 STATIC AND MEDIA HANDLER
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
        AWS_REGION = 'eu-central-1' # Endpoint: cp-media-static-bucket.s3-website.eu-central-1.amazonaws.com
        AWS_ACCESS_KEY_ID = "<your_access_key_id>"
        AWS_SECRET_ACCESS_KEY = "<your_secret_access_key>"
        AWS_STORAGE_BUCKET_NAME = "<your_s3_bucket_name>"
        AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"
        AWS_PRELOAD_METADATA = True
        
        if AWS_STORAGE_BUCKET_NAME:
            STATIC_URL = 'https://s3-%s.amazonaws.com/%s/static/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
            MEDIA_URL = 'https://s3-%s.amazonaws.com/%s/media/' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
            STATICFILES_STORAGE = '<your_project_name>.customstorages.StaticStorage'
            DEFAULT_FILE_STORAGE = '<your_project_name>.customstorages.MediaStorage'
            STATICFILES_LOCATION = 'static'  # name of folder within bucket
            MEDIAFILES_LOCATION = 'media'    # name of folder within bucket
        else:
            STATIC_URL = '/static/'
            MEDIA_URL = '/media/'
        
        MEDIA_URL = os.environ.get('MEDIA_URL', MEDIA_URL)
        STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)
        
        STATICFILES_DIRS = (
            os.path.join(os.path.dirname(BASE_DIR), "static", "static_dirs"),
        )
        ```
        
        	8. Run `python manage.py collectstatic` and you should be all setup.

Links:
[link1](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)
[link2](http://notes.webutvikling.org/django-on-heroku-with-aws-s3-bucket-for-static-and-media-files/)

That's all.
Cheers!
