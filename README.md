[![CodeFactor](https://www.codefactor.io/repository/github/dylanzenner/afk_trader/badge)](https://www.codefactor.io/repository/github/dylanzenner/afk_trader)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dylanzenner/afk_trader)
![GitHub last commit](https://img.shields.io/github/last-commit/dylanzenner/afk_trader)



# Afk Trader
An automated trading bot built on top of the Alpaca API. Completly hosted in the AWS ecosystem with a quick and easy CloudFormation deployment.

 If you'd like to replicate this project head over to the readme.md in the cfn directory
 
 ### This is not financial advice. Only risk what you are willing to lose when participating in the stock market. The Maintainers of this repository are not responsible for your gains or losses when utilizing this bot.
 
 
 ## Architecture
![](architecture.png)

Streaming Data is sourced from the Alpaca Trade markets (https://alpaca.markets/) containing information on particular stocks (In this case, Bitcoin). A python file residing on an EC2 instance continuously pulls the data via the alpaca trade api and orchestrates buy/sell orders based upon a simple RSI strategy.



## Infrastructure
The project is housed in the AWS ecosystem, packaged into two CloudFormation templates and utilizes the following resources:

**VPC:**
-   Custom built VPC with two subnets (1 private, 1 public)
-   IGW, NATGW and Route Tables

**Secrets Manager:**
-   For storing connection variables and API tokens

**S3 Bucket with versioning enabled:**
-   For storing the source code files

**t3.xlarge EC2 Instance:**
-   For running Afk Trader


# Warning:

You will incur AWS charges when you deploy this bot. Some of the most expensive things in this project are as follows:
-   t3.xlarge EC2 instance: $0.1670 / hr (On-Demand mode)
-   NATGateway: $0.045 / hr plus data processing charges

### Again, THIS IS NOT SOMETHING WHICH IS FREE TO RUN. YOU WILL INCUR CHARGES!!!
