from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Unicode, func, \
    Column, Integer, String, Column, Integer, String, create_engine, create_engine

from sqlalchemy.ext.declarative import declarative_base, declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.schema import UniqueConstraint
import os
Base = declarative_base()


class Project(Base):
    """A Project class is an entity having database table."""

    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    basePath = Column('base_path', String, nullable=False)
    name = Column('name', String)
    dirName = Column('dir_name', String)
    status = Column('status', Boolean)  # defing is project open = True, if close status=False
    nature = Column('nature', String)  # example of nature are java, python, javascript
    created_on = Column(DateTime, default=func.now())
    UniqueConstraint(basePath, name, dirName, name='project_unique')
#     project_workspace_link_id = Column(Integer,
#             ForeignKey('project_workspace_link.project_id', ondelete='CASCADE')
#                 )

#     workspaces = relationship(
#         Workspace,
#         secondary='workspace_project_link', cascade="all"
#     )

    def __init__(self, basePath, name, dirName, status, nature):
        self.basePath = basePath
        self.name = name
        self.dirName = dirName
        self.status = status
        self.nature = nature

    def getProjectPath(self):
        return os.path.join(self.basePath, self.dirName)

    def __repr__(self):
        return f"""id:{self.id}, basePath:{self.basePath}"""


class Workspace(Base):
    """A Workspace class is an entity having database table."""

    __tablename__ = 'workspace'
    id = Column(Integer, primary_key=True)
    workspacePath = Column('workspace_path', String, nullable=False, unique=True)
    active = Column('active', Boolean)
    created_on = Column(DateTime, default=func.now())
    projects = relationship(
        Project,
        secondary='project_workspace_link', cascade="all"
    )

    def __init__(self, workspacePath, active=True, projects=None):
        self.workspacePath = workspacePath
        self.active = active
#         self.projects = projects
    
    def __repr__(self):
        return f"""id:{self.id}, workspacePath:{self.workspacePath}"""


class Setting(Base):
    """A Setting class is an entity having database table.
        here we are defining workspace setting for eclipse.
    """

    __tablename__ = 'setting'
    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    value = Column('value', String)
    description = Column('description', String)
    created_on = Column(DateTime, default=func.now())
    UniqueConstraint(name, value, description, name='setting_unique')
    workspaces = relationship(
        Workspace,
        secondary='workspace_setting_link', cascade="all"
    )

    def __init__(self, name, value, description):
        self.name = name
        self.value = value
        self.description = description

    def __repr__(self):
        return f"""id:{self.id}, authorName:{self.workspacePath}"""


class ProjectWorkspaceLink(Base):
    """A ProjectWorkspaceLink class is an entity having database table. This class is for many to many association between Author and Book."""

    __tablename__ = 'project_workspace_link'
    id = Column(Integer, primary_key=True)
    projectId = Column('project_id', Integer, ForeignKey('project.id'))
    workspaceId = Column('workspace_id', Integer, ForeignKey('workspace.id'))
#     extra_data = Column(String(256))
    project = relationship(Project, backref=backref("project_assoc", cascade="all, delete-orphan"))
    workspace = relationship(Workspace, backref=backref("workspace_project_assoc", cascade="all, delete-orphan"))
#     UniqueConstraint('project_id', 'workspace_id', name='uix_1')
    createdOn = Column('created_on', DateTime, default=func.now())

    def __init__(self, project, workspace):
        self.project = project
        self.workspace = workspace

    def __repr__(self):
        return f"""id:{self.id}, projectId:{self.projectId}, workspaceId:{self.workspaceId}"""


class WorkspaceSettingLink(Base):
    """A WorkspaceSettingLink class is an entity having database table. This class is for many to many association between Author and Book."""

    __tablename__ = 'workspace_setting_link'
    id = Column(Integer, primary_key=True)
    workspaceId = Column('workspace_id', Integer, ForeignKey('workspace.id'))
    settingId = Column('setting_id', Integer, ForeignKey('setting.id'))
#     extra_data = Column(String(256))
    workspace = relationship(Workspace, backref=backref("workspace_setting_assoc", cascade="all, delete-orphan"))
    setting = relationship(Setting, backref=backref("setting_assoc", cascade="all, delete-orphan"))
#     UniqueConstraint('workspace_id', 'setting_id', name='uix_1')
    createdOn = Column('created_on', DateTime, default=func.now())

    def __init__(self, workspace, setting):
        self.workspace = workspace
        self.setting = setting

    def __repr__(self):
        return f"""id:{self.id}, workspaceId:{self.workspaceId}, settingId:{self.settingId}"""
