import time


from agents.base_agent import BaseAgent


class TestAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="Test Agent",
            description="Framework test."
        )

    def execute(self):

        self.logger.info("Doing some work...")

        time.sleep(3)

        self.update_metric("rows", 100)

        self.logger.info("Finished work.")

        return "Success"