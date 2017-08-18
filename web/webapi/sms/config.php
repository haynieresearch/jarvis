<?php
#**********************************************************
#* CATEGORY    SMS AUTOMATION
#* GROUP       HOME AUTOMATION
#* AUTHOR      LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#**********************************************************
#Jarvis Home Automation
#Copyright (C) 2017  Haynie Research & Development

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

$twilio_sid = 'AC4bbd8542d05810f24efaf2c28adc5763';
$twilio_token = 'df267e8a426269917a52650e4b122855';

$validNumbers = array(
	"+14355251418", //Lance
	"+14352725103", //Katie
	"+14357735320", //Vickie
	"+14357733283", //Robert
	"+14356197079" //Chris B.
//	"+14357733385" //Hudson
);

$RelayNumbers = array(
	"+14355251418", //Lance
);

$alertNumbers = array(
	"561-49", //NWS
	"+15303494355", //NWS
	"+16265392474", //NWS
	"+15306944687", //NWS
  "+14352720084" //NWS
);

$nwsRelayNumbers = array(
	"14355251418", //Lance
	"14352725103", //Katie
	"14357733385" //Hudson
);

$host = "http://10.0.1.200:8123/api/";
$password = "haynie";
$passwordUrl = "?api_password=" . $password;
$fromNumber = "+14352720084";

?>
