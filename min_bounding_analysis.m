%% Import the dataset

KM2_data = readtable("data/bounding_data/KM2.csv");
prism_data = readtable("data/prism_data.csv");
full_data = readtable("data/full_dataset.csv");
modern_oceans = readtable("data/modern_oceans.csv");

prism_data = rmmissing(prism_data);
full_data = rmmissing(full_data);
modern_oceans = rmmissing(modern_oceans);

%% Print KM2 Data

% Adds a path to the minimum bounding triangle function
addpath("MinBoundSuite/MinBoundSuite")

[tx,ty] = minboundtri(modern_oceans.d18O, modern_oceans.d13C);
plot(modern_oceans.d18O, modern_oceans.d13C,'r+',tx,ty,'b-')
% text(modern_oceans.d18O + 0.01, modern_oceans.d13C + 0.01, modern_oceans.Core);

