gnome = import('gnome')

message('Compiling resources')

gnome.compile_resources(
  meson.project_name(),
  meson.project_name() + '.gresources.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: DATA_DIR,
  install: true,
  dependencies: configure_file (
    input: 'about_dialog.ui.in',
    output: 'about_dialog.ui',
    configuration: conf
  )
)

desktop_conf = configuration_data()
desktop_conf.set('ICON', application_id)
desktop = i18n.merge_file(
  'desktop',
  input: configure_file(
    input: files(project_id + '.desktop.in.in'),
    output: project_id + '.desktop.in',
    configuration: desktop_conf
  ),
  output: '@0@.desktop'.format(application_id),
  po_dir: join_paths(meson.source_root(), 'po'),
  type: 'desktop',
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'applications')
)

# Validating the desktop file
desktop_file_validate = find_program('desktop-file-validate', required:false)
if desktop_file_validate.found()
  test (
    'Validate desktop file',
    desktop_file_validate,
    args: join_paths(meson.current_build_dir (), application_id + '.desktop')
  )
endif

appdata_conf = configuration_data()
appdata_conf.set('APPID', application_id)
appdata = i18n.merge_file(
  'appdata',
  input: configure_file(
    input: files(project_id + '.appdata.xml.in.in'),
    output: project_id + '.appdata.xml.in',
    configuration: appdata_conf
  ),
  output: application_id + '.appdata.xml',
  install: true,
  install_dir: join_paths(join_paths('share'), 'metainfo'),
  po_dir: join_paths(meson.source_root(), 'po')
)


# Validating the appdata file
appstreamcli = find_program('appstream-util', required: false)
if appstreamcli.found()
  test (
    'Validate appdata file',
    appstreamcli,
    args: ['validate-relax', join_paths(meson.current_build_dir (), application_id + '.appdata.xml')]
  )
endif

subdir('icons')

install_subdir('assets', install_dir: DATA_DIR)
