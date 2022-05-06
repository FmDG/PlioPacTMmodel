%% Import the dataset

KM2_data = readtable("data/bounding_data/KM2.csv");
modern_oceans = readtable("data/modern_oceans.csv");

%% Print KM2 Data

% Adds a path to the minimum bounding triangle function
addpath("MinBoundSuite/MinBoundSuite")

[tx,ty] = minboundtri(modern_oceans.d18O,modern_oceans.d13C);
plot(modern_oceans.d18O,modern_oceans.d13C,'r+',tx,ty,'b-')
text(modern_oceans.d18O + 0.01, modern_oceans.d13C + 0.01, modern_oceans.Core, 'Fontsize', 10);

%% Plot geospatial data

scatter(modern_oceans.latitude, modern_oceans.longitude)
text(modern_oceans.latitude + 0.1, modern_oceans.longitude + 0.1, modern_oceans.Core, 'Fontsize', 10);


