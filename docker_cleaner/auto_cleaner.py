import docker

import re
import time
import logging
from datetime import datetime

import logger


def loop(func):
    def wrapper(self, *args, **kwargs):
        if self.timeout is not None:
            while True:
                func(self, *args, **kwargs)
                time.sleep(self.timeout * 60)
        else:
            func(self, *args, **kwargs)
        return
    return wrapper


class AutoCleaner(object):
    def __init__(self, timeout=None, force=[], version="auto", oldest=0,
                 images_include=[], volumes_include=[],
                 images_exclude=[], volumes_exclude=[],
                 filelog=None):
        global log

        if "log" not in globals():
            if filelog is not None:
                log = logging.getLogger(__name__)
                log.addHandler(logger.FileHandler(filelog))
                log.setLevel(logging.DEBUG)
            else:
                log = logging.getLogger(__name__)
                log.addHandler(logger.StreamHandler())
                log.setLevel(logging.DEBUG)

        self.docker_client = docker.DockerClient(version=version)
        self.i_force = True if "image" in force or "all" in force else False
        self.v_force = True if "volume" in force or "all" in force else False
        self.timeout = int(timeout) if timeout is not None else None
        self.oldest = int(oldest)
        self.images_include = images_include
        self.volumes_include = volumes_include
        self.images_exclude = images_exclude
        self.volumes_exclude = volumes_exclude

    @loop
    def clean(self):
        try:
            self.docker_client.images.prune()
            log.info("Images pruned successfully")
        except Exception as ex:
            log.warning("Can't prune images")
        images = self.docker_client.images.list(all=True)

        filtered_images = [el for el in images if any(
            map(lambda x: x in str(el), self.images_include))]
        filtered_images = [el for el in filtered_images if not any(
            map(lambda x: x in str(el), self.images_exclude))]

        for image in filtered_images:
            time_diff = datetime.now() - \
                datetime.fromtimestamp(image.attrs["Created"])
            if time_diff.seconds / 60 > self.oldest:
                try:
                    self.docker_client.images.remove(image.id,
                        force=self.i_force)
                    log.info("{} image removed successfully".format(image.id))
                except Exception as ex:
                    log.warning("Can't remove image {}".format(image.id))

        try:
            volumes = self.docker_client.volumes.prune()
            log.info("Volumes pruned successfully")
        except Exception as ex:
            log.warning("Can't prune volumes")
        volumes = self.docker_client.volumes.list()

        filtered_volumes = [el for el in images if any(
            map(lambda x: x in str(el), self.volumes_include))]
        filtered_volumes = [el for el in filtered_volumes if not any(
            map(lambda x: x in str(el), self.volumes_exclude))]

        for volume in filtered_volumes:
            try:
                volume.remove(force=self.v_force)
                log.info("{} volume removed successfully".format(volume.id))
            except Exception as ex:
                log.warning("Can't remove volume {}".format(volume.id))

