from iron_worker import *

worker = IronWorker()

task = Task(code_name="link_checker")
task.run_every = 86400
task.scheduled = True
response = worker.queue(task)