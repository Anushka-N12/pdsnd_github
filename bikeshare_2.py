import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Collect target city
    while True:
        city = input("Would you like to see the data for Chicago, New York City or Washington? : ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid input. Accepted answers are Chicago/New York City/Washington. Try again. ")
    
    #Ask target month & day
    while True:
        choice = input("Would you like to filter the data by month, day, both, or neither? : ").lower()
        if choice in ['month', 'day', 'both', 'neither']:
            break
        else:
            print("Invalid input. Accepted answers are month/day/both/neither. Try again.")
    month, day = 'all', 'all'
    if choice in ['month', 'both']:
        while True:
            month = input("For which month? : ").lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print("Invalid input. Accepted answers are January/February/March/April/May/June. Try again.")
    if choice in ['day', 'both']:
        while True:
            day = input("For which day of the week? : ").lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print("Invalid input. Accepted answers are monday/tuesday/wednesday/thursday/friday/saturday/sunday. Try again.")

    print('-'*40)
    return city, month, str(day)

def load_data(city, month, day):
   
    #Assumption made that datasets are in the same directory
    df = pd.read_csv(CITY_DATA[city])
    if month != 'all':
        months = {'january':'01', 'february':'02', 'march':'03', 'april':'04', 'may':'05', 'june':'06'}
        df = df[df['Start Time'].str.slice(start=5, stop=7) == months[month]]

    df['Day of the week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    if day != 'all':
        days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
        df = df[df['Day of the week'] == days[day]]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nAs per the given month & day restrictions,")
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['Start Time'].str.slice(start=5, stop=7).mode().unique()[0]
    months = {'01':'january', '02':'february', '03':'march', '04':'april', '05':'may', '06':'june'}
    print("Most common month of travel  is - ", months[most_common_month])

    most_common_day = df['Day of the week'].mode().unique()[0]
    days = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}
    print("Most common day of the week is - ", days[most_common_day])

    print("Most common hour of travel is - ", df['Start Time'].str.slice(start=11, stop=13).mode().unique()[0], " hrs.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most common start station is - ", df['Start Station'].mode().unique()[0])

    print("Most common end station is - ", df['End Station'].mode().unique()[0])

    print("Most common combination of start station and end station trip is - ", (df['Start Station'] + ' to ' + df['End Station']).mode().unique()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    duration = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    print("Total time travelled is - ", duration.sum())
    print("Average time travelled is - ", duration.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Below are counts of user types - ")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city in ['chicago', 'new york city']:
        print("\nBelow are counts of user genders - ")
        print(df['Gender'].value_counts())
        print("\nEarliest birth year found is - ", df['Birth Year'].min())
        print("Latest birth year found is - ", df['Birth Year'].max())
        print("Most common birth year is - ", df['Birth Year'].mode().unique()[0])
    else:
        print('\nGender & birth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data as per user's request"""
    n = 0      #Refernce to indexes being printed
    while n < len(df):
        choice = input("Would you like to see 5 rows of raw data? : ").lower()
        if choice == 'yes':
            sub_df = df[n:n+5]
            cols = len(sub_df.columns)
            section_1 = sub_df[sub_df.columns[:cols//2]]
            section_2 = sub_df[sub_df.columns[cols//2:]]
            print(section_1)
            print(section_2)
            n += 5
        elif choice == 'no':
            break
        else:
            print("Invalid input. Accepted answers are yes/no. Try again.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? : ').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
