%% Import the dataset

% Read the dataset of Pacific points
pacific = readtable("data/pacific_modern.csv");

% Calculate the mean and the distance from the mean for every point in the
% pacific database.
A = ones(height(pacific), 2);
A = A .* [mean(pacific.d18O) mean(pacific.d13C)];
B = [pacific.d18O pacific.d13C];
dist  = sqrt(sum((A' - B') .^ 2));

% Add the distance parameter to the table and then select all those points
% that fall within the percentile
pacific = [table(dist', 'VariableNames', {'distance'})  pacific];

figure_no = 1;



for i = 60:5:95
    % This selects the percentile of objects by their distance from the mean
    % point in oxygen carbon space.
    percentile = i;
    
    limit = prctile(dist, percentile);
    pacificSelected = pacific(pacific.distance < limit, :);
    
        % Adds a path to the minimum bounding triangle function
    addpath("MinBoundSuite/MinBoundSuite")
    
    % Plot the bounding triangle that describes this resulting function.
    figure(figure_no);
    figure_no = figure_no + 1;
    [tx,ty] = minboundtri(pacificSelected.d18O, pacificSelected.d13C);
    % plot(pacificSelected.d18O, pacificSelected.d13C,'r+',tx,ty,'b-');

    figure(12)
    plot(tx, ty)
    hold on

end


figure(12)
scatter(pacific.d18O, pacific.d13C, "Marker", "+")
legend(["60th", "65th", "70th", "75th", "80th", "85th", "90th", "95th", "Data"]);
xlim([0, 5.5])

%%

for i = 1:6
    selection = endmembers(1, :);


end