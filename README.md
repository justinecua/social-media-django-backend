Getting Started

Instructions on setting up your project locally. To get a local copy up and running, follow these simple example steps.

Prerequisites

This is a list of required software to run this locally.

Create an Ubuntu 22.04 environment/Ubuntu 22.04 VM.

Install Python 3.12

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12
python3.12 --version

Install Python 3.12 virtual environment

sudo apt-get install build-essential libssl-dev libffi-dev python3.12-dev
sudo apt-get install -y python3.12-venv

Install mysqlclient

sudo apt install python3.12-dev build-essential
sudo apt install libssl3
sudo apt install libssl-dev
sudo apt install libmysqlclient-dev

Installation

Create a folder on your desktop, name it anything you want, and open it in the terminal.

Create a virtual environment

python3.12 -m venv name_of_your_env

Activate the environment

source name_of_your_env/bin/activate

To deactivate the environment

deactivate

Clone/Download this repository to the folder you just created and name it 'src'

https://github.com/justinecua/social-media-django-backend.git

Navigate into src

cd src/

Install packages using pip

pip install -r requirements.txt

Apply database migrations

python manage.py makemigrations
python manage.py migrate

Create a superuser and fill in all the necessary fields

python manage.py createsuperuser

Run the project

python manage.py runserver 0.0.0.0:8000

Your project is running locally. Enjoy!
