from pslog import LOG
import matplotlib.pyplot as plt

log = LOG('test2', True)

log.make_title()

log.message('back to text')

log.start_capture()

print('capturing print 1')

print('another line')

log.end_capture()

print('not captured')

log.save(pdf=True)
