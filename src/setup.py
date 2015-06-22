import sys
import os
import pip

from cx_Freeze import setup, Executable
from importlib import import_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
import django
django.setup()
from django.conf import settings
from django.core import management


def query_yes_no(question, default='yes'):
    valid = {'yes': True, 'y': True, "no": False, 'n': False}

    if default is None:
        prompt = " [y/n] "
    elif default in ['yes', 'y']:
        prompt = " [Y/n] "
    elif default in ['no', 'n']:
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer!")

    while True:
        sys.stdout.write('\n' + question + prompt)

        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'.\n")


def get_packages_in_path(path):
    packages = []
    for folder in os.listdir(path):
        if os.path.exists(os.path.join(path, folder, '__init__.py')):
            packages.extend([folder, ])
        elif folder.endswith('.egg') and not os.path.isfile(os.path.join(path, folder)):
            for subfolder in os.listdir(os.path.join(path, folder)):
                if os.path.exists(os.path.join(path, folder, subfolder, '__init__.py')):
                    packages.extend([subfolder, ])
    return packages


def get_installed_packages():
    site_packages = pip.util.site_packages

    return get_packages_in_path(site_packages)


def get_local_packages():
    return get_packages_in_path(settings.BASE_DIR)


print("You should only run this build script if you are a CLEAN VirtualEnv!\n"
      "The VirtualEnv will be deployed with the project, so make sure it ONLY has the REQUIRED dependencies installed!")
if not query_yes_no("Are you in a CLEAN Python Environment?", default='no'):
    sys.exit()

# if not os.path.exists(os.path.join(settings.BASE_DIR, 'static')):
#     os.makedirs(os.path.join(settings.BASE_DIR, 'static'))
# management.call_command('collectstatic', interactive=False, clear=True)

build_exe_options = {
    'optimize': 2,
    'excludes': [
        'development_scripts',
    ],
    'includes': [

    ],
    'packages': [
        # Known missing Python imports.
        # This may need to be updated from time to time as new projects uncover more missing packages.
        'html',
        'shutil',
    ],
    'replace_paths': [('*', '')],
    'compressed': False,
    'include_files': [
        ('Sample Scenarios', 'Sample Scenarios'),
        ('static', 'static'),
    ],
    'include_msvcr': True
}

# Grab all the packages that we should include (local and those installed in the virtualenv)
build_exe_options['packages'].extend(get_installed_packages())
build_exe_options['packages'].extend(get_local_packages())
# Cleanup packages to account for any excludes
build_exe_options['packages'] = [package for package in build_exe_options['packages'] if package not in build_exe_options['excludes']]

# Grab any templates or translation files for installed apps and copy those
for app_name in settings.INSTALLED_APPS:
    app = import_module(app_name)
    if os.path.exists(os.path.join(app.__path__[0], 'templates')):
        build_exe_options['include_files'].extend([(os.path.join(app.__path__[0], 'templates'), os.path.join('templates', app.__name__)), ])
    # TODO: Do we need to grab translation files for apps not listed in settings.py?
    # TODO: Django still doesn't properly find translation for domain 'django' after collecting everything
    # if os.path.exists(os.path.join(app.__path__[0], 'locale')):
    #     build_exe_options['include_files'].extend([(os.path.join(app.__path__[0], 'locale'), os.path.join('locale', app.__name__)), ])

# Check all installed packages and see if they list any dependencies they need copied when frozen
for package in build_exe_options['packages']:
    try:
        package = import_module(package)
        if getattr(package, '__include_files__', False):
            build_exe_options['include_files'].extend(package.__include_files__)
    except Exception as e:
        print("Error bringing in dependent files!", str(e))
        continue

base = None
if sys.platform == 'win32':
    base = 'Console'  # TODO: Change to Win32GUI and so on for each OS

setup(name='ADSM',
      version='3.3.33',
      description='Test ADSM Application',
      options={'build_exe': build_exe_options},
      executables=[Executable('ADSM.py', base=base), ]
      )
