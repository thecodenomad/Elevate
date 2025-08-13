pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'elevate'
gnome = import('gnome')

# Add a reference to the compiler to use
blueprint_compiler = find_program('blueprint-compiler')

# Dynamically collect all .blp files in the blueprints/ directory
blueprint_files = run_command(
  'find',
  meson.current_source_dir() / 'blueprints',
  '-type', 'f',
  '-name', '*.blp',
  check: true,
).stdout().strip().split('\n')

# Filter out empty strings in case no files are found
blueprint_files = blueprint_files.length() > 0 and blueprint_files[0] != '' ? blueprint_files : []

# Convert blueprint files to ui files
ui_files = []

foreach blueprint_file : blueprint_files
  # Ensure the file is treated as a Meson file object
  blueprint_file = files(blueprint_file)[0]
  path_as_string = '@0@'.format(blueprint_file.full_path())
  filename = path_as_string.split('/')[-1]

  ui_file = custom_target(
    path_as_string.underscorify(),
    input: blueprint_file,
    output: filename.replace('.blp', '.ui'),
    command: [blueprint_compiler, 'compile', '--output', '@OUTPUT@', '@INPUT@'],
  )
  ui_files += ui_file
endforeach

# Generate warchest.gresource.xml dynamically
ui_file_entries = []
foreach ui_file : ui_files
  filename = ui_file.full_path().split('/')[-1]
  # Skip window.ui as it's handled separately
  if filename != 'window.ui'
    ui_file_entries += '    <file preprocess="xml-stripblanks">' + filename + '</file>'
  endif
endforeach

# Generate elevate.gresource.xml
gresource_xml = configure_file(
  output: 'elevate.gresource.xml',
  input: 'elevate.gresource.xml.in',
  configuration: configuration_data({'UI_FILES': '\n'.join(ui_file_entries)}),
)

# Compile resources with dependencies on the generated UI files
gnome.compile_resources('elevate',
  gresource_xml,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: ui_files,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'elevate.in',
  output: 'elevate',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

# Dynamically collect Python source files in src/, excluding blueprints/ and __pycache__/
python_sources = run_command(
  'find',
  meson.current_source_dir(),
  '-type', 'f',
  '-name', '*.py',
  '-not', '-path', meson.current_source_dir() / 'blueprints/*',
  '-not', '-path', meson.current_source_dir() / '__pycache__/*',
  '-not', '-name', 'main.py.in',
  check: true,
).stdout().strip().split('\n')

# Filter out empty strings and convert to file objects with correct install paths
elevate_sources = []
foreach src : python_sources
  if src != ''
    # Convert absolute path to relative path from src/
    rel_path = src.replace(meson.current_source_dir() + '/', '')
    elevate_sources += files(rel_path)
  endif
endforeach

# Install Python files, preserving directory structure
install_data(
  elevate_sources,
  install_dir: moduledir,
  install_tag: 'runtime',
  preserve_path: true
)

install_data(
  install_dir: moduledir,
  install_tag: 'runtime',
  preserve_path: true
)

# Install the generated elevate.gresource.xml
install_data(
  gresource_xml,
  install_dir: moduledir,
  install_tag: 'runtime'
)
