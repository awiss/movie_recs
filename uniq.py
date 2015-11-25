with open('movies', 'r') as f:
    with open('movies_unique', 'w') as f2:
        lines = f.readlines()
        existing = set()
        for line in lines:
            id = line.split('\t')[0]
            if id not in existing:
                f2.write(line + '\n')
                existing.add(id)
            else:
                print "duplicate"
