from to_test.models import *

session = Session()

user1 = Users(first_name="Igor", last_name="Leleka", email="igorlel@gmail.com", username="igorlel", password="20061995il", userstatus=0)
user2 = Users(first_name="Kolya", last_name="Dzibiuk", email="koldzib@gmail.com", username="koldzib", password="30112002kd", userstatus=1)
user3 = Users(first_name="Denys", last_name="Malaniuk", email="denmal@gmail.com", username="denmalan", password="12091999dm", userstatus=1)

note1 = Notes(title="Some note", text="qwertyuiopasdfghjklzxcvbnm", ispublic=True, user=user1, dateofediting='2022-12-24')
note2 = Notes(title="Another note", text="qazxswedcvfrtgbnhyujm,kiol./;p[", ispublic=False, user=user2, dateofediting='2018-3-13')
note3 = Notes(title="Useless note", text="qwertyuiopasdfghjklzxcvbnmbhhvkbnjkbgdfjddbghfjfdsbjghfk", ispublic=True, user=user3, dateofediting='2021-08-30')

tag1 = Tags(text='Important')
tag2 = Tags(text='Sport')
tag3 = Tags(text='Robots')

tagnote1 = TagNote(note=note1, tag=tag1)
tagnote2 = TagNote(note=note1, tag=tag2)
tagnote3 = TagNote(note=note2, tag=tag3)
tagnote4 = TagNote(note=note3, tag=tag2)

stat1 = Stats(user=user1, numofnotes=1, numofeditingnotes=3, dateofcreating='2022-10-23')
stat2 = Stats(user=user3, numofnotes=1, numofeditingnotes=3, dateofcreating='2022-10-22')

allowedNote1 = AllowedNotes(user=user1, note=note1)
allowedNote2 = AllowedNotes(user=user2, note=note1)
allowedNote3 = AllowedNotes(user=user3, note=note1)

session.add(user1)
session.add(user2)
session.add(user3)

session.add(note1)
session.add(note2)
session.add(note3)

session.add(tag1)
session.add(tag2)
session.add(tag3)

session.add(tagnote1)
session.add(tagnote2)
session.add(tagnote3)
session.add(tagnote4)

session.add(stat1)
session.add(stat2)

session.add(allowedNote1)
session.add(allowedNote2)
session.add(allowedNote3)

session.commit()

print(session.query(Users).all()[0].first_name, session.query(Users).all()[0].last_name)