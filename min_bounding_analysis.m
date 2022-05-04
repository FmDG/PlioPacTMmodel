%% Import the dataset

KM2_data = readtable("data/bounding_data/KM2.csv");

%% Print KM2 Data

x = KM2_data.d18O;
y = KM2_data.d13C;

[tx,ty] = minboundtri(x,y);
plot(x,y,'r+',tx,ty,'b-')
text(KM2_data.d18O + 0.01, KM2_data.d13C + 0.01, KM2_data.Site, 'Fontsize', 10);




