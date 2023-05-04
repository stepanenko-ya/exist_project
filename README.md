# For starting:

### Step #1
**You need to clone the latest version of the project**
```bash
git clone git@github.com:stepanenko-ya/exist_project.git
```

### Step #2:
**Now you need to create a Virtual Environment and activate it**
```bash
pip install virtualenv
```
```bash
virtualenv -p python3 venv
```
```bash
source venv/bin/activate
```

### Step #3:
**You need to open the folder**
```bash
cd exist
```

### Step #4:
**Now you need to install all the libraries and dependencies**
```bash
pip install -r requirements.txt
```

### Step #5:
**You need to run the project**
```bash
python manage.py runserver
```

### Step #6:
**You need to run celery in another terminal**
```bash
celery -A exist worker -l info
```
