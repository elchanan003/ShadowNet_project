from db_connection import DB_connection, db
from schems import Agent


class DB_agent():
    def __init__(self, db:DB_connection):
        self.db = db


    def create_agent(self, data:Agent):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                INSERT INTO agents(name, specialty, is_active, completed_missions, failed_missions, agent_rank) 
                VALUES(%s, %s, %s, %s, %s, %s)    
                """
                val = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank)

                cur.execute(sql, val)
                conn.commit()
            
                sql = """
                SELECT * FROM agents
                WHERE id = %s
                """
                new_id = cur.lastrowid()

                cur.execute(sql, (new_id,))

                agent = cur.fetchone()
                return agent if agent else False
            
    def get_all_agents(self):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = "SELECT * FROM agents"
                
                cur.execute(sql)

                agents = cur.fetchall()
                return agents if agents else False
            
    def get_agent_by_id(self, id:int):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                SELECT * FROM agents 
                WHERE id = %s 
                """

                cur.execute(sql, (id,))

                agent = cur.fetchone()
                return agent if agent else None
    
    def update_agent(self, id:int, data:Agent):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                UPDATE agents
                SET name = %s, specialty =%s, is_active=%s, completed_missions=%s, failed_missions=%s, agent_rank=%s)   
                WHERE id = %s 
                """
                val = (data.name, data.specialty, data.is_active, data.completed_missions, data.failed_missions, data.agent_rank, id)

                cur.execute(sql, val)
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'
              
    def deactivate_agent(self, id:int):
         with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql="""
                UPDATE agents
                SET is_active = False
                WHERE id = %s
                """

                cur.execute(sql, (id,))
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'
    
    def increment_completed(self, id:int):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql="""
                UPDATE agents
                SET completed_missions = completed_missions + 1
                WHERE id = %s
                """

                cur.execute(sql, (id,))
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'
            
    def increment_failed(self, id:int):
        with self.db.get_conection() as conn:
            with conn.cursor(dictionary=True) as cur:
                sql="""
                UPDATE agents
                SET completed_missions = completed_missions - 1
                WHERE id = %s
                """

                cur.execute(sql, (id,))
                conn.commit()

                if cur.rowcount() > 0:
                    return 'Updated successfully'
                return 'Update failed'
            
    def get_agent_performance(self, id:int):  
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT completed_missions, failed_missions, FROM agents
                WHERE id = %s
                """

                cur.execute(sql, (id,))

                data = cur.fetchall()
                if data and len(data) == 2:
                    completed, failed = data[0], data[1]
                    total = completed + failed

                    perform_dic = {
                        'completed': completed, 
                        'failed': failed, 
                        'total': total, 
                        'success_rate': (completed/total) * 100
                        }
                    
                    return perform_dic
                return False
            
    def count_active_agents(self):
        with self.db.get_conection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT COUNT(*) FROM agents
                WHERE is_active = True
                """        

                cur.execute(sql)
                
                count = cur.fetchone()
                if count:
                    return count[0]
                return False