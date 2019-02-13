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
        city=input('Would you like to see data for Chicago, Washington or New York City? \n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input\n')
    month_filter, day_filter = False, False

    while True:
        filter_type = input('Would you like to filter data by month, day, or both, or not at all? Type "None" for no time filter.\n').lower()
        if filter_type == 'month':
            month_filter = True
        elif filter_type == 'day':
            day_filter = True
        elif filter_type == 'both':
            month_filter = True
            day_filter = True
        elif filter_type != 'none':
            print('Invalid input\n')
            continue
        break
    month = None
    day = None
    # TO DO: get user input for month (all, january, february, ... , june)
    if month_filter:
        while True:
            month = input('Which month? Janurary, Feburary, March, April, May, or June?\n').lower()
            if month in ['january','feburary','march','april','may','june']:
                break
            else:
                print('Invalid input\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if day_filter:
        while True:
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').lower()
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                break
            else:
                print('Invalid input\n')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day:
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_index = df['month'].value_counts().idxmax()
    print('The Most Frequent Month of Travel:{}.'.format(month_index))

    # TO DO: display the most common day of week
    day_index = df['day_of_week'].value_counts().idxmax()
    print('The Most Frequent Day of Travel:{}.'.format(day_index))

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    hour_index = df['hour'].value_counts().idxmax()
    print('The Most Frequent Hour of Travel:{}.'.format(hour_index))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_index = df['Start Station'].value_counts().idxmax()
    print('The Most commonly used start station:{}.'.format(start_station_index))

    # TO DO: display most commonly used end station
    end_station_index = df['End Station'].value_counts().idxmax()
    print('The Most commonly used end station:{}.'.format(end_station_index))

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station'],['End Station']).size().sort_values(ascending=False)
    combination_index = conbination.index[0]
    print('The most frequent combination of start station and end station trip:{}-->{}'.format(combination_index[0],combination_index[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds'.format(total_travel_time))


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in range(len(user_types.index)):
        print('The counts of {} is {}'.format(user_types.index[i], user_types.values[i]))

    # TO DO: Display counts of gender
   if 'Gender' in df:
        gender = df['Gender'].value_counts()
        for i in range(len(gender.index)):
            print('The counts of {} is {}'.format(gender.index[i], gender.values[i]))
    else:
        print('Gender information is missing in database.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year = df['Birth Year'].dropna().values
        print('The earliest year of birth is {}.'.format(np.min(birth_year)))
        print('The most recent year of birth is {}.'.format(np.max(birth_year)))
        common_year = df['Birth Year'].dropna().value_counts().idxmax()
        print('The most common year of birth is {}.'.format(common_year))
    else:
        print('The information is missing in the database.')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
