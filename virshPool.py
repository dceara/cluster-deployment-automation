from typing import Optional

import host
from logger import logger


class VirshPool:
    def __init__(self, name: str, host: host.Host, *, image_path: Optional[str] = None):
        self._host = host
        self._name = name
        self._image_path = image_path

    def __str__(self) -> str:
        return f"{self._name}@{self._host.hostname()}"

    def name(self) -> str:
        return self._name

    def image_path(self) -> Optional[str]:
        return self._image_path

    def initialized(self) -> bool:
        cmd = f"virsh pool-info {self._name}"
        return self._host.run(cmd).returncode == 0

    def ensure_initialized(self) -> None:
        if not self.initialized():
            self.initialize()
        else:
            logger.info(f"virsh-pool[{self}]: Pool {self._name} already initialized (image-path={self._image_path})")

    def _host_run(self, cmd: str) -> None:
        self._host.run(cmd)

    def remove(self) -> None:
        self._host_run(f"virsh pool-destroy {self._name}")
        self._host_run(f"virsh pool-undefine {self._name}")

    def ensure_removed(self) -> None:
        if self.initialized():
            self.remove()

    def initialize(self) -> None:
        if not self._image_path:
            raise RuntimeError("The VirshPool is created without an image path and cannot be initialized")

        logger.info(f"virsh-pool[{self}]: Initializing pool {self._name} at {self._image_path}")
        self._host_run(f"virsh pool-define-as {self._name} dir - - - - {self._image_path}")
        self._host_run(f"mkdir -p {self._image_path}")
        self._host_run(f"chmod a+rw {self._image_path}")
        self._host_run(f"virsh pool-start {self._name}")
        logger.info(f"virsh-pool[{self}]: Pool initialized")
