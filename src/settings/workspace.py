'''
Created on Feb 26, 2019

@author: xbbntni
'''
import json
from datetime import date
import time


class Project():

    def __init__(self, projectPath=None,):
        self.projectPath = projectPath  # directory path in system
        self.natures = list()  # java, javascript, python
    
    def addNature(self, nature=None):
        self.natures.append(nature)


class Workspace():

    def __init__(self, workspacePath=None):
        self.workspacePath = workspacePath
        self.projects = list()
        self.active = True
        self.createdOn = date.today()

    def addProject(self, project=None):
        self.projects.append(project)


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


class Setting():

    def __init__(self):
        pass


if __name__ == '__main__':
    workspace = Workspace(workspacePath=r'C:\Users\xbbntni\eclipse-workspace')
    project = Project(projectPath=r'c:\1\sql_editor')
    project.addNature(nature='python')
    project = Project(projectPath=r'c:\1\sql_editor')
    project.addNature(nature='python')
    workspace.addProject(project)
    
    js = json.dumps(workspace.__dict__, sort_keys=True, indent=4, default=serialize)
    print(js)
