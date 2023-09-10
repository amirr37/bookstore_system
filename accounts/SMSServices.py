from abc import ABC, abstractmethod
from accounts.circuit_breaker import CircuitBreaker
from accounts.otp_utils import generate_otp


class AbstractService(ABC):
    def __init__(self, service_name):
        self.service_name = service_name
        self.circuit_breaker = CircuitBreaker(service_name=self.service_name)

    @abstractmethod
    def execute(self, request) -> bool:
        pass


class OTPSMSService1(AbstractService):
    def __init__(self, service_name='service1'):
        super().__init__(service_name)

    def execute(self, request):
        otp_request = generate_otp(request)
        # Replace this with your actual SMS sending code for Service
        is_send_message_success = True
        print(otp_request.otp_code)
        print(self.service_name)

        if is_send_message_success:
            return True
        else:
            self.circuit_breaker.increment_failures()
            return False


class OTPSMSService2(AbstractService):
    def __init__(self, service_name='service2'):
        super().__init__(service_name)

    def execute(self, request):
        otp_request = generate_otp(request)
        # Replace this with your actual SMS sending code for Service
        is_send_message_success = True
        print(otp_request.otp_code)
        print(self.service_name)
        if is_send_message_success:
            return True
        else:
            self.circuit_breaker.increment_failures()
            return False


class OTPSMSService3(AbstractService):
    def __init__(self, service_name='service1'):
        super().__init__(service_name)

    def execute(self, request):
        otp_request = generate_otp(request)
        # Replace this with your actual SMS sending code for Service
        is_send_message_success = True
        print(otp_request.otp_code)
        print(self.service_name)
        if is_send_message_success:
            return True
        else:
            self.circuit_breaker.increment_failures()
            return False
