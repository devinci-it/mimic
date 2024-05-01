import glob
def expand_wildcards(data_files):
    expanded_data_files = []
    for dir, files in data_files:
        expanded_files = []
        for file in files:
            if '*' in file:
                expanded_files.extend(glob.glob(file))
            else:
                expanded_files.append(file)
        expanded_data_files.append((dir, expanded_files))
    return expanded_data_files

