datadir = join_paths('share', 'icons')
icondir = join_paths('hicolor', 'scalable', 'apps')
install_data (
    join_paths(icondir, project_id + '.svg'),
    install_dir: join_paths(datadir, icondir),
    rename: application_id + '.svg'
)

icondir = join_paths('hicolor', 'symbolic', 'apps')
install_data (
    join_paths(icondir, project_id + '-symbolic.svg'),
    install_dir: join_paths(datadir, icondir),
    rename: application_id + '-symbolic.svg'
)
