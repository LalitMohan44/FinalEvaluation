import pypyodbc


conn = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-VQETJ77Q;"
    "Database=ABC;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

select1 = ("SELECT username,username "
           "FROM UserProfiles ")

cursor.execute(select1)
result1 = cursor.fetchall()
name = [(None, '--Select--')]
name.extend(result1)

result2 = [('Non', '--Select--'),
           ('Round1', 'Round 1'),
           ('Round2', 'Round 2'),
           ('Round3', 'Round 3'),
           ('Round4', 'Round 4'),
           ('HR', 'HR'),
           ('Offer', 'Offer'),
           ('Joined', 'Joined')]


result3 = [('1', '--Select--'),
           ('Scheduled', 'Scheduled'),
           ('Selected', 'Selected'),
           ('Rejected', 'Rejected'),
           ('On Hold', 'On Hold'),
           ('Offer Rolled out', 'Offer Rolled out'),
           ('Offer Accepted', 'Offer Accepted'),
           ('Offer Declined', 'Offer Declined')]


select2 = ("SELECT distinct skills,skills "
           "FROM UserProfiles")
cursor.execute(select2)
result4 = cursor.fetchall()
skill = [("%", '--Select--')]
skill.extend(result4)

select3 = ("SELECT JobID,JobID "
           "FROM Jobs")
cursor.execute(select3)
result5 = cursor.fetchall()
job = [("%", '--Select--')]
job.extend(result5)


