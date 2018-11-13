import re
import logging.config
from src.view.constants import LOG_SETTINGS

logger = logging.getLogger('extensive')

logging.config.dictConfig(LOG_SETTINGS)


class SqlParser():
    
    def __init__(self):
        pass
    
    def createSqlToDict(self, createSql=None):
        
#         https://www.debuggex.com/
# https://pythex.org/
#         logger.debug(createSql)
#         pattern='''(\s*CREATE TABLE\s*)("?\w+"?)\s+(\(\s+((("?\w+"?)*\s*(UNIQUE\s+(\(\w+\))|PRIMARY KEY\s+(\(\w+\))|FLOAT|DATETIME|INTEGER\s*(NOT NULL)*|VARCHAR\(\d*\)),?\s+))*\s*\))(\s*;?)'''
#         pattern='''(\s*CREATE TABLE\s*)("?\w+"?)\s+(\(\s+((("?\w+"?)*\s*(UNIQUE\s+(\(\w+\))|PRIMARY KEY\s+(\(\w+\))|FLOAT|DATETIME|INTEGER\s*(NOT NULL)*|VARCHAR\(\d*\)),?\s+))*\s*\))(\s*;?)'''
#         pattern='''(\s*CREATE TABLE\s*)("?\w+"?)\s+(\(\s+("?\w+"?)\s+((UNIQUE\s+(\(\w+\))|PRIMARY KEY\s+(\(\w+\))|FLOAT|DATETIME|INTEGER\s*(NOT NULL)*|VARCHAR\(\d*\))))'''
        pattern = '''\s*(CREATE TABLE)\s+("?\w+"?)\s+\(\s+(("?\w+"?\s+(INTEGER|FLOAT|DATETIME|VARCHAR\(\d*\))\s*(NOT NULL|PRIMARY KEY)?,?\s*)*)\s+(((\s*(PRIMARY KEY|UNIQUE)\s+\(\w+\)),?\s)*)(\)\s*;?)'''
        matchObj = re.match(pattern, createSql, re.I)
        
        if matchObj:
            logger.debug ("matchObj.groups() : ", matchObj.groups())
#             for g in matchObj.groups():
#                 logger.debug(g)
            logger.debug ("matchObj.group(0) : ", matchObj.group(0))
            logger.debug ("matchObj.group(1) : ", matchObj.group(1))
            logger.debug ("matchObj.group(2) : ", matchObj.group(2))
        else:
            logger.debug ("No match!!")
    
    def getColumn(self, createSql=None):
        columnDict = dict()
        if createSql:
            # picking bracket part of create sql
            h_0, t_0 = createSql.split("(", 1)
            h_1, t_1 = t_0.rsplit(")", 1)
            logger.debug("columns: {}".format(h_1))
            logger.debug (t_0)
            
            
            columnText=self.getAllConstrantInSeparteLine(columnText=h_1)
            
            # removing constrinat as last line. primary key , unique key , foreign key
            
            columnPattern = r'''((('|"|`).+?\3)|(\[?\w+\]?))\s*((?i)\bANY\b|(?i)\bJSON\b|(?i)\bINT\b|(?i)\bINTEGER\b|(?i)\bTINYINT\b|(?i)\bSMALLINT\b|(?i)\bMEDIUMINT\b|(?i)\bBIGINT\b|(?i)\bUNSIGNED BIG INT\b|(?i)\bINT2\b|(?i)\bINT8\b|(?i)CHARACTER\([0-9]{3}\)|(?i)\bVARYING CHARACTER\([0-9]{3}\)|(?i)\bNCHAR\([0-9]{3}\)\b|(?i)\bNATIVE CHARACTER\([0-9]{3}\)\b|(?i)\bNVARCHAR\([0-9]+\)|(?i)\bFLOAT\b|(?i)\bNUMERIC\b(\([0-9]+,[0-9]+\))?|(?i)\bDECIMAL\(d+\)\b|(?i)\bBOOLEAN\b|(?i)\bDATE\b|(?i)\bDATETIME\b|(?i)\[timestamp\]|(?i)\bREAL\b|(?i)\bDOUBLE\b|(?i)\bDOUBLE PRECISION\b|(?i)\bCLOB\b|(?i)\bBLOB\b|(?i)\bTEXT\b|(?i)\bDATETIME\b|(?i)VARCHAR\([0-9]*\))?\s*((?i)\bHIDDEN\b|(?i)\bNULL\b|(?i)\bNOT NULL\b|(?i)\bPRIMARY KEY\b\s*(ASC|DSC)?)?((?i)\bDEFAULT\b .*)?(\s+(?i)\bAUTOINCREMENT\b|(?i)\bUNIQUE\b)?,?\s*(-{2}.*)?'''
            columnDict[0] = ("#", "Name", "Datatype", "PRIMARY KEY", "Nullable", "Unique", "Auto increment", "Hidden", "Default data","Description")
            # this is column name
            columnMatchObj = re.match(columnPattern, columnText, re.MULTILINE)
            if columnMatchObj:
                logger.info(columnMatchObj.groups())
            logger.debug(columnMatchObj)
            columnObj = re.findall(columnPattern, columnText, re.MULTILINE)
            if columnObj:
                for idx, columnName in enumerate(columnObj):
                    default_data = None
                    if columnName[6] and 'default' in columnName[6].lower():
                        default_data = columnName[6].lower().replace("default", "").strip()
                    auto_increment = None
                    if columnName[7] and 'AUTOINCREMENT' in columnName[7].upper():
                        auto_increment = 'AUTOINCREMENT'
                    nullable = None
                    if columnName[7] and 'NOT NULL' in columnName[7].upper():
                        nullable = 'NOT NULL'
                    description = None
                    if columnName[9] and '--' in columnName[9]:
                        description = columnName[9]
                    primaryKey = None
                    if columnName[5] and columnName[5].upper().startswith('PRIMARY KEY'):
                        primaryKey = columnName[5]
                    unique = None
                    if columnName[8] and 'PRIMARY KEY' in columnName[8].upper():
                        unique = columnName[8]
                    hidden = None
                    if columnName[5] and 'HIDDEN' in columnName[5].upper():
                        hidden = columnName[5]
                    columnNameInfo = [idx + 1, columnName[0], columnName[4], primaryKey, nullable, unique, auto_increment,hidden, default_data, description] 
                    columnDict[idx + 1] = tuple(columnNameInfo)
            else:
                logger.debug ("columns : {}".format(h_1))      
        
#         createTablePattern='''\s*(CREATE TABLE)\s+((('|").*?\4)|("?\w+"?))\s+\(\s*((((('|").*?\10)|("?\w+"?))\s+(INTEGER|FLOAT|DATETIME|VARCHAR\(\d*\))\s*(NOT NULL|PRIMARY KEY)?,?\s*)*)\s+(((\s*(PRIMARY KEY|UNIQUE)\s+\(\w+\)),?\s)*)(\)\s*;?)'''
#         tableMatchObj = re.match( createTablePattern, createSql, re.I)
#         
#         columnPattern='''(('|").+?\1)\s+(INTEGER|FLOAT|DATETIME|VARCHAR\(\d*\))\s*(NOT NULL|PRIMARY KEY)?,?\s*'''
#         if tableMatchObj:
# #             logger.debug ("tableMatchObj.groups() : ", tableMatchObj.groups())
#             
#             for idx, matchValue in enumerate(tableMatchObj.groups()):
#                 if idx==6:
#                     columnDict[0]=("Position #", "Name", "Datatype", "Nullable", "Auto increment", "Default data")
#                     # this is column name
#                     columnMatchObj = re.findall( columnPattern, matchValue, re.I)
#                     if columnMatchObj:
#                         for idx, columnName in enumerate(columnMatchObj):
#                             columnNameInfo=[idx+1]+list(columnName)+[None, None] 
#                             columnDict[idx+1]= tuple(columnNameInfo)
#                     else:
#                         logger.debug ("columns : {}".format(matchValue))
#                             
#         else:
#             logger.debug ("No match!! : {}".format(createSql))
        return columnDict

    def getAllConstrantInSeparteLine(self, columnText=None):
        onlyColumns=[]
        columnsList = columnText.split(",")
        for column in columnsList:
            logger.debug(column.strip())
            column1=column.strip().lower()
            if not column1.startswith(('constraint','primary key','unique','foreign key')):
                onlyColumns.append(column)
        logger.debug(onlyColumns)   
        return ",".join(onlyColumns)    

if __name__ == "__main__":
    columns = '''
    id INTEGER NOT NULL, 
    vc1_dept_descr VARCHAR(250), 
    work_location_country VARCHAR(250), 
    middle_initial VARCHAR(250), 
    floor_number VARCHAR(250), 
    hr_latest_hire_date VARCHAR(250), 
    hr_department_desc VARCHAR(250), 
    user_type VARCHAR(250), 
    mu_cost_code VARCHAR(250), 
    assistant_dept VARCHAR(250), 
    countrya2 VARCHAR(250), 
    paygroup VARCHAR(250), 
    countrya3 VARCHAR(250), 
    employee_id_number VARCHAR(250), 
    comit_id VARCHAR(250), 
    display_name VARCHAR(250), 
    company VARCHAR(250), 
    phone VARCHAR(250), 
    assistant_phone VARCHAR(250), 
    mu_full_name VARCHAR(250), 
    email_id VARCHAR(250), 
    job_title VARCHAR(250), 
    descr VARCHAR(250), 
    hire_dt DATETIME, 
    assistant_name VARCHAR(250), 
    lync_phone VARCHAR(250), 
    work_location_city VARCHAR(250), 
    management_unit VARCHAR(250), 
    dept VARCHAR(250), 
    friendly_company VARCHAR(250), 
    first_name VARCHAR(250), 
    last_name VARCHAR(250), 
    building_name VARCHAR(250), 
    active_flag VARCHAR(250), 
    manager VARCHAR(250), 
    hr_department VARCHAR(250), 
    mu_company_code_description VARCHAR(250), 
    sector_id VARCHAR(250), 
    hr_supervisor_id VARCHAR(250), 
    preferred_first_name VARCHAR(250), 
    city VARCHAR(250), 
    deptm VARCHAR(250), 
    manager_email VARCHAR(250), 
    manager_comit VARCHAR(250), 
    ms_rtcsip_primary_user_address VARCHAR(250), 
    shift_info VARCHAR(250), 
    dn VARCHAR(250), 
    office VARCHAR(250), 
    dialing_code VARCHAR(250), 
    assistant_comit VARCHAR(250), 
    bud_description VARCHAR(250), 
    sector_description VARCHAR(250), 
    employee_status VARCHAR(250), 
    aim_number VARCHAR(250), 
    mu_company_code VARCHAR(250), 
    hr_supervisor_first_name VARCHAR(250), 
    preferred_last_name VARCHAR(250), 
    functional_manager VARCHAR(250), 
    business_unit VARCHAR(250), 
    e164_mobile VARCHAR(250), 
    mu_owner_comit_id VARCHAR(250), 
    mu_owner_first_name VARCHAR(250), 
    grade VARCHAR(250), 
    postal VARCHAR(250), 
    domain VARCHAR(250), 
    work_location_state VARCHAR(250), 
    dept_descr VARCHAR(250), 
    friendly_department VARCHAR(250), 
    empl_type VARCHAR(250), 
    state VARCHAR(250), 
    shift VARCHAR(250), 
    manager_phone VARCHAR(250), 
    dept_entry_dt DATETIME, 
    full_name VARCHAR(250), 
    hr_supervisor_last_name VARCHAR(250), 
    dept_id VARCHAR(250), 
    per_org VARCHAR(250), 
    sector_short_description VARCHAR(250), 
    address2 VARCHAR(250), 
    address1 VARCHAR(250), 
    hrdept_short_mb VARCHAR(250), 
    mail_drop VARCHAR(250), 
    full_part_time VARCHAR(250), 
    mu_owner_last_name VARCHAR(250), 
    mgmtchain VARCHAR(250), 
    subords VARCHAR(250), 
    management_unit_description VARCHAR(250), 
    downward_reporting VARCHAR(250), 
    "laDateTimee_date" DATETIME, 
    ind INTEGER, 
    score FLOAT, 
    corp_title VARCHAR(250), 
    _version_ INTEGER, 
    _lw_batch_id_s VARCHAR(250), 
    _lw_data_source_pipeline_s VARCHAR(250), 
    _lw_data_source_type_s VARCHAR(250), 
    _lw_data_source_collection_s VARCHAR(250), 
    _lw_data_source_s VARCHAR(250), 
    PRIMARY KEY (id), 
    UNIQUE (comit_id), 
    UNIQUE (email_id)
    '''
    
    createSql_2 = "CREATE TABLE 'Table 1' ( 'column 1' INTEGER PRIMARY KEY )"
    createSql_1 = 'create TABLE "ABC" ( "id" INTEGER PRIMARY KEY ) ;  '
    createSql1 = '''
CREATE TABLE employee (
    id INTEGER NOT NULL, 
    vc1_dept_descr VARCHAR(250), 
    work_location_country VARCHAR(250), 
    middle_initial VARCHAR(250), 
    floor_number VARCHAR(250), 
    hr_latest_hire_date VARCHAR(250), 
    hr_department_desc VARCHAR(250), 
    user_type VARCHAR(250), 
    mu_cost_code VARCHAR(250), 
    assistant_dept VARCHAR(250), 
    countrya2 VARCHAR(250), 
    paygroup VARCHAR(250), 
    countrya3 VARCHAR(250), 
    employee_id_number VARCHAR(250), 
    comit_id VARCHAR(250), 
    display_name VARCHAR(250), 
    company VARCHAR(250), 
    phone VARCHAR(250), 
    assistant_phone VARCHAR(250), 
    mu_full_name VARCHAR(250), 
    email_id VARCHAR(250), 
    job_title VARCHAR(250), 
    descr VARCHAR(250), 
    hire_dt DATETIME, 
    assistant_name VARCHAR(250), 
    lync_phone VARCHAR(250), 
    work_location_city VARCHAR(250), 
    management_unit VARCHAR(250), 
    dept VARCHAR(250), 
    friendly_company VARCHAR(250), 
    first_name VARCHAR(250), 
    last_name VARCHAR(250), 
    building_name VARCHAR(250), 
    active_flag VARCHAR(250), 
    manager VARCHAR(250), 
    hr_department VARCHAR(250), 
    mu_company_code_description VARCHAR(250), 
    sector_id VARCHAR(250), 
    hr_supervisor_id VARCHAR(250), 
    preferred_first_name VARCHAR(250), 
    city VARCHAR(250), 
    deptm VARCHAR(250), 
    manager_email VARCHAR(250), 
    manager_comit VARCHAR(250), 
    ms_rtcsip_primary_user_address VARCHAR(250), 
    shift_info VARCHAR(250), 
    dn VARCHAR(250), 
    office VARCHAR(250), 
    dialing_code VARCHAR(250), 
    assistant_comit VARCHAR(250), 
    bud_description VARCHAR(250), 
    sector_description VARCHAR(250), 
    employee_status VARCHAR(250), 
    aim_number VARCHAR(250), 
    mu_company_code VARCHAR(250), 
    hr_supervisor_first_name VARCHAR(250), 
    preferred_last_name VARCHAR(250), 
    functional_manager VARCHAR(250), 
    business_unit VARCHAR(250), 
    e164_mobile VARCHAR(250), 
    mu_owner_comit_id VARCHAR(250), 
    mu_owner_first_name VARCHAR(250), 
    grade VARCHAR(250), 
    postal VARCHAR(250), 
    domain VARCHAR(250), 
    work_location_state VARCHAR(250), 
    dept_descr VARCHAR(250), 
    friendly_department VARCHAR(250), 
    empl_type VARCHAR(250), 
    state VARCHAR(250), 
    shift VARCHAR(250), 
    manager_phone VARCHAR(250), 
    dept_entry_dt DATETIME, 
    full_name VARCHAR(250), 
    hr_supervisor_last_name VARCHAR(250), 
    dept_id VARCHAR(250), 
    per_org VARCHAR(250), 
    sector_short_description VARCHAR(250), 
    address2 VARCHAR(250), 
    address1 VARCHAR(250), 
    hrdept_short_mb VARCHAR(250), 
    mail_drop VARCHAR(250), 
    full_part_time VARCHAR(250), 
    mu_owner_last_name VARCHAR(250), 
    mgmtchain VARCHAR(250), 
    subords VARCHAR(250), 
    management_unit_description VARCHAR(250), 
    downward_reporting VARCHAR(250), 
    "laDateTimee_date" DATETIME, 
    ind INTEGER, 
    score FLOAT, 
    corp_title VARCHAR(250), 
    _version_ INTEGER, 
    _lw_batch_id_s VARCHAR(250), 
    _lw_data_source_pipeline_s VARCHAR(250), 
    _lw_data_source_type_s VARCHAR(250), 
    _lw_data_source_collection_s VARCHAR(250), 
    _lw_data_source_s VARCHAR(250), 
    PRIMARY KEY (id), 
    UNIQUE (comit_id), 
    UNIQUE (email_id)
)
        '''
    sqlParser = SqlParser()
#     sqlParser.createSqlToDict(createSql=createSql)
#     columnDict = sqlParser.getColumn(createSql=columns)
    columnText="""   _lw_data_source_collection_s VARCHAR(250), 
        _lw_data_source_s VARCHAR(250), 
        PRIMARY KEY (id), 
        UNIQUE (comit_id), 
        UNIQUE (email_id)
    """
    sqlParser.getAllConstrantInSeparteLine(columnText)
#     logger.debug(columnDict)
    logger.debug("Finish")
