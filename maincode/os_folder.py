import os


for k in range(3):
    for m in range(3):
        for l in range(3):
            for n in range(3):

                path = f"C:\\Users\\alexsey\\Desktop\\диплом\\test\\k = {k}, m = {m}, l = {l}, n = {n}"
                try:
                    os.mkdir(path)
                except OSError:
                    print ("Creation of the directory %s failed" % path)
                else:
                    print ("Successfully created the directory %s " % path)

