import cognitive_face as CF

KEY = 'a5999be9dd034999b6d0451131f5394c'  #Azure Subscription Key
CF.Key.set(KEY)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

person_groupid = '0'

def resetGroup(testUser=True):
	CF.person_group.delete(person_groupid)
	CF.person_group.create(person_groupid)
	if testUser:
		pid = CF.person.create(person_groupid, 'testUser')['personId']
		CF.person.add_face('/Users/LukeM/Desktop/FR_testimages/jamesb_test1.jpeg', person_groupid, pid)
		print('testUser created')
	
	CF.person_group.train(person_groupid)
	print('Person Group '+str(person_groupid)+' Cleard')

resetGroup(False)
