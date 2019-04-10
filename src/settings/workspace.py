'''
Created on Feb 26, 2019

@author: xbbntni
'''
import json, os
import time
from datetime import date


def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """
    serial = None
    if isinstance(obj, date):
        serial = obj.isoformat()
    else:
        serial = obj.__module__

    #  Populate the dictionary with object meta data 
    obj_dict = {
      "__class__": obj.__class__.__name__,
      "__module__": serial
    }
    
    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)
    
    return obj_dict


def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")
        
        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")
        
        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)
        
        # Get the class from the module
        class_ = getattr(module, class_name)
        
        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj


class Project():

    def __init__(self, basePath=None, projectDirName=None, projectName=None, natures=list()):
        self.basePath = basePath
        self.projectName = projectName
        self.projectDirName = projectDirName
#         self.projectPath = os.path.join(basePath, projectDirName)  # directory path in system
        self.natures = natures  # java, javascript, python

    def addNature(self, nature=None):
        self.natures.append(nature)

    def __repr__(self):
        return f'{{basePath:{self.basePath},projectName:{self.projectName},projectDirName:{self.projectDirName}}}'


class Workspace():

    def __init__(self, workspacePath=None, projects=list(), active=True):
        self.workspacePath = workspacePath
        self.projects = projects
        self.active = active
#         self.createdOn = date.today()

    def addProject(self, project=None):
        self.projects.append(project)

    def removeProject(self, projectName=None):
        for project in self.projects:
            if project.projectName == projectName:
                self.projects.remove(project)
                break

    def __repr__(self):
        return f'{{workspacePath:{self.workspacePath},active:{self.active},projects:{self.projects},createdOn :{self.createdOn}}}'

# def serialize(obj):
#     """JSON serializer for objects not serializable by default json code"""
# 
#     if isinstance(obj, date):
#         serial = obj.isoformat()
#         return serial
# 
#     return obj.__dict__


class Setting():

    def __init__(self, workspaces=list(), maxWorkspace=10, showWorkspaceSelectionDialog=True):
        self.workspaces = workspaces
        self.maxWorkspace = maxWorkspace  # maximum number of workspaces
        self.showWorkspaceSelectionDialog = showWorkspaceSelectionDialog
#         self.loadSettings()
#         self.activeWorkspace = self.getActiveWorkspace()

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
        project = Project(basePath=r'/docs/work/python_project', projectDirName='sql_editor')
        project.addNature(nature='python')
        workspace.addProject(project)
        project = Project(basePath=r'c:\1', projectDirName='sql_editor')
        project.addNature(nature='python')
        workspace.addProject(project)

#         settings = Setting()
        self.addWorkspace(workspace)

#     def write(self):
#         with open('user.json', 'w') as file:
#             json.dump(self, file, sort_keys=True, indent=4)
        
    def loadJsonSettings(self):
        self.loadSettings()
        
#         with open('dumpFile.txt', 'r') as file:
#             settingData = json.loads(file)
# #             setting_data=json.loads(file, object_hook=dict_to_obj)
#         va=str(settingData)
#         try:
#             dataform = str(settingData).strip("'<>()[]\"` ").replace('\'', '\"')
# #             struct = json.loads(dataform)
#             struct=json.loads(dataform, object_hook=dict_to_obj)
#         except Exception as e:
#             print(e)
#         print(settingData)
#         print('hi')

    def __repr__(self):
        return f'Setting:{{workspaces:{self.workspaces},maxWorkspace:{self.maxWorkspace},showWorkspaceSelectionDialog:{self.showWorkspaceSelectionDialog},activeWorkspace :{self.activeWorkspace}}}'


if __name__ == '__main__':

    settings = Setting()
    settings.loadJsonSettings()
#     settings.write()
#     print(settings)
#     settings.loadSettings()
# 
    with open('settings.json', 'w') as file:
        js = json.dump(settings, file, sort_keys=True, indent=4, default=convert_to_dict)
    with open('settings.json', 'r') as json_file:
        settingData = json.load(json_file)
    dataform = settingData.__str__().strip("'<>() ").replace('\'', '\"')
    dataform = dataform.replace('None', 'null')
    dataform = dataform.replace('True', 'true')
    dataform = dataform.replace('False', 'false')
    print(dataform)
    settings_reloaded=json.loads(dataform, object_hook=dict_to_obj)
    print('compltet')
        
