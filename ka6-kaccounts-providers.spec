#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kaccounts-providers
Summary:	KAccounts Providers
Name:		ka6-%{kaname}
Version:	24.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	dc1cc0a2855a3e482fa98aa59827f767
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	ka6-kaccounts-integration-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	libaccounts-glib-devel
BuildRequires:	libaccounts-qt6-devel
BuildRequires:	libsignon-qt6-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE Accounts Providers.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%dir %{_sysconfdir}/signon-ui
%dir %{_sysconfdir}/signon-ui/webkit-options.d
%{_sysconfdir}/signon-ui/webkit-options.d/accounts.google.com.conf
%{_sysconfdir}/signon-ui/webkit-options.d/api.twitter.com.conf
%{_sysconfdir}/signon-ui/webkit-options.d/identi.ca.conf
%{_sysconfdir}/signon-ui/webkit-options.d/www.facebook.com.conf
%dir %{_libdir}/qt6/plugins/kaccounts
%dir %{_libdir}/qt6/plugins/kaccounts/ui
%attr(755,root,root) %{_libdir}/qt6/plugins/kaccounts/ui/owncloud_plugin_kaccounts.so
%{_datadir}/accounts
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.owncloud
%{_iconsdir}/hicolor/256x256/apps/kaccounts-owncloud.png

%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/qt6/plugins/kaccounts/ui/nextcloud_plugin_kaccounts.so
%{_iconsdir}/hicolor/scalable/apps/kaccounts-nextcloud.svg
%dir %{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud
%dir %{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents
%dir %{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents/ui
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents/ui/Server.qml
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents/ui/Services.qml
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents/ui/WebLogin.qml
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/contents/ui/main.qml
%{_datadir}/kpackage/genericqml/org.kde.kaccounts.nextcloud/metadata.desktop
%endif
