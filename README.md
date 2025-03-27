<!-- GETTING STARTED -->

## Getting Started

Instructions on setting up your project locally. To get a local copy up and
running follow these simple example steps.

### Prerequisites

This is a list of required software to run this locally.

- create ubuntu 21.10 environment/ ubuntu 21.10 VM.
- install python 3.9
  ```sh
  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt install python3.9
  python3.9 --version
  ```
- install python 3.9 virtual environment
  ```sh
  sudo apt-get install build-essential libssl-dev libffi-dev python-dev
  sudo apt-get install -y python3-venv
  ```
- mysqlclient
  ```sh
  sudo apt install python3.9-dev build-essential
  sudo apt install libssl1.1
  sudo apt install libssl1.1=1.1.1f-1ubuntu2
  sudo apt install libssl-dev
  sudo apt install libmysqlclient-dev
  ```

### Installation

1. Create a folder to your desktop name it anything you want then open it in
   terminal.
2. Create a virtual environment
   ```sh
   python3.9 -m venv name_of_your_env
   ```
3. Activate environment
   ```sh
   source name_of_your_env/bin/activate
   ```
4. To deactivate environment
   ```sh
   deactivate
   ```
5. Clone/Download this repository to the folder you just created and name it as
   'src'
   ```sh
   git clone http://192.168.0.26/ict/drf-boilerplate.git src
   ```
6. Cd into src
   ```sh
   cd src/
   ```
7. Install packages using pip
   ```sh
   pip install -r requirements.txt
   ```
8. DB migrations
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
9. Create superuser and fill all the necessary fields
   ```sh
   python manage.py createsuperuser
   ```
10. Run the project

```sh
python manage.py runserver 0.0.0.0:8000
```

11. Your project is running locally, enjoy.

### Deployment to production with apache2

1. Update and Upgrade linux server
   ```sh
   sudo apt-get update
   sudo apt-get upgrade
   ```
2. Set your hostname
   ```sh
   hostnamectl set-hostname your_hostname
   ```
3. Update hosts
   ```sh
   sudo nano /etc/hosts
   ```
4. Paste this in the hosts
   ```sh
   IP_ADRESS_OF_YOUR_SERVER   your_hostname
   ```
5. Create a folder inside the home directory of your server
   ```sh
   mkdir name_of_your_folder
   ```
6. Cd into that folder
   ```sh
   cd name_of_your_folder
   ```
7. Create python virtual environment
   ```sh
   python3 -m venv name_of_your_env
   ```
8. Activate environment
   ```sh
   source name_of_your_env/bin/activate
   ```
9. Clone repository
   ```sh
   git clone your_repository src
   ```
10. Cd into that cloned repository
    ```sh
    cd src
    ```
11. Install all the required packages

```sh
pip install -r requirements.txt
```

12. Generate static folder or run this commmand everytime you have changes
    inside your static folder

```sh
python manage.py collectstatic
```

13. Test if all is working fine

```sh
python manage.py runserver 0.0.0.0:8000
```

14. If all is fine kill the server

```sh
ctrl+c
```

15. Install apache2

```sh
sudo apt-get install apache2
```

16. Install mod_wsgi

```sh
sudo apt-get install libapache2-mod-wsgi-py3
```

17. Configure apache2 web server

```sh
cd /etc/apache2/sites-available/

sudo cp 000-default.conf name_of_your_config.conf

sudo nano name_of_your_config.conf
   copy this above the </VirtualHost> closing tag
   "
   Alias /static /home/your_username/name_of_the_folder_you_created_earlier/src/staticfiles
   <Directory /home/your_username/name_of_the_folder_you_created_earlier/src/staticfiles>
      Require all granted
   </Directory>

   Alias /media /home/your_username/name_of_the_folder_you_created_earlier/src/media
   <Directory /home/your_username/name_of_the_folder_you_created_earlier/src/media>
      Require all granted
   </Directory>

   <Directory /home/your_username/name_of_the_folder_you_created_earlier/src/src>
      <Files wsgi.py>
         Require all granted
      </Files>
   </Directory>

   WSGIScriptAlias / /home/your_username/name_of_the_folder_you_created_earlier/src/src/wsgi.py
   WSGIDaemonProcess your_custom_django_app_name python-path=path_of_your_cloned_repo python-home=path_of_your_virtual_environment
   WSGIProcessGroup your_custom_django_app_name
   "
   then save it.
```

18. Enable a site in apache2

```sh
sudo a2ensite name_of_your_config.conf
```

19. Disable the default site

```sh
sudo a2dissite 000-default.conf
```

20. Configure file permissions

```sh
sudo chown :www-data name_of_the_cloned_repo/db.sqlite3 #skip this if you don't have db.sqlite3
sudo chmod 664 name_of_the_cloned_repo/db.sqlite3 #skip this if you don't have db.sqlite3
sudo chown :www-data name_of_the_cloned_repo/
sudo chmod 775 name_of_the_cloned_repo/
sudo chown -R path_of_your_media_folder #skip this if you don't have a media folder
sudo chmod -R 775 path_of_your_media_folder #skip this if you don't have a media folder
```

21. Restart apache server

```sh
sudo service apache2 restart
```
