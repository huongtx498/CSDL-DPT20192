# CSDL-DPT

- Cơ sở dữ liệu đa phương tiện - 20192
- require python version <= 3.7

## Install dependency
* Make new python env
```sh
$ py -m venv CSDLDPT
```
* Active enviroment (on Window)
```sh
$ CSDLDPT\Scrpits\Active.bat 
```
* Clone repositori and put it to env folder
* Install dependency
```sh
$ pip install -r requirements.txt 
```

## Config

* Dowload resource from links

```sh
class_names: https://drive.google.com/open?id=1t_CbZRTgkXBvAYtbx-XvuRdmG66OjTPG
```
```sh
Model trained: https://drive.google.com/open?id=1r3tIegXiMCtnw6VRnRshKZufhE4SLRxO
```
* Create database from sql file
* Update your informations to database config, class_name path, model_trained path
* Run server
```sh
$ python3 manage.py runserver
```

### Now, go to http://localhost:8000

## Authors

* **Team 6** - *IT2.02-HUST* -

