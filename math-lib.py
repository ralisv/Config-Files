from math import e, factorial
from scipy.stats import norm

def product(*args):
    res = 1
    for arg in args:
        res *= arg
    return res if args else 0


def average(*args):
    return sum(args) / len(args)


def geo_average(*args):
    return product(args) / len(args)


def dexp(x: float, rate: float) -> float:
    """
    The probability density function (PDF) of the exponential distribution is given by:
    
    f(x) = rate * e^(-rate * point)
    

    The probability of a component failing at a specific time is zero, 
    since the probability density function is continuous and the probability of any specific value is zero.
    However, the dexp function returns the probability density at a given point, not the probability itself.
    The probability density represents the rate at which the failure times occur, 
    and can be used to calculate the probability of a failure occurring within a range of times.

    For example, if we want to calculate the probability of a component failing between time t1 and t2,
    we can integrate the probability density function over the range t1 to t2.

    @param x the random variable
    @param rate the frequency at which an even occurs
    """
    return rate * e ** (-rate * point)


def pexp(x: float, rate: float) -> float:
    """
    The cumulative distribution function (CDF) of the exponential distribution.
    The exponential distribution is a continuous probability distribution that describes the time between
    events in a Poisson process.
    The probability density
    
    So pexp(1, 2) returns the probability of an event occuring two times per period t on average occuring
    only 1 or 0 times.

    @param x the random variable
    @param rate the frequency at which an even occurs

    Example:

    Time Between Customers
    The number of minutes between customers who enter a certain shop can be modeled by the exponential distribution.

    For example, suppose a new customer enters a shop every two minutes, on average. After a customer arrives,
    find the probability that a new customer arrives in less than one minute.

    To solve this, we can start by knowing that the average time between customers is two minutes. Thus, the rate can be calculated as:

    We can plug in mean = 0.5 and x = 1 to the formula for the CDF:

    pexp(1, 0.5) ~~ 0.3935

    The probability that we’ll have to wait less than one minute for the next customer to arrive is 0.3935.
    """
    return 1 - e ** (-rate * x)


def dpois(x: float, mean: float) -> float:
    """
    The probability mass function (PMF) of the Poisson distribution for a given set of parameters.
    The formula for the PMF of a Poisson distribution is:

    f(x) = (mean^x * e^(-mean)) / x!

    @param x the number of events
    @param mean the average rate at which event occur
    """
    return (mean ** x * e ** (-mean)) / factorial(x)


def ppois(x: float, mean: float) -> float:
    """
    the cumulative distribution function (CDF) of the Poisson distribution. 
    The CDF gives the probability that a random variable X is less than or equal to a certain value x.
    The formula for the CDF of the Poisson distribution is defined as:

    f(x) = e^(-mean) * sum[mean^k / k! for k in 0..x]

    @param x the number of events
    @param mean the average rate at which event occur

    Example:
    
    Number of Arrivals at a Restaurant
    Restaurants use the Poisson distribution to model the number of expected customers that will arrive at the restaurant per day.

    For example, suppose a given restaurant receives an average of 100 customers per day.
    We can use the Poisson distribution calculator to find the probability that the restaurant receives more than a certain number of customers:

    x > 110 customers ~~ 1 - ppois(110, 100) ~~ 0.14714
    x <= 90 customers ~~ ppois(90, 100) ~~ 0.17138

    This gives restaurant managers an idea of the likelihood that they’ll receive more than a certain number of customers in a given day.
    """
    return e ** (-mean) * sum(mean ** k / factorial(k) for k in range(x + 1))


def dnorm(x: float, mean: float, deviation: float) -> float:
    """
    The normal distribution is a probability distribution that is widely used in statistics. It is also known as 
    the Gaussian distribution or the bell curve. The formula for the normal distribution is:

    f(x) = (1 / (deviation * sqrt(2 * pi))) * e^(-((x - mean)^2) / (2 * deviation^2))

    This returns probability density in point x.

    @param x the point of interest
    @param mean the average value of interest

    dnorm function is used in pnorm to calculate the value of the PDF at a given point x, 
    and the CDF is approximated using numerical integration methods.
    @deviation 
    """
    return (1 / (deviation * (2 * pi) ** 0.5)) * e ** ((-(x - mean) ** 2) / (2 * deviation ** 2))


def pnorm(x: float, mean: float, deviation: float) -> float:
    """
    The cumulative distribution function (CDF) of the normal distribution at a given point. 
    The CDF gives the probability that a random variable is less than or equal to a given value.
    It is given by the formula:

    pnorm(x, mean, deviation) = 1 / (deviation * sqrt(2π)) ∫(-∞, x) e^(-(t-mean)^2 / (2 * deviation^2)) * deviation
    """
    return norm.cdf(x, loc=mean, scale=deviation)


def std_norm(x: float) -> float:
    """
    The cumulative distribution function of the standardized normal distribution at a given point.
    """
    return norm.cdf(x)