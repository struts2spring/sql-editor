from src.dao.workspace.WorkspaceDao import WorkspaceDatasource


class WorkspaceHelper():

    def __init__(self):
        datasource = WorkspaceDatasource()
        self.workspace = datasource.findActiveWorkspace()

    def getWorkpacePath(self):
        return self.workspace.workspacePath