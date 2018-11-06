def readSoliloquy():
    with open("dataset/soliloquy.txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    return data

def readSchedule(date):
    task_list = []
    time_list = []
    with open("schedule/schedule"+date+".txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    for i in data:
        try:
            task,time = i.split(";")
            task = task.split(",")
            task_list.append(task)
            time_list.append(time)
        except:
            continue
    return task_list,time_list
    
def readCommand():
    commandList = []
    with open("dataset/command.txt", "r") as f:
        data = f.read()
    data = data.split("\n") 
    for i in data:
        description,command,no,useImg = i.split(",")
        commandList.append( (description,command,no,useImg) )
    return commandList