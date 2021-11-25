from django.contrib import auth
from django.shortcuts import redirect, render

from django.http import HttpResponse
from .models import *
# ระบบส่งไลน์
from songline import Sendline
# ระบบส่งเมล์
from .emailsystem import sendthai

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required # เข้าถึงโดยต้อง login

from django.core.files.storage import FileSystemStorage


#def Home(request):
#	return HttpResponse('<h1>Hello World!</h1> <br> <p> by Company</p>')
def Login(request):

	context = {}

	if request.method == 'POST':
		data = request.POST.copy()
		username = data.get('username')
		password = data.get('password')
		try:
			user = authenticate(username = username, password = password)
			login(request,user)
			return redirect('profile-page')
		except:
			context['message'] = 'user or password is not correct'

		
		
	return render(request, 'company/login.html',context)

def Home(request):
	allproduct = Product.objects.all()
	context = {'allproduct':allproduct}
	# แยกแถวละ 3 card เพื่อทำ pagination
	allrow = []
	row = []
	for i,p in enumerate(allproduct):
		if i % 3 == 0:
			if i != 0: # ถ้าไม่ใช่ i = 0 จะเพิ่มเข้า allrow
				allrow.append(row)
			row =[]
			row.append(p)
		else:
			row.append(p)
	allrow.append(row)
	context['allrow'] = allrow # แนบ allrow

	return render(request, 'company/home.html',context)

def AboutUs(request):
	return render(request, 'company/aboutus.html')

def ContactUs(request):

	context = {}

	if request.method == 'POST':
		data = request.POST.copy()
		title = data.get('title')
		email = data.get('email')
		detail = data.get('detail')
		print(title)
		print(email)
		print(detail)
		
		# กรณี ยูเซอร์ ไม่กรอกข้อมูล title email เช็คอย่างไร แบบง่าย
		if title == '' or email == '':
			context['message'] = "รบกวนกรอกข้อมูลให้ครบ"
			return render(request, 'company/contact.html',context)
		
		
		print('เมื่อได้ข้อมูลแล้วจะบันทึกข้อมูลลงดาต้าเบส')
		# ContactList(title=title, email = email, detail=detail).save()
		newrecord = ContactList()
		newrecord.title = title
		newrecord.email = email
		newrecord.detail = detail
		newrecord.save()
		context['message'] = 'ได้รับเรียนร้อยแล้ว'

		#ส่งอีเมล์ตอบกลับด้วย sendthai
		text = 'สวัสดีคุณลูกค้า\n\nทางเราได้รับปัญาที่่ท่านสอบถามเรียบร้อยแล้ว'
		sendthai(email,'Uncle สอบถามปัญหา',text)

		#ส่งไลน์
		token = 've9A8RasjvZs2WOCjmWzz2mIvjB9X09n8kFX6aknnFK'
		m = Sendline(token)
		m.sendtext('\nหัวข้อ:{} \nอีเมลล์:{}\n >>> {}'.format(title,email,detail))

	return render(request, 'company/contact.html',context)

from django.contrib.auth.decorators import login_required

@login_required()
def Accountant(request):
	#if request.user.profile.usertype != 'accountant': # วิธีที่ 1
	# วิธีที่ 2 อนูญาติ admin ด้วย โดยสร้าง list เพื่อ เช็ค type
	allow_user = ['accountant','admin']
	if request.user.profile.usertype not in allow_user:
		return redirect('home-page') # improt redirect

	contact = ContactList.objects.all().order_by('-id')
	context = {'contact':contact}
	return render(request, 'company/accountant.html',context)

#from django.contrib.auth.models import User
def Register(request):

	context = {}

	if request.method == 'POST':
		data = request.POST.copy()
		fullname = data.get('fullname')
		mobile = data.get('mobile')
		email = data.get('username')
		username = email.split("@")[0]
		password = data.get('password')
		password2 = data.get('password2')

	# มี User อยู่แล้วไหม
		try:
			check = User.objects.get(email=email)
			context['warning'] = 'email:{} มีในระบบแล้ว กรุณาใช้ email.ใหม่'.format(email)
			context['fullname']= fullname
			context['mobile']= mobile
			return render(request, 'company/register.html',context)
		except:
	# เช็คพาสเวฺด 2 ครั้ง เหมือนไหม
			if password != password2:
				context['warning'] = 'กรุุณากรอกรหัสสองครั้งให้ถูกต้อง'
				context['fullname']= fullname
				context['mobile']= mobile
				return render(request, 'company/register.html',context)
			newuser = User()
			newuser.username = username
			#newuser.username = username
			newuser.email = email
			newuser.first_name = fullname
			newuser.set_password(password)
			newuser.save()

			u = uuid.uuid1() #สร้าง uid เพื่อ verity token โดยต้องสร้าง model verify ใน Profile ก่อน
			token = str(u)

			newprofile = Profile()
			#print('1 profile:{} '.format(username))
			newprofile.user = User.objects.get(username=username)
			newprofile.mobile = mobile
			newprofile.verify_token = token
			newprofile.save()

			text = 'กรุณากดลิ้งค์นีเพื่อ ยืนยันการเป็นสมาชิก \n\n LINK: http://localhost:8000/verify-email/' + token
			sendthai(email,'ยืนยันการสมัครสมาชิก',text)
			#return redirect('profile-page')

		try:
			user = authenticate(username = username, password = password)
			login(request,user)
			return redirect('profile-page') ##### ล่าสุด หาทาง return
		except:
			context['message'] = 'user or password is not correct'

	
	return render(request, 'company/register.html',context)

# verity sussuss
def Verify_Success(request,token):
	context = {}
	try:
	# check token Profile ว่าตรงกันไหม
		check = Profile.objects.get(verify_token=token)
		check.verified = True
		check.point = 100
		check.save()
	except:
		context['error'] = 'ลิงค์สำหรับยืนยันตัวจนของคุณไม่ถูกต้อง กรุณา copy มาวางบน Browser แทน'
	return render(request, 'company/verifyemail.html', context)


@login_required()
def ProfilePage(request):
	context = {}
	profileuser = Profile.objects.get(user=request.user)
	context['profile'] = profileuser
	return render(request, 'company/profile.html',context)

import uuid

def ResetPassword(request):

	context = {}

	if request.method == 'POST':
		data = request.POST.copy()
		email = data.get('email')
		#print('1 email:{} '.format(email))
		username = email.split("@")[0]
		try: 
			user = User.objects.get(email=email)
			#print('2 emailcheck:{} '.format(user))
			#user = emailcheck.split("@")[0]
			
			
			u = uuid.uuid1()
			token = str(u)
			#print('3 user:{} '.format(token))

			newreset =  ResetPasswordToken()
			newreset.user = user
			#print(newreset.user)
			newreset.token = token
			newreset.save()
			# ส่งเมล์
			text = 'กรุณากดลิ้งค์นีเพื่อ reset \n\n LINK: http://localhost:8000/reset-new-password/' + token
			sendthai(email,'reset password link (uncle shop)',text)
			context['message'] = 'กรุณาตรวจสอบอีเมล์ล่าสุุดของคุณ'
		except:
			context['message'] = 'อีเมล์ของคุณไม่มีในระบบ กรูณาตรวจสอบความถูกต้อง'

	return render(request, 'company/resetpassword.html',context)

def ResetNewPassword(request,token):
	context = {}
	print('token:', token)

	try:
	# check token ว่าตรงกันไหม
		check = ResetPasswordToken.objects.get(token=token)
		if request.method == 'POST':
			data = request.POST.copy()
			password1 = data.get('resetpassword1')   # name="ใน form"
			password2 = data.get('resetpassword2')
			if password1 == password2:
				user = check.user   #ใช้ check.user ได้เพราะผูกกันในโมเดลแล้ว
				user.set_password(password1)
				user.save()
				# login automatic
				user = authenticate(username = user.username, password = password1)
				login(request,user)
				# redirect to profile auto
				return redirect('profile-page')
			else:
				context['error'] = 'รหัสไม่ถูกต้องกรุณากรอกใหม่อีกครั้ง'
	except:
		context['error'] = 'ลิงค์สำหรับรีเซ็ตรหัสผ่านของคุณไม่ถูกต้อง'
	return render(request, 'company/resetnewpassword.html', context)

def ActionPage(request, cid): # cid = contactlist id
	context ={}

	contact = ContactList.objects.get(id=cid)
	context['contact'] = contact
	print('1 contact:{} '.format(contact))
	
	try:
		action = Action.objects.get(contactlist = contact)
		print('2 action:{} '.format(action))
		context['action'] = action
	except: pass

	if request.method == 'POST':
		data = request.POST.copy() 	# print(data) --->>>  Output 'detail': ['asdffadfa'], 'save': ['']
		print('3 data:{} '.format(data))
		detail = data.get('detail')


		# เขียน check method post ว่า user กดปุ่มส่ง nmae ไหนมา
		if 'save' in data: 	#  ปุ่มบันทึก และแก้ไข
			print('save data')
			try:
				check = Action.objects.get(contactlist=contact)
				if check.actiondetail == detail:
					pass
				else :
					check.actiondetail = detail   # ถ้ามี save ทับ
					check.save()
					context['action'] = check # เพื่อ update เมื่อมีการแก้ไข
				#print(context['action'])
			except:
				new = Action()
				new.contactlist = contact
				new.actiondetail = detail
				new.save()
				context['action'] = new
		elif 'delete' in data:
			print('delete data')
			try: 
				#check = Action.objects.get(contactlist=contact)
				#check.delete() # delete action
				
				contact.delete()
				
				return redirect('accountant-page')
			except:
				pass
		elif 'complete' in data:
			print ('mark completed')
			contact.complete = not contact.complete
			contact.save()
			return redirect('accountant-page')

		# ไม่มี else เนื่องจากไม่มีโอกาส user กดปุ่มอื่นใน page นั้น

	return render(request, 'company/action.html',context)

# Add Product
def AddProduct(request):
	if request.method == 'POST':
		data =request.POST.copy()
		title = data.get('title')
		description = data.get('description')
		price = data.get('price')
		quantity = data.get('quantity')
		instock = data.get('instock')
		# ทดสอบ
		#print('1 Files', request.FILES)
		

		new = Product()
		new.title = title
		new.description = description
		new.price = float(price)
		new.quantity = int(quantity)
		# if instock != None 
		if instock == instock :
			new.instock = True

		if 'picture' in request.FILES:
			file_image = request.FILES['picture']
			file_image_name = file_image.name.replace(' ','') # ตัด spec ทิ้ง
			# from django.core.files.storage import FileSystemStorage
			fs = FileSystemStorage(location='/media/product')
			filename = fs.save(file_image_name, file_image)
			upload_file_url = fs.url(filename)
			print('Picture URL:',upload_file_url)
			new.picture = '/product' + upload_file_url[6:] #ตัด media

		if 'specfile' in request.FILES:
			file_specfile = request.FILES['specfile']
			file_specfile_name = file_image.name.replace(' ','') # ตัด spec ทิ้ง
			# from django.core.files.storage import FileSystemStorage
			fs = FileSystemStorage()
			filename = fs.save(file_specfile_name, file_specfile)
			upload_file_url = fs.url(filename)
			print('Picture URL:',upload_file_url)
			new.specfile = upload_file_url[6:] #ตัด media
		new.save()




		
	return render(request, 'company/addproduct.html')