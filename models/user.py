#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

from google.appengine.ext import db

from controllers import config

class User(db.Expando):
	twitter_id = db.StringProperty(required=True)
	twitter_access_token_key = db.StringProperty(required=True)
	twitter_access_token_secret = db.StringProperty(required=True)
	username = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	bio = db.TextProperty(required=False)
	avatar = db.StringProperty(required=False)
	ideas = db.IntegerProperty(required=True, default=0)
	email = db.StringProperty(required=False)
	country = db.StringProperty(required=False)
	email_idea_comment = db.BooleanProperty(required=True, default=True)
	email_idea_feedback = db.BooleanProperty(required=True, default=True)
	email_comment_reply = db.BooleanProperty(required=True, default=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)

	@staticmethod
	def validate_email(email):
		validated = False
		if re.match("[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}", email):
			validated = True
		return validated

	@staticmethod
	def validate_country(country):
		validated = False
		if User.get_country_name(country):
			validated = True
		return validated		

	@staticmethod
	def get_countries():
		countries = [
			{"name":"AFGHANISTAN".decode("utf-8"),"code":"AF"},
			{"name":"ÅLAND ISLANDS".decode("utf-8"),"code":"AX"},
			{"name":"ALBANIA".decode("utf-8"),"code":"AL"},
			{"name":"ALGERIA".decode("utf-8"),"code":"DZ"},
			{"name":"AMERICAN SAMOA".decode("utf-8"),"code":"AS"},
			{"name":"ANDORRA".decode("utf-8"),"code":"AD"},
			{"name":"ANGOLA".decode("utf-8"),"code":"AO"},
			{"name":"ANGUILLA".decode("utf-8"),"code":"AI"},
			{"name":"ANTARCTICA".decode("utf-8"),"code":"AQ"},
			{"name":"ANTIGUA AND BARBUDA".decode("utf-8"),"code":"AG"},
			{"name":"ARGENTINA".decode("utf-8"),"code":"AR"},
			{"name":"ARMENIA".decode("utf-8"),"code":"AM"},
			{"name":"ARUBA".decode("utf-8"),"code":"AW"},
			{"name":"AUSTRALIA".decode("utf-8"),"code":"AU"},
			{"name":"AUSTRIA".decode("utf-8"),"code":"AT"},
			{"name":"AZERBAIJAN".decode("utf-8"),"code":"AZ"},
			{"name":"BAHAMAS".decode("utf-8"),"code":"BS"},
			{"name":"BAHRAIN".decode("utf-8"),"code":"BH"},
			{"name":"BANGLADESH".decode("utf-8"),"code":"BD"},
			{"name":"BARBADOS".decode("utf-8"),"code":"BB"},
			{"name":"BELARUS".decode("utf-8"),"code":"BY"},
			{"name":"BELGIUM".decode("utf-8"),"code":"BE"},
			{"name":"BELIZE".decode("utf-8"),"code":"BZ"},
			{"name":"BENIN".decode("utf-8"),"code":"BJ"},
			{"name":"BERMUDA".decode("utf-8"),"code":"BM"},
			{"name":"BHUTAN".decode("utf-8"),"code":"BT"},
			{"name":"BOLIVIA, PLURINATIONAL STATE OF".decode("utf-8"),"code":"BO"},
			{"name":"BONAIRE, SINT EUSTATIUS AND SABA".decode("utf-8"),"code":"BQ"},
			{"name":"BOSNIA AND HERZEGOVINA".decode("utf-8"),"code":"BA"},
			{"name":"BOTSWANA".decode("utf-8"),"code":"BW"},
			{"name":"BOUVET ISLAND".decode("utf-8"),"code":"BV"},
			{"name":"BRAZIL".decode("utf-8"),"code":"BR"},
			{"name":"BRITISH INDIAN OCEAN TERRITORY".decode("utf-8"),"code":"IO"},
			{"name":"BRUNEI DARUSSALAM".decode("utf-8"),"code":"BN"},
			{"name":"BULGARIA".decode("utf-8"),"code":"BG"},
			{"name":"BURKINA FASO".decode("utf-8"),"code":"BF"},
			{"name":"BURUNDI".decode("utf-8"),"code":"BI"},
			{"name":"CAMBODIA".decode("utf-8"),"code":"KH"},
			{"name":"CAMEROON".decode("utf-8"),"code":"CM"},
			{"name":"CANADA".decode("utf-8"),"code":"CA"},
			{"name":"CAPE VERDE".decode("utf-8"),"code":"CV"},
			{"name":"CAYMAN ISLANDS".decode("utf-8"),"code":"KY"},
			{"name":"CENTRAL AFRICAN REPUBLIC".decode("utf-8"),"code":"CF"},
			{"name":"CHAD".decode("utf-8"),"code":"TD"},
			{"name":"CHILE".decode("utf-8"),"code":"CL"},
			{"name":"CHINA".decode("utf-8"),"code":"CN"},
			{"name":"CHRISTMAS ISLAND".decode("utf-8"),"code":"CX"},
			{"name":"COCOS (KEELING) ISLANDS".decode("utf-8"),"code":"CC"},
			{"name":"COLOMBIA".decode("utf-8"),"code":"CO"},
			{"name":"COMOROS".decode("utf-8"),"code":"KM"},
			{"name":"CONGO".decode("utf-8"),"code":"CG"},
			{"name":"CONGO, THE DEMOCRATIC REPUBLIC OF THE".decode("utf-8"),"code":"CD"},
			{"name":"COOK ISLANDS".decode("utf-8"),"code":"CK"},
			{"name":"COSTA RICA".decode("utf-8"),"code":"CR"},
			{"name":"CÔTE D'IVOIRE".decode("utf-8"),"code":"CI"},
			{"name":"CROATIA".decode("utf-8"),"code":"HR"},
			{"name":"CUBA".decode("utf-8"),"code":"CU"},
			{"name":"CURAÇAO".decode("utf-8"),"code":"CW"},
			{"name":"CYPRUS".decode("utf-8"),"code":"CY"},
			{"name":"CZECH REPUBLIC".decode("utf-8"),"code":"CZ"},
			{"name":"DENMARK".decode("utf-8"),"code":"DK"},
			{"name":"DJIBOUTI".decode("utf-8"),"code":"DJ"},
			{"name":"DOMINICA".decode("utf-8"),"code":"DM"},
			{"name":"DOMINICAN REPUBLIC".decode("utf-8"),"code":"DO"},
			{"name":"ECUADOR".decode("utf-8"),"code":"EC"},
			{"name":"EGYPT".decode("utf-8"),"code":"EG"},
			{"name":"EL SALVADOR".decode("utf-8"),"code":"SV"},
			{"name":"EQUATORIAL GUINEA".decode("utf-8"),"code":"GQ"},
			{"name":"ERITREA".decode("utf-8"),"code":"ER"},
			{"name":"ESTONIA".decode("utf-8"),"code":"EE"},
			{"name":"ETHIOPIA".decode("utf-8"),"code":"ET"},
			{"name":"FALKLAND ISLANDS (MALVINAS)".decode("utf-8"),"code":"FK"},
			{"name":"FAROE ISLANDS".decode("utf-8"),"code":"FO"},
			{"name":"FIJI".decode("utf-8"),"code":"FJ"},
			{"name":"FINLAND".decode("utf-8"),"code":"FI"},
			{"name":"FRANCE".decode("utf-8"),"code":"FR"},
			{"name":"FRENCH GUIANA".decode("utf-8"),"code":"GF"},
			{"name":"FRENCH POLYNESIA".decode("utf-8"),"code":"PF"},
			{"name":"FRENCH SOUTHERN TERRITORIES".decode("utf-8"),"code":"TF"},
			{"name":"GABON".decode("utf-8"),"code":"GA"},
			{"name":"GAMBIA".decode("utf-8"),"code":"GM"},
			{"name":"GEORGIA".decode("utf-8"),"code":"GE"},
			{"name":"GERMANY".decode("utf-8"),"code":"DE"},
			{"name":"GHANA".decode("utf-8"),"code":"GH"},
			{"name":"GIBRALTAR".decode("utf-8"),"code":"GI"},
			{"name":"GREECE".decode("utf-8"),"code":"GR"},
			{"name":"GREENLAND".decode("utf-8"),"code":"GL"},
			{"name":"GRENADA".decode("utf-8"),"code":"GD"},
			{"name":"GUADELOUPE".decode("utf-8"),"code":"GP"},
			{"name":"GUAM".decode("utf-8"),"code":"GU"},
			{"name":"GUATEMALA".decode("utf-8"),"code":"GT"},
			{"name":"GUERNSEY".decode("utf-8"),"code":"GG"},
			{"name":"GUINEA".decode("utf-8"),"code":"GN"},
			{"name":"GUINEA-BISSAU".decode("utf-8"),"code":"GW"},
			{"name":"GUYANA".decode("utf-8"),"code":"GY"},
			{"name":"HAITI".decode("utf-8"),"code":"HT"},
			{"name":"HEARD ISLAND AND MCDONALD ISLANDS".decode("utf-8"),"code":"HM"},
			{"name":"HOLY SEE (VATICAN CITY STATE)".decode("utf-8"),"code":"VA"},
			{"name":"HONDURAS".decode("utf-8"),"code":"HN"},
			{"name":"HONG KONG".decode("utf-8"),"code":"HK"},
			{"name":"HUNGARY".decode("utf-8"),"code":"HU"},
			{"name":"ICELAND".decode("utf-8"),"code":"IS"},
			{"name":"INDIA".decode("utf-8"),"code":"IN"},
			{"name":"INDONESIA".decode("utf-8"),"code":"ID"},
			{"name":"IRAN, ISLAMIC REPUBLIC OF".decode("utf-8"),"code":"IR"},
			{"name":"IRAQ".decode("utf-8"),"code":"IQ"},
			{"name":"IRELAND".decode("utf-8"),"code":"IE"},
			{"name":"ISLE OF MAN".decode("utf-8"),"code":"IM"},
			{"name":"ISRAEL".decode("utf-8"),"code":"IL"},
			{"name":"ITALY".decode("utf-8"),"code":"IT"},
			{"name":"JAMAICA".decode("utf-8"),"code":"JM"},
			{"name":"JAPAN".decode("utf-8"),"code":"JP"},
			{"name":"JERSEY".decode("utf-8"),"code":"JE"},
			{"name":"JORDAN".decode("utf-8"),"code":"JO"},
			{"name":"KAZAKHSTAN".decode("utf-8"),"code":"KZ"},
			{"name":"KENYA".decode("utf-8"),"code":"KE"},
			{"name":"KIRIBATI".decode("utf-8"),"code":"KI"},
			{"name":"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF".decode("utf-8"),"code":"KP"},
			{"name":"KOREA, REPUBLIC OF".decode("utf-8"),"code":"KR"},
			{"name":"KUWAIT".decode("utf-8"),"code":"KW"},
			{"name":"KYRGYZSTAN".decode("utf-8"),"code":"KG"},
			{"name":"LAO PEOPLE'S DEMOCRATIC REPUBLIC".decode("utf-8"),"code":"LA"},
			{"name":"LATVIA".decode("utf-8"),"code":"LV"},
			{"name":"LEBANON".decode("utf-8"),"code":"LB"},
			{"name":"LESOTHO".decode("utf-8"),"code":"LS"},
			{"name":"LIBERIA".decode("utf-8"),"code":"LR"},
			{"name":"LIBYA".decode("utf-8"),"code":"LY"},
			{"name":"LIECHTENSTEIN".decode("utf-8"),"code":"LI"},
			{"name":"LITHUANIA".decode("utf-8"),"code":"LT"},
			{"name":"LUXEMBOURG".decode("utf-8"),"code":"LU"},
			{"name":"MACAO".decode("utf-8"),"code":"MO"},
			{"name":"MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF".decode("utf-8"),"code":"MK"},
			{"name":"MADAGASCAR".decode("utf-8"),"code":"MG"},
			{"name":"MALAWI".decode("utf-8"),"code":"MW"},
			{"name":"MALAYSIA".decode("utf-8"),"code":"MY"},
			{"name":"MALDIVES".decode("utf-8"),"code":"MV"},
			{"name":"MALI".decode("utf-8"),"code":"ML"},
			{"name":"MALTA".decode("utf-8"),"code":"MT"},
			{"name":"MARSHALL ISLANDS".decode("utf-8"),"code":"MH"},
			{"name":"MARTINIQUE".decode("utf-8"),"code":"MQ"},
			{"name":"MAURITANIA".decode("utf-8"),"code":"MR"},
			{"name":"MAURITIUS".decode("utf-8"),"code":"MU"},
			{"name":"MAYOTTE".decode("utf-8"),"code":"YT"},
			{"name":"MEXICO".decode("utf-8"),"code":"MX"},
			{"name":"MICRONESIA, FEDERATED STATES OF".decode("utf-8"),"code":"FM"},
			{"name":"MOLDOVA, REPUBLIC OF".decode("utf-8"),"code":"MD"},
			{"name":"MONACO".decode("utf-8"),"code":"MC"},
			{"name":"MONGOLIA".decode("utf-8"),"code":"MN"},
			{"name":"MONTENEGRO".decode("utf-8"),"code":"ME"},
			{"name":"MONTSERRAT".decode("utf-8"),"code":"MS"},
			{"name":"MOROCCO".decode("utf-8"),"code":"MA"},
			{"name":"MOZAMBIQUE".decode("utf-8"),"code":"MZ"},
			{"name":"MYANMAR".decode("utf-8"),"code":"MM"},
			{"name":"NAMIBIA".decode("utf-8"),"code":"NA"},
			{"name":"NAURU".decode("utf-8"),"code":"NR"},
			{"name":"NEPAL".decode("utf-8"),"code":"NP"},
			{"name":"NETHERLANDS".decode("utf-8"),"code":"NL"},
			{"name":"NEW CALEDONIA".decode("utf-8"),"code":"NC"},
			{"name":"NEW ZEALAND".decode("utf-8"),"code":"NZ"},
			{"name":"NICARAGUA".decode("utf-8"),"code":"NI"},
			{"name":"NIGER".decode("utf-8"),"code":"NE"},
			{"name":"NIGERIA".decode("utf-8"),"code":"NG"},
			{"name":"NIUE".decode("utf-8"),"code":"NU"},
			{"name":"NORFOLK ISLAND".decode("utf-8"),"code":"NF"},
			{"name":"NORTHERN MARIANA ISLANDS".decode("utf-8"),"code":"MP"},
			{"name":"NORWAY".decode("utf-8"),"code":"NO"},
			{"name":"OMAN".decode("utf-8"),"code":"OM"},
			{"name":"PAKISTAN".decode("utf-8"),"code":"PK"},
			{"name":"PALAU".decode("utf-8"),"code":"PW"},
			{"name":"PALESTINE, STATE OF".decode("utf-8"),"code":"PS"},
			{"name":"PANAMA".decode("utf-8"),"code":"PA"},
			{"name":"PAPUA NEW GUINEA".decode("utf-8"),"code":"PG"},
			{"name":"PARAGUAY".decode("utf-8"),"code":"PY"},
			{"name":"PERU".decode("utf-8"),"code":"PE"},
			{"name":"PHILIPPINES".decode("utf-8"),"code":"PH"},
			{"name":"PITCAIRN".decode("utf-8"),"code":"PN"},
			{"name":"POLAND".decode("utf-8"),"code":"PL"},
			{"name":"PORTUGAL".decode("utf-8"),"code":"PT"},
			{"name":"PUERTO RICO".decode("utf-8"),"code":"PR"},
			{"name":"QATAR".decode("utf-8"),"code":"QA"},
			{"name":"RÉUNION".decode("utf-8"),"code":"RE"},
			{"name":"ROMANIA".decode("utf-8"),"code":"RO"},
			{"name":"RUSSIAN FEDERATION".decode("utf-8"),"code":"RU"},
			{"name":"RWANDA".decode("utf-8"),"code":"RW"},
			{"name":"SAINT BARTHÉLEMY".decode("utf-8"),"code":"BL"},
			{"name":"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA".decode("utf-8"),"code":"SH"},
			{"name":"SAINT KITTS AND NEVIS".decode("utf-8"),"code":"KN"},
			{"name":"SAINT LUCIA".decode("utf-8"),"code":"LC"},
			{"name":"SAINT MARTIN (FRENCH PART)".decode("utf-8"),"code":"MF"},
			{"name":"SAINT PIERRE AND MIQUELON".decode("utf-8"),"code":"PM"},
			{"name":"SAINT VINCENT AND THE GRENADINES".decode("utf-8"),"code":"VC"},
			{"name":"SAMOA".decode("utf-8"),"code":"WS"},
			{"name":"SAN MARINO".decode("utf-8"),"code":"SM"},
			{"name":"SAO TOME AND PRINCIPE".decode("utf-8"),"code":"ST"},
			{"name":"SAUDI ARABIA".decode("utf-8"),"code":"SA"},
			{"name":"SENEGAL".decode("utf-8"),"code":"SN"},
			{"name":"SERBIA".decode("utf-8"),"code":"RS"},
			{"name":"SEYCHELLES".decode("utf-8"),"code":"SC"},
			{"name":"SIERRA LEONE".decode("utf-8"),"code":"SL"},
			{"name":"SINGAPORE".decode("utf-8"),"code":"SG"},
			{"name":"SINT MAARTEN (DUTCH PART)".decode("utf-8"),"code":"SX"},
			{"name":"SLOVAKIA".decode("utf-8"),"code":"SK"},
			{"name":"SLOVENIA".decode("utf-8"),"code":"SI"},
			{"name":"SOLOMON ISLANDS".decode("utf-8"),"code":"SB"},
			{"name":"SOMALIA".decode("utf-8"),"code":"SO"},
			{"name":"SOUTH AFRICA".decode("utf-8"),"code":"ZA"},
			{"name":"SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS".decode("utf-8"),"code":"GS"},
			{"name":"SOUTH SUDAN".decode("utf-8"),"code":"SS"},
			{"name":"SPAIN".decode("utf-8"),"code":"ES"},
			{"name":"SRI LANKA".decode("utf-8"),"code":"LK"},
			{"name":"SUDAN".decode("utf-8"),"code":"SD"},
			{"name":"SURINAME".decode("utf-8"),"code":"SR"},
			{"name":"SVALBARD AND JAN MAYEN".decode("utf-8"),"code":"SJ"},
			{"name":"SWAZILAND".decode("utf-8"),"code":"SZ"},
			{"name":"SWEDEN".decode("utf-8"),"code":"SE"},
			{"name":"SWITZERLAND".decode("utf-8"),"code":"CH"},
			{"name":"SYRIAN ARAB REPUBLIC".decode("utf-8"),"code":"SY"},
			{"name":"TAIWAN, PROVINCE OF CHINA".decode("utf-8"),"code":"TW"},
			{"name":"TAJIKISTAN".decode("utf-8"),"code":"TJ"},
			{"name":"TANZANIA, UNITED REPUBLIC OF".decode("utf-8"),"code":"TZ"},
			{"name":"THAILAND".decode("utf-8"),"code":"TH"},
			{"name":"TIMOR-LESTE".decode("utf-8"),"code":"TL"},
			{"name":"TOGO".decode("utf-8"),"code":"TG"},
			{"name":"TOKELAU".decode("utf-8"),"code":"TK"},
			{"name":"TONGA".decode("utf-8"),"code":"TO"},
			{"name":"TRINIDAD AND TOBAGO".decode("utf-8"),"code":"TT"},
			{"name":"TUNISIA".decode("utf-8"),"code":"TN"},
			{"name":"TURKEY".decode("utf-8"),"code":"TR"},
			{"name":"TURKMENISTAN".decode("utf-8"),"code":"TM"},
			{"name":"TURKS AND CAICOS ISLANDS".decode("utf-8"),"code":"TC"},
			{"name":"TUVALU".decode("utf-8"),"code":"TV"},
			{"name":"UGANDA".decode("utf-8"),"code":"UG"},
			{"name":"UKRAINE".decode("utf-8"),"code":"UA"},
			{"name":"UNITED ARAB EMIRATES".decode("utf-8"),"code":"AE"},
			{"name":"UNITED KINGDOM".decode("utf-8"),"code":"GB"},
			{"name":"UNITED STATES".decode("utf-8"),"code":"US"},
			{"name":"UNITED STATES MINOR OUTLYING ISLANDS".decode("utf-8"),"code":"UM"},
			{"name":"URUGUAY".decode("utf-8"),"code":"UY"},
			{"name":"UZBEKISTAN".decode("utf-8"),"code":"UZ"},
			{"name":"VANUATU".decode("utf-8"),"code":"VU"},
			{"name":"VENEZUELA, BOLIVARIAN REPUBLIC OF".decode("utf-8"),"code":"VE"},
			{"name":"VIET NAM".decode("utf-8"),"code":"VN"},
			{"name":"VIRGIN ISLANDS, BRITISH".decode("utf-8"),"code":"VG"},
			{"name":"VIRGIN ISLANDS, U.S.".decode("utf-8"),"code":"VI"},
			{"name":"WALLIS AND FUTUNA".decode("utf-8"),"code":"WF"},
			{"name":"WESTERN SAHARA".decode("utf-8"),"code":"EH"},
			{"name":"YEMEN".decode("utf-8"),"code":"YE"},
			{"name":"ZAMBIA".decode("utf-8"),"code":"ZM"},
			{"name":"ZIMBABWE".decode("utf-8"),"code":"ZW"},
		]
		
		return countries

	@staticmethod
	def get_country_name(country):
		name = None

		countries = User.get_countries()
		for c in countries:
			if c["code"] == country.upper():
				name=c["name"]
				break

		return name





