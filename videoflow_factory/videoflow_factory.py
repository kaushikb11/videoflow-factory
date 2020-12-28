import os
from typing import Any, Dict, Union
import yaml
from videoflow_factory.flowbuilder import FlowBuilder


class VideoflowFactory:
    def __init__(self, config_filepath: str) -> None:
        videoflow_factory._validate_config_filepath(config_filepath=config_filepath)
        self.config_filepath: str = config_filepath
        self.config: Dict[str, Any] = videoflow_factory._load_config(
            config_filepath=config_filepath
        )

    @staticmethod
    def _validate_config_filepath(config_filepath: str) -> None:
        """
        Validates config file path is absolute
        """
        if not os.path.isabs(config_filepath):
            raise Exception("videoflow_factory `config_filepath` must be absolute path")

    @staticmethod
    def _load_config(config_filepath: str) -> Dict[str, Any]:
        """
        Loads YAML config file to dictionary
        :returns: dict from YAML config file
        """
        try:
            config: Dict[str, Any] = yaml.load(
                stream=open(config_filepath, "r"), Loader=yaml.FullLoader
            )
        except Exception as err:
            raise Exception(f"Invalid videoflow_factory config file; err: {err}")
        return config

    def __call__(self):
        for flow_name, flow_config in self.config.items():
            flow_builder: FlowBuilder = FlowBuilder(name=flow_name, config=flow_config)
            try:
                flow = flow_builder.build()
            except Exception as err:
                raise Exception(
                    f"Failed to generate flow {flow_name}. verify config is correct. err:{err}"
                )
        return flow
