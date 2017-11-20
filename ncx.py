#!/usr/bin/env python3
#
# Authors: Boonlert Archevarahuprok
# E-mail:  boonlert.arc@tmd.go.th
#          lertarc@gmail.com
#
# Address: Thai Meteorological Department (TMD)
#          4353 Sukhumvit Road, Bangna, Bangkok 10260, THAILAND
#          Tel: (66-2) 3991423, Fax: (66-2) 3838827
#
# This is free software: you can redistribute it and/or modify it under the terms of
# the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or later version. See more details
# <http://www.gnu.org/licenses/>.
#
# Date: December 6, 2015
#
import os
import sys
from netCDF4 import Dataset, num2date
def atindx(x, xvar):

    indx = None

    if x[0] > x[-1]:

        for n in range(len(x)):

            if x[n] < xvar:
                indx = n

                if abs(x[n - 1] - xvar) < abs(x[n] - xvar):
                    indx = n - 1

                break

    else:

        for n in range(len(x)):

            if x[n] > xvar:
                indx = n

                if abs(x[n - 1] - xvar) < abs(x[n] - xvar):
                    indx = n - 1

                break

    return indx
def nearleast(lat, lon, slat, slon, debug):

    jlat = atindx(lat, slat)
    ilon = atindx(lon, slon)

    if debug:
        print("-1",jlat-1,lat[jlat-1],slat,abs(lat[jlat-1]-slat))
        print(" 0",jlat,lat[jlat],slat,abs(lat[jlat]-slat))
        print("+1",jlat+1,lat[jlat+1],slat,abs(lat[jlat+1]-slat))

        print("-1",ilon-1,lon[ilon-1],slon,abs(lon[ilon-1]-slon))
        print(" 0",ilon,lon[ilon],slon,abs(lon[ilon]-slon))
        print("+1",ilon+1,lon[ilon+1],slon,abs(lon[ilon+1]-slon))
        #sys.exit()

    return jlat, ilon
def dtype(type):

    types={"S1":"char","int32":"int","float32":"float","float64":"double"}

    return types[type]
def isnc(filename):

    # magic number

    fp = open(filename, 'rb')
    header = fp.read(4)
    fp.close()
    #print(header)

    # classic format (CDF-1)
    if header == b'CDF\x01':
        return True

    # pnetcdf (CDF-2)
    elif header == b'CDF\x02':
        return True

    # CDF-5
    elif header == b'CDF\x05':
        return True

    # HDF-5
    elif header == b'\x89HDF':
        return True

    else:
        print(header)
        return False
def nc_varname(filen, var):

    nc_attrs, nc_dims, nc_vars = nc_getinfo(filen, False)

    for dim in nc_dims:
        # print(dim)
        if var in dim:
            return dim

    return None
def nc_getij(filen, slat, slong, debug):

    nc_fid = Dataset(filen, 'r')
    nc_dims = [dim for dim in nc_fid.dimensions]
    nc_vars = [var for var in nc_fid.variables]

    nclat_name, nclong_name = None, None

    for dim in nc_dims:
        # print(dim)
        if "lat" in dim:
            nclat_name = dim

        if "lon" in dim:
            nclong_name = dim

    if nclat_name is None:
        for var in nc_vars:
            if "lat" in var:
                nclat_name = var

    if nclong_name is None:
        for var in nc_vars:
            if "lon" in var:
                nclong_name = var

    if nclat_name is not None:
        lat = nc_fid.variables[nclat_name][:]

    else:
        print("None latitude in file",nc_dims, nc_vars)


    if nclong_name is not None:
        long = nc_fid.variables[nclong_name][:]

    else:
        print("None longitude in file", nc_dims, nc_vars)

    nc_fid.close()

    if len(lat) > 0 and len(long) > 0:
        return nearleast(lat, long, float(slat), float(slong), debug)

    else:
        print("None location in file", slat, slong)
        return None, None
def nc_getime(filen, var):

    nc_fid = Dataset(filen,'r')

    nc_dims = [dim for dim in nc_fid.dimensions]

    for dim in nc_dims:
        # print(dim)
        if var in dim:
            nctime_name = dim

    if nctime_name is not None:
        var_time_units=nc_fid.variables[nctime_name].units

        try:
            var_time_calendar=nc_fid.variables[nctime_name].calendar

        except:
            var_time_calendar=u"gregorian" # or standard

        dtime = num2date(nc_fid.variables[nctime_name][:], units=var_time_units, calendar=var_time_calendar)
        #print(nc_fid.variables[nctime_name][:])
        #ctime=dtime[0]

    else:
        dtime = None

    nc_fid.close()

    return dtime
def nc_getvardim(filen, var):

    nc_fid = Dataset(filen, 'r')
    nc_vars = [var for var in nc_fid.variables]

    dimension = 0
    if var in nc_vars:
        x = nc_fid.variables[var]
        dimension = len(x.dimensions)

    nc_fid.close()

    return dimension
def nc_getinfo(filen, verb=True):

    if not isnc(filen):
        print("Non't CDF-1 file format",filen)
        print("Non't CDF-2 file format",filen)
        print("Non't CDF-5 file format",filen)
        print("Non't HDF-5 file format", filen)
        sys.exit()

    nc_fid = Dataset(filen,'r')

    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    '''

    def print_ncattr(key):

        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:

            print("\t\ttype:", repr(nc_fid.variables[key].dtype))

            for ncattr in nc_fid.variables[key].ncattrs():
                print('\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr)))

        except KeyError:

            print("\t\tWARNING: %s does not contain variable attributes" % key)

    # NetCDF global attributes

    nc_attrs = nc_fid.ncattrs()

    # Dimension shape information.

    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions

    # Variable information.

    nc_vars = [var for var in nc_fid.variables]  # list of nc variables


    if verb:
        print("netcdf %s {"%(os.path.split(filen)[1]))

        print("dimension:")

        for dim in nc_dims:
            print("\t\t{} = {} ;".format(dim, len(nc_fid.dimensions[dim])))
            #print("\t\tsize:", len(nc_fid.dimensions[dim]))
            #print_ncattr(dim)

        print("variable:")

        for var in nc_vars:

            if var not in nc_dims:
                #print(repr(nc_fid.variables[var].dtype).replace("dtype('",'').replace("')",''))
                print("\t\t{} {}{} ;".format(dtype(repr(nc_fid.variables[var].dtype).replace("dtype('",'').replace("')",'')),
                                             var,
                                             nc_fid.variables[var].dimensions).replace("'","").replace(",)",")"))
                #print('\tName:', var)
                #print("\t\tdimensions:", nc_fid.variables[var].dimensions)
                #print("\t\tsize:", nc_fid.variables[var].size)
                #print_ncattr(var)

        print("\\\\ global attributes:")

        for nc_attr in nc_attrs:
            print("\t\t\t\t:{} = {} ;".format(nc_attr, repr(nc_fid.getncattr(nc_attr))))

        print("}")

    nc_fid.close()

    return nc_attrs, nc_dims, nc_vars
def options_var(var, default, options):

    if var in options:
        return options[var]

    else:
        return default
def options_default(options):


    var = options_var("var","",options)
    fact = options_var("fact", "", options)
    point = options_var("point", "", options)
    filen = options_var("filen", "", options)
    info = options_var("info", False, options)
    debug = options_var("debug", False, options)
    thai = options_var("thai", False, options)

    return  var, fact, point, filen, info, thai, debug
def help(prog, thai):

    lang = "en"

    if thai:
        lang = "th"

    print("{}: {} {}".format({"en":"usage","th":"การใช้งาน"}[lang],prog,{"en":"[options] [flags]","th":"[ค่าตัวเลือก] [สถานะ]"}[lang]))
    print("\n {}:".format({"en":"Options","th":"ค่าตัวเลือก"}[lang]))
    print("     --help or -help or -h         {}".format({"en":"Help information",
                                                          "th":"ความหมายของรายละเอียดการใช้งาน"}[lang]))
    print("     var=<variable name>           {}".format({"en": "Variable to display",
                                                          "th": "ชื่อตัวแปรที่ต้องการ"}[lang]))
    print("     point=<latitude,longitude>    {}".format({"en": "Geographic location latitude and longitude",
                                                          "th": "ตำแหน่งพิกัดละติจูดและลองกิจูดที่ต้องการให้แสดงข้อมูล"}[lang]))
    print("     fact=<factor value>           {}".format({"en": "Factor value",
                                                          "th": "ค่าเฟคเตอร์ของตัวแปร"}[lang]))
    print("     filen=<file name>             {}".format({"en": "NetCDF file name",
                                                          "th": "ชื่อแฟ้มข้อมูล"}[lang]))

    print("\n {}:".format({"en":"Flags","th":"การกำหนดสถานะ"}[lang]))
    print("     debug                         {}".format({"en": "Debug",
                                                          "th": "แสดงรายละเอียดของการทำงาน"}[lang]))
    print("     thai                          {}".format({"en": "Flag for local thai language",
                                                          "th": "การกำหนดภาษาไทย"}[lang]))
    print("     info                          {}".format({"en": "Information of netcdf file",
                                                          "th": "แสดงรายการที่เก็บบันทึกอยู่ในแฟ้มข้อมูล"}[lang]))
def argv_dict(lines):

    keys={}

    for n in range(1,len(lines)):

        if "=" in lines[n]:
            line = lines[n]
            j = line.index("=")
            keys[line[:j]] = line[j+1:]

        else:
            keys[lines[n]]=True

    return keys
def fact_value(x, fact):

    if "-" in fact:
        return x - float(fact.replace('-', ''))

    elif "+" in fact:
        return x + float(fact.replace('+', ''))

    elif "*" in fact:
        return x * float(fact.replace('*', ''))

    elif "/" in fact:
        return x / float(fact.replace('/', ''))

    elif "^" in fact:
        return x ** float(fact.replace('^', ''))

    else:
        return x
def export_data(filen, var, dimension, fact, timex, jlat, ilong):

    nc_fid = Dataset(filen, 'r')

    x = nc_fid.variables[var]

    if dimension == 1:
        for i in range(len(timex)):
            print("{} {}".format(timex[i], fact_value(x[i], fact)))

    elif dimension == 3:
        for i in range(len(timex)):
            print("{} {}".format(timex[i], fact_value(x[i, jlat, ilong], fact)))

    else:
        print("Dimension is not 1 or 3")

    nc_fid.close()
def main():

    options = argv_dict(sys.argv)

    var, fact, point, filen, info, thai, debug = options_default(options)

    if debug:
        print(options)
        print(var, fact, point, filen, info, thai, debug)

    if "--help" in options or "-help" in options or "-h" in options:
        help(sys.argv[0], thai)

    if info and os.path.exists(filen):
        nc_attrs, nc_dims, nc_vars = nc_getinfo(filen, True)

    if var is not "" and os.path.exists(filen):
        dimension = nc_getvardim(filen, var)
        timex = nc_getime(filen,"time")

        if dimension == 1:
            export_data(filen, var, dimension, fact, timex, None, None)

        elif dimension > 1 and point is not "":
            slat, slong = point.split(",")
            jlat, ilong = nc_getij(filen, slat, slong, debug)

            export_data(filen, var, dimension, fact, timex, jlat, ilong)
if __name__ == "__main__":
    main()
