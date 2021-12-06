[![CodeFactor](https://www.codefactor.io/repository/github/dylanzenner/afk_trader/badge)](https://www.codefactor.io/repository/github/dylanzenner/afk_trader)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dylanzenner/afk_trader)
![GitHub last commit](https://img.shields.io/github/last-commit/dylanzenner/afk_trader)



# afk_trader
 If you'd like to replicate this project head over to the readme.md in the cfn directory
 
 
 ## Architecture
![](architecture.png)

Streaming Data is sourced from the Alpaca Trade markets (https://alpaca.markets/) containing information on particular stocks (In this case, Bitcoin). A python file residing on an EC2 instance continuously pulls the data via the alpaca trade api and orchestrates buy/sell orders based upon a simple RSI strategy.
