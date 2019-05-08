# Description
pyconcourse lets you talk to the Concourse API with Python.

This library implements a major subset of all the [API calls](https://github.com/concourse/concourse/blob/master/atc/routes.go) in Concourse.

# Usage
You can either use this library without installation like this:
```python3
import sys

sys.path.append('full_path_to_this library')
import pyconcourse
```
Or you can install it permanently:
```shell
python3 -m pip install --user "<full_path_to_this library>" pyconcourse
```

# Examples
```python3
import pyconcourse

ci = pyconcourse.API('https://cconcourse.example.com', 'username', 'password')

# Print all pipelines
for pipeline in ci.list_pipelines():
  print(pipeline['name'])

# Print all jobs of a pipeline
for job in ci.list_jobs('example_pipeline'):
  print(job['name'])
```

For a full list of available calls, use in Python
```python3
help(pyconcourse.API)
```
