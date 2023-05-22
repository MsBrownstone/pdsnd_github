import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}
cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # print message initiating user experience
    print('Hello! Let\'s explore some US bikeshare data.')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city data would you like to access: Chicago, New York or Washington? \n').lower()
        if city in cities:
            break
        else:
            print('Sorry, this is not a valid input. Please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month data would you like to access? Type month from January to June or all to apply no filter. \n').lower()
        if month in months:
            break
        elif month == 'all':
            break
        else:
            print('Sorry, this is not a valid input. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day data would you like to access? Type day from Monday to Sunday or all to apply no filter. \n').lower()
        if day in days:
            break
        elif day == 'all':
            break
        else:
            print('Sorry, this is not a valid input. Please try again.')

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of the week and hour from start time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_name = months[common_month -1].title()
    print("The most common month for chosen filters is " + common_month_name, "\n")

    # display the most common day of week
    print("The most common day of the week is ", df['day_of_week'].mode()[0], "\n")

    # display the most common start hour
    print("The most common start hour is ", df['hour'].mode()[0], "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['fr_combination'] = df['Start Station'] + " and " + df['End Station']
    print("The most frequent combination of start and end station is ", df['fr_combination'].mode()[0], "\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is ", df['Trip Duration'].sum(), "\n")

    # display mean travel time
    print("Average travel time is ", df['Trip Duration'].mean(), "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    # resetting index so that mode can function correctly
    df.reset_index(drop=True, inplace=True)

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print("The types of user counts are: ", df['User Type'].value_counts(), "\n")

    # display counts of gender
    if city == 'chicago' or city == 'new york':
        print("There are {} counts of genders \n".format(df['Gender'].value_counts()))
    else:
        print("Washington has no data on gender")

    # display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york':
        print("Earliest year of birth is ", df['Birth Year'].min(), "\n")
        print("Most recent year of birth is ", df['Birth Year'].max(), "\n")
        print("Most common year of birth is ", df['Birth Year'].mode()[0], "\n")
    else:
        print("Washington has no data on birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data under user condition."""

    # ask user if thy want to see raw data
    view_data = input('Would you like to see 5 rows of individual trip data? Enter yes or no \n').lower()
    start_loc = 0
    while view_data == 'yes':
        # print 5 rows of data
        print(df.iloc[start_loc:start_loc+5])
        # update starting location
        start_loc += 5
        # ask user if they want to see another 5 rows of data
        view_data = input('Would you like to see another 5 rows of individual trip data? Enter yes or no \n').lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()