#!/usr/bin/env python3

#####################################################################################################################
# 
# Copyright (c) 2020 Bernhard Flühmann. All rights reserved.
#
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.
#
######################################################################################################################


# TODO: Improve comments

class Location:
  def __init__(self, name_abbr, name_de, name_en, latitude, longitude): 
    self.name_abbr = name_abbr
    self.name_de    = name_de
    self.name_en    = name_en
    self.latitude   = latitude
    self.longitude  = longitude

class Locations(dict):
  def __init__(self): 
    #self = dict()
    #    name_abbr        name_abbr   , name_de                 , name_en            , latitude  , longitude
    # Cantons
    self["AG"]        = Location("AG"        , "Aargau"                  , "Aargau"             , 47.449406 , 8.327495  )
    self["AI"]        = Location("AI"        , "Appenzell Innerrhoden"   , "Appenzell AI. Rh."  , 47.328414 , 9.409647  )
    self["AR"]        = Location("AR"        ,	"Appenzell Ausserrhoden" ,	"Appenzell AI. Rh." , 47.38271  , 9.27186   )
    self["BE"]        = Location("BE"        , "Bern"                    , "Berne"              , 46.916667 , 7.466667  )
    self["BL"]        = Location("BL"        , "Basel-Landschaft"        , "Basel-Landschaft"   , 47.482779 , 7.742975  )
    self["BS"]        = Location("BS"        ,	"Basel-Stadt"            , "Basel-Stadt"        , 47.558395 , 7.573271  )
    self["FR"]        = Location("FR"        , "Freiburg"                , "Fribourg"           , 46.718391 , 7.074008  )
    self["GE"]        = Location("GE"        ,	"Genf"                   , "Geneva"             , 46.195602 , 6.148113  )
    self["GL"]        = Location("GL"        ,	"Glarus"                 ,	"Glarus"            , 47.04057  , 9.068036  )
    self["GR"]        = Location("GR"        , "Graubünden"              , "Graubünden"         , 46.796756 , 10.305946 )
    self["JU"]        = Location("JU"	       , "Jura"                    , "Jura"               , 47.350744 , 7.156107  )
    self["LU"]        = Location("LU"        ,	"Luzern"                 , "Lucerne"            , 47.083333 , 8.266667	)
    self["NE"]        = Location("NE"        ,	"Neuenburg"              ,	"Neuchâtel"         , 46.995534 , 6.780126  )
    self["NW"]        = Location("NW"        ,	"Nidwalden"              , "Nidwalden"          , 46.95805  , 8.36609   )
    self["OW"]        = Location("OW"        ,	"Obwalden"               , "Obwalden"           , 46.898509 , 8.250681	)
    self["SG"]        = Location("SG"        ,	"St.Gallen"              , "St. Gallen"         , 47.43162  , 9.39845   )
    self["SH"]        = Location("SH"        , "Schaffhausen"            , "Schaffhausen"       , 47.71357  , 8.59167   )
    self["SO"]        = Location("SO"        , "Solothurn"               , "Solothurn"          , 47.206649 , 7.516605  )
    self["SZ"]        = Location("SZ"        , "Schwyz"                  , "Schwyz"             , 47.061787 , 8.756585  )
    self["TG"]        = Location("TG"        , "Thurgau"                 , "Thurgau"            , 47.55993  , 8.8998    )
    self["TI"]        = Location("TI"        , "Tessin"                  , "Ticino"             , 46.009279 , 8.955576  )
    self["UR"]        = Location("UR"        , "Uri"                     , "Uri"                , 46.880422 , 8.644409  )
    self["VD"]        = Location("VD"        , "Waadt"                   , "Vaud"               , 46.536900 , 6.584780  )
    self["VS"]        = Location("VS"        , "Wallis"                  , "Valais"             , 46.209567 , 7.604659  )
    self["ZG"]        = Location("ZG"        , "Zug"                     , "Zug"                , 47.157296 , 8.537294  )
    self["ZH"]        = Location("ZH"        , "Zürich"                  , "Zurich"             , 47.451542 , 8.564572  )
    # FOPH, WTF? 
    self["Unbekannt"] = Location("N/A"       , "Unbekannt"               , "Unknown"            , 46.7985   , 8.2319    )
    # Switzerland
    self["CH"]        = Location("CH"        , "Schweiz"                 , "Switzerland"      , 46.7985   , 8.2319    )
