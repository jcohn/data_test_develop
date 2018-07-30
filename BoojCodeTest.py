#!/usr/bin/python

import csv
import sys
import datetime
import pandas as pd
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

''' CSV Requirements

    Contains only properties listed from 2016 [DateListed]
    Contains only properties that contain the word "and" in the Description field
    CSV ordered by DateListed
    Required fields:
      MlsId
      MlsName
      DateListed
      StreetAddress
      Price
      Bedrooms
      Bathrooms
      Appliances (all sub-nodes comma joined)
      Rooms (all sub-nodes comman joined)
      Description (the first 200 characters)

    Technical Requirements

    Interpreter version: python 2.7
    Reasonable unit test coverage
    All libraries used must be documented in requirements.txt
      We will be using pip install -r requirements.txt prior to running your code
    Raw information to parse / feed url
      http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml
      This feed must be downloaded from with in the script, raw data must not be downloaded manually
'''

class BoojCodeTestHandler(ContentHandler):
  # TODO This code implements a brute force handler for a specific xml feed
  # TODO Should re-architect to read the xml feed definition and requirements
  # TODO Metadata defining how to process the feed, possibly including
  # TODO scheduling should be read from a file or database

  # TODO Need to add exception handling for parser detected feed errors
  _MlsIdFlag = False
  _MlsId = ""
  _MlsNameFlag = False
  _MlsName = ""
  _DateListedFlag = False
  _DateListed = ""
  _StreetAddressFlag = False
  _StreetAddress = ""
  _PriceFlag = False
  _Price = ""
  _BedroomsFlag = False
  _Bedrooms = ""
  _BathroomsFlag = False
  _Bathrooms = ""
  _AppliancesFlag = False
  _Appliances = ""
  _RoomsFlag = False
  _Rooms = ""
  _DescriptionFlag = False
  _Description = ""

  def startElement(self, name, attrs):
    if name == "Listing":
      self._MlsIdFlag = False
      self._MlsId = ""
      self._MlsNameFlag = False
      self._MlsName = ""
      self._DateListedFlag = False
      self._DateListed = ""
      self._StreetAddressFlag = False
      self._StreetAddress = ""
      self._PriceFlag = False
      self._Price = ""
      self._BedroomsFlag = False
      self._Bedrooms = ""
      self._BathroomsFlag = False
      self._Bathrooms = ""
      self._AppliancesFlag = False
      self._Appliances = ""
      self._RoomsFlag = False
      self._Rooms = ""
      self._DescriptionFlag = False
      self._Description = ""
    elif name == "MlsId":
      self._MlsIdFlag = True
    elif name == "MlsName":
      self._MlsNameFlag = True
    elif name == "DateListed":
      self._DateListedFlag = True
    elif name == "StreetAddress":
      self._StreetAddressFlag = True
    elif name == "Price":
      self._PriceFlag = True
    elif name == "Bedrooms":
      self._BedroomsFlag = True
    elif name == "Bathrooms":
      self._BathroomsFlag = True
    elif name == "Appliances":
      self._AppliancesFlag = True
    elif name == "Rooms":
      self._RoomsFlag = True
    elif name == "Description":
      self._DescriptionFlag = True

  def endElement(self, name):
    if name == "Listing":
      # TODO This method of finding the word "and" will miss cases like "and,"
      if "2016" in self._DateListed and " and " in self._Description:
        self._Description = self._Description[:200] if len(self._Description) > 200 else self._Description
        writer.writerow((self._MlsId, self._MlsName, self._DateListed, self._StreetAddress, self._Price, self._Bedrooms, self._Bathrooms, self._Appliances, self._Rooms, self._Description))
    if name == "MlsId":
      self._MlsIdFlag = False
    elif name == "MlsName":
      self._MlsNameFlag = False
    elif name == "DateListed":
      self._DateListedFlag = False
    elif name == "StreetAddress":
      self._StreetAddressFlag = False
    elif name == "Price":
      self._PriceFlag = False
    elif name == "Bedrooms":
      self._BedroomsFlag = False
    elif name == "Bathrooms":
      self._BathroomsFlag = False
    elif name == "Appliances":
      self._AppliancesFlag = False
    elif name == "Rooms":
      self._RoomsFlag = False
    elif name == "Description":
      self._DescriptionFlag = False

  def characters(self, content):
    if self._MlsIdFlag:
      self._MlsId = self._MlsId + content
    elif self._MlsNameFlag:
      self._MlsName = self._MlsName + content
    elif self._DateListedFlag:
      self._DateListed = self._DateListed + content
    elif self._StreetAddressFlag:
      self._StreetAddress = self._StreetAddress + content
    elif self._PriceFlag:
      self._Price = self._Price + content
    elif self._BedroomsFlag:
      self._Bedrooms = self._Bedrooms + content
    elif self._BathroomsFlag:
      # TODO This node doesn't wrap potential sub-nodes for Full, Half, and
      # TODO ThreeQuarter Baths. Perhaps should sum those into this node?
      self._Bathrooms = self._Bathrooms + content
    elif self._AppliancesFlag:
      content = content.strip()
      if len(content):
        if len(self._Appliances):
          self._Appliances = self._Appliances + ','
        self._Appliances = self._Appliances + content
    elif self._RoomsFlag:
      content = content.strip()
      if len(content):
        if len(self._Rooms):
          self._Rooms = self._Rooms + ','
        self._Rooms = self._Rooms + content
    elif self._DescriptionFlag:
      self._Description = self._Description + content

parser = make_parser()
handler = BoojCodeTestHandler()

parser.setContentHandler(handler)

csv_file = "BoojCodeTest.csv"
f = open(csv_file, 'wt')
writer = csv.writer(f)

parser.parse("http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml")

f.close()

df = pd.DataFrame.from_csv(csv_file, header=None)
df[2] = df[2].astype('datetime64[ns]')
df = df.sort_values(2)

df.to_csv(csv_file, header=None)
