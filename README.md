

<!-- PROJECT LOGO -->
<br />
<p align="center">
<img src='./assets/bfb.png' alt='Project Logo' style="margin-right: 10%; width: 30%; height:auto">
  <!-- <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Money Talks - Twitter Scraper</h3>

  <p align="center">
    Backend library designed to scrape tweets and insert target mentions into a PostgreSQL DB, run entirely autonomously on a Raspberry Pi 3
    <br />
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## About Money Talks
This repo contains the code for the Twitter Scraper associated with the Money-Talks project. The Twitter-Scraper is responsible for downloading tweets from users, parsing text for mentions of ticker symbols, and inserting data found to a remote PostgreSQL server.

There is a specific subset of users on Twitter who monitor, analyze and comment on various tradable stock market assets. These users have a wide range of followers ranging from 10-40 followers to several hundred thousand followers. The Money-Talks projects aims at scraping tweets from these users and tracking the relative mention frequency of tradable stock market "Tickers".

The primary metric used to track tickers is the "Estimated Outreach" of a particular ticker on a particular day. The estimated outreach of a ticker is the combined sum of mentions by each user multiplied by the number of followers each particular user has. If a ticker symbol is mentioned ten times by a user with ten followers, the estimated outreach for that ticker on that day would be 100. If a user with one million followers mentioned the same ticker later that day (Think Elon Musk Tweeting Dogecoin memes...) the estimated outreach of that ticker on that day would increase to 1,000,100, the sum of the two users.

The goal of this project was to determine the correlation, if any, between the value of a tradable asset and the chatter or "hype" behind it. There are several examples in the dataset where you can see stock prices and mentions increase together in a very short time-span. It's out of my league to determine if chatter inspires market change or if market change inspires chatter, but the data is interesting nonetheless. 

The Money-Talks front-end client was developed with React and can be visited <a href='https://money-talks-front-end.herokuapp.com/'>here.</a>

## Twitter Scraper

The heart of this repo is located in the main.py script. When run, it authorizes a connection to the Twitter API through personal developer credentials by way of the [Tweepy](https://www.tweepy.org/) module. Once authorized, a csv file containing a list of UUID's is read in as a pandas dataframe. The dataframe contains information about the user id, last read tweet from the user (to prevent duplicates), and the number of followers a user has. Main.py iterates over this dataframe and downloads as many tweets from each user as possible and saves each as a csv. Next, main.py iterates through the directory of CSV's and parses through each tweet, if it identifies a ticker symbol mentioned in the tweet, it is pushed to the database. Throughout the run there are several meta-data stats being collected, such as the number of tweets downloaded total, number of users checked, total process time, etc. At the end of the process the email_report.py script is called to send an email containing report statistics to my personal email address to allow for remote monitoring of the process. Finally, by making use of the crontab Raspbian tool, I was able to schedule the task of activating the main.py script to once a day allowing for the entire process to take place autonomously.


## Sister Repos:

 * [Twitter Scraper](https://github.com/tracedelange/money-talks-twitter-scrape)
 * [Sinatra API](https://github.com/tracedelange/money-talks-sinatra)


### Built With

* [Ruby](https://www.ruby-lang.org/en/)
* [Sinatra](http://sinatrarb.com/)
* [ActiveRecord](https://guides.rubyonrails.org/active_record_basics.html)
* [Postgresql](https://www.postgresql.org/)
* [Heroku](https://id.heroku.com/login)



<!-- GETTING STARTED -->
## Access

The front-end site can be accessed [here](https://money-talks-front-end.herokuapp.com/)


<!-- CONTACT -->
## Contact

If you have any questions about this project or just want to chat, don't hesitate to reach out.

Trace DeLange - [LinkedIn](linkedin.com/in/trace-delange-991067169) - tracedelange@me.com

Project Link: [Money-Talks-Sinatra](https://github.com/tracedelange/money-talks-front-end)

Want to learn more about this project? Check out [my blog](https://tracedelange.github.io/)
