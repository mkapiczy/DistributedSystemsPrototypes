import itertools
from random import randint, choice
from time import sleep

processList = ["proc1", "proc2", "proc3", "proc4", "proc5"]
jobsList = ["job1", "job2", "job3", "job4", "job5", "job6", "job7", "job8", "job9", "job10"]
doneJobs = []
roundRobin = itertools.cycle(processList)

def executeJob(job, processToExecute, assignedProcessorTime):
    print("Job " + job + " is beeing executed by " + processToExecute)
    sleep(assignedProcessorTime)
    print("Job " + job + " executed by " + processToExecute)

while len(doneJobs) < len(jobsList):
    processToExecute = next(roundRobin)
    jobTobeExecuted = choice(jobsList)
    assignedProcessorTime = randint(0, 10)
    executeJob(jobTobeExecuted, processToExecute, assignedProcessorTime)
    doneJobs.append(jobTobeExecuted)

print('All jobs done')


