# Scientific Collection of Open-Source Policy Evidence (SCOPE)

Crittenden, Matthew, "SCOPE: Building and Testing an Integrated Manual-Automated Event Extraction Tool
for Online Text-Based Media Sources" (2021). Undergraduate Honors Theses. Paper 1651.
https://scholarworks.wm.edu/honorstheses/1651 


SCOPE data collection+coding platform (2GZM demo)

WARNING (THIS README NEEDS TO BE UPDATED)

## Instructions for Collaborators + Django Basics

The SCOPE data collection 2GZM demo website is implemented in a Python web framework called Django. All you need is a laptop, a Python installation, and a browser for testing the website. 

### Backend Setup

1. Install Python 3, if you haven't already done so:
    - For Windows: Download and run the [Python 3.11.2 installer](https://www.python.org/ftp/python/3.11.2/python-3.11.2.exe).
    - For macOS: Download and run the [Python 3.11.2 installer](https://www.python.org/ftp/python/3.11.2/python-3.11.2-macos11.pkg).

2. Install Git, if you haven't already done so:
    - For Windows: Download and run the [Git 2.39.2 installer](https://github.com/git-for-windows/git/releases/download/v2.39.2.windows.1/Git-2.39.2-32-bit.exe).
    - For macOS: Git should already be installed on your system. If not, run `brew install git` to install.

3. Once Python and Git are installed, open a command prompt or terminal and run the following commands to verify the installations:
```console
python3 --version
git --version
```

4. Clone the repository by running the following in your console:
```console
git clone https://github.com/wmgeolab/scope.git
```

5. Install the dependencies. If you're on Windows, download and install the [MariaDB Connector/C library](https://dlm.mariadb.com/2862617/Connectors/c/connector-c-3.3.4/mariadb-connector-c-3.3.4-win32.msi). Once you've installed the library, open a command prompt and navigate to the root of this repository (the main folder for the project). Then, type this command and press Enter:


	- Windows: 
	 ```console
	 pip install mariadb
	 ```
	- MacOS:
	 ```console
	 brew install mysql
	 ```

6. Make note of the local path where you copied the `scope` project folder, this is the folder you'll be working in. Personally, I like to keep my coding projects in the `Documents` folder. 
7. Connect to the website database. The website connects to an external MySQL database and requires the database login credentials to be stored in a file called `db_config.cnf`. Contact @joegenius98 to get access to this file, and save it in the top-level project folder. 

To run the backend server:
1. Change your directory to the [`backend`](backend) folder
2. `python manage.py runserver`
3. Note: Both frontend and backend servers must be running to make queries.

That should be all you need to work on developing and testing the website codebase. 

### Frontend Setup

1. Install [`Node.js`](https://nodejs.org/en/download/). (Last version used: `16.7.1`)
2. Navigate to the [`frontend`](frontend) folder 
3. `npm install` (Last version used: `8.15.0`)
4. `npm start`

As an alternative to `npm`, you can use `yarn`. I'm not too certain as how it compares to `npm`,
but I have heard it can be better.

1. `curl -o- -L https://yarnpkg.com/install.sh | bash`
2. Check that `yarn` installed successfully with `yarn --version` (Last version used: `1.22.19`)
3. Navigate to the [`frontend`](frontend) folder
4. Run `yarn` (which will automatically install from `package.json`)
5. `yarn run`


### Running with Docker

If you have [Docker](https://docs.docker.com/get-docker/) installed you can run
everything in a containerized development environment without installing Node, Python, or MySQL libraries
locally.

1. Clone this repository to your local machine
2. Run `docker compose build`
3. Run `docker compose run frontend npm install`
  - This step installs the node modules in the Docker image. In production this is handled automatically.
4. Run `docker compose up`

At this point you'll have the frontend piece running at http://localhost:3000 and the Python backend
components running at http://localhost:8080. Both servers will use your local clone of this repository, but
will use containerized versions of Node and Python. To updated versions edit the Dockerfile in `frontend/` and
in the root directory respectively.

### A brief overview of the project folder

The `scope` project folder contains all the files and folders needed to make the SCOPE website/platform work. Here's an overview of the top level folder structure that you'll need to know about:

- `scope`
	- `core`
		This folder controls the workings and settings of the "main" website, such as the home or about pages. 
	- `apps`
		This folder contains one or more "apps" -- self-contained mini websites that are nested within the main website. In our case, each "app" is a SCOPE workflow "module", since these are independent website components that may or may not be included for different SCOPE data coding projects. 
	- `examples`
		... 
	- `resources`
		... 

### Testing the website

Before submitting a new commit, it's sometimes a good idea to check that your code works locally on your computer and see how your changes have impacted the website. This requires starting the Django development web-server, which you can do as follows:

1. Open a commandline window, navigate to the [`backend`](backend) folder, and type `python manage.py runserver`. This will run some basic checks of the website code and, if successfull, should display `Quit the server with CTRL-BREAK`. 
2. Open a webbrowser and go to the url `http://127.0.0.1:8000/`. This should show your local version of the website. The data contents of the website however (such as rows in tables) is the same external MySQL database shared between all collaborators. 

As long as you keep the commandline window open, you'll be able to interact with the website. Plus, any changes you make to the code will immediately take effect (except when you make changes to the database, see below). 

### Making changes to the database

Whenever you have made changes to any of the data models in `models.py`, you will need to make sure these changes are registered to the central MySQL database:

1. In the commandline window, type `python manage.py makemigrations` (if the web server is running, you have to stop it first by pressing CTRL-C). This command tells django to make a record of what changes need to be made in the database, based on your changes in `models.py` (this is recorded in a file inside the `migrations` folder). 
2. Again in the commandline window, type `python manage.py migrate`. This is what actually applies the changes from the previous step to the database.
3. Start up the webserver again to see that your changes are reflected in the website. However, in most cases when you make changes to the database, the website will "break" and you'll see some errors. You'll need to update the code in whichever scripts rely on those data models. Read the errors -- they'll help you identify what needs fixing. 

If all goes well, whatever changes you made locally in `models.py` will be reflected in the external MySQL database shared by everyone. 

