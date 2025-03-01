from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUserType
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import uuid

CustomUser = get_user_model()


# Create your views here.
def home(request):
    user_types = CustomUserType.objects.all()
    context = {
        'user_types': user_types,
    }

    return render(request, 'home.html', context)

def register_user(request):
    """
    Handle registration form submission
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')
        user_type_id = request.POST.get('user_type')
        consent = request.POST.get('saglasnost') == 'on'

        if password != confirm_password:
            messages.error(request, "Lozinke se ne poklapaju!")
            return redirect('home')

        try:
            # Create the user
            user = CustomUser.objects.create(
                username=email,  # Use email as the username
                email=email,
                first_name=full_name.split(' ')[0],  # Split first name if provided as full name
                last_name=' '.join(full_name.split(' ')[1:]),  # Remaining as last name
                user_type_id =user_type_id,
                phone_number=phone_number,
                consent=consent
            )

            # Set and hash the password
            user.set_password(password)
            user.save()

            messages.success(request, "Uspešno ste se registrovali!")
            return redirect('home')
        except Group.DoesNotExist:
            messages.error(request, "Greška: odabrana korisnička grupa ne postoji!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Greška tokom registracije: {e}")
            return redirect('home')

    # If GET, redirect to the home page
    return redirect('home')


def login_user(request):
    """
    Handle login form submission
    """
    if request.method == 'POST':
        email = request.POST.get('email')  # Email is used as the username
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                # User is active => log them in
                login(request, user)
                messages.success(request, "Uspešno ste se prijavili!")
                return redirect('home')  # or your desired view
            else:
                # User exists but is inactive
                messages.error(request, "Vaš nalog je obrisan. Za reaktivaciju kliknite na ovaj <a href='http://192.168.1.8:8000/zaboravljena-lozinka'>link</a>.")
                return redirect('home')
        else:
            # Handle invalid credentials
            messages.error(request, "Neispravni kredencijali. Pokušajte ponovo.")
            return redirect('home')  # Redirect back to the login page (home)

    # If GET request, redirect to home
    return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, "Uspešno ste se odjavili.")
    return redirect('home')

def zaboravljena_lozinka(request):
    return render(request, 'zaboravljena-lozinka.html')

"""================================================================"""


def prodaja_stanova(request):
    return render(request, 'prodaja/prodaja-stanova.html')

def agencije(request):
    return render(request, 'agencije/agencije.html')

def investitor(request):
    return render(request, 'investitor/investitor.html')


"""================================================================"""

@login_required
def postavi_oglas(request):
    return render(request, 'korisnik/postavi-oglas.html')

@login_required
def moji_oglasi(request):
    return render(request, 'korisnik/moji-oglasi.html')

def compress_image(uploaded_file, quality=70):
    """
    Takes an uploaded image (from request.FILES) and compresses it 
    (reduces quality) using Pillow, returning an in-memory file suitable 
    for saving with Django’s FileSystemStorage or an ImageField.
    """
    # 1) Open the uploaded image using Pillow
    img = Image.open(uploaded_file)
    
    # 2) Convert to RGB if needed (to avoid issues if it's RGBA or grayscale)
    img = img.convert('RGB')
    
    # 3) Use an in-memory buffer to store the compressed image
    image_io = BytesIO()
    
    # 4) Save as JPEG with a lower quality; you can adjust 'quality=70'
    img.save(image_io, format='JPEG', quality=quality)
    
    # 5) Create a ContentFile, which Django can handle as a normal uploaded file
    compressed_image = ContentFile(image_io.getvalue(), name='compressed.jpg')
    return compressed_image

@login_required
def podesavanja(request):
    user = request.user  # The logged-in user
    uploaded_file_url = None

    if request.method == 'POST':
        # Check if the form was submitted for updating user details
        if 'full_name' in request.POST:
            # Extract data from the form
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            user_type_id = request.POST.get('user_type')
            profile_image = request.FILES.get('profile_image')  # File input for the profile image

            # Split full name into first and last name
            first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

            try:
                # Update user fields
                user.first_name = first_name
                user.last_name = last_name
                user.username = email
                user.email = email
                user.phone_number = phone_number
                if user_type_id:
                    user.user_type_id = user_type_id  # Assign the foreign key
                if profile_image:
                    # --- COMPRESS THE IMAGE BEFORE STORING ---
                    compressed_image = compress_image(profile_image, quality=70)

                     # 1) Location (folder) and base URL.
                    fs = FileSystemStorage(
                        location='media/profile_images',    # Folder in your project where images go
                        base_url='/media/profile_images'     # URL path to access those images
                    )

                    # 2) Generate a unique filename using uuid, preserving extension.
                    extension = profile_image.name.split('.')[-1]  # e.g. 'jpg'
                    unique_filename = f"{uuid.uuid4()}.{extension}"

                    # 3) Actually save the file.
                    filename = fs.save(unique_filename, compressed_image)

                    # 4) Build the URL to serve in templates.
                    uploaded_file_url = fs.url(filename)

                    # 5) Save the path/filename on the user (if you want to store it)
                    user.image_url = filename  # or user.image_url = uploaded_file_url

                # Save the updated user
                user.save()
                messages.success(request, "Vaši podaci su uspešno ažurirani.")

            except Exception as e:
                messages.error(request, f"Došlo je do greške pri ažuriranju: {e}")
            return redirect('podesavanja')

        # Handle other buttons (e.g., delete account)
        elif 'obrisi-nalog' in request.POST:
            user.is_active = False
            user.save()
            logout(request)
            messages.success(request, 'Vaš nalog je uspešno obrisan.')
            return redirect('home')

        elif 'verifikuj-nalog' in request.POST:
            messages.info(request, 'Verifikacija naloga je u toku.')
            return redirect('podesavanja')

    # For GET requests, render the settings page
    user_types = CustomUserType.objects.all()
    context = {
        'user_types': user_types,
        'user': user,  # Pass the user object to pre-fill the form fields
        'uploaded_file_url': uploaded_file_url,
    }
    return render(request, 'korisnik/podesavanja.html', context)

@login_required
def sacuvane_pretrage(request):
    return render(request, 'korisnik/sacuvane-pretrage.html')

@login_required
def sacuvani_oglasi(request):
    return render(request, 'korisnik/sacuvani-oglasi.html')

