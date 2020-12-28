from videoflow_factory import VideoflowFactory
import os
import logging

logging.basicConfig(level=logging.INFO)

od_flow_config = os.path.abspath("./od_flow.yaml")

od_flow = VideoflowFactory(od_flow_config)()

od_flow.run()
od_flow.join()
