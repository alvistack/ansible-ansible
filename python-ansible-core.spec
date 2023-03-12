# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: python-ansible-core
Epoch: 100
Version: 2.14.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Ansible IT Automation
License: GPL-3.0-only
URL: https://github.com/ansible/ansible/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: fdupes
BuildRequires: libyaml-devel
BuildRequires: python-rpm-macros
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed on
remote nodes. Extension modules can be written in any language and are
transferred to managed machines automatically.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%py3_build

%install
%py3_install
install -Dpm755 -d %{buildroot}%{_sysconfdir}/ansible
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/collections
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/action
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/become
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/cache
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/callback
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/cliconf
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/connection
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/doc_fragments
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/filter
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/httpapi
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/inventory
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/lookup
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/module_utils
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/modules
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/netconf
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/strategy
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/terminal
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/test
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/plugins/vars
install -Dpm755 -d %{buildroot}%{_datadir}/ansible/roles
find %{buildroot}%{python3_sitelib} -type d -name '.*' -prune -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '.*' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.orig' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.pem' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.pyc' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.rej' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.swp' -exec rm -rf {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.rst' -exec chmod a-x {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.py' -exec sed -i -e 's|^#!/usr/bin/env python|#!/usr/bin/python3|' {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.py' -exec sed -i -e 's|^#!/usr/bin/python.*|#!/usr/bin/python3|' {} \;
find %{buildroot}%{python3_sitelib} -type f -name '*.py' | xargs grep -E -l -e '^#!/usr/bin/python3' | xargs chmod a+x
rm -rf %{buildroot}%{python3_sitelib}/ansible_test/_data/requirements/sanity.ps1
rm -rf %{buildroot}%{python3_sitelib}/ansible_test/_data/sanity/pslint/pslint.ps1
rm -rf %{buildroot}%{python3_sitelib}/ansible_test/_data/sanity/validate-modules/validate_modules/ps_argspec.ps1
fdupes -qnrps %{buildroot}%{python3_sitelib}/ansible
fdupes -qnrps %{buildroot}%{python3_sitelib}/ansible_core*
fdupes -qnrps %{buildroot}%{python3_sitelib}/ansible_test*

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n ansible-core
Summary: Ansible IT Automation
Requires: libyaml-0-2
Requires: python3
Requires: python3-cryptography
Requires: python3-Jinja2
Requires: python3-jmespath
Requires: python3-netaddr
Requires: python3-packaging
Requires: python3-PyYAML >= 5.1
Requires: python3-resolvelib >= 0.5.3
Provides: python3-ansible-core = %{epoch}:%{version}-%{release}
Provides: python3dist(ansible-core) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-ansible-core = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(ansible-core) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-ansible-core = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(ansible-core) = %{epoch}:%{version}-%{release}

%description -n ansible-core
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed on
remote nodes. Extension modules can be written in any language and are
transferred to managed machines automatically.

%package -n ansible-test
Summary: Ansible IT Automation
Requires: ansible-core = %{epoch}:%{version}-%{release}
Provides: python3-ansible-test = %{epoch}:%{version}-%{release}
Provides: python3dist(ansible-test) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-ansible-test = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(ansible-test) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-ansible-test = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(ansible-test) = %{epoch}:%{version}-%{release}

%description -n ansible-test
This package installs the ansible-test command for testing modules and
plugins developed for ansible.

%files -n ansible-core
%license COPYING
%dir %{_sysconfdir}/ansible
%dir %{_datadir}/ansible
%{_bindir}/ansible
%{_bindir}/ansible-config
%{_bindir}/ansible-connection
%{_bindir}/ansible-console
%{_bindir}/ansible-doc
%{_bindir}/ansible-galaxy
%{_bindir}/ansible-inventory
%{_bindir}/ansible-playbook
%{_bindir}/ansible-pull
%{_bindir}/ansible-vault
%{python3_sitelib}/ansible
%{python3_sitelib}/ansible_core*

%files -n ansible-test
%license COPYING
%{_bindir}/ansible-test
%{python3_sitelib}/ansible_test*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n ansible-core
Summary: Ansible IT Automation
Requires: libyaml
Requires: python3
Requires: python3-cryptography
Requires: python3-jinja2
Requires: python3-jmespath
Requires: python3-netaddr
Requires: python3-packaging
Requires: python3-pyyaml >= 5.1
Requires: python3-resolvelib >= 0.5.3
Provides: python3-ansible-core = %{epoch}:%{version}-%{release}
Provides: python3dist(ansible-core) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-ansible-core = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(ansible-core) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-ansible-core = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(ansible-core) = %{epoch}:%{version}-%{release}

%description -n ansible-core
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed on
remote nodes. Extension modules can be written in any language and are
transferred to managed machines automatically.

%package -n ansible-test
Summary: Ansible IT Automation
Requires: ansible-core = %{epoch}:%{version}-%{release}
Provides: python3-ansible-test = %{epoch}:%{version}-%{release}
Provides: python3dist(ansible-test) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}-ansible-test = %{epoch}:%{version}-%{release}
Provides: python%{python3_version}dist(ansible-test) = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}-ansible-test = %{epoch}:%{version}-%{release}
Provides: python%{python3_version_nodots}dist(ansible-test) = %{epoch}:%{version}-%{release}

%description -n ansible-test
This package installs the ansible-test command for testing modules and
plugins developed for ansible.

%files -n ansible-core
%license COPYING
%dir %{_sysconfdir}/ansible
%dir %{_datadir}/ansible
%{_bindir}/ansible
%{_bindir}/ansible-config
%{_bindir}/ansible-connection
%{_bindir}/ansible-console
%{_bindir}/ansible-doc
%{_bindir}/ansible-galaxy
%{_bindir}/ansible-inventory
%{_bindir}/ansible-playbook
%{_bindir}/ansible-pull
%{_bindir}/ansible-vault
%{python3_sitelib}/ansible
%{python3_sitelib}/ansible_core*

%files -n ansible-test
%license COPYING
%{_bindir}/ansible-test
%{python3_sitelib}/ansible_test*
%endif

%changelog
