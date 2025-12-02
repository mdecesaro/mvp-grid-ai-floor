class ExecutorManager:
    def __init__(self, executor):
        self.executor = executor
        self.plan = None
        
    def set_executor(self, executor):
        self.executor = executor
        
    def is_ready(self):
        return self.executor.is_ready()

    def load_plan(self, plan):
        if not self.executor:
            raise RuntimeError("Nenhum executor definido.")
        self.executor.set_plan(plan)

    def start(self):
        if not self.executor:
            raise RuntimeError("Nenhum executor definido.")
        self.executor.execute()