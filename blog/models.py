from django.db import models
from django.db	import	models
from django.utils import timezone
from django.contrib.auth.models	import User
from django.urls import reverse

# Create your models here.


class PublishedManager(models.Manager):
	def	get_queryset(self):
		return super(PublishedManager, self).get_queryset()\
		.filter(status='published')

class Post(models.Model):
				STATUS_CHOICES	=(
								('draft',	'Draft'),
								('published',	'Published'),
				                    )

				title =	models.CharField(max_length=250)
				slug = models.SlugField(max_length=250,unique_for_date='publish')
				author = models.ForeignKey(User, on_delete=models.CASCADE)
				body = models.TextField()
				publish	= models.DateTimeField(default=timezone.now)
				created	= models.DateTimeField(auto_now_add=True)
				updated	= models.DateTimeField(auto_now=True)
				status	= models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
				objects	= models.Manager()	#	The	default	manager.
				published =	PublishedManager()	#	Our	custom	manager.
				class Meta:
					ordering	=	('-publish',)

				def	__str__(self):
					return	self.title
				def	get_absolute_url(self): 
					return	reverse('blog:post_detail',
						args=[self.publish.year,
						self.publish.month,
						self.publish.day,
						self.slug])


class Comment(models.Model):	
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name =	models.CharField(max_length=80)	
	email =	models.EmailField()	
	body =	models.TextField()	
	created	= models.DateTimeField(auto_now_add=True)	
	updated	= models.DateTimeField(auto_now=True)	
	active = models.BooleanField(default=True)

	class Meta:	
		ordering = ('created',)	
	
	def	__str__(self):	
		return	'Comment by	{} on {}'.format(self.name,	self.post)	

	

	# def	post_detail(request, year, month, day, post):
	# post = get_object_or_404(Post,	slug=post,
	# 										status='published',  
	# 										publish__year=year,
	# 										publish__month=month,
	# 										publish__day=day)
	# return	render(request, 'blog/post/detail.html',{'post': post})


	
# {% for comment in comments %}
# 		<div class="comment">
# 				<p class="info">
# 					Comment	{{ forloop.counter }} by {{	comment.name }}
# 						{{ comment.created }}
# 				</p>
# 				{{ comment.body|linebreaks }}
# 		</div>
# {% empty %}
# 	<p>There are no	comments yet.</p>
# {% endfor %}



# {% if new_comment %}
# 		<h2>Your comment has been added.</h2>
# {% else %}
# 	<h2>Add	a new comment</h2>
# 	<form action="." method="post">
# 				{{	comment_form.as_p	}}
# 				{%	csrf_token	%}
# 				<p><input	type="submit"	value="Add	comment"></p>
# 		</form>
# {% endif %
