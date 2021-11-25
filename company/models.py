from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create Autholization
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	usertype = models.CharField(max_length=100,default='member')
	point = models.IntegerField(default=0)
	mobile = models.CharField(max_length=20,null=True,blank=True)
	# เพิ่ม model เพื่อตรวจสอบ สมาชิก
	verified = models.BooleanField(default=False)
	verify_token = models.CharField(max_length=100,default='no token')

	def __str__(self):
		return self.user.username

class ResetPasswordToken(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeigKey
	token = models.CharField(max_length=100)
	
	def __str__(self):
		return self.user.username

class Product(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
	quantity = models.IntegerField(null=True, blank=True)
	instock = models.BooleanField(default=True)
	# file And instll pagket pillow
	picture = models.ImageField(upload_to='product', null=True, blank=True)
	specfile = models.FileField(upload_to='specfile', null=True, blank=True)

	def __str__(self):
		return self.title

# ลูกค้าส่งปัญหา
class ContactList(models.Model):
	title = models.CharField(max_length=200)
	email = models.CharField(max_length=100)
	detail = models.TextField(null=True, blank=True)
	complete = models.BooleanField(default=False)

	def __str__(self):
		return '{} --- {}' .format(self.title, self.detail)

# สร้าง CRUD สำหรับ accountan ใช้ดำเนินการ
class Action(models.Model):
# user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeigKey
	contactlist = models.ForeignKey(ContactList, on_delete=CASCADE)
	actiondetail = models.TextField()

	def __str__(self):
		return '{} ----- {}' .format(self.contactlist.title, self.actiondetail)

 