from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction

from logicbook.forms import RegistrationForm
from logicbook.models import User, UserProfile, ModuleDefinition, ModuleInstance, Port

@login_required
def home(request):
    """
    The home view includes the workspace where designs can be created and edited.
    """
    return render(request,'logicbook/home.html')

@login_required
def browse(request):
    """
    The Browse view allows users to view existing designs, users, and groups.
    """

@login_required
def user(request):
    """
    The User view shows a summary of a user's profile, designs, and groups.
    """

@login_required
def new_definition(request):
    """
    Asynchronous view. Request to allocate a new ModuleDefinition.
    If successful, return:
    {
     success: true,
     definition: {
       id, name, nodeCount, svgPath, ports
     }
    }
    Else return:
    {
     success: false,
     errorMessage
    }
    """
    new_definition = ModuleDefinition(creator=request.user, 
        node_count=3,
        svg_path="/static/images/box.svg"
        )
    new_definition.save()
    default_ports = [
      Port(name="in0", width=1, parent=new_definition, direction=PortDirection.input, 
        node=0, posX=0.0, posY=0.3),
      Port(name="in1", width=1, parent=new_definition, direction=PortDirection.input, 
        node=1, posX=0.0, posY=0.7),
      Port(name="out", width=1, parent=new_definition, direction=PortDirection.output, 
        node=2, posX=1.0, posY=0.5)
    ]
    for port in default_ports:
        port.save()
    response_json = {
        "success": True,
        "definition": new_definition.dict()
    }
    return HttpResponse(response_json, content_type='application/json')



# Until we are hosted in an environment where one of us can attach our password
# securely, we won't confirm email addresses when creating accounts.
CONFIRM_EMAIL_ADDRESS = False

EMAIL_BODY_TEMPLATE = """
Welcome to Logicbook!  Please click the link below to
verify your email address and complete the registration of your account:
  http://%s%s
""" 

@transaction.atomic
def register(request):
    """ Either get the register page or handle a RegistrationForm POST request. """
    context = {}

    if request.method == 'GET':
        # Get the register page
        context['registration_form'] = RegistrationForm()
        return render(request, 'logicbook/register.html', context)

    form = RegistrationForm(request.POST)
    context['registration_form'] = form

    if not form.is_valid():
        return render(request, 'logicbook/register.html', context)

    # The form is valid; create a new user
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'],
                                        email=request.POST['email'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'])

    if CONFIRM_EMAIL_ADDRESS:
        new_user.is_active = False

    new_user.save()
    # Create a new blogger and link to the user
    new_user_profile = UserProfile(user=new_user)
    new_user_profile.save()

    if CONFIRM_EMAIL_ADDRESS:
        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(new_user)
        email_body = EMAIL_BODY_TEMPLATE % (request.get_host(), 
            reverse('confirm', args=(new_user.username, token)))
        send_mail(subject="Verify your email address",
            message= email_body,
            from_email="cmbarker@andrew.cmu.edu",
            recipient_list=[new_user.email],
            fail_silently=False)
        context['email'] = form.cleaned_data['email']
        return render(request, 'logicbook/needs-confirmation.html', context)
    else:
        new_user = authenticate(username=request.POST['username'],
            password=request.POST['password1'])
        login(request, new_user)
        return redirect(reverse('home'))

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'logicbook/confirmed.html', {})