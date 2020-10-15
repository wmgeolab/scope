# scope

SCOPE data collection+coding platform (2GZM demo)

## Instructions for Collaborators + Django Basics

The SCOPE data collection 2GZM demo website is implemented in a Python web framework called Django. All you need is a laptop, a Python installation, and a browser for testing the website. 

### Setup

Setting up the website on your local computer is fairly easy: 

1. Install Python 3 (if you don't already have it). 
2. Install the dependencies. These are listed in `requirements-dev.txt` and can be installed easily via the commandline: `pip install -r 'path/to/scope_site/requirements-dev.txt'`.
3. Clone/copy this repository to your local computer. As a collaborator, you should have access to view and make changes to this repository in your GitHub account. Open GitHub Desktop, and in the top menu choose `File -> Clone Repository -> scope_site`. 
4. Make note of the local path where you copied the `scope_site` project folder, this is the folder you'll be working in. 
5. Connect to the website database. The website connects to an external MySQL database and requires the database login credentials to be stored in a file called `db_config.cnf`. Contact @karimbahgat to get access to this file, and save it in the top-level project folder. 

That should be all you need to work on developing and testing the website codebase. 

### Workflow

#### Starting your work-session

A good habit for whenever you're sitting down and ready to work on the website:

1. Open GitHub Desktop, switch to the `scope_site` repository from the left menu, and click `Fetch origin`. This will make sure your local version of the website codebase is up to date with the latest changes from the other collaborators. 
2. Open your local project folder, this will be your main workspace, and is where you'll find the various Python scripts and other files that make the website run. 
3. Open a commandline window, and set the working directory to the top level of your local project folder: `cd path/to/scope_site`. From this window you'll be performing various administrative/management related website task. This is done by running the `manage.py` script in the top level folder, by typing `python manage.py` followed by whatever action you want to do (see examples below). 
4. Start coding! 

Throughout your work-session, whenever you finish some task:

1. Open up GitHub Desktop
2. Write a brief description of the changes you made, and click `Commit to master`. 

Don't forget to make all your latest changes available to your fellow collaborators, by clicking the "Sync/Push/Upload" button in the top menu. 

#### A brief overview of the project folder

The `scope_site` project folder contains all the files and folders needed to make the website work. Here's an overview of the top level structure and the purpose of the main files and folders that you will be using:

- `scope_site`
	- `manage.py`
		This file is what you call on from the commandline, e.g. to start the website server. 
	- `scope_site`
		This folder, with the same name as the project folder, controls the workings and settings of the "main" website. 
		- `settings.py`
			Controls various configurations and settings of the website, notably: the database settings, and the list of "apps" to include in the website (see below)
		- `urls.py`
			List of urls specific to the "main" website, such as "/home" or "/about".
		- `views.py`
			Python functions that retrieves the data contents for each of the pages on the "main" website, such as "home" or "about". This is where you typically pull any data to display on the page, and then you send it to be rendered on an html "template" (see next point).
		- `templates`
			This folder contains the django-style html "templates" that define what each page looks like. These documents are just like regular html documents, except django allows you to write the html content dynamically. The data that you fetched in the `views.py` script gets sent to one of the template documents, and by using the "django templating language" you can for instance create a loop to generate the html code to display the data in a table, conditionally display some data based on an if-else statement, and more. 
			- `home.html`
			- `...`
	- `app_name`
		All subsequent folders contain independent "apps" -- self-contained mini websites that are nested within the main website. In our case, each "app" is a SCOPE workflow "module", since these are independent website components that may or may not be included for different SCOPE data coding projects. 
		- `urls.py`
			List of urls specific to this particular "app".
		- `models.py`
			Python classes that define the database tables relevant for this "app" sub-section of the website. 
		- `views.py`
			Python functions that retrieves the data contents for each of the pages for this "app" sub-section of the website. 
		- `templates`
			This folder contains the django-style html "templates" that define what each page looks like for this "app" sub-section of the website. 
			- `example.html`
			- `...`

#### Testing the website

To check that your code works and see how your changes have impacted the website you will need to start the website server. This is a local Django-based process that lets you view and interact with your local version of the website in a browser window. To do so:

1. Go to your commandline window (see above) and type `python manage.py runserver`. This will run some basic checks of the website code and, if successfull, should display `Quit the server with CTRL-BREAK`. 
2. Open a webbrowser and go to the url `localhost:1000`. This should show your local version of the website. The data contents of the website however (such as rows in tables) is the same external MySQL database shared between all collaborators. 

As long as you keep the commandline window open, you'll be able to interact with the website. Plus, any changes you make to the code will immediately take effect (except when you make changes to the database, see below). 

#### Making changes to the database

Changes to the website database are made in the following way:

1. Open the `models.py` file. 
2. Make your desired changes to the data model class definitions. Each `class` in this file defines a table in the database, and contain the names and data types of the columns for that table. For a list of available data model fields and options (column types), [click here](https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-types).
3. In the commandline window, type `python manage.py makemigrations` (if the web server is running, you have to stop it first by pressing CTRL-C). This command tells django to make a record of what changes need to be made in the database, based on your changes in `models.py` (this is recorded in a file inside the `migrations` folder). 
4. Again in the commandline window, type `python manage.py migrate`. This is what actually applies the changes from the previous step to the database.
5. Start up the webserver again to see that your changes are reflected in the website. However, in most cases when you make changes to the database, the website will "break" and you'll see some errors. You'll need to update the code in whichever scripts rely on those data models. Read the errors -- they'll help you identify what needs fixing. 

If all goes well, whatever changes you made locally in `models.py` will be reflected in the external MySQL database shared by everyone. 

