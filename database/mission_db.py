from database.db_connection import DB_connection, db
from schems import Mission


class DB_mission():
    def __init__(self, db:DB_connection):
        self.db = db

    def create_mission(self, data:Mission):
        level = ''
        level_num = data.difficulty * 2 + data.importance 
        
        if level_num < 10:
            level = 'LOW' 
        elif 9 < level_num < 18:
            level = 'MEDIUM' 
        elif 17 < level_num < 25:
            level = 'HIGH'
        elif 24 < level_num:    
            level = 'CRITICAL'

        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                INSERT INTO agents(title, description, location, difficulty, importance, status, risk_level, assigned_agent_id) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, None)    
                """
                val = (data.title, data.description, data.location, data.difficulty, data.importance, data.status, level)

                cur.execute(sql, val)
                conn.commit()
            
                sql = """
                SELECT * FROM missions
                WHERE id = %s
                """
                new_id = cur.lastrowid()

                cur.execute(sql, (new_id,))

                mission = cur.fetchone()
                return mission if mission else False
             
    def get_all_missions(self):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = "SELECT * FROM missions"

                cur.execute(sql)
                
                missions = cur.fetchall()
                return missions if missions else False

    def get_mission_by_id(self, id:int):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                SELECT * FROM missions
                WHERE id = %s
                """

                cur.execute(sql, (id,))
                
                mission = cur.fetchone()
                return mission if mission else None  

    def assign_mission(self, m_id:int, a_id:int):
        #is_active=False לא יכול לקבל משימות
        #אם risk_level=CRITICAL — רק סוכן בדרגת Commander יכול לקבל את המשימה.
        #סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.
        #ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                UPDATE mission
                SET assigned_agent_id = %s
                WHERE id = %s
                """
                val = (a_id, m_id)

                cur.execute(sql, val)
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'

    def update_mission_status(self, id:int, status:str):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                UPDATE mission
                SET status = %s
                WHERE id = %s
                """
                val = (status, id)

                cur.execute(sql, val)
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'
            
    def get_open_missions_by_agent(self, id:int):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                SELECT * FROM missions
                WHERE assigned_agent_id = %s  
                """

                cur.execute(sql, (id,))
                
                missions = cur.fetchall()
                
                if missions:
                    missions_ls = []
                    for mission in missions:
                        if mission['status'] == 'IN_PROGRESS' or mission['status'] == 'ASSIGNED':
                            missions_ls.append(mission)
                    
                    return missions_ls
                return []

    def count_all_missions(self):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = "SELECT COUNT(*) FROM missions"

                cur.execute(sql)
                
                count = cur.fetchone()
                if count:
                    return count[0]
                return False

    def count_by_status(self, status:str):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT COUNT(*) FROM missions
                WHERE status = %s
                """

                cur.execute(sql, (status,))
                
                count = cur.fetchone()
                if count:
                    return count[0]
                return False
            
    def count_open_missions(self):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT COUNT(*) FROM missions
                WHERE status = 'IN_PROGRESS' OR 'ASSIGNED'
                """

                cur.execute(sql)
                
                count = cur.fetchone()
                if count:
                    return count[0]
                return False

    def count_critical_missions(self):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT COUNT(*) FROM missions
                WHERE risk_level = 'CRITICAL' 
                """

                cur.execute(sql)
                
                count = cur.fetchone()
                if count:
                    return count[0]
                return False

    def get_top_agent(self):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT * FROM agents
                ORDER BY completed_missions DESC
                LIMIT 1
                """

                cur.execute(sql)
                
                agent = cur.fetchone()
                return agent if agent else False
        

            
    