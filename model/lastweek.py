from preprocess import *
from train_test_set import *
from score import *
from statistics import *
import copy
import numpy as np
def splitdata(user_brand,month,day):

    first_set = {}
    second_set = {}

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2].month < month or (record[2].month == month and record[2].day<day ):
                if not first_set.has_key(user):
                    first_set[user] = [record]
                else:
                    first_set[user].append(record)
            else:
                if not second_set.has_key(user): 
                    second_set[user] = [record]
                else:
                    second_set[user].append(record)
        
    return (first_set, second_set)
def getnewpairs(first_set,second_set):
	u_b_a = user_brand_action_count(second_set)
	for us in u_b_a.keys():
		for brand in u_b_a[us].keys():
			if u_b_a[us][brand][1]==0:
				del u_b_a[us][brand]
	last_month={}
	for us in u_b_a:
		for brand in u_b_a[us]:
			if not last_month.has_key(us):
				last_month[us]=[brand]
			else:
				last_month[us].append(brand)
	u_b_a = user_brand_action_count(first_set)
	pre_month={}
	for us in u_b_a:
		for brand in u_b_a[us]:
			if not pre_month.has_key(us):
				pre_month[us]=[brand]
			else:
				pre_month[us].append(brand)
	newpairs={}
	for us in last_month.keys():
		if not pre_month.has_key(us):
			newpairs[us]=copy.deepcopy(last_month[us])
		else:
			for brand in pre_month[us]:
				if brand not in	pre_month[us] :
					if not newpairs[us].has_key(brand):
						newpairs[us]=[brand]
					else:
						newpairs[us].append(brand)
	return newpairs 


def get_lastweekdata(user_brand, last_month):

    train_set = {}
    test_set = {}

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2].month == last_month and record[2].day>=8:
                if not test_set.has_key(user):
                    test_set[user] = [record]
                else:
                    test_set[user].append(record)
            
        
    return (test_set)
def get_lastmonth(user_brand):
    last_month={}
    datea=datetime.datetime(2013,7,25)

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2]>datea:
                if not last_month.has_key(user):
                    last_month[user] = [record]
                else:
                    last_month[user].append(record)
    u_b_a = user_brand_action_count(last_month)
    lastmonth={}
    for us in u_b_a:
        for brand in u_b_a[us]:
            if u_b_a[us][brand][1]>=1:
                if not lastmonth.has_key(us):
                    lastmonth[us]=[brand]
                else:
                    lastmonth[us].append(brand)
    return lastmonth

def get23(user_brand):
    brand23={}
    datea=datetime.datetime(2013,8,1)

    for user in user_brand.keys():
        for record in user_brand[user]:
            if record[2]>=datea:
                if not brand23.has_key(user):
                    brand23[user] = [record]
                else:
                    brand23[user].append(record)
    u_b_a = user_brand_action_count(brand23)
    user_brand23={}
    for us in u_b_a:
        for brand in u_b_a[us]:
            if u_b_a[us][brand][2]>=1 or u_b_a[us][brand][3]>=1:
                if not user_brand23.has_key(us):
                    user_brand23[us]=[brand]
                else:
                    user_brand23[us].append(brand)
    return user_brand23

def getlastweek(user_brand):
	test_set = get_lastweekdata(user_brand, find_last_month(user_brand))
	u_b_a = user_brand_action_count(test_set)
	for us in u_b_a.keys():
		for brand in u_b_a[us].keys():
			if u_b_a[us][brand][1]!=0:
				del u_b_a[us][brand]

	lastweek={}
	for us in u_b_a:
		for brand in u_b_a[us]:
			if u_b_a[us][brand][0]>=3:
				if not lastweek.has_key(us):
					lastweek[us]=[brand]
				else:
					lastweek[us].append(brand)
	return lastweek