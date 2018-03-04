import cognitive_face as CF
import ast
from time import sleep

KEY = 'a5999be9dd034999b6d0451131f5394c'  #Azure Subscription Key
CF.Key.set(KEY)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

person_groupid = '0'
users = []
userStorage = '/Users/LukeM/faceqr/userStorage.txt'
lastcreatedId = None
persistance = False

def resetGroup():
	CF.person_group.delete(person_groupid)
	CF.person_group.create(person_groupid)
	pid = CF.person.create(person_groupid, 'testUser')['personId']
	CF.person.add_face('/Users/LukeM/Desktop/FR_testimages/jamesb_test1.jpeg', person_groupid, pid)
	CF.person_group.train(person_groupid)

class user():
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.link = 'None'
		users.append(self)

def addLink(link, uid=None):
	if uid is not None:
		for u in users:
			if u.id == uid:
				u.link = link
	else:
		for u in users:
			if u.id == lastcreatedId:
				u.link = link

def storeUsers():
	if persistance is True:
		with open(userStorage, 'w') as store:
			store.write('{')
			c = 0
			for u in users:
				store.write('\''+u.id+'\': \''+u.link+'\'')
				if c < len(users)-1:
					store.write(',')
				c += 1

			store.write('}')

def readUsers():
	with open(userStorage, 'r') as store:
		userDict = store.readline()
		userDict = ast.literal_eval(userDict)
	for k in userDict.keys():
		user(k, userDict[k])

def createUser(Name, img):
	message = {'statusCode': None, 'msg': ''}
	if CF.person_group.lists() is not '[]':
		img.seek(0)
		faceId = CF.face.detect(img)
		lenFaces = len(faceId)
		if lenFaces < 1:
			message['msg'] += 'No face detected... '
			cUser = False
		elif lenFaces > 1:
			message['msg'] += 'More than one face detected... '
			cUser = False
		else:
			faceId = faceId[0]['faceId']
			idDat = CF.face.identify([faceId], person_group_id=person_groupid)
			if len(idDat[0]['candidates']) == 0:
				cUser = True
			else:
				cUser = False
				message['msg'] += 'Face already in userbase... '
	else:
		img.seek(0)
		faceId = CF.face.detect(img)
		lenFaces = len(faceId)
		if lenFaces < 1:
			message['msg'] += 'No face detected... '
			cUser = False
		elif lenFaces > 1:
			message['msg'] += 'More than one face detected... '
			cUser = False
		else:
			cUser = True

	if cUser is False:
		message['statusCode'] = 1
		message['msg'] += 'Error'
		print(str(message))
		return message
	else:
		message['statusCode'] = 0
		message['msg'] += 'Success'
		print(str(message))
		personid = CF.person.create(person_groupid, Name)['personId']
		img.seek(0)
		CF.person.add_face(img,person_groupid, personid)
		user(personid, Name)
		lastcreatedId = personid
		return message

def searchforUser(img):
	message = {'statusCode': None, 'msg': ''}
	sleep(.1)
	CF.person_group.train(person_groupid)
	while True:
		if CF.person_group.get_status(person_groupid)['status'] == 'succeeded':
			break
		else:
			sleep(.5)
	img.seek(0)
	faces = CF.face.detect(img)
	lenFaces = len(faces)
	if lenFaces > 1:
		message['statusCode'] = 1
		message['msg'] += 'More than one face detected... '
	elif lenFaces < 1:
		message['statusCode'] = 1
		message['msg'] += 'No face detected... '
	else:
		faceId = faces[0]['faceId']
		idDat = CF.face.identify([faceId], person_group_id=person_groupid)
		if len(idDat[0]['candidates']) == 0:
			message['msg'] += 'No match found.'
			message['statusCode'] = 0
		else:
			cId = idDat[0]['candidates'][0]
			for u in users:
				if u.id == cId:
					message['msg'] += u.link
	print(message)
	return message
