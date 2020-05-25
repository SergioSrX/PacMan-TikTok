# Pacman-TikTok crawler

## How to use
<ol>
	<li> <b>Install all Python dependencies</b>
		<ul>
			<li> Run "pip install -r requirements.txt" in cmd
		</ul>
	<li> <b> Install Node.js and run nodeJS setup script </b> - this is optional, only if you want to obtain data about user's content
		<ul>
			<li> Download and install NodeJS from https://nodejs.org/en/
			<li> Run setup script located in: Pacman-TikTok/nodeJS/setup-nodeJS.py
			<li> After message: "Crawler is ready to use!" it is all ready.
		</ul>
	<li> <b>Finally run PacMan-TikTok/FinalFiles/GetData/get_data_user.py</b>
		<ul>
			<li> It will obtain all user data and store it in mongoDB.
		</ul>
</ol>

## About
Crawling top TikTok user data from several countries, including data like username, profile image, evolution of followers in time, video content and stats about it and much more. All of the data are stored in non-SQL db (MongoDB). These data are analyzed using matplotlib into graphs.
	
### Directories description

- **TestFiles** (files which are in test stage and not complete)
	
- **FinalFiles** (files which are officially ready to use)
	- **GetData** (files for crawling data)
	- **Data Analysis** (files for analyzing crawled data)
- **nodeJS** (nodejs setup script and needed js libs)

### DB test-client login
- E-mail: packman@thlingo.com
- Pass: MIB123456
