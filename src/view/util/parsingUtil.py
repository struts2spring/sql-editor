import re


class SqlParser():
    
    def __init__(self):
        pass
    
    def createSqlToDict(self, createSql=None):
#         print(createSql)
        pattern='''(\s*CREATE TABLE\s*)("?\w+"?)\s+(\(\s+((("?\w+"?)*\s*(UNIQUE\s+(\(\w+\))|PRIMARY KEY\s+(\(\w+\))|FLOAT|DATETIME|INTEGER\s*(NOT NULL)*|VARCHAR\(\d*\)),?\s+))*\s*\))(\s*;?)'''
#         pattern='''(\s*CREATE TABLE\s*)("?\w+"?)\s+(\(\s+("?\w+"?)\s+((UNIQUE\s+(\(\w+\))|PRIMARY KEY\s+(\(\w+\))|FLOAT|DATETIME|INTEGER\s*(NOT NULL)*|VARCHAR\(\d*\))))'''
#         pattern='''\s*\(\s*'''
        matchObj = re.match( pattern, createSql, re.I)
        
        if matchObj:
            print ("matchObj.groups() : ", matchObj.groups())
#             for g in matchObj.groups():
#                 print(g)
            print ("matchObj.group(0) : ", matchObj.group(0))
            print ("matchObj.group(1) : ", matchObj.group(1))
            print ("matchObj.group(2) : ", matchObj.group(2))
        else:
            print ("No match!!")

if __name__ == "__main__":
    
    createSql='create TABLE "ABC" ( "id" INTEGER PRIMARY KEY ) ;  '
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
    sqlParser=SqlParser()
#     sqlParser.createSqlToDict(createSql=createSql)
    sqlParser.createSqlToDict(createSql=createSql1)
    print("Finish")