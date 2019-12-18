import yaml
import sys
import os.path
from os import path
from jinja2 import Template


##################
# Read YAML Data #
##################

app_template = 'demo_template.yaml'
data_dict = yaml.load(open(app_template))


######################
# Set-up Directories #
######################

cwd_path = os.getcwd()
project_name = data_dict['project_name']

# Set-up project directory
path = "%s/%s/" % (cwd_path, project_name)
if not os.path.exists(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

# Save this path for clean-up later
clean_path = path

# Set-up utils folder
utils_path = "%s/%s/%s/" % (cwd_path, project_name, 'utils')
if not os.path.exists(utils_path):
    try:
        os.mkdir(utils_path)
    except OSError:
        print ("Creation of the directory %s failed" % utils_path)
    else:
        print ("Successfully created the directory %s " % utils_path)


##############
# Run Jinja2 #
##############

# Build application
path = 'jinja_templates/application.txt'
with open(path, 'r') as f:
    text = f.read()
template = Template(text)
output = template.render(data = data_dict)
with open('%s/application.py' % project_name, 'w') as f:
    f.write(output)

# Build resources
path = 'jinja_templates/resources.txt'
with open(path, 'r') as f:
    text = f.read()    
template = Template(text)
output = template.render(data = data_dict)
with open('%s/resources.py' % project_name, 'w') as f:
    f.write(output)

# Build models
path = 'jinja_templates/models.txt'
with open(path, 'r') as f:
    text = f.read()    
template = Template(text)
output = template.render(data = data_dict)
with open('%s/models.py' % project_name, 'w') as f:
    f.write(output)

# Build exceptions
path = 'jinja_templates/exceptions.txt'
with open(path, 'r') as f:
    text = f.read()    
template = Template(text)
output = template.render(data = data_dict)
with open('%s/utils/exceptions.py' % project_name, 'w') as f:
    f.write(output)

# Build manager
path = 'jinja_templates/manager.txt'
with open(path, 'r') as f:
    text = f.read()    
template = Template(text)
output = template.render(data = data_dict)
with open('%s/utils/manager.py' % project_name, 'w') as f:
    f.write(output)

##################
# Clean-up Files #
##################
# print(clean_path)
# cmd = 'for file in %s*; do autopep8 "$file"; done' % (clean_path)
# os.system(cmd)