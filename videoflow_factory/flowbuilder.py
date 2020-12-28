from typing import Any, Callable, Dict, List, Union
from videoflow_factory.utils import import_string
from videoflow.core import flow
from videoflow.core.constants import BATCH


class FlowBuilder:
    def __init__(self, name: str, config: Dict[str, Any]) -> None:
        self.name: str = name
        self.config: Dict[str, Any] = config
        self._producers = []
        self._consumers = []
        self.tasks_dict = {}

    def build(self):
        tasks = self.config["tasks"]
        for task, task_conf in tasks.items():
            self.make_node(task, task_conf)

        for task, task_conf in tasks.items():
            node = task_conf["node"]
            if node == "Producer":
                self.tasks_dict[task] = task_conf["instance"]()
                self._producers.append(self.tasks_dict[task])
            else:
                dependencies = task_conf["dependencies"]
                tasks_deps = {dep: self.tasks_dict[dep] for dep in dependencies}
                self.tasks_dict[task] = task_conf["instance"](*tasks_deps.values())
                if node == "Consumer":
                    self._consumers.append(self.tasks_dict[task])

        auto_flow = flow.Flow(self._producers, self._consumers, flow_type=BATCH)
        return auto_flow

    def make_node(self, task, task_conf):
        node = task_conf["node"]
        operator = task_conf["operator"]
        arguments = task_conf.get("arguments", {})
        try:
            operator_obj = import_string(operator)
        except Exception as err:
            raise Exception(f"Failed to import operator: {operator}. err: {err}")

        task_conf["instance"] = operator_obj(**arguments)
        self.tasks_dict[task] = operator_obj(**arguments)
