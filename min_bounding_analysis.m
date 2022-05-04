%% Import the dataset

prism_data = readtable("data/prism_data.csv");

%% Select only the '3500 ka - M2' data

list_time_periods = ['3500 ka - M2' 'M2' 'mPWP-1' 'KM2' 'mPWP-2' ...
    'G20' 'G20 - 2800 ka'];

match = list_time_periods(1);
selectorate = prism_data(matches(prism_data.TimePeriod, match),:);

scatter(selectorate.d18O, selectorate.d13C)





