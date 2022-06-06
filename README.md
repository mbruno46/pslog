# pslog
A Python utility to create Postscript log files

### Authors

Copyright (C) 2022, Mattia Bruno

## Installation

To install the library directly in your local python distribution,
simply run

```bash
pip install git+https://github.com/mbruno46/pslog.git@main
# or for upgrading
pip install -U git+https://github.com/mbruno46/pslog.git@main
```

After installation, `pyobs` can be imported like any other package 

## Documentation

Learn by examples.

```python
import pslog
import matplotlib.pyplot as plt

log = pslog.LOG()

log.make_title()

log.message('Section 1')
for i in range(10):
    log.message(f"line {i} ads adf df dssf ")

plt.figure()
plt.plot([1, 2, 3])
log.pyplot_figure(plt)

log.message('back to text')

log.start_capture()
print('capturing print')
log.end_capture()

print('not captured')

log.save('test', pdf=True)
```
