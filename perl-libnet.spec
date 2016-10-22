%{?scl:%scl_package perl-libnet}

Name:           %{?scl_prefix}perl-libnet
Version:        3.09
Release:        3%{?dist}
Summary:        Perl clients for various network protocols
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/libnet/
Source0:        http://www.cpan.org/authors/id/S/SH/SHAY/libnet-%{version}.tar.gz
# Convert Changes to UTF-8
Patch0:         libnet-3.09-Normalize-Changes-encoding.patch
# Do not create Net/libnet.cfg, bug #1238689
Patch1:         libnet-3.08-Do-not-create-Net-libnet.cfg.patch
# Fix blocking in Net::FTP and other subclasses, bug #1360610, CPAN RT#116345
Patch2:         libnet-3.09-Override-timeout-method-in-Net-FTP-and-other-subclas.patch
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.64
# Getopt::Std not used because of Do-not-create-Net-libnet.cfg.patch
# IO::File not used because of Do-not-create-Net-libnet.cfg.patch
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Run-time:
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
# Convert::EBCDIC not used
BuildRequires:  %{?scl_prefix}perl(Errno)
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(Fcntl)
# File::Basename not used at tests
BuildRequires:  %{?scl_prefix}perl(FileHandle)
BuildRequires:  %{?scl_prefix}perl(IO::Select)
BuildRequires:  %{?scl_prefix}perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
# IO::Socket::INET6 not used
BuildRequires:  %{?scl_prefix}perl(IO::Socket::IP) >= 0.25
BuildRequires:  %{?scl_prefix}perl(POSIX)
BuildRequires:  %{?scl_prefix}perl(Socket) >= 2.016
BuildRequires:  %{?scl_prefix}perl(Symbol)
BuildRequires:  %{?scl_prefix}perl(Time::Local)
# Optional run-time:
# Authen::SASL not used at tests
# Digest::MD5 not used at tests
%if !%{defined perl_bootstrap} && !%{defined perl_small}
# Core modules must be built without non-core dependencies
BuildRequires:  %{?scl_prefix}perl(IO::Socket::SSL) >= 2.007
%endif
# MD5 not used because we prefer Digest::MD5
# MIME::Base64 not used at tests
# Tests:
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(Cwd)
BuildRequires:  %{?scl_prefix}perl(File::Temp)
BuildRequires:  %{?scl_prefix}perl(IO::File)
BuildRequires:  %{?scl_prefix}perl(Test::More)
# Optional tests:
%if !%{defined perl_bootstrap} && !%{defined perl_small}
# Core modules must be built without non-core dependencies
BuildRequires:  %{?scl_prefix}perl(IO::Socket::SSL::Utils)
%endif
# Test::CPAN::Changes not used
# Test::Perl::Critic not used
# Test::Pod 1.00 not used
# Test::Pod::Coverage 0.08 not used
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(File::Basename)
Requires:       %{?scl_prefix}perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
Requires:       %{?scl_prefix}perl(IO::Socket::IP) >= 0.25
Requires:       %{?scl_prefix}perl(POSIX)
Requires:       %{?scl_prefix}perl(Socket) >= 2.016
Conflicts:      %{?scl_prefix}perl < 4:5.22.0-347

# Filter under-specified dependencies
%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /^%{?scl_prefix}perl(IO::Socket)/d
%filter_from_requires /^%{?scl_prefix}perl(Socket)/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^%{?scl_prefix}perl\\((IO::Socket|Socket)\\)$
%endif

%description
This is a collection of Perl modules which provides a simple and
consistent programming interface (API) to the client side of various
protocols used in the internet community.

%prep
%setup -q -n libnet-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor </dev/null && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=$RPM_BUILD_ROOT%{?scl:'}
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Artistic Copying LICENCE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jul 27 2016 Petr Pisar <ppisar@redhat.com> - 3.09-3
- Fix blocking in Net::FTP and other subclasses (bug #1360610)

* Wed Jul 20 2016 Petr Pisar <ppisar@redhat.com> - 3.09-2
- SCL

* Wed Jul 20 2016 Petr Pisar <ppisar@redhat.com> - 3.09-1
- 3.09 bump

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.08-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.08-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Petr Pisar <ppisar@redhat.com> - 3.08-1
- 8.08 bump

* Mon Jul 20 2015 Petr Pisar <ppisar@redhat.com> - 3.07-1
- 3.07 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> 3.06-1
- Specfile autogenerated by cpanspec 1.78.
- Do not create Net/libnet.cfg (bug #1238689)
