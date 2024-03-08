# -*- coding: UTF-8 -*-
# 与向量有关的计算
import math
import numpy as np
import numpy.linalg as lr

def angle(vec):
	vec_x = np.array([1.0,0.0])
	cos = np.dot(vec,vec_x)/(lr.norm(vec))
	res = math.acos(cos)
	if vec[1]>=0:
		return res
	else:
		return -res

def angle_between(v1,v2):
	a1 = angle(v1)
	a2 = angle(v2)
	res = a2 - a1
	two_pi = 2*math.pi
	while res<-math.pi: res+=two_pi
	while res>math.pi: res-=two_pi
	return res

def vector_combine(list_of_vectors):
	if len(list_of_vectors)<3:
		return list_of_vectors
	vecs = list(list_of_vectors)
	vecs.sort(key=lambda x:angle(x))
	nvec = len(vecs)
	vecs.append(vecs[0])
	angles = []
	dotpds = []
	for idx in range(nvec):
		v1=vecs[idx]
		v2=vecs[idx+1]
		angles.append(angle_between(v1,v2))
		dotpds.append(np.dot(v1,v2))
	if all([dp<0 for dp in dotpds]):
		return list_of_vectors
	vecs.pop()
	min_angle_value = min(angles)
	min_angle_indice = [i for i,v in enumerate(angles) if v==min_angle_value]
	max_product = float("-Inf")
	vec_idx_1 = None
	for idx in min_angle_indice:
		if dotpds[idx]>max_product:
			vec_idx_1 = idx
			max_product = dotpds[idx]
	# vec_idx_1 为最小夹角向量对中点积最大的一组的编号
	vec_idx_1 = np.argmin(angles)
	vec_idx_2 = vec_idx_1 + 1
	if vec_idx_2<nvec:
		new_vec = np.add(vecs[vec_idx_1],vecs[vec_idx_2])
		vecs.pop(vec_idx_2)
		vecs.pop(vec_idx_1)
	else:
		new_vec = np.add(vecs[vec_idx_1],vecs[0])
		vecs.pop(vec_idx_1)
		vecs.pop(0)
	vecs.append(new_vec)
	return vecs
	

def vector_simplization(list_of_vectors):
	vecs = list(list_of_vectors)
	nvec = len(vecs)+1
	while len(vecs)<nvec:
		nvec = len(vecs)
		vecs = vector_combine(vecs)
		if nvec<=2: break
	return vecs
















