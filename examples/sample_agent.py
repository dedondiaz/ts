class SampleAgent:
    def propose(self, state):
        return {"price": 15.0}


def get_agent():
    return SampleAgent()
