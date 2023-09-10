import random

from rest_framework.views import APIView

from accounts.SMSServices import AbstractService


class SMSSender:
    def __init__(self, *services: AbstractService):
        self.all_services = list(services)

    def execute(self, request):
        max_attempts = self.count_available_services()  # Define the maximum number of retry attempts
        for _ in range(max_attempts):
            service: AbstractService = self.get_random_service()
            send_message_success: bool = self.try_service(service, request)
            if send_message_success :
                return True
        return False

    def get_random_service(self):
        if not self.all_services:
            raise ValueError("No services available.")

        available_services = [service for service in self.all_services if not service.circuit_breaker.is_open()]

        if not available_services:
            raise ValueError("All services are open.")

        return random.choice(available_services)

    def try_service(self, service: AbstractService, request) -> bool:
        return service.execute(request)

    def count_available_services(self):

        # return len([service for service in self.all_services if not service.circuit_breaker.is_open()])
        return 10
