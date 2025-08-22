project('elevate',
  version: '0.0.0', # Placeholder version, updated below
  meson_version: '>= 1.4.0',
  default_options: [ 'warning_level=2', 'werror=false' ],
)

# Extract version from pyproject.toml
python = import('python').find_installation('python3')
version_result = run_command(
  python, '-c',
  'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["tool"]["poetry"]["version"])',
  check: true
)
project_version = version_result.stdout().strip()

# Define metadata
conf = configuration_data()
conf.set('PYTHON', python.full_path())
conf.set('APP_NAME', 'Elevate')
conf.set('APP_ID', 'io.github.thecodenomad.elevate')
conf.set('APP_WEBSITE', 'https://github.com/thecodenomad/Elevate/')
conf.set('ISSUE_URL', 'https://github.com/thecodenomad/Elevate/issues')
conf.set('DEVELOPER_NAME', 'thecodenomad')
conf.set('VERSION', project_version)
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', get_option('prefix') / get_option('datadir') / meson.project_name())

i18n = import('i18n')
gnome = import('gnome')

subdir('data')
subdir('elevate')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
