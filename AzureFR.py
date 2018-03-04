import cognitive_face as CF
import ast
from time import sleep, time

KEY = 'a5999be9dd034999b6d0451131f5394c'  #Azure Subscription Key
CF.Key.set(KEY)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

person_groupid = '0'
users = []
userStorage = 'userStorage.txt'
lastvalid_img = None

class user():
	def __init__(self, id, name, link):
		self.id = id
		self.name = name
		self.link = link
		users.append(self)

def storeUsers():
	with open(userStorage, 'w') as store:
		store.write('{')
		c = 0
		store.write('\'a449583e-3a6a-475c-8763-1bbd675ec433\': \'testuser.link\',') #store testuser data
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
		user(k, time(), userDict[k])

def checkImage(img):
	global lastvalid_img
	message = {'statusCode': None, 'msg': ''}
	lists = CF.person.lists('0')
	if str(lists) is not '[]':
		print('List')
		print(CF.person.lists('0'))
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
			CF.person_group.train(person_groupid)
			while True:
				if CF.person_group.get_status(person_groupid)['status'] == 'succeeded':
					break
				else:
					sleep(.5)
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
		message['msg'] += 'Error.'
		print(str(message))
		return message
	else:
		message['statusCode'] = 0
		message['msg'] += 'Valid Image.'
		lastvalid_img = img
		print(str(message))
		return message

def createUser(link, name=time(), img=None):
		global lastvalid_img
		if img is None:
			img = lastvalid_img
		message = {'statusCode': None, 'msg': ''}
		message['statusCode'] = 0
		message['msg'] += 'Success... Created User.'
		personid = CF.person.create(person_groupid, name)['personId']
		print(img)
		print(lastvalid_img)
		img.seek(0)
		CF.person.add_face(img,person_groupid, personid)
		user(personid, name, link)
		print(str(message))
		return message

def searchUsers(img):
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
			cId = idDat[0]['candidates'][0]['personId']
			print(cId)
			print('Users: ')
			print(users)
			for u in users:
				print(u.id)
				if u.id == cId:
					print('M: '+u.id)
					print('Match')
					message['msg'] += u.link
	print(message)
	return message
