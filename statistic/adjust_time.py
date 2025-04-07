import pandas as pd
from src.settings import Settings



def adjust_time1(df):
    """ adjust time in the dataframe if there are more than 2 orders in the same time
    if two orders adds 10 minutes to the second order
    if three orders removes 10 minutes from the first order and adds 10 minutes to the third order
    if four orders removes 20 minutes from the first order and 10 minutes from the second order
    and adds 10 minutes to the fourth order
    ...
    Args:
        df (DataFrame pandas): dataframe with the orders

    Returns:
        DataFrame: dataframe with the adjusted time
    """    
    max_iterations = 10  # max number of iterations to avoid infinite loop
    iteration = 0
    
    while iteration < max_iterations:
        # group by time and wenz
        time_groups = df.groupby(['time', 'wenz'])
        
        any_changes = False
        
        result = []
        for _ , group in time_groups:
            if len(group) == 2:
                group.iat[0, group.columns.get_loc('time')] -= pd.Timedelta(minutes=5 + iteration)
                any_changes = True
            elif len(group) == 3:
                group.iat[0, group.columns.get_loc('time')] -= pd.Timedelta(minutes=5 + iteration)
                group.iat[2, group.columns.get_loc('time')] += pd.Timedelta(minutes=5 + iteration)
                any_changes = True
            elif len(group) == 4:
                group.iat[0, group.columns.get_loc('time')] -= pd.Timedelta(minutes=10 + iteration)
                group.iat[1, group.columns.get_loc('time')] -= pd.Timedelta(minutes=5 + iteration)
                group.iat[3, group.columns.get_loc('time')] += pd.Timedelta(minutes=5 + iteration)
                any_changes = True
            elif len(group) >= 5:
                group.iat[0, group.columns.get_loc('time')] -= pd.Timedelta(minutes=10 + iteration)
                group.iat[1, group.columns.get_loc('time')] -= pd.Timedelta(minutes=5 + iteration)
                group.iat[-2, group.columns.get_loc('time')] += pd.Timedelta(minutes=5 + iteration)
                group.iat[-1, group.columns.get_loc('time')] += pd.Timedelta(minutes=10 + iteration) 
                any_changes = True  
            result.append(group)

        df = pd.concat(result)
        
        if not any_changes:
            break  # if no changes were made, exit the loop
        
        iteration += 1
        
    return df


min_interval = pd.Timedelta(minutes=7)

def adjust_time2(df):
    """adjust time in the dataframe if interval between the orders is less tha settings.min_interval
    if the interval is less than settings.min_interval set it equal to settings.min_interval

    Args:
        df (DataFrame): dataframe with the orders

    Returns:
        DataFrame: dataframe with the adjusted time
    """    
    min_interval = pd.Timedelta(minutes=Settings.min_interval)

    df = df.sort_values(by='time').reset_index(drop=True)
    for i in range(1, len(df)):
        prev_time = df.loc[i - 1, 'time']
        curr_time = df.loc[i, 'time']

        if curr_time < prev_time:
            curr_time = prev_time

            df.loc[i, 'time'] = curr_time + min_interval

        else:
            interval = curr_time - prev_time

            if interval < min_interval:
                df.loc[i, 'time'] = curr_time + (min_interval - interval)
    return df

def adjust_times(df):
    """combination of adjust_time1 and adjust_time2 and sort the dataframe by time,
    reset the index and add 1 to the index

    Args:
        df (DataFrame): dataframe with the orders

    Returns:
        DataFrame: dataframe with the adjusted time and sorted by time, with index reset and 1 added to the index
    """    

    # Spread the corses by 10 minutes if they are at the same time
    df = adjust_time1(df)
    df.sort_values("time", inplace=True) # type: ignore

    # Spread the shipments so that the interval between them is not less than Settings.min_interval
    df = df.groupby('wenz')[df.columns].apply(adjust_time2).reset_index(drop=True)
    df.sort_values("time", inplace=True) # type: ignore
    df.reset_index(drop=True, inplace=True)
    df.index=df.index+1

    return df




if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))