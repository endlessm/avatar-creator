project('avatar-creator', 'c',
  version: '0.0.1',
  meson_version: '>= 0.48.0'
)
i18n = import('i18n')
python = import('python3')
project_id = 'org.endlessos.avatarCreator'
contributors = '\n'.join([
  'Daniel García Moreno &lt;danigm@endlessos.org&gt;',
  'Joana Filizola &lt;joana@endlessos.org&gt;',
  'Simon Schampijer &lt;simon.schampijer@endlessos.org&gt;',
])

message('Looking for dependencies')
python_bin = python.find_python()
if not python_bin.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif
dependency('glib-2.0')
dependency('gobject-introspection-1.0', version: '>=1.35.9')
dependency('gtk4', version :'>=4.0.0')

env = environment()

python_dir = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))
LIBEXEC_DIR = join_paths(get_option('prefix'), get_option('libexecdir'))
DATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
bindir = join_paths(get_option('prefix'), get_option('bindir'))

# Profiles
if get_option('profile') == 'development'
    profile = 'Devel'
    name_suffix = ' (Development)'
else
    profile = ''
    name_suffix = ''
endif


conf = configuration_data()
conf.set('PACKAGE_URL', 'https://github.com/endlessm/avatar-creator/')
conf.set('DATA_DIR', DATA_DIR)
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
conf.set('PYTHON_DIR', python_dir)
conf.set('PYTHON_EXEC_DIR', join_paths(get_option('prefix'), python.sysconfig_path('stdlib')))
conf.set('PYTHON', python_bin.path())
conf.set('libexecdir', LIBEXEC_DIR)
if get_option('profile') == 'development'
    conf.set('VERSION', ''.join([run_command(['git', 'describe', '--long', '--tags']).stdout(), get_option('profile')]))
else
    conf.set('VERSION', meson.project_version())
endif
conf.set('CONTRIBUTORS', contributors)
conf.set_quoted('PROFILE', profile)

application_id = project_id
if get_option('profile') == 'development'
  application_id = project_id + 'Devel'
endif
conf.set('APPID', application_id)

subdir('data')
subdir('po')

install_subdir(
  'avatar_creator',
  install_dir: python_dir
)

configure_file(
  input: 'config.py.in',
  output: 'config.py',
  configuration: conf,
  install_dir: join_paths(python_dir, 'avatar_creator')
)

message('Preparing init file')
configure_file(
  input: 'avatar-creator.in',
  output: 'avatar-creator',
  configuration: conf,
  install_dir: bindir
)

meson.add_install_script('meson_post_install.py')
