# see https://github.com/torvalds/linux/blob/5924bbecd0267d87c24110cbe2041b5075173a25/include/uapi/linux/hyperv.h#L158
KEY_SIZE = 512
VALUE_SIZE = 2048


def get_kvps(file):
	pairs = {}
	fd = open(file, 'rb')
	content = fd.read()
	assert len(content) % (KEY_SIZE + VALUE_SIZE) == 0
	for i in range(0, len(content) // (KEY_SIZE + VALUE_SIZE)):	
		start = i * (KEY_SIZE + VALUE_SIZE)
		key = content[start:start + KEY_SIZE].rstrip(b'\x00').decode()
		value = content[start + KEY_SIZE:start + KEY_SIZE + VALUE_SIZE].rstrip(b'\x00').decode()
		pairs.update({key: value})
	return pairs


def main():
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument('pool_file', help='Pool file to open, /var/lib/hyperv/.kvp_pool*')
	ap.add_argument('--get', help='Get a value from this key')
	ap.add_argument('--list', action='store_true', help='Dump all key-value pairs')
	args = ap.parse_args()
	if args.get:
		print(get_kvps(args.pool_file)[args.get])	
	elif args.list:
		print('\n'.join('{}={}'.format(k, v) for k, v in get_kvps(args.pool_file).items()))


if __name__ == '__main__':
	main()