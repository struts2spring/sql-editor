import wx
import tempfile
import os
from src.view.util.common.ed_glob import ID_GOTO_LINE
# from src.settings.workspace import Setting

TITLE = "Eclipse"
VERSION = "0.0.6"

# setting = Setting()

ID_RESOURCE = wx.NewIdRef()
ID_WELCOME = wx.NewIdRef()
ID_UPDATE_CHECK = wx.NewIdRef()
ID_newConnection = wx.NewIdRef()
ID_openConnection = wx.NewIdRef()
ID_newWorksheet = wx.NewIdRef()
ID_deleteWithDatabase = wx.NewIdRef()
ID_FIND_REPLACE = wx.NewIdRef()
ID_FIND_NEXT_MATCH = wx.NewIdRef()
ID_RENAME = wx.NewIdRef()

ID_CONNECTION_PROPERTIES = wx.NewIdRef()

ID_OPEN_FILE = wx.NewIdRef()
ID_OPEN_PROJECT_FROM_FILE_SYSTEM = wx.NewIdRef()
ID_NEW = wx.NewIdRef()
ID_SAVE = wx.NewIdRef()
ID_SAVE_ALL = wx.NewIdRef()
ID_SAVE_AS = wx.NewIdRef()
ID_DEBUG_AS = wx.NewIdRef()
ID_DEBUG_AS_MENU = wx.NewIdRef()
ID_RUN_AS = wx.NewIdRef()
ID_RUN_AS_MENU = wx.NewIdRef()
ID_OPEN_TASK = wx.NewIdRef()
ID_LAST_EDIT = wx.NewIdRef()
ID_BACKWARD = wx.NewIdRef()
ID_FORWARD = wx.NewIdRef()
ID_SEARCH = wx.NewIdRef()
ID_OPEN_TYPE = wx.NewIdRef()
ID_TEXTCTRL_AUTO_COMPLETE = wx.NewIdRef()
ID_SKIP_ALL_BREAKPOINTS = wx.NewIdRef()
ID_NEW_JAVA_PACKAGE = wx.NewIdRef()
ID_NEW_JAVA_CLASS = wx.NewIdRef()
ID_RESUME_DEBUG = wx.NewIdRef()
ID_SUSPEND_DEBUG = wx.NewIdRef()
ID_TERMNATE_DEBUG = wx.NewIdRef()
ID_DISCONNECT_DEBUG = wx.NewIdRef()
ID_STEP_INTO_DEBUG = wx.NewIdRef()
ID_STEP_OVER_DEBUG = wx.NewIdRef()
ID_STEP_RETURN_DEBUG = wx.NewIdRef()
ID_BUILD_ALL = wx.NewIdRef()
ID_BUILD_PROJECT = wx.NewIdRef()

ID_RECENT_FILES = wx.NewIdRef()
ID_CLOSE = wx.NewIdRef()
ID_CLOSE_ALL = wx.NewIdRef()
ID_IMPORT = wx.NewIdRef()
ID_EXPORT = wx.NewIdRef()
ID_PROJECT_PROPERTIES = wx.NewIdRef()
ID_SWITCH_WORKSPACE = wx.NewIdRef()
ID_RESTART = wx.NewIdRef()
ID_SEARCH_MENU = wx.NewIdRef()
ID_GOTO_LINE = wx.NewIdRef()
ID_OPEN_PROJECT = wx.NewIdRef()
ID_CLOSE_PROJECT = wx.NewIdRef()
ID_CLEAN = wx.NewIdRef()
ID_BUILD_AUTO = wx.NewIdRef()

ID_SELECT_SQL = wx.NewIdRef()
ID_INSERT_SQL = wx.NewIdRef()
ID_UPDATE_SQL = wx.NewIdRef()
ID_DELETE_SQL = wx.NewIdRef()

ID_NEW_PROJECT = wx.NewIdRef()
ID_EXAMPLE_MENU = wx.NewIdRef()
ID_OTHER_MENU = wx.NewIdRef()

ID_NEW_JAVA_PROJECT = wx.NewIdRef()

ID_NEW_PYTHON_PROJECT = wx.NewIdRef()
ID_NEW_PYTHON_PACKAGE = wx.NewIdRef()
ID_NEW_PYTHON_MODULE = wx.NewIdRef()

ID_RUN = wx.NewIdRef()
ID_SQL_TEXT = wx.NewIdRef()
ID_DEBUG = wx.NewIdRef()
ID_RUN_HISTORY = wx.NewIdRef()
ID_RUN_CONFIG = wx.NewIdRef()
ID_ORGANIZE_FAVORITES = wx.NewIdRef()
ID_DEBUG_HISTORY = wx.NewIdRef()
ID_DEBUG_CONFIG = wx.NewIdRef()
ID_EXECUTE_SCRIPT = wx.NewIdRef()
ID_PIN = wx.NewIdRef()
ID_ROW_ADD = wx.NewIdRef()
ID_ROW_DELETE = wx.NewIdRef()
ID_RESULT_NEXT = wx.NewIdRef()
ID_RESULT_PREVIOUS = wx.NewIdRef()
ID_RESULT_REFRESH = wx.NewIdRef()
ID_APPLY_CHANGE = wx.NewIdRef()
ID_RESULT_FIRST = wx.NewIdRef()
ID_RESULT_LAST = wx.NewIdRef()
ID_SQL_LOG = wx.NewIdRef()
ID_CONSOLE_LOG = wx.NewIdRef()
ID_DATABASE_NAVIGATOR = wx.NewIdRef()
ID_FILE_EXPLORER = wx.NewIdRef()
ID_PROJECT_EXPLORER = wx.NewIdRef()
ID_PYTHON_SHELL = wx.NewIdRef()
ID_NAVIGATOR = wx.NewIdRef()
ID_TERMINAL = wx.NewIdRef()
ID_TASKS = wx.NewIdRef()
ID_OUTLINE = wx.NewIdRef()
ID_VARIABLE = wx.NewIdRef()
ID_BREAKPOINTS = wx.NewIdRef()
ID_EXPRESSIONS = wx.NewIdRef()
ID_PYTHON_PACKAGE_EXPLORER = wx.NewIdRef()
ID_JAVA_PACKAGE_EXPLORER = wx.NewIdRef()
ID_OTHER_VIEW = wx.NewIdRef()
ID_UNDO = wx.NewIdRef()
ID_REDO = wx.NewIdRef()
ID_COPY = wx.NewIdRef()
ID_PASTE = wx.NewIdRef()
ID_CUT = wx.NewIdRef()
ID_DUPLICATE_LINE = wx.NewIdRef()
ID_FORMAT_FILE = wx.NewIdRef()

ID_SQL_EXECUTION = wx.NewIdRef()
ID_COPY_COLUMN_HEADER = wx.NewIdRef()
ID_CONNECT_DB = wx.NewIdRef()
ID_DISCONNECT_DB = wx.NewIdRef()
ID_ROOT_REFERESH = wx.NewIdRef()
ID_ROOT_NEW_CONNECTION = wx.NewIdRef()
ID_SHOW_VIEW_TOOLBAR = wx.NewIdRef()
ID_PERSPECTIVE_TOOLBAR = wx.NewIdRef()
ID_OTHER_PERSPECTIVE = wx.NewIdRef()
ID_RESOURCE_PERSPECTIVE = wx.NewIdRef()
ID_CALIBRE_PERSPECTIVE = wx.NewIdRef()

ID_OPEN_PERSPECTIVE = wx.NewIdRef()
ID_JAVA_PERSPECTIVE = wx.NewIdRef()
ID_JAVA_EE_PERSPECTIVE = wx.NewIdRef()
ID_DEBUG_PERSPECTIVE = wx.NewIdRef()
ID_PYTHON_PERSPECTIVE = wx.NewIdRef()
ID_GIT_PERSPECTIVE = wx.NewIdRef()
ID_DATABASE_PERSPECTIVE = wx.NewIdRef()

# Prospective menu menu
ID_PREFERENCES = wx.NewIdRef()
ID_PROSPECTIVE_NAVIGATION = wx.NewIdRef()
ID_PROSPECTIVE_OTHER = wx.NewIdRef()
ID_OPEN_PROSPECTIVE = wx.NewIdRef()
# Appearance toolbar menu
ID_CREATE_NEW_WINDOW = wx.NewIdRef()
ID_APPEARANCE = wx.NewIdRef()
# show view menu
ID_SHOW_VIEW = wx.NewIdRef()
ID_HIDE_TOOLBAR = wx.NewIdRef()
ID_HIDE_STATUSBAR = wx.NewIdRef()

# search toolbar menu
ID_SEARCH_FILE = wx.NewIdRef()

ID_COLLAPSE_ALL = wx.NewIdRef()
ID_LINK_WITH_EDITOR = wx.NewIdRef()
ID_VIEW_MENU = wx.NewIdRef()

# Data tableinfo toolbar menu
ID_ADD_ROW = wx.NewIdRef()
ID_DUPLICATE_ROW = wx.NewIdRef()
ID_DELETE_ROW = wx.NewIdRef()
ID_SAVE_ROW = wx.NewIdRef()
ID_REFRESH_ROW = wx.NewIdRef()

ID_JUNIT_TEST_CASE = wx.NewIdRef()
ID_CLASS = wx.NewIdRef()
ID_INTERFACE = wx.NewIdRef()
ID_ENUM = wx.NewIdRef()
ID_ANNOTATION = wx.NewIdRef()
ID_JAX_WS_HANDLER = wx.NewIdRef()
ID_CREATE_DYNAMIC_WEB_PROJECT = wx.NewIdRef()
ID_CREATE_NEW_SERVLET = wx.NewIdRef()
ID_NEW_FOLDER = wx.NewIdRef()
ID_NEW_FILE = wx.NewIdRef()

ID_DYNAMIC_WEB_PROJECT = wx.NewIdRef()
ID_WEB_FRAGMENT_PROJECT = wx.NewIdRef()
ID_EJB_PROJECT = wx.NewIdRef()
ID_ENTERPRISE_APP_PROJECT = wx.NewIdRef()
ID_APP_CLIENT_PROJECT = wx.NewIdRef()
ID_CONNECTER_PROJECT = wx.NewIdRef()
ID_UTILITY_PROJECT = wx.NewIdRef()
ID_STATIC_WEB_PROJECT = wx.NewIdRef()
ID_JPA_PROJECT = wx.NewIdRef()
ID_MAVEN_PROJECT = wx.NewIdRef()

ID_SERVLET = wx.NewIdRef()
ID_FILTER = wx.NewIdRef()
ID_LISTENER = wx.NewIdRef()
ID_SESSION_BEAN = wx.NewIdRef()
ID_MESSAGE_DRIVEN_BEAN = wx.NewIdRef()
ID_EJB_TIMER = wx.NewIdRef()
ID_JPA_ENTITY = wx.NewIdRef()
ID_JPA_ORM_MAPPING_FILE = wx.NewIdRef()
ID_ECLIPSE_LINK_ORM_MAPPING_FILE = wx.NewIdRef()
ID_XDOCKLET_ENTERPRISE_JAVA_BEAN = wx.NewIdRef()
ID_ECLIPSELINK_DYNAMIC_ENTITY = wx.NewIdRef()
ID_WEB_SERVICE = wx.NewIdRef()

ID_DELETE_PROJECT = wx.NewIdRef()
ID_REFRESH_TREE_ITEM = wx.NewIdRef()
ID_PYTHON_RUN = wx.NewIdRef()

keyMap = {
    wx.WXK_BACK : "WXK_BACK",
    wx.WXK_TAB : "WXK_TAB",
    wx.WXK_RETURN : "WXK_RETURN",
    wx.WXK_ESCAPE : "WXK_ESCAPE",
    wx.WXK_SPACE : "WXK_SPACE",
    wx.WXK_DELETE : "WXK_DELETE",
    wx.WXK_START : "WXK_START",
    wx.WXK_LBUTTON : "WXK_LBUTTON",
    wx.WXK_RBUTTON : "WXK_RBUTTON",
    wx.WXK_CANCEL : "WXK_CANCEL",
    wx.WXK_MBUTTON : "WXK_MBUTTON",
    wx.WXK_CLEAR : "WXK_CLEAR",
    wx.WXK_SHIFT : "WXK_SHIFT",
    wx.WXK_ALT : "WXK_ALT",
    wx.WXK_CONTROL : "WXK_CONTROL",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
#     wx.WXK_PRIOR : "WXK_PRIOR",
#     wx.WXK_NEXT : "WXK_NEXT",
    wx.WXK_END : "WXK_END",
    wx.WXK_HOME : "WXK_HOME",
    wx.WXK_LEFT : "WXK_LEFT",
    wx.WXK_UP : "WXK_UP",
    wx.WXK_RIGHT : "WXK_RIGHT",
    wx.WXK_DOWN : "WXK_DOWN",
    wx.WXK_SELECT : "WXK_SELECT",
    wx.WXK_PRINT : "WXK_PRINT",
    wx.WXK_EXECUTE : "WXK_EXECUTE",
    wx.WXK_SNAPSHOT : "WXK_SNAPSHOT",
    wx.WXK_INSERT : "WXK_INSERT",
    wx.WXK_HELP : "WXK_HELP",
    wx.WXK_NUMPAD0 : "WXK_NUMPAD0",
    wx.WXK_NUMPAD1 : "WXK_NUMPAD1",
    wx.WXK_NUMPAD2 : "WXK_NUMPAD2",
    wx.WXK_NUMPAD3 : "WXK_NUMPAD3",
    wx.WXK_NUMPAD4 : "WXK_NUMPAD4",
    wx.WXK_NUMPAD5 : "WXK_NUMPAD5",
    wx.WXK_NUMPAD6 : "WXK_NUMPAD6",
    wx.WXK_NUMPAD7 : "WXK_NUMPAD7",
    wx.WXK_NUMPAD8 : "WXK_NUMPAD8",
    wx.WXK_NUMPAD9 : "WXK_NUMPAD9",
    wx.WXK_MULTIPLY : "WXK_MULTIPLY",
    wx.WXK_ADD : "WXK_ADD",
    wx.WXK_SEPARATOR : "WXK_SEPARATOR",
    wx.WXK_SUBTRACT : "WXK_SUBTRACT",
    wx.WXK_DECIMAL : "WXK_DECIMAL",
    wx.WXK_DIVIDE : "WXK_DIVIDE",
    wx.WXK_F1 : "WXK_F1",
    wx.WXK_F2 : "WXK_F2",
    wx.WXK_F3 : "WXK_F3",
    wx.WXK_F4 : "WXK_F4",
    wx.WXK_F5 : "WXK_F5",
    wx.WXK_F6 : "WXK_F6",
    wx.WXK_F7 : "WXK_F7",
    wx.WXK_F8 : "WXK_F8",
    wx.WXK_F9 : "WXK_F9",
    wx.WXK_F10 : "WXK_F10",
    wx.WXK_F11 : "WXK_F11",
    wx.WXK_F12 : "WXK_F12",
    wx.WXK_F13 : "WXK_F13",
    wx.WXK_F14 : "WXK_F14",
    wx.WXK_F15 : "WXK_F15",
    wx.WXK_F16 : "WXK_F16",
    wx.WXK_F17 : "WXK_F17",
    wx.WXK_F18 : "WXK_F18",
    wx.WXK_F19 : "WXK_F19",
    wx.WXK_F20 : "WXK_F20",
    wx.WXK_F21 : "WXK_F21",
    wx.WXK_F22 : "WXK_F22",
    wx.WXK_F23 : "WXK_F23",
    wx.WXK_F24 : "WXK_F24",
    wx.WXK_NUMLOCK : "WXK_NUMLOCK",
    wx.WXK_SCROLL : "WXK_SCROLL",
    wx.WXK_PAGEUP : "WXK_PAGEUP",
    wx.WXK_PAGEDOWN : "WXK_PAGEDOWN",
    wx.WXK_NUMPAD_SPACE : "WXK_NUMPAD_SPACE",
    wx.WXK_NUMPAD_TAB : "WXK_NUMPAD_TAB",
    wx.WXK_NUMPAD_ENTER : "WXK_NUMPAD_ENTER",
    wx.WXK_NUMPAD_F1 : "WXK_NUMPAD_F1",
    wx.WXK_NUMPAD_F2 : "WXK_NUMPAD_F2",
    wx.WXK_NUMPAD_F3 : "WXK_NUMPAD_F3",
    wx.WXK_NUMPAD_F4 : "WXK_NUMPAD_F4",
    wx.WXK_NUMPAD_HOME : "WXK_NUMPAD_HOME",
    wx.WXK_NUMPAD_LEFT : "WXK_NUMPAD_LEFT",
    wx.WXK_NUMPAD_UP : "WXK_NUMPAD_UP",
    wx.WXK_NUMPAD_RIGHT : "WXK_NUMPAD_RIGHT",
    wx.WXK_NUMPAD_DOWN : "WXK_NUMPAD_DOWN",
#     wx.WXK_NUMPAD_PRIOR : "WXK_NUMPAD_PRIOR",
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
#     wx.WXK_NUMPAD_NEXT : "WXK_NUMPAD_NEXT",
    wx.WXK_NUMPAD_PAGEDOWN : "WXK_NUMPAD_PAGEDOWN",
    wx.WXK_NUMPAD_END : "WXK_NUMPAD_END",
    wx.WXK_NUMPAD_BEGIN : "WXK_NUMPAD_BEGIN",
    wx.WXK_NUMPAD_INSERT : "WXK_NUMPAD_INSERT",
    wx.WXK_NUMPAD_DELETE : "WXK_NUMPAD_DELETE",
    wx.WXK_NUMPAD_EQUAL : "WXK_NUMPAD_EQUAL",
    wx.WXK_NUMPAD_MULTIPLY : "WXK_NUMPAD_MULTIPLY",
    wx.WXK_NUMPAD_ADD : "WXK_NUMPAD_ADD",
    wx.WXK_NUMPAD_SEPARATOR : "WXK_NUMPAD_SEPARATOR",
    wx.WXK_NUMPAD_SUBTRACT : "WXK_NUMPAD_SUBTRACT",
    wx.WXK_NUMPAD_DECIMAL : "WXK_NUMPAD_DECIMAL",
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE"
    }
if 'wxMac' in wx.PlatformInfo:
    keyMap[wx.WXK_RAW_CONTROL] = 'WXK_RAW_CONTROL'
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
else:
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"
LOG_SETTINGS = {
'version': 1,
'handlers': {
    'console': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'stream': 'ext://sys.stdout',
    },
    'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'detailed',
        'filename': os.path.join(tempfile.gettempdir(), 'eclipse.log'),
        'mode': 'a',
        'maxBytes': 10485760,
        'backupCount': 5,
    },

},
'formatters': {
    'detailed': {
        'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s',
    },
    'email': {
        'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
        'Line: %(lineno)d\nMessage: %(message)s',
    },
},
'loggers': {
    'extensive': {
        'level': 'DEBUG',
        'handlers': ['file', 'console']
        },
}
}

baseList = [
        [ID_NEW_PROJECT, 'Project', "new_con.png", None],
        [],
        [ID_EXAMPLE_MENU, 'Example', "new_con.png", None],
        [],
        [ID_OTHER_MENU, 'Other (Ctrl+N)', "new_con.png", None],
        ]

menuItemList = {
    "java":
        [[ID_NEW_JAVA_PROJECT, 'Java Project', 'newjprj_wiz.png', None], ] + 
        baseList[0:1] + 
        [
            [],
            [10003, 'Package', "newpack_wiz.png", None],
            [ID_CLASS, 'Class', 'newclass_wiz.png', None],
            [ID_INTERFACE, 'Interface', 'newint_wiz.png', None],
            [ID_ENUM, 'Enum', 'newenum_wiz.png', None],
            [ID_ANNOTATION, 'Annotation', 'newannotation_wiz.png', None],
            [10008, 'Source Folder', "newpackfolder_wiz.png", None],

            [10009, 'Java Working Set', "newjworkingSet_wiz.png", None],
            [ID_NEW_FOLDER, 'Folder', "new_folder.png", None],
            [ID_NEW_FILE, 'File', "newfile_wiz.png", None],
            [ID_NEW_FILE, 'Untitled text file', "new_untitled_text_file.png", None],
            [10011, 'Task', "new_task.png", None],
            [ID_JUNIT_TEST_CASE, 'JUnit Test Case', "new_testcase.png", None],
        ]
        +baseList[1:],
    "java ee":
        [
            [ID_MAVEN_PROJECT, 'Maven Project', 'maven_project.png', None],
            [ID_ENTERPRISE_APP_PROJECT, 'Enterprise Application Project', 'enterprise_app.png', None],
            [ID_DYNAMIC_WEB_PROJECT, 'Dynamic Web Project', 'create_dynamic_web_project.png', None],
            [ID_EJB_PROJECT, 'EJB Project', 'ejb_project.png', None],
            [ID_CONNECTER_PROJECT, 'Connecter Project', 'connecter_prj.png', None],
            [ID_APP_CLIENT_PROJECT, 'Application Client Project', 'app_client_prj.png', None],
            [ID_STATIC_WEB_PROJECT, 'Static Web Project', 'static_web_project.png', None],
            [ID_JPA_PROJECT, 'JPA Project', 'jpa_orm_mapping.png', None],

         ] + 
        baseList[0:1] + 
        [
            [],

            [ID_SERVLET, 'Servlet', "create_new_servlet.png", None],
            [ID_SESSION_BEAN, 'Session Bean (EJB 3.x)', 'session_bean.png', None],
            [ID_MESSAGE_DRIVEN_BEAN, 'Message-Driven Bean (EJB 3.x)', 'message_driven_bean.png', None],
            [ID_WEB_SERVICE, 'Web Service', 'web_service.png', None],
            [ID_NEW_FOLDER, 'Folder', "new_folder.png", None],
            [ID_NEW_FILE, 'File', "newfile_wiz.png", None],
        ]
        +baseList[1:],
    "python":
        [
            [ID_NEW_PYTHON_PROJECT , 'Python Project', 'new_py_prj_wiz.png', None],
        ] + 
        baseList[0:1] + 
        [
            [],
            [20003, 'Source Folder', "packagefolder_obj.png", None],
            [ID_NEW_PYTHON_PACKAGE, 'Python Package', "package_obj.png", None],
            [ID_NEW_PYTHON_MODULE, 'Python Module', "project.png", None],
            [ID_NEW_FOLDER, 'Folder', "project.png", None],
            [ID_NEW_FILE, 'File', "newfile_wiz.png", None],
        ]
        +baseList[1:],
    "resource": baseList[0:1] + 
        [
            [],
            [ID_NEW_FOLDER, 'Folder', "project.png", None],
            [ID_NEW_FILE, 'File', "newfile_wiz.png", None],
        ]
        +baseList[1:],
    "debug": baseList,
    "database": baseList,
    "calibre": baseList
    }

# Id for book explorer
ID_ADD_BOOK = wx.NewIdRef()
ID_EDIT_BOOK_METADATA = wx.NewIdRef()
ID_CONVERT_BOOK = wx.NewIdRef()
ID_GET_BOOK = wx.NewIdRef()
ID_CONNECT_SHARE_BOOK = wx.NewIdRef()
ID_RELOAD_BOOK = wx.NewIdRef()
ID_EDIT_BOOK = wx.NewIdRef()
ID_REMOVE_BOOK = wx.NewIdRef()

ID_FIRST_RESULT = wx.NewIdRef()
ID_PREVIOUS_RESULT = wx.NewIdRef()
ID_NEXT_RESULT = wx.NewIdRef()
ID_LAST_RESULT = wx.NewIdRef()

########################################

ID_BOOK_INFO = wx.NewIdRef()
ID_DELETE_BOOK = wx.NewIdRef()
ID_OPEN_BOOK = wx.NewIdRef()
ID_EDIT_METADATA = wx.NewIdRef()
ID_SEARCH_SIMILAR = wx.NewIdRef()
ID_OPEN_CONTAINING_FOLDER = wx.NewIdRef()
ID_DOWNLOAD_METADATA = wx.NewIdRef()

bookMenuRightClickList = [
    [ID_DOWNLOAD_METADATA, "download-metadata_16.png", "Download metadata and cover." ],
    [ID_OPEN_CONTAINING_FOLDER, "folder.png", "Open containing folder." ],
    [ID_SEARCH_SIMILAR,"similar_16.png", "Search similar books." ],
    [ID_EDIT_METADATA,"edit_input_16.png", "Edit metadata"],
    [ID_OPEN_BOOK, "view_16.png", "Open Book"],
    [ID_DELETE_BOOK, "remove_books_16.png", "Delete Book"],
    [ID_BOOK_INFO, "catalog_16.png", "Information"],
    ]
