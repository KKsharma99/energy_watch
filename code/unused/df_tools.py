# Functions to Manipulate Building Energy Time Series Data

# Slices the Dataframe by both Date and Buildings
def slice_df(df, start_date, num_days=7, num_min=0, bldgs=None):
    start, end = slice_df_by_date(df, start_date, num_days, num_min)
    return slice_df_by_bldg(bldgs, df.iloc[start:end,:])

# Returns starting and ending indexes of data splice
def slice_df_by_date(df, start_date, num_days=7, num_min=0):
    start = df.index[df['time'] == start_date + ' 00:00'].tolist()[0]
    end = start + num_days * 96 + num_min % 15
    return start, end

# Returns df of Selected Columns (None == All)
def slice_df_by_bldg(df, bldgs=None):
    if bldgs == None: return df.iloc[:, 1:]
    else: return df[bldgs]

# Split Time Stamp Column to Two Columns; Date and Time
def split_date_time(df):
    df[date] = df[time].apply(lambda x: x.split(x)[0], axis = 1)
    df[time] = df[time].apply(lambda x: x.split(x)[1], axis = 1)


# Group By Interval with some Method
# Methods: Sum, Mean, Min, or Max
# Returns a df of grouped data
def group_df(df, method="mean", interval='day', has_time_col=True):
    interval = time_to_row(interval)
    grouped_df = pd.DataFrame()   
    for i in range(0,len(df)//interval):
        if has_time_col: start_date = df['time'][i*interval]
        block = df.iloc[ i*interval:(i+1)*interval, : ]
        # Perform Computation on Row
        if method == "sum": block = block.sum(axis=0)
        elif method == "mean": block = block.mean(axis=0)
        elif method == "min": block = block.min(axis=0)
        elif method == "max": block = block.max(axis=0)
        else:
            print("Invalid Method Entry")
            return
        # Add the Start Date Label
        if has_time_col:
            if method == "mean": block = pd.Series([start_date]).append(block)  
            else: block[0] = start_date
        block = block.to_frame().transpose()
        grouped_df = grouped_df.append(block)
    if method == "mean" and has_time_col: grouped_df = grouped_df.rename(columns={ grouped_df.columns[0]: "time" })
    return grouped_df

# Create Training Data
def training_data(df, start_date, y=None, num_days=7, num_min=0, bldgs=None, method="mean", agg_interval='hour',
                  time_interval="day", has_time_col=True):
    # Slice Data by Time and Buildings
    X = slice_df(start_date, num_days, num_min, bldgs, df)
    X = X.rename(columns={ X.columns[0]: "time" })
    # Aggregate Data on Interval
    X = group_df(method=method, interval=agg_interval, has_time_col=False, df=X)
    if has_time_col: X = X.drop(columns=['time'])
    # Determine Shape of New Dataframe and Reshape
    new_col_ct = int(time_to_row(time_interval)/time_to_row(agg_interval))
    rows_per_instance = int(X.shape[0]/new_col_ct)
    X = X.T.values.reshape(X.shape[1] * rows_per_instance, new_col_ct)
    # Return X or both X and updated y if y is given
    if y == None: return pd.DataFrame(X)
    updated_y = []
    for i in y:
        for j in range(0, rows_per_instance): updated_y.append(i)
    return pd.DataFrame(X), updated_y