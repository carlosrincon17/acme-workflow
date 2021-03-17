
class WorkFlowException(Exception):

    def __init__(self, error, details):
        self.message = "Error: {}. Details: {}".format(error, details)
        super().__init__(self, self.message)


class StepNotFoundException(Exception):

    def __init__(self, step_name):
        self.message = "There step {} does not exists. Please verify your workflow".format(step_name)
        super().__init__(self, self.message)


class ActionNotFoundException(Exception):

    def __init__(self, action):
        self.message = "Action {} was not found.".format(action)
        super().__init__(self, self.message)


class UnauthorizedException(Exception):

    def __init__(self):
        self.message = "The user or pin is wrong, please verify them and try again."
        super().__init__(self, self.message)


class InsufficientFundsError(Exception):

    def __init__(self):
        self.message = "Insufficient funds error"
        super().__init__(self, self.message)
