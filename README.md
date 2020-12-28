# videoflow-factory


*videoflow-factory* is a library for dynamically generating [Videoflow](https://github.com/videoflow/videoflow) DAGs from YAML configuration files.
- [videoflow-factory](#videoflow-factory)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Benefits](#benefits)
  - [Contributing](#contributing)

## Installation

To install *videoflow-factory* run `pip install videoflow-factory`. It requires Python 3.6.0+ and Videoflow.

## Usage

After installing *videoflow-factory* in your environment, there are two steps to creating DAGs. First, we need to create a YAML configuration file. For example:

```yaml
od_flow:
  description: "Fynd Trak: MD & OD to Cache Flow"
  owner: "Kaushik B"
  tasks:
    reader:
      operator: videoflow.producers.VideoFileReader
      node: Producer
      arguments:
        video_file: "./videos/abc_xyz.mp4"
    frame:
      operator: videoflow.processors.basic.FrameIndexSplitter
      node: Processor
      dependencies: [reader]
    od_key:
      operator: videoflow.processors.KeyGenerator
      node: Processor
      arguments:
        store_id: "abc"
        video_id: "abc"
        prefix: "od"
      dependencies: [reader]
    motion_detector:
      operator: videoflow.processors.detector.motion_detector.OpencvMotionDetector
      node: Processor
      dependencies: [frame]
    object_detector:
      operator: videoflow.processors.detector.AsyncObjectDetector
      node: Processor
      arguments:
        url: "https://sample.url.com/api/v1/predict"
        nb_concurrent_tasks: 500
        gradual_increase_task: True
      dependencies: [frame]
    od_md_result_generator:
      operator: videoflow.processors.OdMdResultGenerator
      node: Processor
      dependencies: [motion_detector, object_detector]
    redis_cache:
      operator: videoflow.cache.RedisCache
      node: Consumer
      dependencies: [od_key, od_md_result_generator]
```

Then create a python script like this:

```python
from videoflow_factory import VideoflowFactory
import os

od_flow_config = os.path.abspath("./od_flow.yaml")

od_flow = VideoflowFactory(od_flow_config)()

od_flow.run()
od_flow.join()
```

And this DAG will be generated and the Flow will start running!


## Benefits

* Construct DAGs without knowing Python
* Construct DAGs without learning Airflow primitives
* Avoid duplicative code
* Everyone loves YAML! ;)

## Contributing

Contributions are welcome! Just submit a Pull Request or Github Issue.