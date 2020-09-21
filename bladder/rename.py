# rename bladder cases

import os

originalDir = 'D:/bladder_data/FGFR3W'
#newDir = 'D:/bladder_data/renamed'

#if not os.path.exists(newDir):
    #os.mkdir(newDir)

for dn in os.listdir(originalDir):
    for fn in os.listdir(originalDir + '/' + dn):
        new_fn = fn.replace('01Z', '01A')
        os.rename(os.path.join(originalDir + '/' + dn, fn), os.path.join(originalDir + '/' + dn, new_fn))
    new_dn = dn.replace('01Z', '01A')
    os.rename(os.path.join(originalDir, dn), os.path.join(originalDir, new_dn))
