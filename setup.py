from setuptools import setup


setup(
    name='django-gcs',
    version='0.1',
    description='Django file storage backend for Google Cloud Storage',
    author='Bogdan Radko',
    author_email='bodja.rules@gmail.com',
    packages=[
        'django_gcs'
    ],
    install_requires=[
        'gcloud == 0.11.0'
    ],
    license='MIT',
    url='https://github.com/bodja/django-gcs'
)
