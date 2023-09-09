import random

from rest_framework.views import APIView


class SMSSender:
    def __init__(self, *services: APIView):
        self.all_services = list(services)

    def get_random_service(self) -> APIView:
        if not self.all_services:
            raise ValueError("there is no service")

        available_services = [service for service in self.all_services if not service.circuit_breaker.is_open()]
        print(available_services)
        if not available_services:
            raise ValueError("All services are unavailable")

        return random.choice(available_services)
