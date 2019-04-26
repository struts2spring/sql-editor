from src.dao.workspace.WorkspaceDao import WorkspaceDatasource


class WorkspaceHelper():

    def __init__(self):
        datasource = WorkspaceDatasource()
        self.workspace = datasource.findActiveWorkspace()

    def getWorkpacePath(self):
        return self.workspace.workspacePath
    
    def getLibraryPath(self):
        libraryPath = None
        self.workspace
        for workspaceSetting in self.workspace.workspace_setting_assoc:
            if workspaceSetting.setting.name == 'BOOK_LIBRARY':
                libraryPath = workspaceSetting.setting.value
                break
        return libraryPath
        

if __name__ == '__main__':
    workspaceHelper = WorkspaceHelper()
    libraryPath = workspaceHelper.getLibraryPath()
    print(libraryPath)
