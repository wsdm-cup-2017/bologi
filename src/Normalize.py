def normalize(s):
	minv=min(s.itervalues())
	maxv=max(s.itervalues())
	factor =float(7)/(maxv-minv)
	for k in s:
		s[k]=int(round(((s[k])-minv)*factor))
	print(s)
    
