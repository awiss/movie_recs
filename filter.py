with open('movies', 'r') as f:
    with open('filtered', 'w') as f2:
        for line in f:
            spl = line.split('\t')
            if spl[6] and spl[6] != 'NULL' and int(spl[6]) >= 0:
                print line
                f2.write(line)
