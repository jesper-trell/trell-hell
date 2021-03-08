from nameko.rpc import rpc
from os import system


class GreetingService:
    name = "uploadlistener"

    @rpc
    def start(self):
        system('python manage.py uploadlistener &')
        return "Started the Django uploadlistener service."
