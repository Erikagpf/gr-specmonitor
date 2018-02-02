
def init():
    """ Initialize global variables """
    global registered_tasks
    registered_tasks = {}
    global task_dependency_tree
    task_tree = {}

def register_task_handler(name, ClassPtr):
    registered_tasks[name] = ClassPtr

def retrieve_task_handler(name):
    return registered_tasks[name]

def retrieve_task_handlers():
    return registered_tasks

def set_task_dependency_tree(dtree):
    assert isinstance(dtree,dict)
    global task_tree
    task_tree = dtree

def get_task_dependency_tree():
    return dict(task_tree)