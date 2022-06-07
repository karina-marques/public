% Calculate the best fit theta for each DEM in a directory using TopoToolbox.
% June 7, 2022.

dirData = dir('**/*.tif');
fileNames = strings(1, length(dirData));
for index = 1:length(dirData)
    fileNames(index) = dirData(index).name;
end

mn = zeros(1, length(fileNames));
for index = 1:length(fileNames)
    DEM = GRIDobj(char(fileNames(index))); 
    DEM = inpaintnans(DEM);
    FD = FLOWobj(DEM,'preprocess','carve');
    A = flowacc(FD);
    S = STREAMobj(FD,'minarea',1e6,'unit','map');
    mn(index) = mnoptimvar(S,DEM,A,'varfun',@robustcov,'plot',false);
end

for index = 1:length(fileNames)
    [FILEPATH,NAME,EXT] = fileparts(fileNames(index));
    fileNames(index) = NAME;
end

datatable = array2table(mn);
datatable.Properties.VariableNames(1:length(fileNames)) = fileNames;
writetable(datatable, 'mn_basins.xlsx');