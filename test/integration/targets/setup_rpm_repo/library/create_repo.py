#!/usr/bin/python

from __future__ import annotations

import tempfile

from collections import namedtuple

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.respawn import has_respawned, probe_interpreters_for_module, respawn_module

HAS_RPMFLUFF = True
can_use_rpm_weak_deps = None
try:
    from rpmfluff import SimpleRpmBuild, GeneratedSourceFile, make_gif, expectedArch
    from rpmfluff import YumRepoBuild
except ImportError:
    try:
        from rpmfluff.make import make_gif
        from rpmfluff.sourcefile import GeneratedSourceFile
        from rpmfluff.rpmbuild import SimpleRpmBuild
        from rpmfluff.utils import expectedArch
        from rpmfluff.yumrepobuild import YumRepoBuild
    except ImportError:
        expectedArch = None  # define here to avoid NameError as it is used on top level in SPECS
        HAS_RPMFLUFF = False

can_use_rpm_weak_deps = None
if HAS_RPMFLUFF:
    try:
        from rpmfluff import can_use_rpm_weak_deps
    except ImportError:
        try:
            from rpmfluff.utils import can_use_rpm_weak_deps
        except ImportError:
            pass


RPM = namedtuple('RPM', ['name', 'version', 'release', 'epoch', 'recommends', 'file', 'arch', 'binary'])

SPECS = [
    RPM('dinginessentail', '1.0', '1', None, None, None, None, None),
    RPM('dinginessentail', '1.0', '2', '1', None, None, None, None),
    RPM('dinginessentail', '1.1', '1', '1', None, None, None, None),
    RPM('dinginessentail-olive', '1.0', '1', None, None, None, None, None),
    RPM('dinginessentail-olive', '1.1', '1', None, None, None, None, None),
    RPM('landsidescalping', '1.0', '1', None, None, None, None, None),
    RPM('landsidescalping', '1.1', '1', None, None, None, None, None),
    RPM('dinginessentail-with-weak-dep', '1.0', '1', None, ['dinginessentail-weak-dep'], None, None, None),
    RPM('dinginessentail-weak-dep', '1.0', '1', None, None, None, None, None),
    RPM('noarchfake', '1.0', '1', None, None, None, 'noarch', None),
    RPM('provides_foo_a', '1.0', '1', None, None, 'foo.gif', 'noarch', None),
    RPM('provides_foo_b', '1.0', '1', None, None, 'foo.gif', 'noarch', None),
    RPM('number-11-name', '11.0', '1', None, None, None, None, None),
    RPM('number-11-name', '11.1', '1', None, None, None, None, None),
    RPM('epochone', '1.0', '1', '1', None, None, "noarch", None),
    RPM('epochone', '1.1', '1', '1', None, None, "noarch", None),
    RPM('provides-binary', '1.0', '1', '1', None, None, expectedArch, '/usr/sbin/package-name'),
    RPM('package-name', '1.0', '1', '1', None, None, "noarch", None),
]


def create_repo(arch='x86_64'):
    pkgs = []
    for spec in SPECS:
        pkg = SimpleRpmBuild(spec.name, spec.version, spec.release, [spec.arch or arch])
        pkg.epoch = spec.epoch

        if spec.recommends:
            # Skip packages that require weak deps but an older version of RPM is being used
            if not can_use_rpm_weak_deps or not can_use_rpm_weak_deps():
                continue

            for recommend in spec.recommends:
                pkg.add_recommends(recommend)

        if spec.file:
            pkg.add_installed_file(
                "/" + spec.file,
                GeneratedSourceFile(
                    spec.file, make_gif()
                )
            )

        if spec.binary:
            pkg.add_simple_compilation(installPath=spec.binary)

        pkgs.append(pkg)

    repo = YumRepoBuild(pkgs)
    repo.make(arch, 'noarch', expectedArch)

    for pkg in pkgs:
        pkg.clean()

    return repo.repoDir


def main():
    module = AnsibleModule(
        argument_spec={
            'arch': {'required': True},
            'tempdir': {'type': 'path'},
        }
    )

    if not HAS_RPMFLUFF:
        system_interpreters = ['/usr/libexec/platform-python', '/usr/bin/python3', '/usr/bin/python']

        interpreter = probe_interpreters_for_module(system_interpreters, 'rpmfluff')

        if not interpreter or has_respawned():
            module.fail_json('unable to find rpmfluff; tried {0}'.format(system_interpreters))

        respawn_module(interpreter)

    arch = module.params['arch']
    tempdir = module.params['tempdir']

    # Save current temp dir so we can set it back later
    original_tempdir = tempfile.tempdir
    tempfile.tempdir = tempdir

    try:
        repo_dir = create_repo(arch)
    finally:
        tempfile.tempdir = original_tempdir

    module.exit_json(repo_dir=repo_dir, tmpfile=tempfile.gettempdir())


if __name__ == "__main__":
    main()
