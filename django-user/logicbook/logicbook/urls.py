from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','logicbook.views.home', name='home'),
	url(r'^browse$', 'logicbook.views.browse', name="browse"),
	url(r'^user/(?P<username>.*)$', 'logicbook.views.user', name="user"),

	# Async database updates
	url(r'^new_definition$', 'logicbook.views.new_definition', name="new_definition"),

	# Account management
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'logicbook/login.html'}, name="login"),
	url(r'^register$', 'logicbook.views.register', name="register"),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name="logout"),
	)
