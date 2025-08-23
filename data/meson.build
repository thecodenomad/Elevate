# Ensure i18n module is imported
i18n = import('i18n')

# Desktop file with variable substitution and translation
desktop_file_in = configure_file(
  input: 'io.github.thecodenomad.elevate.desktop.in',
  output: 'io.github.thecodenomad.elevate.desktop.in.tmp',
  configuration: conf
)

desktop_file = i18n.merge_file(
  input: desktop_file_in,
  output: 'io.github.thecodenomad.elevate.desktop',
  type: 'desktop',
  po_dir: meson.project_source_root() / 'po',
  install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

# AppStream file with variable substitution
appstream_file = configure_file(
  input: 'io.github.thecodenomad.elevate.metainfo.xml.in',
  output: 'io.github.thecodenomad.elevate.metainfo.xml',
  configuration: conf,
  install: true,
  install_dir: get_option('datadir') / 'metainfo'
)



# Schema file
install_data('io.github.thecodenomad.elevate.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

# DBus service file with variable substitution
service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
configure_file(
  input: 'io.github.thecodenomad.elevate.service.in',
  output: 'io.github.thecodenomad.elevate.service',
  configuration: service_conf,
  install: true,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

subdir('icons')
