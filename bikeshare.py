import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("Choose the city you want to explore by typing its name [Chicago, New York City, Washington] \n").lower().strip()
        
        # validate user input
        if city in CITY_DATA:
            break
        else:
            print("Please make sure you enter a correct city name \n \n")

    # get user input for month (all, january, february, ... , june)
    print("\nCool! We have data for the first half of the year (January to June).")
    while True:
        month = input("Type the name of the month you'd like to explore or type 'all' to explore all of them \n").title().strip()
        
        # validate user input
        months = ["January", "February", "March", "April", "May", "June", "All"]
        if month in months:
            break
        else:
            print("Please make sure you enter a correct month name or 'all' \n \n") 

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("\nDo you want to explore the data for a specific day?")
    while True:
        day = input("Enter a weekday (Sunday to Saturday) or 'all' to explore all days \n").title().strip()
        
        #validate user input
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "All"]
        if day in days:
            break
        else:
            print("Please make sure you enter a correct weekday or 'all' \n \n")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Loading data...")
    print('-'*40)
    # read data from csv file corresponding to city ccording to user input and convert it to a DataFrame
    # set the column "Unnamed: 0" as index of the DataFrame
    df = pd.read_csv(CITY_DATA[city]).set_index("Unnamed: 0")
    
    # convert Start Time and End Time columns to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    # extract Start Month, Start Day and Start Hour from Start Time
    df["Start Month"] = df["Start Time"].dt.month_name()
    df["Start Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour

    
    # filter DataFrame by month in case user didn't choose all
    if month != "All":
        df = df[df["Start Month"] == month]
    
    # filter DataFrame by day in case user didn't choose all
    if day != "All":
        df = df[df["Start Day"] == day]
    

    return df


def time_stats(df, city):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (DataFrame) df - DataFrame containing the data for the city to be analyzed
        (str) city - name of the city to be analyzed
    """

    input("Press enter to display time stats")
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["Start Month"].mode()[0]
    print("According to the time period you selected, {} was the most popular month among Bikeshare users in {}.".format(most_common_month.upper(), city.title()))

    # display the most common day of week
    most_common_day = df["Start Day"].mode()[0]
    print("And the most common day of week people used Bikeshare was {}.".format(most_common_day.upper()))
    
    # display the most common start hour
    most_common_hour = df["Start Hour"].mode()[0]
    print("While the most popular hour of day was {}.".format(most_common_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    input("Press enter to display station stats")
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most common start station is {}.".format(common_start_station))

    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("While the most common end station is {}.".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_combination = (df["Start Station"] + " to " + df["End Station"]).mode()[0]
    print("And the most common trip was from {}.".format(common_combination))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def time_components(total_seconds):
    """
    Convert number of seconds to days, hours, minutes and seconds
    Args:
        (int) total_seconds - total number of seconds to be coonverted
    Returns:
        (int) days - number of days
        (int) hours - number of hours
        (int) minutes - number of minutes
        (int) seconds - number of remaining seconds
    """
    # get number of days
    days = total_seconds // (24 * 3600)
    # update total_seconds after removing the number of days
    total_seconds = total_seconds % (24 * 3600)
    # get number of hours
    hours = total_seconds // 3600
    # update total_seconds after removing the number of hours
    total_seconds %= 3600
    # get number of minutes
    minutes = total_seconds // 60
    # update total_seconds after removing the number of minutes
    total_seconds %= 60
    # get number of seconds
    seconds = total_seconds
    
    return days, hours, minutes, seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    input("Press enter to display trip duration stats")
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # get total travel time
    total_travel_time = df["Trip Duration"].sum()
    # extract total travel time to its components
    t_days, t_hours, t_minutes, t_seconds = time_components(total_travel_time)
    # display total travel time
    print("The total travel time for all trips in the selected time period was {} days, {} hours, {} minutes and {} seconds.".format(int(t_days), int(t_hours), int(t_minutes), int(t_seconds)))

    # get mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    # extract total travel time to its components
    m_days, m_hours, m_minutes, m_seconds = time_components(mean_travel_time)
    # display total travel time
    print("The average travel time was about {} minutes and {} seconds.".format(int(m_minutes), int(m_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - DataFrame containing the data for the city to be analyzed
        (str) city - name of the city to be analyzed
    """

    input("Press enter to display user stats")
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscibers = df["User Type"].value_counts()["Subscriber"]
    customers = df["User Type"].value_counts()["Customer"]
    print("{} of users were subscribers while {} were normal customers. \n".format(subscibers, customers))
    
    if city == "washington":
        print("Unfortunately there is no data about users' gender or birth year for the city of Washington \n")
    else:
    # Display counts of gender
        male = df["Gender"].value_counts()["Male"]
        female = df["Gender"].value_counts()["Female"]
        print("The number of male Bikeshare users is: {}, while the number of female users is: {} \n".format(male, female))
    # Display earliest, most recent, and most common year of birth
        earliest = int(df["Birth Year"].min())
        most_recent = int(df["Birth Year"].max())
        most_common = int(df["Birth Year"].mode())
        print("The oldest Bikeshare user in {} was born in {}, while the youngest was born in {}. And the most common birth year for Bikeshare users is {}.".format(city, earliest, most_recent, most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Displays raw data from DataFrame upon user request 5 rows at a time """
    
    i = 0
    while i < len(df):
        # ask the user if they would like to see the first 5 rows of raw data
        prompt = input("Would you like to see 5 rows of the raw data? type yes/no \n")
        if prompt == "yes":
            print(df[i : i+5])
        else:
            break
        
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
