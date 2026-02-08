%global __scm git

%define major 2
%define libname %mklibname cupsfilters
%define devname %mklibname cupsfilters -d

Name: libcupsfilters
Version: 2.1.1
Release: 2
Source0: https://github.com/OpenPrinting/libcupsfilters/archive/%{version}/%{name}-%{version}.tar.gz
Summary: Library containing functions useful for developing printer drivers
URL: https://github.com/OpenPrinting/libcupsfilters
License: GPL
Group: System/Libraries
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(cups)
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(pdfio)
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: slibtool
BuildRequires: make
BuildRequires: gettext-devel
BuildRequires: mupdf
BuildRequires: (ghostscript or ghostpdl)
Requires: (ghostscript or ghostpdl)
Requires: mupdf

%patchlist
0001-cfFilterTextToPDF-Let-all-Arabic-characters-be-rende.patch
0002-Fixed-Deadlock-in-Filter-Chain-When-One-Filter-Fails.patch
0003-Allow-building-without-fontconfig-83.patch
0004-cfFilterChain-Initialize-return-value-to-0.patch
0005-imagetopdf-convert-custom-media-size-min_width-and-m.patch
0006-Poppler-imagetoraster-fix-mono-dithering-of-100-blac.patch
0007-Poppler-pdftoraster-disable-font-anti-aliasing-for-1.patch
0008-Poppler-pdftoraster-enable-font-hinting-for-better-f.patch
0009-pdftoraster-ghostscript-mupdftopwg-Check-strchr-resu.patch
0010-PDFTOPDFCollate-comment-parsing-Increment-p-where-ne.patch
0011-pdftoraster-Check-result-of-render_page-95.patch
0012-image-zoom.c-add-the-xsize-and-ysize-check-for-zero-.patch
0013-Add-JPEG-XL-Support-to-libcupsfilters-82.patch
0014-configure.ac-Make-CJK-fonts-name-configurable.patch
0015-cfFilterGhostscript-Introduce-cupsHalftoneType-dithe.patch
0016-Replace-QPDF-by-PDFio-as-PDF-manipulation-library-in.patch
0017-image-jpeg-xl.c-Silenced-warnings-about-unused-varia.patch
0018-Use-bin-sh-for-testfilters.sh-to-avoid-dependency-on.patch
0019-Update-build-system-and-documentation-to-require-PDF.patch
0020-cfFilterImageToPDF-Added-extra-debug-log-messages-co.patch
0021-Fix-for-security-vulnerablity-due-to-use-of-system-f.patch
0022-Fix-PCLm-strip-overflow-and-add-regression-test-105.patch
0023-Merge-commit-from-fork.patch
0024-Fix-out-of-bounds-write-in-cfFilterPDFToRaster.patch
0025-image-tiff.c-Unify-return-values.patch
0026-Potential-heap-buffer-overflow-fix-108.patch
0027-Fix-cache-thrashing-for-large-images-106.patch
0028-add-documentation-comments.patch
0029-Fix-error-in-PDFtoRaster-due-to-execv.patch
0030-fix-padding-issue-when-input-image-is-smaller-than-o.patch
0031-change-the-log-line-to-show-x1-y1-x2-y2-from-x1-x2-y.patch
0032-texttopdf-default-to-UTF-8-when-charset-metadata-is-.patch
0033-Added-a-deterministic-build-time-multipage-UTF-8-lor.patch

%description
CUPS is a standards-based, open-source printing system.
CUPS uses the Internet Printing Protocol ("IPP") and provides System V and
Berkeley command-line interfaces, a web interface, and a C API to manage
printers and print jobs.

CUPS 1.0 was released in early 2000 and since then and until CUPS 2.x (at
least) conversion of the data format of incoming print jobs to the format
the printer needs was done by external filter executables, each taking an
input format on stdin and producing an output format on stdout.

Depending on conversion needs one or more of them were run in a chain.

The filters for common formats were part of CUPS and later on, when Apple
was maintaining CUPS and using their own, proprietary filters for Mac OS,
transferred to OpenPrinting as the cups-filters package.

In the New Architecture for printing we switch to an all-IPP workflow with
PPD files and printer driver executables being abolished and classic CUPS
printer drivers replaced by Printer Applications (software emulation of
driverless IPP printers).

To conserve the functionality of the CUPS filters which got developed over
the last 20+ years into a PPD-less, IPP-driven world without having to
maintain and include the legacy PPD support in OS distributions and other
system environments, the original cups-filters package got split into 5
separate packages: libcupsfilters, libppd, cups-filters, braille-printer-app,
and cups-browsed, with libcupsfilters and braille-printer-app not containing
PPD file support code any more and cups-browsed being planned to drop explicit
use of PPD files.

This package provides the libcupsfilters library, which in its 2.x version
contains all the code of the filters of the former cups-filters package as
library functions, the so-called filter functions.

The call scheme of the filter functions is similar to the one of the CUPS
filter executables (see cupsfilters/filter.h), but generalized. In addition,
it accepts printer and job IPP attributes but not PPD files any more. The PPD
file interfacing for retro-fitting got moved to libppd.

The filter functions are principally intended to be used for the data format
conversion tasks needed in Printer Applications. They are already in use
(together with libppd and pappl-retrofit) by the CUPS-driver retro-fitting
Printer Applications from OpenPrinting.

In addition to the filter functions libcupsfilters also contains several API
functions useful for developing printer drivers/Printer Applications, like
image and raster graphics handling, make/model/device ID matching, ...


%package -n %{libname}
Summary: Library containing functions useful for developing printer drivers
Group: System/Libraries

%description -n %{libname}
Library containing functions useful for developing printer drivers

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Library containing functions useful for developing printer drivers

%prep
%autosetup -p1
sed -i -e 's,glibtoolize,slibtoolize,g' autogen.sh
./autogen.sh
%configure

%build
%make_build

%install
%make_install

%files
%doc %{_docdir}/%{name}
%{_datadir}/cups

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
