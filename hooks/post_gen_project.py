import os
import shutil

print('Project created successfully!')
print('Next steps:')
print('1. cd {{cookiecutter.project_slug}}')
print('2. git init')
print('3. git add .')
print('4. git commit -m "Initial commit"')
print('5. git branch -M main')
print('6. git remote add origin {Your repo}')
print('7. git push -u origin main')
print('8. git switch -c develop')

# Удаление ненужного пользователю
if '{{ cookiecutter.use_docker }}' != 'y':
    shutil.rmtree('docker')
if '{{ cookiecutter.use_k8s }}' != 'y' or '{{ cookiecutter.use_docker }}' != 'y':
    shutil.rmtree('k8s')
if '{{ cookiecutter.use_gitlab }}' != 'y':
    shutil.rmtree('.gitlab')
    os.remove('.gitlab-ci.yml')
if '{{ cookiecutter.use_todo_md }}' != 'y':
    os.remove('TODO.md')

# Лицензия
license_ = "{{ cookiecutter.license }}"
if license_ in {"MIT", "BSD", "Apache", "GPL"}:
    shutil.move('template_data/licenses/{{ cookiecutter.license }}', 'LICENSE')

# Удаление лишнего
shutil.rmtree('template_data')