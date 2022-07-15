# Latent Class Analysis for Data Representation
## Andrew J. Otis & Hsing Yu Chen


## Summary
Our group utilizes Latent Class Analysis(LCA) as a statistical model to determine if distinct unobservable classes exist within a dataset utilized in a study by Bertrand and Mullainathan(2004). 
LCA is model in which individuals can be classified into mutually exclusive and exhaustive events known as latent classes, based on their pattern of response and measured with categorical variables. 
Analysis was carried out in Rstudio using the poLCA function which estimates latent class models for polytomous outcomes. It can also estimate latent class regression models, but these results were not utilized in the analysis. Ultimately, the results were determined to not be valid; but served a pedagogical purpose to demonstrate the process of LCA

## Introduction
The cross-sectional data was originally used as part of a larger study to aid researchers in determining if an individual’s implied ethnicity had an effect on their chances of progressing through the application process, specifically African American or Caucasian. The data was from employer ads posted in Chicago and Boston, where the information on the resumes is randomly generated and assigned. This information included things like gender, ethnicity, and name, plus the information posted on the job ads.  Our group is simply utilizing the dataset described to perform LCA. Even we wanted to perform a similar task to that of the researchers, LCA would not be the model to use to make predictions; it is a model for data representation.

The data source has come cleaned in columns separating the types of responses in the data set. For LCA, it was decided that we would look at the columns “equal”=employer offers equal opportunity, “reqeduc”=education requirement, “reqcomp”=computer competency requirement, “reqorg”=organizational requirement, “ethnicity”=implied ethnicity based on the sound of name, and “call”=whether or not the applicant proceeded in the application process. The columns chosen are details regarding requirements of the job in question and a few person-centered details regarding the applicant.

### Table 1

The isolated data then has responses transformed into 1’s and 0’s for probabilistic algorithms to run.  These responses may be binomial (i.e. only two outcomes) or multimodal(i.e. more than two outcomes

### Table 2

We must now ask “does the data satisfy the requirements of LCA?”, this is important regarding the validity of our results.
The Assumptions of LCA are as follows,
1.	Data is non-parametric 
2.	Data is categorical
3.	Observations in each class must be independent from one another

The way our data is currently structured, we would meet the first two assumptions of LCA, however the data set fails to meet the final assumption of LCA. Due to a lack of company id present in responses, we cannot guarantee that responses in each class determined are independent of one another.  For example, one company having more than one ad or more than one resume being sent in response to the same ad. Therefore, the results cannot be considered valid.  For pedagogical purposes we continued with the analysis to demonstrate the process of LCA.

## Summary Statistics

## Conclusion
The LCA model chosen was on the basis of the Bayesian Information Criterion (BIC) for estimating how well a given LCA model would fit our dataset.

BIC=kln(n)-2 ln⁡(L ̂ )

BIC prefers models where the number of samples (n), far outnumber the number of parameters (k) and in our case, a lower BIC value is indicative for the best fit model. Referring to the Summary Statistics section of the paper, we can observe BIC stop decreasing and begin to increase during the transition from 3 to 4 class LCA models. Allowing us to conclude that a 2 or 3-class LCA model would be best fitted for the data set.

Recall, the original research question was if the data set can be split into distinct groups and to model callback response to possible gain some insight on that particular variable.  

Now let’s interpret the results of our 3-class LCA model. Referring to table 1, we can observe that no matter what class an individual is in, they have higher than a 90% chance of progressing through the application process. We can also observe that there exist other item differences that could possibly imply a distinction of  classes. The resulting classes can be described as follows,

Class 1: Are jobs that rarely require computer skills and consisting of mostly male applicants

Class 2: Are Jobs that don’t offer equal opportunity employment and rarely have an education requirement

Class 3: Are jobs whose applicant pool consisted of mostly female

It was determined in the introduction that the data set does not suit itself very well for LCA, for further confirmation, a Chi Squared test was ran regarding each item in Table 1 to compare the 3-Class LCA model values to the actual observed values collected from our data source. Referring to the summary statistics questions, we can observe that every single item was not very well represented by the model; except for “gender”; confirming the lack of validity of our model’s results. Still, we hope the process of LCA makes a bit more sense and the implications it has on the field of statistics.

LCA is a model that is widely used to represent data in sociological and mental health settings. Such as the classification of drinking groups, or types of voters, etc. While we did not name our classes, doing so presents researchers with the unethical choice of purposefully giving names to classes that inaccurately represent class membership.

