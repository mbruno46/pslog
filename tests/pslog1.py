from pslog import LOG
import matplotlib.pyplot as plt

log = LOG()

log.make_title()

log.message('Section 1')
for i in range(10):
    log.message(f"line {i} ads adf df dssf ")

plt.figure()
plt.plot([1, 2, 3])
log.pyplot_figure(plt)

log.message('back to text')

log.start_capture()

print('capturing print 1')
print('capturing print 2')

log.end_capture()

print('not captured')

log.save('test', pdf=True)
