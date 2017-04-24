# coding: utf-8
import logging


__all__ = (
    'Message',

    'EMailService',
    'InterGalaxyService'
)


log = logging.getLogger('post_service')


class Message(object):
    def __init__(self, text, service):
        self.text = text
        self.service = service

    def send(self):
        self.service.send(self.text)


class BasePostService(object):
    def send(self, message):
        raise NotImplementedError


class EMailService(BasePostService):
    def send(self, message):
        log.info(message)


class InterGalaxyService(BasePostService):
    def __init__(self, galaxy):
        self.galaxy = galaxy

    def send(self, message):
        self.galaxy.send(message)
