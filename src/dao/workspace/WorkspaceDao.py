'''
Created on 02-Dec-2015

@author: vijay
'''

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine
from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import os
import sys
import sqlalchemy
# from src.dao.Author import Author
# from src.dao.AuthorBookLink import AuthorBookLink
import json
# from src.dao.Book import Base, Book
# from src.dao.Book import engine
from src.dao.workspace.WorksapaceEntities import Base, Project, Workspace, WorkspaceSettingLink, Setting, ProjectWorkspaceLink
import shutil
import traceback
# from src.static.constant import Workspace
import datetime
# from src.static.SessionUtil import SingletonSession
from os.path import expanduser
import logging
# from build.lib.src.view.util.FileOperationsUtil import data

logger = logging.getLogger('extensive')

# if os.path.exists(Workspace().libraryPath):
#     os.chdir(Workspace().libraryPath)
#     listOfDir = os.listdir(Workspace().libraryPath)
#     

 
class WorkspaceDatasource():

    def __init__(self, databaseFileName='_opal.sqlite'):
        '''
        Creating database for library.
        '''
        self.home = home = expanduser("~")
        databasePath = os.path.join(home, databaseFileName)
        logger.debug('databasePath: %s', databasePath)
        logger.debug('CreateDatabase')
        databasePath = os.path.join(home, databaseFileName)
        isDatabaseExist = os.path.exists(databasePath)

        databaseFilePath = f'sqlite:///{databasePath}'
        self.engine = create_engine(databaseFilePath , echo=True, connect_args={'check_same_thread': False})
        Session = sessionmaker(autoflush=True, autocommit=False, bind=self.engine)
        self.session = Session()
        
        os.makedirs(home, exist_ok=True)
#         Base.metadata.create_all(self.engine)
        if not isDatabaseExist:
#             os.mkdir(libraryPath)
            self.creatingDatabase()
        os.chdir(home)

    def recreateDatabase(self):
        logger.debug('recreateDatabase')
        os.chdir(self.home)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        logger.debug('database created blank')

    def saveEntity(self, entity):
        self.session.add(entity)
        try:
            self.session.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
            self.session.rollback()
            raise
    
#     def getWorkspaceSetting(self, id=None, workspaceId, settingId):
#         if id:
#             self.session.querry()
    
    def findAllWorkspace(self):
        query = self.session.query(Workspace)
        workspaces = None
        try:    
            workspaces = query.all()
        except Exception as e:
            logger.error(e, exc_info=True)
        return workspaces

    def load(self):
        project = Project(r'C:\work\python_project', r'sql_editor', r'sql-editor')
        workspace = Workspace(r'C:\work\python_project')
    #     workspace.projects=[project]
        setting = Setting('SHOW_RECENT_WORKS', 'user.home/workspace', 'RECENT_WORKSPACES')
        projectWorkspace = ProjectWorkspaceLink(project, workspace)
        workspaceSetting = WorkspaceSettingLink(workspace, setting)
        datasource.saveEntity(projectWorkspace)
        datasource.saveEntity(workspaceSetting)

    def findActiveWorkspace(self):
        workspace = self.session.query(Workspace).filter_by(active=True).first()
        return workspace
    
    def findAllProject(self):
        workspace = self.findActiveWorkspace()
        return workspace.projects

    def addProject(self, project):
        workspace = self.findActiveWorkspace()
        if workspace:
            workspace.projects.append(project)
            self.saveEntity(workspace)
        
    def removeProject(self, projectName=''):
        workspace = self.findActiveWorkspace()
        project=None
        for p in workspace.projects:
            if p.name == projectName:
                workspace.projects.remove(p)
                project=p
                self.session.delete(p)
                break
        self.saveEntity(workspace)
#         try:
#             if project:
#                 self.session.delete(project)
#         except Exception as e:
#             logger.error(e)
        
        
    def findAllSetting(self):
        query = self.session.query(Setting)
        settings = None
        try:    
            settings = query.all()
        except Exception as e:
            logger.error(e, exc_info=True)
        return settings

    def addSetting(self, setting):
        workspace = self.findActiveWorkspace()
        workspace.settings.append(setting)
        self.saveEntity(workspace)

        
def getWorkspace():
    datasource = WorkspaceDatasource()
    return datasource.findActiveWorkspace()

        
if __name__ == '__main__':
    datasource = WorkspaceDatasource()
    datasource.recreateDatabase()
    datasource.load()
    datasource.addProject(Project(r'C:\work\python_project', r'Phoenix', r'Phoenix'))
    datasource.addProject(Project(r'C:\work\python_project', r'TextEditor', r'TextEditor'))
    datasource.removeProject('TextEditor')
#     workspaces = datasource.findAllWorkspace()
#     workspace = None
#     for workspace in workspaces:
#         print(workspace)
#         workspace = workspace
#     datasource.addProject(Project(r'C:\work\python_project', r'sql_editor', r'sql-editor'))
#     workspaceSettingLink=workspace.workspace_setting_assoc[0]
#     workspaceSettingLink.
    
    print('hi')
#     datasource.saveEntity(workspace.projects.append(Project(r'C:\work\python_project','Phoenix','Phoenix')))
#     datasource.recreateDatabase()

#     CreateDatabase().addingData()

#     books = CreateDatabase().findByBookName("java")
#     libraryPath = r'/docs/new/library'
#     if not os.path.exists(libraryPath):
#         print('no workspace')
        
#     try:
#         createdb = CreateDatabase()
# #         createdb.creatingDatabase()
# #         createdb.addingData()
#         x = createdb.getMaxBookID()
#         page = createdb.pagination(10, 10)
#         logger.debug(page)
# #         createdb.findAllBook()
#     except Exception as e:
#         print(e)
#     for b in books:
#         print b.isbn_13, b.id

#         createdb.removeBook(b)

    pass
