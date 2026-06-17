__תאור המערכת__

ניהול סוכנים ומשימות של יחידת מודיעין.
המערכת עובדת מול מסד נתונים המכיל מידע על סוכנים ומשימות,
היא אחראית על יצירת הגדרת ואיתור הסוכנים, על יצירת ושיוך המשימות, וכן על ניתוח נתונים והחזרת דוחות


__מבנה התיקיות__

```text
shadownet_project/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```


__טבלאות__

agents:
(
    id,
    name,
    specialty,
    is_active,
    completed_missions,
    failed_mission,
    agent_rank
)

missions:
(
    id,
    title,
    description,
    location,
    difficulty,
    status,
    risk_level,
    assigned_agent_id
)


__מחלקות__

DB_connection:
___
get_connection() --> מחזירה חיבור פעיל ל sql

create_database() --> יוצרת את Intelligence_db אם לא קיים

create_tables() --> יוצרת את שתי הטבלאות אם לא קיימות


AgentDB:
___
create_agent(data) --> יוצרת סוכן חדש ומחזירה את המילון של הסוכן

get_all_agents() --> מחזירה רשימת כל הסוכנים

get_agent_by_id(id) --> מחזירה סוכן אחד לפי ID, או None

update_agent(id, data) --> UPDATE לכל השורה (אין אפשרות לשנות id)

deactivate_agent(id) --> מגדירה מצב סוכן ללא פעיל

increment_completed(id) --> מעדכן את כמות המשימות שהושלמו 

increment_failed(id) --> מעדכן את כמות המשימות שנכשלו

get_agent_performance(id) --> מחזירה מילון עם המפתחות האלו completed, failed, total, success_rate

count_active_agents() --> מחזירה את מספר הסוכנים הפעילים 


MissionDB:
___
create_mission(data) --> יצירת משימה חדשה ומחזירה את כל האובייקט

get_all_missions() --> מחזירה את כל המשימות

get_mission_by_id(id) --> מחזירה משימה אחת לפי ID, או None

assign_mission(m_id, a_id) --> משייכת משימה לסוכן

update_mission_status(id, status) --> משמשת לכל שינוי סטטוס

get_open_missions_by_agent(id) --> מחזירה משימות ASSIGNED/IN_PROGRESS של סוכן

count_all_missions() --> סה"כ משימות

count_by_status(status) --> סופרת לפי סטטוס מסוים

count_open_missions() --> סופרת משימות פתוחות

count_critical_missions() --> סופרת משימות CRITICAL

get_top_agent() --> הסוכן עם completed_missions הגבוה ביותר


__עשרה חוקים לרשימת הנתונים__

 rank חייב להיות Junior / Senior / Commander — כל ערך אחר זורק שגיאה.

 difficulty ו-importance חייבים להיות בין 1 ל-10 — אחרת שגיאה.

 risk_level מחושב אוטומטית בעת יצירת משימה — המשתמש לא שולח אותו.

 סוכן עם is_active=False לא יכול לקבל משימות.

 סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.

 אם risk_level=CRITICAL — רק סוכן בדרגת Commander יכול לקבל את המשימה.

 ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.

 ניתן להתחיל רק משימה בסטטוס ASSIGNED. לאחר: status=IN_PROGRESS.

 ניתן לסיים רק משימה. IN_PROGRESS  ולשנות לסטטוס failed or completed

 ניתן לבטל רק משימה בסטטוס NEW או ASSIGNED — אחרת שגיאה.

__הוראות הרצה__

docker run -p 3306:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -d mysql:8.0

*הטבלאות נוצרות בהפעלת הקובץ main

