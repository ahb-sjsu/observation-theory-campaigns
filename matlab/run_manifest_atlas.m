function run_manifest_atlas(manifestPath, outputDirectory)
%RUN_MANIFEST_ATLAS Run a CSV manifest on Atlas using parfor when available.
arguments
    manifestPath (1,1) string
    outputDirectory (1,1) string
end

manifest = readtable(manifestPath,'TextType','string');
if ~isfolder(outputDirectory)
    mkdir(outputDirectory);
end
n = height(manifest);
results = cell(n,1);

hasParallel = license('test','Distrib_Computing_Toolbox') ...
    && ~isempty(ver('parallel'));
if hasParallel
    pool = gcp('nocreate');
    if isempty(pool)
        parpool('Processes');
    end
    parfor k = 1:n
        results{k} = pf.run_toy_row(manifest(k,:));
    end
else
    for k = 1:n
        results{k} = pf.run_toy_row(manifest(k,:));
    end
end

for k = 1:n
    record = results{k};
    record.manifest_row = table2struct(manifest(k,:));
    record.generated_utc = char(datetime('now','TimeZone','UTC', ...
        'Format','yyyy-MM-dd''T''HH:mm:ss.SSSXXX'));
    payload = jsonencode(record,'PrettyPrint',true);
    filename = fullfile(outputDirectory, record.scenario_id + ".json");
    fid = fopen(filename,'w');
    cleaner = onCleanup(@() fclose(fid));
    fwrite(fid,payload,'char');
    clear cleaner;
end
fprintf('Wrote %d records to %s\n',n,outputDirectory);
end
