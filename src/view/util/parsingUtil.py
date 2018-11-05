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
            h_0, t_0 = createSql.split("(", 1)
            h_1, t_1 = t_0.rsplit(")", 1)
            logger.debug (h_0)
            logger.debug (t_0)
            columnPattern = r'''((('|"|`).+?\3)|(\w+))\s*(INTEGER|FLOAT|NUMERIC|REAL|BLOB|TEXT|DATETIME|VARCHAR\(\d*\))?\s*(NOT NULL|PRIMARY KEY)?(\s+AUTOINCREMENT|UNIQUE)?,?\s*(-{2}.*)?'''
            columnDict[0] = ("Position #", "Name", "Datatype", "Nullable", "Auto increment", "Default data", "Description")
            # this is column name
            columnMatchObj=re.match(columnPattern, h_1, re.MULTILINE)
            if columnMatchObj:
                logger.info(columnMatchObj.groups())
            logger.debug(columnMatchObj)
            columnObj = re.findall(columnPattern, h_1, re.MULTILINE)
            if columnObj:
                for idx, columnName in enumerate(columnObj):
                    columnNameInfo = [idx + 1, columnName[0], columnName[4], None, columnName[6], None, columnName[7]] 
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
    columnDict = sqlParser.getColumn(createSql=columns)
    logger.debug(columnDict)
    logger.debug("Finish")
