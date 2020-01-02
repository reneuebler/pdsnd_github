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
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_choice = input("Please tell me the city you want to explore (chicago, new york city, washington): ")
            if city_choice.lower() in CITY_DATA:
                city = city_choice.lower()
            else:
                print("invalid input, please try again...")
                continue


    # TO DO: get user input for month (all, january, february, ... , june)
            month_choice = input("Please enter the desired month (all, january, february, ... , june): ")
            month_choice = month_choice.lower()
            if month_choice in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
                month = month_choice
            else:
                print("invalid input, please try again...")
                continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
            day_choice = input("Please enter the desired day of the week (all, monday, tuesday, ... sunday): ")
            day_choice = day_choice.lower()
            if day_choice in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                day = day_choice
                break
            else:
                print("invalid input, please try again...")
                continue
        except Exception:
            break


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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('\nThe most common month is: ', common_month)

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of week is: ', common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most common start hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', common_start)

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', common_end)

    # TO DO: display most frequent combination of start station and end station trip
    common_start_end = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    common_start_end_count = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)[0]
    result = '\nThe most common combination of start station and end station is: {} with {} combinations'.format(common_start_end, common_start_end_count)
    print(result)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    sum_trip = df['Trip Duration'].sum()
    time_sum = pd.Timedelta(seconds = sum_trip)
    print('\nThe total travel time is: ', time_sum)

    # TO DO: display mean travel time
    mean_trip = df['Trip Duration'].mean()
    time_mean = pd.Timedelta(seconds = mean_trip)
    print('\nThe total travel time is: ', time_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df:
        users = df['User Type'].unique()
        print('\nThese are the user types: ', users)
    else:
        print("\n I'm sorry, but there is no Data for this city showing user type information...")

    # TO DO: Display counts of gender
    if 'Gender' in df:
        male = df['Gender'].str.count('Male').sum()
        print('\nTotal count of male people: ', male)
        female = df['Gender'].str.count('Female').sum()
        print('\nTotal count of female people: ', female)
        nans = df['Gender'].isnull().sum()
        print('\nTotal count of no information: ', nans)
    else:
        print("\n I'm sorry, but there is no Data for this city showing gender information...")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest year of birth: ', earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('\nThe most recent year of birth: ', most_recent_year)
        most_common_year = df['Birth Year'].mode()
        print('\nThe most common year of birth: ', most_common_year)
    else:
        print("\n I'm sorry, but there is no Data for this city showing gender information...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        while input('\nDo you want to view the raw data? Enter yes to go on: ') == 'yes':
            print(df[i:i+5])
            i += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
