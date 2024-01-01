<!-- ABOUT THE PROJECT -->
## About The Project

This a web scraping project that scrapes data from two betting websites and compares odds for specific matches. The project is built with Python and uses the Selenium library to scrape the data. It uses Apache Airflow to schedule the scraping and to manage concurrency. The is no need to store data since the project is aimed to send notifications to a telegram channel when the odds are favorable. This project is deployed locally.

### Built With

* [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
* [![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)]()
* [![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache%20airflow&logoColor=white)]()


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

In order to run this locally, you must have docker installed. You can install it from [here](https://docs.docker.com/get-docker/).

Then you must clone this repository and build the docker image contained in the docker-compose.yml file.

You need to have an .env file with the following variables: TELEGRAM_API_KEY, TELEGRAM_CHANNEL_ID. The first one is a telegram bot api key. You can get one from [here](https://core.telegram.org/bots#6-botfather). The second one is the id of the telegram channel where you want to send the notifications. You can get it from [here](https://stackoverflow.com/questions/33858927/how-to-obtain-the-chat-id-of-a-private-telegram-channel). 

That should be it. Just initiate the docker build and you should be good to go.

It will start spaming the telegram channel with messages that it is scraping the data, and if it finds a favorable odd, it will send a message with the odds, profit, team and player.


<!-- CONTACT -->
## Contact

Your Name - [@fernando-cortes-tejada](https://github.com/fernando-cortes-tejada) - fcortes@pucp.edu.pe

Project Link: [https://github.com/fernando-cortes-tejada/safebets-airflow](https://github.com/fernando-cortes-tejada/safebets-airflow)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
