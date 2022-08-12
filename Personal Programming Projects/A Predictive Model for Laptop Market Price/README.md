# Index
Home page [here](https://github.com/JAMPS657/Personal_Projects)

Project Selection [here](https://github.com/JAMPS657/Personal_Projects/tree/main/Personal%20Programming%20Projects)

# Predictive Model for Laptop Market Price
## Andrew J. Otis & Hsing Yu Chen

PowerPoint Presentation [here](https://github.com/JAMPS657/Personal_Projects/blob/main/Personal%20Programming%20Projects/A%20Predictive%20Model%20for%20Laptop%20Market%20Price/PPT_presentation/Bayes_Regression_Presentation.pdf)

Paper [here](https://github.com/JAMPS657/Personal_Projects/blob/main/Personal%20Programming%20Projects/A%20Predictive%20Model%20for%20Laptop%20Market%20Price/Bayesian%20Regression.pdf)

## Executive Summary
There exist two established frameworks regarding the field of statistics, Frequentist and Bayesian. utilizing the Bayesian framework, which results in a distribution. As opposed to the Frequentist framework, where a point estimate for variable of interest as a result. Under the Bayesian framework and with data of laptop prices in relation to their specifications, what is the probability of a laptop’s market price, given its specifications? Specifically, the model of linear regression under a Bayesian perspective is utilized. Two similar Bayesian models are constructed and explored, one with all relevant predictors and another with all the relevant predictors; excluding brand factors.

The Bayesian regression model with brands included do not fit our data well. However, the Bayesian model with brands excluded did fit the data well, and therefore would result in more valid results/interpretations. 

It is possible that the brand portion of the data is oversaturated with one type of response (e.g. majority of responses consisting of the most popular products at the time).

Thus, it is believed the model with brands included could be improved by the removal of brand factors within the model that do not have a significant effect, re-specifying parameters of the prior distribution with industry expert input or wait for more data to be collected.

While the analysis does not answer this question, it does provide a great starting point in the form of a model that fits the data. Follow up studies on the topic, it is recommended that predictions be made using the constructed Bayesian Model or attempt any of the following recommended adjustments to correct the model including “brand” variables.

## Data Source and Definitions
The data set can be found and accessed on Kaggle under the “References” section in the category “Data”. The data was originally sourced from the web domain “flipkart.com” for a chrome extension application called “Instant Data Scrapper”. Luckily, the secondary source utilized had already done a majority of the data cleaning required for analysis, having 896 observations and 34 attributes.

The data consists of factors considered to be relevant when it comes to a laptop’s market price, suggested to affect laptop prices, such as company name and owned laptop brands, the price of the laptop when first released and later in product’s life, and the hardware that comes with it. 

Through exploratory analysis, it was discovered that the response variable being continuous, and all predictor variables are categorical.

## Exploratory Analysis
As part of exploratory analysis, two major data transformations are performed. First, the responses of columns are transformed in to multivariate (i.e. 1, 2, 3,…, etc.) form. 

Second, another column is added for the logistic transformation of the response variable “latest_price”. This is due to the original form of the response variable produces a distribution skewed towards the left, the result is a response  After these transformations, the data set ready for analysis with 896 observations and 35 attributes.

To determine whether or not he had continuous or categorical predictors, histograms of each of them individually were constructed.

## Bayesian Data Analysis, In Principle
Recall, under the Bayesian Framework, the model produces a distribution. How? Bayes Theorem.

Bayes Theorem: P(A│B) α P(B│A)P(A)

Where,                                                                                                                                                                                  
P(A│B)→Posterior Distribution                                                                                                                                  

P(B│A)→Likelihood Distribution,            given event A has occured, what is probability of event B?

P(A)→Prior Distribution,                                        Inital guess of the variable of interest

The resulting posterior distribution can be interpreted as a report on both the level certainty and uncertainty (i.e. ±0, ±1, …,±n standard deviations )regarding the probability of an event and model parameters

## Bayesian Regression
A linear model can be utilized for data analysis under the Bayesian Framework. To get our Prior Distribution, we will simply run a regular multiple regression. Without industry expert input, this type of prior is commonly referred to as a “non-informative prior”.

y_i=(β_0+β_1 x_1+⋯+β_n x_n )+(ε_i)     , for data (x_n, y_n)

Where,                                                                                       
ε_i←Noise                                                                     
β_0←y-intercept                                                       

To get our Likelihood Distribution the model runs thousands of samples, each with their own likelihood parameter, which together create a distribution of the likelihood parameters.

These calculations can be accomplished by utilizing the JAGS package in statistical software like R

## Applied Bayesian Regression
Through the JAGS R package, the Markov chain Monte Carlo (MCMC) algorithm is applied
Imagine a target distribution you want to analyze, have data on it, but can no longer collect the data?  The MCMC algorithm would be a viable solution. Thus, MCMC is simply an algorithm for sampling from a distribution.

One of the most common uses of the MCMC algorithm is to sample the posterior probability distribution of some model in Bayesian inference

Regarding Analysis, four Markov Chains are set up for the predictors, “brand”, “ram_gb”, “hdd”, “ssd”

With the formal equation

log⁡_price=(β_0+brand〖*x〗_1+ram_gb*x_2+hdd*x_3+ssd*x_4 )     , for data (x_n, y_n)

## Data Satisfaction
For results of the created Bayesian model to be considered valid, four data requirements must be met by the Bayesian model’s predicted values to determine to see how well it fits the data.

The four data considerations are that there exists a linear relationship between predictors and response, homoscedasticity across predictor values, independence in responses (i.e. residuals demonstrate random dispersal across a horizontal trendline), and normality (i.e. a well fit QQ plot of the residuals plotted against predicted values).

