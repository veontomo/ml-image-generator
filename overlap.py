def linearOverlap(seg1, seg2):
	"""Overlap of two segments, seg = [x, y] """
	b1, e1 = seg1[0], seg1[1]
	b2, e2 = seg2[0], seg2[1]
	return max(0, min(e1, e2) - max(b1, b2))

test = [[[0, 1], [2, 3], 0], [[0, 2], [1, 3], 1], [[0, 3], [1, 2], 1]]
for t in test:
	result1 = linearOverlap(t[0], t[1])
	result2 = linearOverlap(t[1], t[0])
	expected = t[2]
	if not result1 == result2:
		print('non symmetric result')
	else: 
		print('symmetric result')
	if not result1 == expected:
		print('expected:', expected, 'actual:', actual, 'for', t)
	else:
		print('expected = actual', expected)


# r1: [[0, 1], [2, 3]]
def planeOverlap(r1, r2):
	"""overlap of two rectangles: r = [[xmin, ymin], [xmax, ymax]] """
	a1, a2 = r1[0], r1[1]
	b1, b2 = r2[0], r2[1]
	seg1x, seg2x = [a1[0], a2[0]], [b1[0], b2[0]]
	seg1y, seg2y = [a1[1], a2[1]], [b1[1], b2[1]]
	return linearOverlap(seg1x, seg2x)*linearOverlap(seg1y, seg2y)

print(planeOverlap([[0, 0], [2, 2]], [[0, 0], [1, 1]]))