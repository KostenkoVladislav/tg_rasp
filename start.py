import runpy

while True:
	try:
		runpy.run_module(mod_name="main")
	except BaseException as e:
		print(" ", e)
