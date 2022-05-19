# -*- coding: UTF-8 -*-



def mean(x):
	return float(sum(x))/len(x)

def std(x,sampling=True):
	mu=mean(x)
	n=len(x)
	acc=0.0
	for i in x:
		acc+=(i-mu)**2
	if sampling:
		acc/=(n-1)
	else:
		acc/=n
	return acc**0.5

def cov(x,y,sampling=True):
	if len(x)<>len(y):
		raise Exception("样本数量不同")
	n=len(x)
	m1=mean(x)
	m2=mean(y)
	acc=0.0
	for i in range(n):
		acc+=(x[i]-m1)*(y[i]-m2)
	if sampling:
		acc/=n-1
	else:
		acc/=n
	return acc

def pearson(x,y):
	return cov(x,y)/std(x)/std(y)

def rankify(x):
	n=len(x)
	rank_X=[1]*n
	for i in range(n):
		r=1
		s=1
		for j in range(i):
			if x[j] < x[i]:
				r+=1
			elif x[j] == x[i]:
				s+=1
		for j in range(i+1,n):
			if x[j] < x[i]:
				r = r+1
			elif x[j] == x[i]:
				s = s+1
		rank_X[i]=r+(s-1)*0.5
	return rank_X

def spearman(x,y):
	rx=rankify(x)
	ry=rankify(y)
	return pearson(rx,ry)
























