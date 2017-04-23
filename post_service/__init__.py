# coding: utf-8

__all__ = (
    'Message',

    'EMailService',
    'InterGalaxyService'
)


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
        print message


class InterGalaxyService(BasePostService):
    def __init__(self, galaxy):
        self.galaxy = galaxy

    def send(self, message):
        self.galaxy.send(message)
