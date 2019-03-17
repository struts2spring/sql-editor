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
        self.workspaces = list()
        self.maxWorkspace = 10  # maximum number of workspaces
        self.showWorkspaceSelectionDialog = True

    def showWorkspaceSelection(self):
        showDialog = True
        if any([workspce.active for workspce in self.workspaces]):
            showDialog = False
        return showDialog

    def addWorkspace(self, workspace=None):
        for workspce in self.workspaces:
            workspce.active = False
        if len(self.workspaces) > self.maxWorkspace:
            self.workspaces[0] = workspace
        else:
            self.workspaces.append(workspace)
        self.showWorkspaceSelectionDialog = self.showWorkspaceSelection()

    def getActiveWorkspace(self):
        workspce = None
        for workspce in self.workspaces:
            if workspce.active:
                workspce = workspce
                break
        return workspce

    def loadSettings(self):
        workspace = Workspace(workspacePath=r'C:\Users\xbbntni\eclipse-workspace')
        project = Project(projectPath=r'/docs/work/python_project/sql_editor')
        project.addNature(nature='python')
        workspace.addProject(project)
        project = Project(projectPath=r'c:\1\sql_editor')
        project.addNature(nature='python')
        workspace.addProject(project)

#         settings = Setting()
        self.addWorkspace(workspace)


if __name__ == '__main__':

    settings = Setting()
    settings.loadSettings()

    js = json.dumps(settings, sort_keys=True, indent=4, default=serialize)
    print(js)
