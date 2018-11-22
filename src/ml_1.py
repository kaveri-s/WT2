import pymysql
import numpy as np
db = pymysql.connect("localhost", "wt2", "pass", "Wt2", charset="latin1")
def reco(sem, s_id):
    s=[]
    for z in range(1,3):
        # sem=5
        pool=z
        # s_id="14ECS100"
        cursor = db.cursor()
        sql = "select c_id from course where  elective=1 and sem=%s and pool=%s;"
        args = ([sem,pool])
        cursor.execute(sql,args)
        electives = list(cursor.fetchall())
        cursor.close()
        electives=[i[0] for i in electives]
        weights=[]

        for i in electives:
        
            cursor=db.cursor()
            sql="select course.c_id from course,c_p_map where course.c_id=c_p_map.p_id and c_p_map.c_id=%s;"
            args=([i])
            cursor.execute(sql,args)
            prereq = [j[0] for j in list(cursor.fetchall())]
            cursor.close()
            if(len(prereq)==0):
                weights.append(0)
            else:
                '''
                prereqs="(\""+prereq[0]+"\""
                for j in range(1,len(prereq)):
                    prereqs+=",\""+prereq[j]+"\""
                prereqs+=")"
                '''
                
                #got prereq codes for that elective
                sql="select sum(marks)/count(marks) from s_c_map where s_id=%s and c_id in %s;"
                args=([s_id,prereq])
                cursor=db.cursor()
                cursor.execute(sql,args)
                prereqavg=cursor.fetchall()
                # print(prereqavg)
                cursor.close()
                prereqavg=float(prereqavg[0][0])


                sql="select sum(marks)/count(marks) from s_c_map where s_id=%s;"
                args=([s_id])
                cursor=db.cursor()
                cursor.execute(sql,args)
                cgpa=cursor.fetchall()
                cursor.close()
                cgpa=float(cgpa[0][0])
                weights.append(prereqavg-cgpa)

        x=list(zip(weights,electives))
        x.sort(reverse=True)
        x=x[:3]
        _,top_electives=zip(*x)
        top_electives=list(top_electives)
        s.extend(top_electives)
    # print(s)
    p=["c_id"]
    l = [dict(zip(p,s)) for row in s]
    print(l)
    return l

# reco(6,"14ECS100")

