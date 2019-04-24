import wx
import re
from src.view.constants import ID_DATABASE_PERSPECTIVE, ID_DEBUG_PERSPECTIVE, \
    ID_GIT_PERSPECTIVE, ID_JAVA_PERSPECTIVE, ID_PYTHON_PERSPECTIVE, \
    ID_JAVA_EE_PERSPECTIVE, ID_RESOURCE_PERSPECTIVE

bookExplorerList = [
        [wx.NewIdRef(), "Authors", 'user.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Languages", 'language.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Series", 'books_in_series_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Formats", 'fomat_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Publisher", 'publisher_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Rating", 'rating_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "News", 'news_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Tags", 'tags_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],
        [wx.NewIdRef(), "Identifiers", 'identifiers_16.png', None, [
            [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
            ], ],

    ]

importProjectDataList = [
        [wx.NewIdRef(), "General", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Archive File", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Existing Project into Workspace", 'console_view.png', None, None],
                [wx.NewIdRef(), "File System", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Preferences", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Project From Folder or Archive", 'internal_browser.png', None, None],
                [wx.NewIdRef(), "Working Sets", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Git", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Project from git", 'breakpoint_view.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Install", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "git interactive rebase", 'rebase_interactive.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Run/Debug ", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "cheat sheets", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "help", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Team", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "caugth exceptions", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Third party configuration", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "History", 'history_view.png', None, None],
                [wx.NewIdRef(), "Syncheronize", 'synch_synch.png', None, None],
            ]
        ],
      
    ]

viewdataList = [
        [wx.NewIdRef(), "Database", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "database browser", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "database Navigator", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "process", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "project explorer", 'resource_persp.png', None, None],
                [wx.NewIdRef(), "projects", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "query manager", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "general", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "bookmarks", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "classic search", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "console", 'console_view.png', None, None],
                [wx.NewIdRef(), "error log", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "internal web browser", 'internal_browser.png', None, None],
                [wx.NewIdRef(), "markers", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "navigator", 'filenav_nav.png', None, None],
                [wx.NewIdRef(), "outline", 'outline_co.png', None, None],
                [wx.NewIdRef(), "palette", 'welcome16.png', None, None],
                [wx.NewIdRef(), "problem", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "progress", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "project explorer", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "properties", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "search", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "tasks", 'tasks_tsk.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "debug", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "brekpoints", 'breakpoint_view.png', None, None],
                [wx.NewIdRef(), "debug", 'debug_view.png', None, None],
                [wx.NewIdRef(), "expressions", 'watchlist_view.png', None, None],
                [wx.NewIdRef(), "memory", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "modules", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "registers", 'register_view.png', None, None],
                [wx.NewIdRef(), "variables", 'variable_view.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "git", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "git interactive rebase", 'rebase_interactive.png', None, None],
                [wx.NewIdRef(), "git reflog", 'reflog.png', None, None],
                [wx.NewIdRef(), "git repositories", 'repo_rep.png', None, None],
                [wx.NewIdRef(), "git staging", 'staging.png', None, None],
                [wx.NewIdRef(), "git tree compare", 'gitrepository.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "help ", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "cheat sheets", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "help", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "python", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "caugth exceptions", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "code coverage", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "hierarchy view", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "profile (python monitor)", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "python package explorer", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "pyUnit", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Referrers View", 'fileType_filter.png', None, None],
            ],
        ],
        [wx.NewIdRef(), "Team", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "History", 'history_view.png', None, None],
                [wx.NewIdRef(), "Syncheronize", 'synch_synch.png', None, None],
            ]
        ],
        [wx.NewIdRef(), "Calibre", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Book Explorer", 'file_explorer.png', None, None],
                [wx.NewIdRef(), "Book Browser", 'library-16.png', None, None],
            ]
        ]
    ]

perspectiveList = [
        [wx.NewIdRef(), "Database Debug", 'database_debug_perspective.png', None, None],
        [ID_DATABASE_PERSPECTIVE, "Database Development", 'database.png', None, None],
        [ID_DEBUG_PERSPECTIVE, "Debug", 'debug_persp.png', None, None],
        [ID_GIT_PERSPECTIVE, "Git", 'gitrepository.png', None, None],
        [ID_JAVA_PERSPECTIVE, "Java", 'jperspective.png', None, None],
        [ID_PYTHON_PERSPECTIVE, "Python", 'python_perspective.png', None, None],
        [wx.NewIdRef(), "Java Browsing", 'browse_persp.png', None, None],
        [ID_JAVA_EE_PERSPECTIVE, "Java EE", 'javaee_perspective.png', None, None],
        [wx.NewIdRef(), "Java Type Hierarchy", 'java_type_hierarchy.png', None, None],
        [wx.NewIdRef(), "JavaScript", 'javascript_perspective.png', None, None],
        [wx.NewIdRef(), "JPA", 'jpa.png', None, None],
        [wx.NewIdRef(), "Planning", 'perspective-planning.png', None, None],
        [wx.NewIdRef(), "Plug-in Development", 'plugin_perspecitve.png', None, None],
        [wx.NewIdRef(), "Remote System Explorer", 'remote_perspective.png', None, None],
        [ID_RESOURCE_PERSPECTIVE, "Resource", 'resource_persp.png', None, None],
        [wx.NewIdRef(), "SVN Repository Exploring", 'svn_perspective.png', None, None],
        [wx.NewIdRef(), "Team Synchronizing", 'synch_synch.png', None, None],
        [wx.NewIdRef(), "Web", 'web_perspective.png', None, None],
        [wx.NewIdRef(), "XML", 'xml_perspective.png', None, None],
    ]
perferenceTreeList = [
    [wx.NewIdRef(), "General", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "Appearance", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Colors and Fonts", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Label Decorations", 'fileType_filter.png', None, None],
            ]
        ],
        [wx.NewIdRef(), "Capabilities", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Compare/Patch", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Content Types", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Editors", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Autosave", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "File Associations", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Structured Text Editors", 'fileType_filter.png', None, None],
            ]
        ],
        [wx.NewIdRef(), "Error Reporting", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Globalization", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Keys", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Network Connections", 'folderType_filter.png', None, [
            [wx.NewIdRef(), "Cache", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "SSH2", 'fileType_filter.png', None, None],
            ]
         ]
        ]
    ],
    [wx.NewIdRef(), "Ant", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Colors and Fonts", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Label Decorations", 'fileType_filter.png', None, None],
            ]
        ],
        [wx.NewIdRef(), "Runtime", 'fileType_filter.png', None, None],
        ]
    ],
    [wx.NewIdRef(), "Cloud Foundry", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "HTTP Tracing", 'fileType_filter.png', None, None],
        ]
    ], [wx.NewIdRef(), "Code Recommenders", 'folderType_filter.png', None, [
            [wx.NewIdRef(), "Advisors", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "Completions", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Calls", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Chains", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Constructors", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Overrides", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Statics", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Subwords", 'fileType_filter.png', None, None],
            ]
        ],
            [wx.NewIdRef(), "Models", 'fileType_filter.png', None, None],
        ]
    ],
    [wx.NewIdRef(), "Data Management", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "Connectivity", 'folderType_filter.png', None, [
            [wx.NewIdRef(), "Database Connection Profile", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "Driver Definitions", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "Open Data Access", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "XML Data Set", 'fileType_filter.png', None, None],
                ]],
            ]],
        [wx.NewIdRef(), "Label Decorations", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "SQL Development", 'folderType_filter.png', None, [
            [wx.NewIdRef(), "Execution Plan View Options", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "General", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "Schema Object Editor Configuration", 'fileType_filter.png', None, None],
            [wx.NewIdRef(), "SQL Editor", 'folderType_filter.png', None, [
                [wx.NewIdRef(), "Code Assist", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "SQL Files/Scrapbooks", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None],
                [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None],
                ]],
            ]],
        ]
    ],
    [wx.NewIdRef(), "Gradle", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Help", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content", 'fileType_filter.png', None, None], ]],
    [wx.NewIdRef(),
     "Install/Update", 'folderType_filter.png', None, [
            [wx.NewIdRef(), 'Automatic Updates', 'fileType_filter.png', None, None],
            [wx.NewIdRef(), 'Available plugins', 'fileType_filter.png', None, None]
        ]
     ],
    [wx.NewIdRef(), "Java", 'folderType_filter.png', None, [[wx.NewIdRef(), "Appearance", 'folderType_filter.png', None, [[wx.NewIdRef(), "Members Sort Order", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Type Filters", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Build Path", 'folderType_filter.png', None, [[wx.NewIdRef(), "Classpath Variables", 'fileType_filter.png', None, None], [wx.NewIdRef(), "User Liberaries", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Code Coverage", 'fileType_filter.png', None, None],
             [wx.NewIdRef(), "Code Style", 'folderType_filter.png', None, [[wx.NewIdRef(), "Clean Up", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Code Templates", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Formatter", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Organize Imports", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Compiler", 'folderType_filter.png', None, [[wx.NewIdRef(), "Building", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Errors/Warning", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Javadoc", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Task Tags", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Debug", 'folderType_filter.png', None, [[wx.NewIdRef(), "Detail Formatters", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Heap Walking", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Logical Structures", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Premitive Display Options", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Step Filtering", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content Assist", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Folding", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Hovers", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Mark Occurrences", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Save Actions", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Typing", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "Installed JREs", 'folderType_filter.png', None, [[wx.NewIdRef(), "Execution Environments", 'fileType_filter.png', None, None], ]],
             [wx.NewIdRef(), "JUnit", 'fileType_filter.png', None, None],
             [wx.NewIdRef(), "Properties Files Editor", 'fileType_filter.png', None, None],

             ]],
    [wx.NewIdRef(), "Java EE", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Java Persistence", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "JavaScript", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "JSON", 'folderType_filter.png', None, [[wx.NewIdRef(), "JSON Catalog", 'fileType_filter.png', None, None], [wx.NewIdRef(), "JSON Files", 'folderType_filter.png', None, [[wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content Assist", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], ]], [wx.NewIdRef(), "Validation", 'fileType_filter.png', None, None], ]]]],
    [wx.NewIdRef(), "Maven", 'folderType_filter.png', None, [[wx.NewIdRef(), "Archetypes", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Discovery", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Errors/Warning", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Installations", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Java EE Integration", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Lifecycle Mappings", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Source Lookup", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], [wx.NewIdRef(), "User Interface", 'fileType_filter.png', None, None], [wx.NewIdRef(), "User Settings", 'fileType_filter.png', None, None], ]],
    [wx.NewIdRef(), "Calibre", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "Interface", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Conversion", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Import/Export", 'fileType_filter.png', None, None],
        [wx.NewIdRef(), "Sharing", 'fileType_filter.png', None, None],

        ]],
    
    [wx.NewIdRef(), "Python", 'folderType_filter.png', None, [[wx.NewIdRef(), "Builders", 'fileType_filter.png', None, None],
               [wx.NewIdRef(), "Debug", 'folderType_filter.png', None, [[wx.NewIdRef(), "Source Locator", 'fileType_filter.png', None, None], ]],
               [wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Auto Imports", 'fileType_filter.png', None, None], ]],
               [wx.NewIdRef(), "Code Analysis", 'folderType_filter.png', None, [[wx.NewIdRef(), "PyLint", 'fileType_filter.png', None, None], ]],
               [wx.NewIdRef(), "Code Completion [ctx insensitive and common tokens]", 'fileType_filter.png', None, None],
               [wx.NewIdRef(), "Code Folding", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Code Style", 'folderType_filter.png', None, [[wx.NewIdRef(), "Block Comments", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Code Formatter", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Docstrings", 'fileType_filter.png', None, None], [wx.NewIdRef(), "File types", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Imports", 'fileType_filter.png', None, None], ]],
               [wx.NewIdRef(), "Editor caption/icon", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Hover", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Mark Occurrences", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Overview Ruler Minimap", 'fileType_filter.png', None, None],
               ]],
    [wx.NewIdRef(), "Remote Systems", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Run/Debug", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Server", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Team", 'folderType_filter.png', None, [[wx.NewIdRef(), "File Content", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Git", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "Committing", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Configuration", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Confirmation and Warning", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Date Format", 'fileType_filter.png', None, None], [wx.NewIdRef(), "History", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Label Decorations", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Projects", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Staging View", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Synchronize", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Window Cache", 'fileType_filter.png', None, None],
        ]],
        [wx.NewIdRef(), "Ignored Resources", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Models", 'fileType_filter.png', None, None],
    ]],
    [wx.NewIdRef(), "Terminal", 'folderType_filter.png', None, [[wx.NewIdRef(), "Local Terminal", 'fileType_filter.png', None, None], ]],
    [wx.NewIdRef(), "Validation", 'fileType_filter.png', None, None],
    [wx.NewIdRef(), "Web", 'folderType_filter.png', None, [
        [wx.NewIdRef(), "CSS Files", 'folderType_filter.png', None, [[wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content Assist", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], ]]]],
        [wx.NewIdRef(), "HTML Files", 'folderType_filter.png', None, [[wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content Assist", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Typing", 'fileType_filter.png', None, None], ]], [wx.NewIdRef(), "Validation", 'fileType_filter.png', None, None], ]],
        [wx.NewIdRef(), "JavaServer Faces Tools", 'folderType_filter.png', None, [[wx.NewIdRef(), "FacesConfig Editor", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Validation", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Views", 'folderType_filter.png', None, [[wx.NewIdRef(), "JSP Tag Registry", 'fileType_filter.png', None, None], ]]]],
        [wx.NewIdRef(), "JSP Files", 'folderType_filter.png', None, [[wx.NewIdRef(), "Editor", 'folderType_filter.png', None, [[wx.NewIdRef(), "Content Assist", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Syntax Coloring", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Templates", 'fileType_filter.png', None, None], ]]]],

    ]],
    [wx.NewIdRef(), "Web Services", 'folderType_filter.png', None, [[wx.NewIdRef(), "Axis Emitter", 'fileType_filter.png', None, None], [wx.NewIdRef(), "Axis2 Preferences", 'fileType_filter.png', None, None], ]],
    [wx.NewIdRef(), "XML", 'fileType_filter.png', None, None],
]

traverse = []


class Node():

    def __init__(self, id, name, imageName=None, tooltip=None, child=None):
        self.id = id,
        self.name = name.title()
        if tooltip:
            self.tooltip = tooltip
        else:
            self.tooltip = name

        self.imageName = imageName
        self.child = child
        
    def getFirstChildNode(self):
        firstChild = None
        if self.child:
            firstChild = self.child[0]
        return firstChild

    def __repr__(self):
        return f' name:{self.name},  child:{self.child}'


class TreeSearch():

    def __init__(self):
        self.treeData = []
        self.traverse = []

    def searchedNodes(self, dataList=None, searchText=None):
        treeData = []
        for data in dataList:
            print(data)
            node = self.getNode(data, searchText=searchText)
#             if searchText == None:
            if node:
                treeData.append(node)
#             else:
#                 for treeLabel in flatTreeLabelList :
#                     if searchText and re.search(searchText, treeLabel, re.I):
#                         treeData.append(node)
#                         break
                    
        return treeData

    def isSearchMatch(self, text, searchText):
        searchMatch = False
        if searchText == None:
            searchMatch = True
        elif searchText and re.search(searchText, text, re.I):
            searchMatch = True
        else:
            searchMatch = False
        return searchMatch
    
    def getNode(self, data, searchText=None):
        print(data)
        node = None
        flatTreeLabelList = []
        try:
            if data :
                flatTreeLabelList.append(data[1])
#                 self.traverse.append(self.isSearchMatch(searchText, data[1]))
                node = Node(data[0], data[1], imageName=data[2], tooltip=data[3] , child=None)
                if data[4]:
                    node.child = []
                    for d in data[4]:
                        child = self.getNode(d, searchText=searchText)
                        
#                         child=self.someMethod(flatTreeLabelList, child, searchText)
                        if child:
                            node.child.append(child)
        except Exception as e:
            print(data) 
            print(e)
                
        return node
    
    def searchTreeData(self, searchText=None):
        for treeDataItem in self.treeData:
            pass


if __name__ == '__main__':
    treeSearch = TreeSearch()
    treeItems = treeSearch.searchedNodes(dataList=perferenceTreeList, searchText=None)
    print('pass')
